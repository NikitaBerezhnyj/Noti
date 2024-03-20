import json
import config
import schedule
import datetime
import calendar
import time
import telebot
from telebot import types
from user_manager import UserManager

# Ініціалізація бота
print("Starting...")
bot = telebot.TeleBot(config.TOKEN)

# Виклик команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_manager = UserManager()
    user_manager.handle_start(message, bot)

# Виклик команди /help
@bot.message_handler(commands=['help'])
def send_help(message):
    user_manager = UserManager()
    user_manager.handle_help(message, bot)

# Виклик команди /info
@bot.message_handler(commands=['info'])
def send_info(message):
    user_manager = UserManager()
    user_manager.handle_info(message, bot)

# Виклик команди /add_notification
@bot.message_handler(commands=['add_notification'])
def add_command(message):
    user_manager = UserManager()
    user_manager.handle_add_notification(message, bot)

# Виклик команди /edit_notification
@bot.message_handler(commands=['edit_notification'])
def edit_command(message):
    user_manager = UserManager()
    user_manager.handle_edit_notification(message, bot)

# Виклик команди /remove_notification
@bot.message_handler(commands=['remove_notification'])
def remove_command(message):
    user_manager = UserManager()
    user_manager.handle_remove_notification(message, bot)

# Виклик команди /remove_user
@bot.message_handler(commands=['remove_user'])
def remove_user(message):
    user_manager = UserManager()
    user_manager.handle_remove_user(message, bot)

# Виклик якщо текст не є командою
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Вибачте, на жаль я не знаю такої команди.\nВикористайте команду /help щоб детальніше дізнатись про мої можливості.")

english_to_ukrainian_days = {
    "Mon": "Пн",
    "Tue": "Вт",
    "Wed": "Ср",
    "Thu": "Чт",
    "Fri": "Пт",
    "Sat": "Сб",
    "Sun": "Нд"
}

def daily_notification():
    # Отримання поточної дати
    today = datetime.datetime.now()

    # Завантаження даних з файлу users.json
    with open('users.json', 'r') as file:
        data = json.load(file)

    for user_id, user_info in data.items():
        if 'notifications' in user_info:
            for notification in user_info['notifications']:
                for key, value in notification.items():
                    notification_text = value.get('notification_text')
                    notification_data = value.get('notification_data')
                    notification_day = value.get('notification_day')

                    # Перевірка для "На початку місяця"
                    if notification_data == "На початку місяця" and today.day == 1:
                        chat_id = user_info.get('chat_id')
                        if chat_id:
                            bot.send_message(chat_id, f"Нагадую!\nСьогодні: {notification_text}")

                    # Перевірка для "В кінці місяця"
                    elif notification_data == "В кінці місяця" and today.day == calendar.monthrange(today.year, today.month)[1]:
                        chat_id = user_info.get('chat_id')
                        if chat_id:
                            bot.send_message(chat_id, f"Нагадую!\nСьогодні: {notification_text}")
                    
                    # Перевірка для "Кожен день"
                    elif notification_data == "Кожен день":
                        chat_id = user_info.get('chat_id')
                        if chat_id:
                            bot.send_message(chat_id, f"Нагадую!\nСьогодні: {notification_text}")

                    # Перевірка для "У визначений день тиждня"
                    elif notification_data == "У визначений день тижня":
                        # Перевіряємо, чи notification_day не пустий і співпадає з поточним днем тижня
                        if notification_day and english_to_ukrainian_days.get(today.strftime("%a")) == notification_day:
                            chat_id = user_info.get('chat_id')
                            if chat_id:
                                bot.send_message(chat_id, f"Нагадую!\nСьогодні: {notification_text}")

# Реєстрація роботи функції для виклику щодня о заданому часі
schedule.every().day.at("12:27").do(daily_notification)

# Функція для запуску планувальника
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Почнемо роботу планувальника у окремому потоці
import threading
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

# Запуск бота
print("Polling...")
bot.infinity_polling()
