import logging, config, json, time, calendar, asyncio, schedule
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Змінні
API_TOKEN = config.TOKEN    # Токен бота

# Конфігурація запуску
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота і диспечера 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.storage = MemoryStorage()

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    firstname = message.from_user.first_name
    secondname = message.from_user.last_name
    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {
            "username": username,
            "first_name": firstname,
            "second_name": secondname,
            "notifications": []
        }
        await message.answer(f"Вітаю, {message.from_user.first_name}! Я – Noti, ваш вірний помічник. Я тут, щоб допомогти вам у всьому, що ви потребуєте. Щоб дізнатися більше про мої можливості, будь ласка, скористайтеся командою /help. Я вже зареєстрував вас у нашій базі даних, тому ви можете бути впевнені, що я завжди буду готовий надати вам допомогу та нагадати про важливі події.")
    else:
        await message.answer("Вибачте, ви певно переплутали команду, бо ви вже зареєстровані у нашій базі. Щоб дізнатися більше про мої можливості, будь ласка, скористайтеся командою /help.")
    with open("./users.JSON", "w") as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

# Команда /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("Я маю такі команди для вас, як:\n/help - інформація про функції\n/info - кількість днів до попередження\n/add_notification - додати нове повідомлення\n/remove_notification - видалити повідомлення\n/edit_notification - редагувати повідомлення\n/remove_user - видалення особистої інформації")

# Функції для визначення кількості днів до визначеного дня
def Monday_check(today_weekday, notification_day):
    if notification_day == "Пн":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Вт":
        days_until = 1
        return days_until
    elif notification_day == "Ср":
        days_until = 2
        return days_until
    elif notification_day == "Чт":
        days_until = 3
        return days_until
    elif notification_day == "Пт":
        days_until = 4
        return days_until
    elif notification_day == "Сб":
        days_until = 5
        return days_until
    elif notification_day == "Нд":
        days_until = 6
        return days_until
def Tuesday_check(today_weekday, notification_day):
    if notification_day == "Вт":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Ср":
        days_until = 1
        return days_until
    elif notification_day == "Чт":
        days_until = 2
        return days_until
    elif notification_day == "Пт":
        days_until = 3
        return days_until
    elif notification_day == "Сб":
        days_until = 4
        return days_until
    elif notification_day == "Нд":
        days_until = 5
        return days_until
    elif notification_day == "Пн":
        days_until = 6
        return days_until
def Wednesday_check(today_weekday, notification_day):
    if notification_day == "Ср":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Чт":
        days_until = 1
        return days_until
    elif notification_day == "Пт":
        days_until = 2
        return days_until
    elif notification_day == "Сб":
        days_until = 3
        return days_until
    elif notification_day == "Нд":
        days_until = 4
        return days_until
    elif notification_day == "Пн":
        days_until = 5
        return days_until
    elif notification_day == "Вт":
        days_until = 6
        return days_until
def Thursday_check(today_weekday, notification_day):
    if notification_day == "Чт":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Пт":
        days_until = 1
        return days_until
    elif notification_day == "Сб":
        days_until = 2
        return days_until
    elif notification_day == "Нд":
        days_until = 3
        return days_until
    elif notification_day == "Пн":
        days_until = 4
        return days_until
    elif notification_day == "Вт":
        days_until = 5
        return days_until
    elif notification_day == "Ср":
        days_until = 6
        return days_until
def Friday_check(today_weekda, notification_day):
    if notification_day == "Пт":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Сб":
        days_until = 1
        return days_until
    elif notification_day == "Нд":
        days_until = 2
        return days_until
    elif notification_day == "Пн":
        days_until = 3
        return days_until
    elif notification_day == "Вт":
        days_until = 4
        return days_until
    elif notification_day == "Ср":
        days_until = 5
        return days_until
    elif notification_day == "Чт":
        days_until = 6
        return days_until
def Saturday_check(today_weekday, notification_day):
    if notification_day == "Сб":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Нд":
        days_until = 1
        return days_until
    elif notification_day == "Пн":
        days_until = 2
        return days_until
    elif notification_day == "Вт":
        days_until = 3
        return days_until
    elif notification_day == "Ср":
        days_until = 4
        return days_until
    elif notification_day == "Чт":
        days_until = 5
        return days_until
    elif notification_day == "Пт":
        days_until = 6
        return days_until
