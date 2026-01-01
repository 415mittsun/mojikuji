import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread
import logging

# ログを詳しく出す設定
logging.basicConfig(level=logging.INFO)

app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# インテントを「全部許可」にする
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"

@bot.event
async def on_ready():
    # 起動に成功したら必ずこれが出る
    print("---------------------------------------")
    print(f'成功！ Discordにログインしました: {bot.user.name}')
    print("---------------------------------------")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # メッセージを受け取ったら必ずこれが出る
    print(f"メッセージ受信: {message.content} (ID: {message.channel.id})")

    TARGET_CHANNEL_ID = 1456153594968543325 
    if message.channel.id == TARGET_CHANNEL_ID:
        if "😀" in message.content:
            length = random.randint(2, 6)
            result = "".join(random.choice(HIRAGANA) for _ in range(length))
            await message.channel.send(f"結果：{result}")

# 実行開始のログ
print("プログラムを開始します...")
keep_alive()

token = os.getenv('DISCORD_TOKEN')
if token is None:
    print("エラー: DISCORD_TOKEN が設定されていません！")
else:
    print(f"トークンを読み込みました (先頭3文字: {token[:3]}...)")
    try:
        bot.run(token)
    except Exception as e:
        print(f"致命的なエラーが発生しました: {e}")
