import asyncio
from aiogram import Bot, types
            
API_TOKEN = '6347258430:AAEqy3e5mvRnxlMmuMWEqtQOgFoAXOSwc8I'
CHANNEL_ID = '-1001828493881'
            
bot = Bot(token=API_TOKEN, parse_mode="HTML")
            
            
async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)
            
            
async def main(matn):
    await send_message(CHANNEL_ID, f'<b>{matn}</b>')
            


# if __name__ == "__main__":
#     asyncio.run(main(matn))
            