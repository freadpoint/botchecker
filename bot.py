import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS requests (user_id INTEGER PRIMARY KEY, chat_id INTEGER)")
conn.commit()

def save_request(userId, chatId):
    cursor.execute("REPLACE INTO requests (user_id, chat_id) VALUES (?, ?)", (userId, chatId))
    conn.commit()

def get_chat_id(userId):
    cursor.execute("SELECT chat_id FROM requests WHERE user_id = ?", (userId,))
    res = cursor.fetchone()
    if res:
        return res[0]
    return None

TOKEN = "8808691336:AAFAbTQVAfyYMkscK4Xx44aESKGRPFj_HQc"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.chat_join_request()
async def join_request(request: types.ChatJoinRequest):
    userId = request.from_user.id
    chatId = request.chat.id
    save_request(userId, chatId)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я не бот", callback_data="cap_success")]
    ])
    try:
        await bot.send_message(
            chat_id=userId,
            text="Подтверди, что ты не бот, нажав кнопку ниже.",
            reply_markup=keyboard
        )
    except Exception:
        pass

@dp.callback_query(F.data == "cap_success")
async def check_captcha(callback: types.CallbackQuery):
    userId = callback.from_user.id
    chatId = get_chat_id(userId)
    if not chatId:
        await callback.answer("Заявка не найдена или уже обработана.", show_alert=True)
        return
    
    await bot.approve_chat_join_request(chat_id=chatId, user_id=userId)
    await callback.message.edit_text("Проверка успешно пройдена. Заявка одобрена.")
    
    name = callback.from_user.first_name
    mention = f"<a href='tg://user?id={userId}'>{name}</a>"
    await bot.send_message(chat_id=chatId, text=f"{mention}, твоя заявка принята.", parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())