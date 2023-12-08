import asyncio
from main import bot


async def sendMessagetoUser(userId, message, keyboard):
    await bot.send_message(userId,
        message,
        reply_markup=keyboard)
