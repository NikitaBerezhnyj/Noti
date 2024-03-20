import json
import calendar
from telebot import types
from datetime import datetime, timedelta

class UserManager:
    def __init__(self, users_file="./users.json"):
        self.users_file = users_file

    # Завантаження даних з users.json
    def load_users_data(self):
        with open(self.users_file, "r") as f_o:
            return json.load(f_o)

    # Запис даних в users.json
    def save_users_data(self, data):
        with open(self.users_file, "w") as f_o:
            json.dump(data, f_o, indent=4, ensure_ascii=False)

    #_____________________________________________________________________________________________
    #---------------------------------------Команда /start----------------------------------------
    #_____________________________________________________________________________________________
    
    # Виклик команди /start
    def handle_start(self, message, bot):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        username = message.from_user.username
        firstname = message.from_user.first_name
        secondname = message.from_user.last_name
        data_from_json = self.load_users_data()
        if user_id not in data_from_json:
            data_from_json[user_id] = {
                "chat_id": chat_id,
                "username": username,
                "first_name": firstname,
                "second_name": secondname,
                "notifications": []
            }
            bot.reply_to(message, f"Вітаю, {firstname}! Я – Noti, ваш вірний помічник. Я тут, щоб нагадувати вам про все, про що ви мене попросите. Щоб дізнатися більше про мої можливості, будь ласка, скористайтеся командою /help. Я вже зареєстрував вас у своїй базі даних, тому ви можете бути впевнені, що я точно нагадаю вам про важливі події.")
        else:
            bot.reply_to(message, "Вибачте, ви певно переплутали команду, бо ви вже зареєстровані у моїй базі. Щоб дізнатися більше про мої можливості, будь ласка, скористайтеся командою /help.")
        self.save_users_data(data_from_json)

    #_____________________________________________________________________________________________
    #--------------------------------------Команда /help------------------------------------------
    #_____________________________________________________________________________________________
    
    # Виклик команди /help
    def handle_help(self, message, bot):
        bot.reply_to(message, "Я можу виконати такі команди для вас:\n/start - запуск бота\n/help - інформація про функції\n/info - кількість днів до попередження\n/add_notification - додати нове повідомлення\n/edit_notification - редагувати повідомлення\n/remove_notification - видалити повідомлення\n/remove_user - видалення особистої інформації")

    #_____________________________________________________________________________________________
    #--------------------------------------Команда /info------------------------------------------
    #_____________________________________________________________________________________________

    # Виклик команди /info
    def handle_info(self, message, bot):
        user_id = str(message.from_user.id)
        data_from_json = self.load_users_data()

        if user_id in data_from_json:
            user_notifications = data_from_json[user_id].get("notifications", [])

            if not user_notifications:
                bot.reply_to(message, 'У вас немає жодних повідомлень.')
                return

            response = "Інформація про ваші повідомлення:\n"
            today = datetime.now()

            for i, notification_data in enumerate(user_notifications, start=1):
                notification_text = list(notification_data.values())[0]['notification_text']
                notification_date = list(notification_data.values())[0]['notification_data']
                notification_day = list(notification_data.values())[0]['notification_day']

                if notification_date not in ['На початку місяця', 'В кінці місяця', 'Кожен день'] and notification_day is None:
                    bot.reply_to(message, f"Помилка: значення для дня нагадування не встановлено у повідомленні {i}.")
                    return

                if notification_date == 'На початку місяця' and notification_day is None:
                    next_month = today.replace(day=28) + timedelta(days=4)
                    target_date = next_month.replace(day=1)
                elif notification_date == 'На початку місяця':
                    target_date = today.replace(day=1)
                elif notification_date == 'В кінці місяця':
                    _, days_in_month = calendar.monthrange(today.year, today.month)
                    target_date = today.replace(day=days_in_month)
                elif notification_date == 'Кожен день':
                    target_date = today + timedelta(days=1)
                else:
                    weekday_map = {'Пн': 0, 'Вт': 1, 'Ср': 2, 'Чт': 3, 'Пт': 4, 'Сб': 5, 'Нд': 6}
                    today_weekday = today.weekday()
                    if notification_day in weekday_map:
                        target_weekday = weekday_map[notification_day]
                        if today_weekday <= target_weekday:
                            days_until_target = target_weekday - today_weekday
                        else:
                            days_until_target = 7 - (today_weekday - target_weekday)
                        target_date = today + timedelta(days=days_until_target)

                if target_date == today:
                    days_until_notification = 7
                else:
                    days_until_notification = (target_date - today).days
                
                response += f"{i}. {notification_text} - залишилось {days_until_notification} днів\n"

            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Вас немає в базі користувачів.")

    #_____________________________________________________________________________________________
    #---------------------------------Команда /add_notification-----------------------------------
    #_____________________________________________________________________________________________

    # Виклик команди /add_notification
    def handle_add_notification(self, message, bot):
        user_id = str(message.from_user.id)
        notification_text = message.text
        data_from_json = self.load_users_data()
        user_notifications = data_from_json.setdefault(user_id, {}).setdefault("notifications", [])
        if len(user_notifications) >= 8:
            bot.reply_to(message, "На жаль у вас вже багато повідомлень. Для того, щоб мені було зручніше та легше вам нагадувати, кількість повідомлень обмежена 8. Будь ласка, видаліть якесь зі старих, щоб додати нове.")
            return
        else:
            bot.reply_to(message, "Введіть текст нового повідомлення")
            bot.register_next_step_handler(message, self.handle_notification_text, bot)

    # Отримання тексту повідомлення
    def handle_notification_text(self, message, bot):
        user_id = str(message.from_user.id)
        notification_text = message.text
        add_noti_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_start_m = types.KeyboardButton(text='На початку місяця')
        item_end_m = types.KeyboardButton(text='В кінці місяця')
        item_day = types.KeyboardButton(text='У визначений день тижня')
        item_every = types.KeyboardButton(text='Кожен день')
        add_noti_markup.add(item_start_m, item_end_m, item_day, item_every)
        user_data = {'notification_text': notification_text}
        bot.reply_to(message, "Оберіть тип нового повідомлення", reply_markup=add_noti_markup)
        bot.register_next_step_handler(message, self.handle_notification_type, user_data, bot)

    # Отримання типу повідомлення
    def handle_notification_type(self, message, user_data, bot):
        user_id = str(message.from_user.id)
        notification_type = message.text
        notification_text = user_data['notification_text']
        data_from_json = self.load_users_data()
        user_notifications = data_from_json.setdefault(user_id, {}).setdefault("notifications", [])
        notification_counter = len(user_notifications) + 1
        new_notification_key = f"notification{notification_counter}"
        new_notification = {
            "notification_text": notification_text,
            "notification_data": notification_type
        }
        if notification_type == 'У визначений день тижня':
            add_noti_day_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_pn = types.KeyboardButton(text='Пн')
            item_vt = types.KeyboardButton(text='Вт')
            item_sr = types.KeyboardButton(text='Ср')
            item_ct = types.KeyboardButton(text='Чт')
            item_pt = types.KeyboardButton(text='Пт')
            item_sb = types.KeyboardButton(text='Сб')
            item_nd = types.KeyboardButton(text='Нд')
            add_noti_day_markup.add(item_pn, item_vt, item_sr, item_ct, item_pt, item_sb, item_nd)
            bot.reply_to(message, 'Оберіть день для нового повідомлення', reply_markup=add_noti_day_markup)
            bot.register_next_step_handler(message, self.handle_notification_day, new_notification, new_notification_key, bot)
        else:
            new_notification["notification_day"] = None
            user_notifications.append({new_notification_key: new_notification})
            self.save_users_data(data_from_json)
            bot.reply_to(message, 'Повідомлення було додано', reply_markup=types.ReplyKeyboardRemove())

    # Отримання конкретного дня тижня, якщо тип повідомлення 'У визначений день тижня'
    def handle_notification_day(self, message, new_notification, new_notification_key, bot):
        user_id = str(message.from_user.id)
        notification_day = message.text
        data_from_json = self.load_users_data()
        new_notification["notification_day"] = notification_day
        user_notifications = data_from_json.setdefault(user_id, {}).setdefault("notifications", [])
        user_notifications.append({new_notification_key: new_notification})
        self.save_users_data(data_from_json)
        bot.reply_to(message, 'Повідомлення було додано', reply_markup=types.ReplyKeyboardRemove())

    #_____________________________________________________________________________________________
    #--------------------------------Команда /edit_notification-----------------------------------
    #_____________________________________________________________________________________________

    # Виклик команди /edit_notification
    def handle_edit_notification(self, message, bot):
        user_id = str(message.from_user.id)
        data_from_json = self.load_users_data()
        if user_id in data_from_json:
            user_notifications = data_from_json[user_id].get("notifications", [])
            if not user_notifications:
                bot.reply_to(message, 'У вас немає жодних повідомлень для редагування.')
            else:
                response = "Ваші повідомлення для редагування:\n"
                for i, notification_data in enumerate(user_notifications, start=1):
                    notification_text = list(notification_data.values())[0]['notification_text']
                    response += f"{i}. {notification_text}\n"
                bot.reply_to(message, response)
                edit_notification_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = []
                for i, _ in enumerate(user_notifications, start=1):
                    buttons.append(types.KeyboardButton(str(i)))
                buttons.append(types.KeyboardButton("Скасувати"))
                edit_notification_markup.add(*buttons)
                bot.reply_to(message, "Оберіть номер повідомлення, яке бажаєте змінити:", reply_markup=edit_notification_markup)
                bot.register_next_step_handler(message, self.enter_edit_num, data_from_json, user_notifications, edit_notification_markup, bot)
        else:
            bot.reply_to(message, "Вас немає в базі користувачів.", reply_markup=types.ReplyKeyboardRemove())

    # Отримання порядкового номера повідомлення, яке буде змінено
    def enter_edit_num(self, message, data_from_json, user_notifications, edit_notification_markup, bot):
        user_id = str(message.from_user.id)
        user_input = message.text
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(user_notifications):
                bot.reply_to(message, "Введіть новий текст для повідомлення:", reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, self.enter_edit_text, data_from_json, user_notifications, index, bot)
            else:
                bot.reply_to(message, "Номер повідомлення недійсний. Спробуйте ще раз.", reply_markup=edit_notification_markup)
        elif user_input.lower() == "скасувати":
            bot.reply_to(message, "Редагування повідомлення скасовано.", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.reply_to(message, "Невірний формат введення. Виберіть номер повідомлення або введіть 'скасувати'.", reply_markup=edit_notification_markup)

    # Отримання зміненого тексту повідомлення
    def enter_edit_text(self, message, data_from_json, user_notifications, index, bot):
        user_id = str(message.from_user.id)
        user_input = message.text
        if user_input:
            user_notifications[index][list(user_notifications[index].keys())[0]]["notification_text"] = user_input
            with open(self.users_file, "w") as f_o:
                json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
            bot.reply_to(message, "Текст повідомлення було оновлено.", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.reply_to(message, "Новий текст повідомлення не може бути порожнім.")

    #_____________________________________________________________________________________________
    #-------------------------------Команда /remove_notification----------------------------------
    #_____________________________________________________________________________________________
    
    # Виклик команди /remove_notification
    def handle_remove_notification(self, message, bot):
        user_id = str(message.from_user.id)
        data_from_json = self.load_users_data()
        if user_id in data_from_json:
            user_notifications = data_from_json[user_id].get("notifications", [])
            if not user_notifications:
                bot.reply_to(message, 'У вас немає жодних повідомлень для видалення')
            else:
                response = "Ваші повідомлення:\n"
                for i, notification_data in enumerate(user_notifications, start=1):
                    notification_text = list(notification_data.values())[0]['notification_text']
                    response += f"{i}. {notification_text}\n"
                bot.reply_to(message, response)
                remove_notification_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = []
                for i, _ in enumerate(user_notifications, start=1):
                    buttons.append(types.KeyboardButton(str(i)))
                buttons.append(types.KeyboardButton("Скасувати"))
                remove_notification_markup.add(*buttons)
                bot.reply_to(message, "Оберіть номер повідомлення, яке ви хочете видалити:", reply_markup=remove_notification_markup)
                bot.register_next_step_handler(message, self.handle_remove_notification_confirm, data_from_json, user_notifications, bot)
        else:
            bot.reply_to(message, "Вас немає в базі користувачів.")

    # Отримання підтвердження на видалення повідомлення
    def handle_remove_notification_confirm(self, message, data_from_json, user_notifications, bot):
        user_id = str(message.from_user.id)
        try:
            remove_num = int(message.text)
            if 1 <= remove_num <= len(user_notifications):
                del user_notifications[remove_num - 1]
                data_from_json[user_id]['notifications'] = user_notifications
                with open(self.users_file, "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                bot.reply_to(message, 'Повідомлення було видалено', reply_markup=types.ReplyKeyboardRemove())
            elif message.text == "Скасувати":
                bot.reply_to(message, 'Видалення скасовано', reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.reply_to(message, 'Невірний номер повідомлення. Спробуйте ще раз.', reply_markup=types.ReplyKeyboardRemove())
        except ValueError:
            bot.reply_to(message, 'Невірний номер повідомлення. Спробуйте ще раз.', reply_markup=types.ReplyKeyboardRemove())

    #_____________________________________________________________________________________________
    #------------------------------------Команда /remove_user-------------------------------------
    #_____________________________________________________________________________________________
    
    # Виклик команди /remove_user
    def handle_remove_user(self, message, bot):
        user_id = str(message.from_user.id)
        data_from_json = self.load_users_data()
        if user_id in data_from_json:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            accept_btn = types.KeyboardButton("Так")
            cancel_btn = types.KeyboardButton("Ні")
            markup.add(accept_btn, cancel_btn)
            bot.send_message(message.chat.id, "Ви впевнені, що хочете видалити свій обліковий запис? Це неможливо буде відмінити.", reply_markup=markup)
            bot.register_next_step_handler(message, self.handle_remove_user_confirm, markup, bot)
        else:
            bot.reply_to(message, "Вас немає в базі користувачів.")

    # Отримання підтвердження на видалення користувача з бази даних
    def handle_remove_user_confirm(self, message, markup, bot):
        if message.text.lower() == 'так':
            user_id = str(message.from_user.id)
            data_from_json = self.load_users_data()
            data_from_json.pop(user_id)
            with open(self.users_file, "w") as f_w:
                json.dump(data_from_json, f_w, indent=4, ensure_ascii=False)
            bot.send_message(message.chat.id, f"Ваш обліковий запис успішно видалено. До зустрічі, {message.from_user.first_name}!", reply_markup=types.ReplyKeyboardRemove())
        elif message.text.lower() == 'ні':
            bot.send_message(message.chat.id, "Видалення облікового запису скасовано.", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "Невірна відповідь, будь ласка, натисніть 'Так' або 'Ні'.", reply_markup=types.ReplyKeyboardRemove())