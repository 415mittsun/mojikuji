import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread
import logging
import asyncio

# ログを詳細に出力
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # ポート8080でWebサーバーを起動
    app.run(host='0.0.0.0', port=8080)

# インテント設定（message_contentだけでOK）
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
TARGET_CHANNEL_ID = 1456153594968543325

@bot.event
async def on_ready():
    logger.info("---------------------------------------")
    logger.info(f'成功！ Discordにログインしました: {bot.user.name}')
    logger.info(f'Bot ID: {bot.user.id}')
    logger.info("---------------------------------------")

@bot.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == bot.user:
        return
    
    logger.info(f"メッセージ受信: {message.content} (チャンネルID: {message.channel.id})")
    
    # 特定のチャンネルでのみ反応
    if message.channel.id == TARGET_CHANNEL_ID:
        if "😀" in message.content:
            length = random.randint(2, 6)
            result = "".join(random.choice(HIRAGANA) for _ in range(length))
            await message.channel.send(f"結果：{result}")
            logger.info(f"ランダム文字列を送信: {result}")
    
    # コマンドも処理できるようにする
    await bot.process_commands(message)

async def main():
    """非同期でBotを起動"""
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("エラー: DISCORD_TOKEN が見つかりません。")
        return
    
    logger.info("トークンを確認しました。Discordへ接続を試みます...")
    
    try:
        async with bot:
            await bot.start(token)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            logger.error("速度制限(429)が発生中です。しばらく時間を置いてから再起動してください。")
            logger.info("60秒待機してから再試行します...")
            await asyncio.sleep(60)
            await bot.start(token)
        else:
            logger.error(f"接続エラーが発生しました: {e}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")

if __name__ == "__main__":
    # 1. Webサーバーを別スレッドで開始
    logger.info("Webサーバーを起動中...")
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # 2. Discord Botを非同期で開始
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot を終了します...")
