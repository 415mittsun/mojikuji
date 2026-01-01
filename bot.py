import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread

# --- 1. 24時間稼働（スリープ防止）用の設定 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Bot自身のメッセージには反応しない
    if message.author == bot.user:
        return

    # ★ ログ出力：メッセージを受け取ったことをRenderのLogsに表示する
    print(f"メッセージを受信しました: 内容='{message.content}', チャンネルID={message.channel.id}, 送信者={message.author}")

    TARGET_CHANNEL_ID = 1456153594968543325 

    if message.channel.id == TARGET_CHANNEL_ID:
        print("-> 指定されたチャンネルでの発言を確認しました") # ID一致のログ
        
        if "😀" in message.content:
            print("-> 絵文字を検知しました。返信を送信します。") # 条件一致のログ
            length = random.randint(2, 6)
            result = "".join(random.choice(HIRAGANA) for _ in range(length))
            await message.channel.send(f"結果：{result}")
    else:
        print("-> 別のチャンネルでの発言のため無視します") # ID不一致のログ

    await bot.process_commands(message)

# 実行
keep_alive() # 生存確認用サーバーを起動
# RenderのEnvironmentで設定した「DISCORD_TOKEN」を読み込む
token = os.getenv('DISCORD_TOKEN')
bot.run(token)



