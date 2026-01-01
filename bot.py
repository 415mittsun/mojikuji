import discord
from discord.ext import commands
import random

# Botの基本設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 使用するひらがなのリスト
HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ★特定のチャンネルIDを指定（例: 123456789012345678）
    # 整数（int型）として比較します
    TARGET_CHANNEL_ID = 1456153594968543325 

    if message.channel.id == TARGET_CHANNEL_ID:
        if message.content == "😀":
            length = random.randint(2, 6)
            result = "".join(random.choice(HIRAGANA) for _ in range(length))
            await message.channel.send(f"結果：{result}")

    await bot.process_commands(message)

# ここに先ほどメモしたトークンを貼り付ける
bot.run('YOUR_BOT_TOKEN_HERE')