def Sunday_check(today_weekday, notification_day):
    if notification_day == "Нд":
        days_until = "Сьогодні"
        return days_until
    elif notification_day == "Пн":
        days_until = 1
        return days_until
    elif notification_day == "Вт":
        days_until = 2
        return days_until
    elif notification_day == "Ср":
        days_until = 3
        return days_until
    elif notification_day == "Чт":
        days_until = 4
        return days_until
    elif notification_day == "Пт":
        days_until = 5
        return days_until
    elif notification_day == "Сб":
        days_until = 6
        return days_until

# Команда /info
@dp.message_handler(commands=['info'])
async def info_command(message: types.Message):
    # Завантаження даних з JSON-файлу
    with open('./users.JSON', 'r', encoding='utf-8') as file:
        data = json.load(file)

    user_id = str(message.chat.id)

    if user_id in data:
        notifications = data[user_id]['notifications']
        if notifications:
            response = f"У вас є наступні робочі повідомлення:\n"
            today = datetime.now()
            today_weekday = today.strftime('%A')  # Отримуємо поточний день тижня

            for i, notification in enumerate(notifications, start=1):
                notification_data = list(notification.values())[0]
                notification_text = notification_data['notification_text']
                notification_date = notification_data['notification_data']
                days_until = 0

                # Перевірка дати для надсилання
                if "На початку місяця" in notification_date:
                    today = datetime.now().date()
                    first_day_of_current_month = datetime(today.year, today.month, 1).date()
                    first_day_of_next_month = (first_day_of_current_month + timedelta(days=32)).replace(day=1)
                    days_difference = (first_day_of_next_month - today).days
                    days_until = days_difference
                    if days_difference == 0:
                        days_until = "Сьогодні"
                    else:
                        days_until = days_difference

                elif "У визначений день тиждня" in notification_date:
                    notification_day = notification_data['notification_day']
                    today_weekday = datetime.now().weekday()
                    if today_weekday == 0:
                        days_until = Monday_check(today_weekday, notification_day)
                    elif today_weekday == 1:
                        days_until = Tuesday_check(today_weekday, notification_day)
                    elif today_weekday == 2:
                        days_until = Wednesday_check(today_weekday, notification_day)
                    elif today_weekday == 3:
                        days_until = Thursday_check(today_weekday, notification_day)
                    elif today_weekday == 4:
                        days_until = Friday_check(today_weekday, notification_day)
                    elif today_weekday == 5:
                        days_until = Saturday_check(today_weekday, notification_day)
                    elif today_weekday == 6:
                        days_until = Sunday_check(today_weekday, notification_day)

                elif "В кінці місяця" in notification_date:
                    current_datetime = datetime.now()
                    current_year = current_datetime.year
                    current_month = current_datetime.month
                    _, last_day = calendar.monthrange(current_year, current_month)
                    today = datetime.now().date()
                    current_year = today.year
                    current_month = today.month
                    last_day_of_month = datetime(current_year, current_month, last_day).date()
                    days_difference = (last_day_of_month - today).days
                    if days_difference == 0:
                        days_until = "Сьогодні"
                    else:
                        days_until = days_difference

                if days_until == "Сьогодні":
                    response += f"{i}. {notification_text}, {days_until}\n"
                else:
                    response += f"{i}. {notification_text}, через {days_until} днів\n"
        else:
            response = "У вас немає робочих повідомлень."
    else:
        response = "Вас немає в базі користувачів."

    await message.answer(response)

# Перелік станів для додавання повідомлення
class AddStates(StatesGroup):
    get_text_state = State()
    get_type_state = State()
    get_day_state = State()

# Команда /add_notification
@dp.message_handler(commands=['add_notification'])
async def add_command(message: types.Message):
    user_id = str(message.from_user.id)
    
    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)
    
    user_notifications = data_from_json.setdefault(user_id, {}).setdefault("notifications", [])
    
    if len(user_notifications) >= 8:
        await message.answer("Нажаль у вас вже багато повідомлень. Для того, щоб мені було зручніше та легше вам нагадувати кількість повідомлень - це 8, тож видаліть якесь зі старих, щоб додати нове")
        return
    else:
        await message.answer("Введіть текст нового повідомлення")
        await AddStates.get_text_state.set()

