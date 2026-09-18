import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8705078684:AAHPNPd-Ffags8ayB3XMrY_0SSrq8Lv_H6Q"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# 7 ta klub nomi va ularning bo'lajak sayt manzillari
CLUBS = [
    {"name": "🗣️ DEBAT KLUBI", "url": "https://debat-klub.netlify.app"},
    {"name": "🌿 EKO-SCHOOL O'ZBEKISTAN KLUBI", "url": "https://eko-school.netlify.app"},
    {"name": "🎭 IQTIDOR MAKTAB ANSAMBILI", "url": "https://iqtidor-ansambli.netlify.app"},
    {"name": "📖 JADIDLAR IZIDAN KLUBI", "url": "https://jadidlar-izidan.netlify.app"},
    {"name": "🌐 KELAJAK UCHUN XORIJIY TIL KLUBI", "url": "https://xorijiy-til-klubi.netlify.app"},
    {"name": "💻 RAQAMLI AVLOD QIZLARI KLUBI", "url": "https://raqamli-avlod.netlify.app"},
    {"name": "🎪 TURON TEATRI KLUBI", "url": "https://turon-teatri.netlify.app"},
]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for club in CLUBS:
        button = InlineKeyboardButton(
            text=f"📝 {club['name']} — Ro'yxatdan o'tish", 
            url=club['url']
        )
        keyboard.add(button)
    
    caption = (
        f"<b>Assalomu Aleykum, {message.from_user.full_name}!</b>\n\n"
        "Qanday klubga qatnashmoqchisiz?\n"
        "Quyidagi ro'yxatdan o'zingizga ma'qul klubni tanlang va tugmani bosing:"
    )
    
    await message.answer(caption, reply_markup=keyboard)

# Render uxlab qolmasligi uchun kichik ping-server
async def handle(request):
    return web.Response(text="Bot 24/7 ishlamoqda!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    executor.start_polling(dp, skip_updates=True)
