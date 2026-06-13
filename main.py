import telebot
from datetime import datetime
import time
import threading
from reg import TOKEN

bot = telebot.TeleBot(TOKEN)

SCHEDULE = "📅 СБ 19:00 - Штучка 🌟"

# Клавиатура
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row("📅 Расписание", "⭐ Оценить урок")
keyboard.row("ℹ️ О школе", "📞 Контакты")

# Хранилище оценок
ratings = []

# ========== НАПОМИНАНИЕ (простое и понятное) ==========
def reminder():
    """Простое напоминание каждую субботу в 18:40"""
    while True:
        now = datetime.now()
        # Суббота = 5 (пн=0, вт=1, ср=2, чт=3, пт=4, сб=5, вс=6)
        if now.weekday() == 5 and now.hour == 18 and now.minute == 40:
            bot.send_message(8723046268, "⏰ Напоминание!\n\nЧерез 20 минут урок: Штучка 🌟\n\nГотовься!")
            time.sleep(61)  # Чтобы не отправляло несколько раз
        time.sleep(30)

# Запускаем напоминания в отдельном потоке
threading.Thread(target=reminder, daemon=True).start()

# ========== ОСНОВНЫЕ КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.chat.first_name}!\n\n📅 Расписание: СБ 19:00\n⏰ Напомню за 20 минут\n⭐ После урока поставь оценку!",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == "📅 Расписание")
def get_schedule(message):
    bot.send_message(message.chat.id, SCHEDULE, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "ℹ️ О школе")
def about(message):
    bot.send_message(message.chat.id, "🎓 ОМЕГА ШКОЛА\n\n• 123123123131 учеников\n• Опытные преподаватели\n• Сайт: чучучучу", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "📞 Контакты")
def contacts(message):
    bot.send_message(message.chat.id, "📞 Поддержка: @ЧИКСЧИКС\n📧 Email: БЭМСБЭМС", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "⭐ Оценить урок")
def rate_lesson(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("1 ⭐", callback_data="1"),
        telebot.types.InlineKeyboardButton("2 ⭐", callback_data="2"),
        telebot.types.InlineKeyboardButton("3 ⭐", callback_data="3"),
        telebot.types.InlineKeyboardButton("4 ⭐", callback_data="4"),
        telebot.types.InlineKeyboardButton("5 ⭐", callback_data="5")
    )
    bot.send_message(message.chat.id, "Как прошёл урок?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def save_rating(call):
    rating = int(call.data)
    
    ratings.append({
        'rating': rating,
        'date': datetime.now().strftime("%d.%m.%Y %H:%M")
    })
    
    if rating == 5:
        msg = "🌟 Супер! Рад, что понравилось!"
    elif rating == 4:
        msg = "😊 Хорошо! Спасибо!"
    elif rating == 3:
        msg = "🙂 Спасибо! Что улучшить?"
    elif rating == 2:
        msg = "😐 Понял, сделаем лучше!"
    else:
        msg = "😔 Жаль... Напиши, что не так?"
    
    if ratings:
        avg = sum(r['rating'] for r in ratings) / len(ratings)
        msg += f"\n\n📊 Всего оценок: {len(ratings)}\n⭐ Средний балл: {avg:.1f}"
    
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, "Используй кнопки 👇", reply_markup=keyboard)

if __name__ == "__main__":
    print("✅ Бот запущен!")
    print("📅 Расписание: СБ 19:00")
    print("⏰ Напоминание придёт в субботу в 18:40")
    bot.infinity_polling()