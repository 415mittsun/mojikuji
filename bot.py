import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread
import logging

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

# インテント設定
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"

@bot.event
async def on_ready():
    print("---------------------------------------")
    print(f'成功！ Discordにログインしました: {bot.user.name}')
    print("---------------------------------------")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    print(f"メッセージ受信: {message.content} (ID: {message.channel.id})")

    TARGET_CHANNEL_ID = 1456153594968543325 
    if message.channel.id == TARGET_CHANNEL_ID:
        if "😀" in message.content:
            length = random.randint(2, 6)
            result = "".join(random.choice(HIRAGANA) for _ in range(length))
            await message.channel.send(f"結果：{result}")

if __name__ == "__main__":
    # 1. 先にWebサーバーを別スレッドで開始
    print("Webサーバーを起動中...")
    t = Thread(target=run_flask)
    t.start()

    # 2. メインスレッドでBotを起動
    token = os.getenv('DISCORD_TOKEN')
    if token:
        print(f"トークンを確認しました。Discordへ接続します...")
        bot.run(token)
    else:
        print("エラー: DISCORD_TOKEN が見つかりません。")
