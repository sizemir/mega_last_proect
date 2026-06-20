import telebot
import db

TOKEN = "8723046268:AAHeSE5gLp7xpRFH_rpmIaOIUUHHihhyMTs"
bot = telebot.TeleBot(TOKEN)

SCHEDULE = "📅 СБ 19:00 - Штучка 🌟"

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row("📅 Расписание", "⭐ Оценить урок")
keyboard.row("ℹ️ О школе", "📞 Контакты")
keyboard.row("📊 Личный кабинет")

@bot.message_handler(commands=['start'])
def start(message):
    # Открываем картинку nn.jpg из папки с ботом
    with open('nn.png', 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f"🌟 Привет, {message.chat.first_name}!\n\n📅 Расписание: СБ 19:00\n⭐ После урока поставь оценку!",
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

@bot.message_handler(func=lambda message: message.text == "📊 Личный кабинет")
def profile(message):
    user_id = str(message.chat.id)
    ratings = db.get_ratings(user_id)
    
    total = len(ratings)
    avg = sum(r[0] for r in ratings) / total if total > 0 else 0
    
    text = f"""
👤 Личный кабинет

Имя: {message.chat.first_name}
Всего оценок: {total}
Средний балл: {avg:.1f}
    """
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def save_rating(call):
    rating = int(call.data)
    user_id = str(call.message.chat.id)
    
    db.save_rating(user_id, rating)
    
    ratings = db.get_ratings(user_id)
    total = len(ratings)
    avg = sum(r[0] for r in ratings) / total
    
    if rating == 5:
        msg = "🌟 Супер!"
    elif rating == 4:
        msg = "😊 Хорошо!"
    elif rating == 3:
        msg = "🙂 Спасибо!"
    elif rating == 2:
        msg = "😐 Понял!"
    else:
        msg = "😔 Жаль..."
    
    msg += f"\n\n📊 Всего оценок: {total}\n⭐ Средний балл: {avg:.1f}"
    
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, "Используй кнопки 👇", reply_markup=keyboard)

if __name__ == "__main__":
    db.init_db()
    print("✅ Бот запущен! Картинка nn.jpg подключена.")
    bot.infinity_polling()