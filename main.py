import asyncio
import os
import sys

import discord
from discord import MessageType
from loguru import logger
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode("HTML"))

discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    print(message)
    if message.type != MessageType.channel_follow_add:
        try:
            logger.success(f"Сообщение с канала {message.author} успешно отправлено!")
            await bot.send_photo(chat_id=telegram_channel_id,
                                 photo=message.attachments[0].proxy_url,
                                 caption=f"{message.author}\n\n{message.content}")
        except IndexError:
            await bot.send_message(chat_id=telegram_channel_id,
                                   text=f"{message.author}\n\n{message.content}")


client.run(os.getenv("DISCORD_TOKEN"))