# Обробка введеного тексту повідомлення
@dp.message_handler(state=AddStates.get_text_state)
async def get_notification_text(message: types.Message, state=FSMContext):
    user_id = str(message.from_user.id)
    notification_text = message.text

    add_noti_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item_start_m = KeyboardButton(text='На початку місяця')
    item_end_m = KeyboardButton(text='В кінці місяця')
    item_day = KeyboardButton(text='У визначений день тиждня')
    add_noti_markup.add(item_start_m, item_end_m, item_day)

    # Зберігаємо текст повідомлення в змінну користувача
    user_data = {'notification_text': notification_text}
    await message.answer("Оберіть тип нового повідомлення", reply_markup=add_noti_markup)

    # Зберігаємо дані користувача для обробки наступних кроків
    await AddStates.get_type_state.set()
    await state.update_data(user_data=user_data)

# Обрабка вибору типу повідомлень
@dp.message_handler(state=AddStates.get_type_state)
async def handle_notification_type(message: types.Message, state=FSMContext):
    user_state_data = await state.get_data()
    user_data = user_state_data['user_data']
    user_id = str(message.from_user.id)
    notification_type = message.text
    notification_text = user_data['notification_text']

    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)

    notification_counter = len(data_from_json.setdefault(user_id, {}).get("notifications", [])) + 1
    new_notification_key = f"notification{notification_counter}"
    new_notification = {
        "notification_text": notification_text,
        "notification_data": notification_type
    }

    if notification_type == 'У визначений день тиждня':
        # Виводимо меню для вибору дня тижня
        add_noti_day_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        item_pn = types.KeyboardButton(text='Пн')
        item_vt = types.KeyboardButton(text='Вт')
        item_sr = types.KeyboardButton(text='Ср')
        item_ct = types.KeyboardButton(text='Чт')
        item_pt = types.KeyboardButton(text='Пт')
        item_sb = types.KeyboardButton(text='Сб')
        item_nd = types.KeyboardButton(text='Нд')
        add_noti_day_markup.add(item_pn, item_vt, item_sr, item_ct, item_pt, item_sb, item_nd)
        await message.answer('Оберіть день для нового повідомлення', reply_markup=add_noti_day_markup)
        # Зберігаємо дані користувача для обробки наступних кроків
        # bot.register_next_step_handler(message, handle_notification_day, user_data, new_notification, new_notification_key)
        await AddStates.get_day_state.set()
        await state.update_data(new_notification=new_notification)
        await state.update_data(new_notification_key=new_notification_key)
    else:
        # Якщо тип повідомлення не "У визначений день тиждня", то зберігаємо його інформацію
        user_notifications = data_from_json.setdefault(user_id, {}).setdefault("notifications", [])
        new_notification["notification_day"] = None  # Додаємо поле "notification_day" зі значенням None
        user_notifications.append({new_notification_key: new_notification})  # Додавання як окремого словника
        with open("./users.JSON", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
        
        await message.answer('Повідомлення було додано', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

# Обробка вибору дня тижня
@dp.message_handler(state=AddStates.get_day_state)
async def handle_notification_type(message: types.Message, state=FSMContext):
    user_state_data = await state.get_data()
    user_data = user_state_data['user_data']
    new_notification = user_state_data['new_notification']
    new_notification_key = user_state_data['new_notification_key']
    user_id = str(message.from_user.id)
    notification_day = message.text
    data_from_json = {}

    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)

    new_notification["notification_day"] = notification_day  # Оновлюємо поле "notification_day"
    user_notifications = data_from_json.setdefault(user_id, {}).setdefault("notifications", [])
    user_notifications.append({new_notification_key: new_notification})  # Додавання як окремого словника
    with open("./users.JSON", "w") as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

    await message.answer('Повідомлення було додано', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

# Перелік станів для видалення повідомлень
class RemoveState(StatesGroup):
    get_remove_num = State()

# Команда /remove_notification
@dp.message_handler(commands=['remove_notification'])
async def remove_command(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)

    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)

    if user_id in data_from_json:
        user_notifications = data_from_json[user_id].get("notifications", [])
        if not user_notifications:
            await message.answer('У вас немає жодних повідомлень для видалення')
        else:
            # Виведення усіх повідомлень
            response = "Ваші повідомлення:\n"
            for i, notification_data in enumerate(user_notifications, start=1):
                notification_text = notification_data[list(notification_data.keys())[0]]["notification_text"]
                response += f"{i}. {notification_text}\n"
            await message.answer(response)

            # Створення клавіатури для видалення
            remove_notification_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = []
            for i, _ in enumerate(user_notifications, start=1):
                buttons.append(types.KeyboardButton(str(i)))
            buttons.append(types.KeyboardButton("Скасувати"))
            remove_notification_markup.add(*buttons)

            # await message.answer("Оберіть номер повідомлення, яке ви хочете видалити:", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Оберіть номер повідомлення, яке ви хочете видалити:", reply_markup=remove_notification_markup)
            await RemoveState.get_remove_num.set()
            await state.update_data(data_from_json=data_from_json)
            await state.update_data(user_notifications=user_notifications)
    else:
        await message.answer("Вас немає в базі користувачів.")

# Обробка підтвердження видалення повідомлення
@dp.message_handler(state=RemoveState.get_remove_num)
async def confirm_remove_notification(message: types.Message, state=FSMContext):
    user_state_data = await state.get_data()
    data_from_json = user_state_data['data_from_json']
    user_notifications = user_state_data['user_notifications']

    user_id = str(message.from_user.id)
    user_input = message.text

    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(user_notifications):
            removed_notification = user_notifications.pop(index)  # Видаляємо обране повідомлення
            with open("./users.JSON", "w") as f_o:
                json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
            await message.answer("Повідомлення було видалено", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer("Номер повідомлення недійсний. Спробуйте ще раз.", reply_markup=types.ReplyKeyboardRemove())
    elif user_input.lower() == "скасувати":
        await message.answer("Видалення повідомлення скасовано.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Невірний формат введення. Виберіть номер повідомлення або введіть 'скасувати'.")

# Перелік станів для редагування повідомлень
class EditState(StatesGroup):
    get_edit_num = State()
    get_edit_text = State()

# Команда /edit_notification
@dp.message_handler(commands=['edit_notification'])
async def edit_command(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)

    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)

    if user_id in data_from_json:
        user_notifications = data_from_json[user_id].get("notifications", [])
        if not user_notifications:
            await message.answer('У вас немає жодних повідомлень для редагування.')
        else:
            # Виведення усіх повідомлень для редагування
            response = "Ваші повідомлення для редагування:\n"
            for i, notification_data in enumerate(user_notifications, start=1):
                notification_text = notification_data[list(notification_data.keys())[0]]["notification_text"]
                response += f"{i}. {notification_text}\n"
            await message.answer(response)

            # Створення клавіатури для вибору повідомлення для редагування
            edit_notification_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = []
            for i, _ in enumerate(user_notifications, start=1):
                buttons.append(types.KeyboardButton(str(i)))
            buttons.append(types.KeyboardButton("Скасувати"))
            edit_notification_markup.add(*buttons)

            await message.answer("Оберіть номер повідомлення, яке ви хочете редагувати:", reply_markup=edit_notification_markup)
            await EditState.get_edit_num.set()
            await state.update_data(data_from_json=data_from_json)
            await state.update_data(user_notifications=user_notifications)
    else:
        await message.answer("Вас немає в базі користувачів.", reply_markup=types.ReplyKeyboardRemove())

# Обробка введення нового тексту для повідомлення
@dp.message_handler(state=EditState.get_edit_num)
async def enter_edit_text(message: types.Message, state: FSMContext):
    user_state_data = await state.get_data()
    data_from_json = user_state_data['data_from_json']
    user_notifications = user_state_data['user_notifications']

    user_id = str(message.from_user.id)
    user_input = message.text

    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(user_notifications):
            await message.answer("Введіть новий текст для повідомлення:", reply_markup=types.ReplyKeyboardRemove())
            await EditState.get_edit_text.set()
            await state.update_data(data_from_json=data_from_json)
            await state.update_data(user_notifications=user_notifications)
            await state.update_data(index=index)
        else:
            await message.answer("Номер повідомлення недійсний. Спробуйте ще раз.")
    elif user_input.lower() == "скасувати":
        await message.answer("Редагування повідомлення скасовано.")
    else:
        await message.answer("Невірний формат введення. Виберіть номер повідомлення або введіть 'скасувати'.")

# Обробка оновлення тексту повідомлення
@dp.message_handler(state=EditState.get_edit_text)
async def update_notification_text(message: types.Message, state: FSMContext):
    user_state_data = await state.get_data()
    data_from_json = user_state_data['data_from_json']
    user_notifications = user_state_data['user_notifications']
    index = user_state_data['index']

    user_id = str(message.from_user.id)
    new_text = message.text

    if new_text:
        user_notifications[index][list(user_notifications[index].keys())[0]]["notification_text"] = new_text
        with open("./users.JSON", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
        await message.answer("Текст повідомлення було оновлено.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("Новий текст повідомлення не може бути порожнім.")

# Перелік станів для видалення користувача
class RemoveUserState(StatesGroup):
    get_confirmation = State()

# Команда /remove_user
@dp.message_handler(commands=['remove_user'])
async def remove_user_command(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)

    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)

    if user_id in data_from_json:
        remove_user_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        accept_btn = types.KeyboardButton("Так")
        cancel_btn = types.KeyboardButton("Ні")
        remove_user_markup.add(accept_btn, cancel_btn)
        await message.answer("Ви впевнені, що хочете видалити свій обліковий запис? Це неможливо буде відмінити.", reply_markup=remove_user_markup)
        await RemoveUserState.get_confirmation.set()
    else:
        await message.answer("Вас немає в базі користувачів.")

# Обробка підтвердження видалення користувача
@dp.message_handler(state=RemoveUserState.get_confirmation)
async def confirm_remove_user(message: types.Message, state=FSMContext):
    user_id = str(message.from_user.id)

    if message.text == "Так":
        # Видалити користувача із бази даних
        with open("./users.JSON", "r") as f_o:
            data_from_json = json.load(f_o)

        data_from_json.pop(user_id)

        with open("./users.JSON", "w") as f_w:
            json.dump(data_from_json, f_w, indent=4, ensure_ascii=False)

        await message.answer(f"Ваш обліковий запис успішно видалено. До зустрічі, {message.from_user.first_name}!", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("Видалення облікового запису скасовано.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

# Повертаємо текст який не є командою
@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'На початку місяця' or message.text == 'В кінці місяця' or message.text == 'У визначений день':
        await bot.send_message(message.chat.id, "Ви напевно забули ввести команду /add_notification. Введіть її та повторіть будь ласка")
    else:
        await bot.send_message(message.chat.id, "Вибачте, я напевно вас не зрозумів.\nПовторіть будь ласка, або перевірте чи можу я це виконати за допомогою команди /help")
    
# Функція для відправки повідомлення
async def send_notification(user_id, notification_info):
    try:
        chat_id = int(user_id)
        text = notification_info.get("notification_text")
        await bot.send_message(chat_id, text)
    except Exception as e:
        print(f"Error sending notification: {e}")

# Перейменування англійських днів тижня для перевірки
def rename_days():
    today_name = datetime.now().strftime("%A")
    if today_name == 'Monday':
        today_name = "Пн"
    elif today_name == 'Tuesday':
        today_name = "Вт"
    elif today_name == 'Wednesday':
        today_name = "Ср"
    elif today_name == 'Thursday':
        today_name = "Чт"
    elif today_name == 'Friday':
        today_name = "Пт"
    elif today_name == 'Saturday':
        today_name = "Сб"
    elif today_name == 'Sunday':
        today_name = "Нд"

# Функція для перевірки та відправки повідомлень
async def send_daily_notifications():
    with open("./users.JSON", "r") as f_o:
        data_from_json = json.load(f_o)

    for user_id, user_data in data_from_json.items():
        notifications = user_data.get("notifications", [])
        for notification in notifications:
            for notification_key, notification_info in notification.items():
                notification_text = notification_info.get("notification_text")
                notification_data = notification_info.get("notification_data")
                notification_day = notification_info.get("notification_day")

                if notification_data == "На початку місяця" and datetime.now().day == 1:
                    await send_notification(int(user_id), f"НАГАДУЮ!\n{notification_info}")
                elif notification_data == "В кінці місяця" and datetime.now().day == 30:
                    await send_notification(int(user_id), notification_info)
                elif notification_data == "У визначений день тиждня":
                    rename_days()
                    if notification_day == datetime.now().strftime("%A"):
                        await send_notification(int(user_id), notification_info)

# Обробник часу
async def scheduled(wait_for):
    while True:
        now = datetime.now()
        hours = now.hour
        minutes = now.minute
        if hours == 8 and minutes == 0:
            await send_daily_notifications()
        await asyncio.sleep(wait_for)

# Запуск бота та обробника часу
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(90))
    executor.start_polling(dp, skip_updates=True)
