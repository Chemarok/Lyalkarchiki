import telebot
import webbrowser
from telebot import types
import sqlite3
from telegram.ext import CallbackContext, CallbackQueryHandler
import datetime
import threading
from time import sleep
from telebot.types import WebAppInfo
import json
import config

bot = telebot.TeleBot('7631342234:AAG78itP6ZBMn3gH4gxDS-VmLaFp-nreyl0')
def delete_message_after_delay(chat_id, message_id, delay=5):
    threading.Timer(delay, lambda: bot.delete_message(chat_id, message_id)).start()

homework_data = {}
all_users = set()
def register_user(user_id):
    all_users.add(user_id)
user_data = {}
user_messages = {}
birthdays = {
    "01-05": "Лариса Василівна",
    "01-12": "Марія Сергіївна",
    "01-23": "Тетяна Іванівна",
    "01-29": "Євген Іванович",
    "02-27": "Леся Петрівна",
    "03-06": "Дар’я Олексіївна",
    "03-13": "Леонід Петрович",
    "03-25": "Анастасія Петрівна",
    "04-19": "Леся Ярославівна",
    "06-03": "Михайло Якович",
    "06-04": "Волокушина",
    "07-03": "Віра Миколаївна",
    "07-06": "Катерина Олександрівна",
    "08-25": "Задорожня Даря",
    "08-28": "Войткович-Шевченко",
    "10-23": "Лада Дмитрівна",
    "10-26": "Олександр Людвигович та Людмила Олександрівна",
    "10-30": "Іван Валентинович",
    "11-27": "Сергій Олександрович",
    "12-06": "Руслан Валентинович",
    "12-10": "Ірина Іванівна",
}

# Підключення до бази даних
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Створюємо таблицю, якщо її немає
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()



@bot.message_handler(commands=['start'])
def start(message):
    register_user(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('📅 Розклад пар', callback_data='Plans')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('🌐 Соцмережі', callback_data='Media')
    btn3 = types.InlineKeyboardButton('⏰ Нагадування', callback_data='Notes')
    markup.row(btn2, btn3)
    btn4 = types.InlineKeyboardButton('📞 Важливі номери', callback_data='Numbers')
    btn5 = types.InlineKeyboardButton('🔗 Корисні посилання', callback_data='us_web')
    markup.row(btn4, btn5)
    btn6 = types.InlineKeyboardButton('📚 Домашнє завдання', callback_data='home_w')
    markup.row(btn6)
    btn8 = types.InlineKeyboardButton('🎮 Ігри', callback_data='games')
    markup.row(btn8)
    #btn7 = types.InlineKeyboardButton('💸 Підтримати автора', callback_data='donate')
    #markup.row(btn7)
    #file = open('SaM studio.png', 'rb')
    #bot.send_photo(message.chat.id, photo=file, caption='SaM studio',  reply_markup=markup)
    bot.send_message(message.chat.id, "🎭 <b>Привіт, лялькарю!</b> 🧵✨\n\n"
        "Я твій новий помічник у навчанні та повсякденних справах. Давай спрощувати життя разом!\n\n"
        "Ось, що я можу для тебе:\n"
        "📅 <b>Розклад пар</b> — щоб ти завжди знав(-ла), коли і де заняття.\n"
        "🌐 <b>Соцмережі</b> — швидкий доступ до наших спільнот та важливих новин.\n"
        "⏰ <b>Нагадування</b> — щоб не пропустити важливі події чи дедлайни.\n"
        "📞 <b>Важливі номери</b> — щоб довго не шукати в *Страстях*.\n"
        "🔗 <b>Корисні посилання</b> — ресурси, які стануть у пригоді.\n"
        "📚 <b>Домашнє завдання</b> — записуй свої завдання та переглядай їх у будь-який момент.\n\n"
        "Обери що тобі потрібно нижче, і я одразу допоможу! 🚀\n"
        "Разом ми впораємось із будь-яким завданням! 💪", reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    if message.web_app_data and message.web_app_data.data:
        try:
            data = json.loads(message.web_app_data.data)
            amount = data.get('amount', 0)
            bot.send_message(message.chat.id, f"Отримано дані: {amount}")
            bot.send_invoice(
                chat_id=message.chat.id,
                title='Дякую за підтримку!',
                description='Оплатити товар',
                invoice_payload='invoice',  # Ідентифікатор платежу
                provider_token='5775769170:LIVE:TG_k__FwSt0MNppRyJxSNV0GusA',
                currency='UAH',  # Код валюти
                prices=[types.LabeledPrice('DONATION', amount * 100)]  # Сума у копійках
            )
            #bot.send_invoice(message.chat.id, 'Дякую за підритмку', 'Оплатити товар', 'invoice', '2051251535:TEST:OTk5MDA4ODgxLTAwNQ', 'UAH', [types.LabeledPrice('DONATION', amount * 100)])
        except json.JSONDecodeError:
            bot.send_message(message.chat.id, "Не вдалося обробити дані.")
    else:
        bot.send_message(message.chat.id, "Дані не отримано.")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Plans_2':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "📅 <b>Розклад пар</b>\n\n"
        "🔸 <b>Понеділок:</b> \n"
        "09:30 – 11:00 🎤 Вокал\n"
        "11:10 – 12:40 🎭 Майстерність актора\n"
        "13:30 – 15:00 🎨 ТВТЛ\n"
        "15:10 – 16:40 🖐️ Майстерність роботи з планшетною лялькою\n\n"
        
        "🔸 <b>Вівторок:</b> \n"
        "09:30 – 11:00 🎭 Майстерність роботи з маскою\n"
        "11:10 – 12:40 🎤 Вокал\n"
        "13:30 – 15:00 💃 Танці\n"
        "15:10 – 16:40 🎭 Майстерність актора\n\n"
        
        "🔸 <b>Середа:</b> \n"
        "09:30 – 11:00 🖐️ Майстерність роботи з планшетною лялькою\n"
        "11:10 – 12:40 🎤 Вокал\n"
        "13:30 – 15:00 🎨 ТВТЛ\n"
        "15:10 – 16:40 🎭 Майстерність роботи з маскою\n\n"
        
        "🔸 <b>Четвер:</b> \n"
        "09:30 – 11:00 🎭 Майстерність актора\n"
        "11:10 – 12:40 🖐️ Майстерність роботи з планшетною лялькою\n"
        "13:30 – 15:00 🎤 Вокал\n"
        "15:10 – 16:40 💃 Танці\n\n"
        
        "🔸 <b>П’ятниця:</b> \n"
        "09:30 – 11:00 🎨 ТВТЛ\n"
        "11:10 – 12:40 🎭 Майстерність роботи з маскою\n"
        "13:30 – 15:00 🎤 Вокал\n"
        "15:10 – 16:40 🎭 Майстерність актора\n\n"
        
        "🔸 <b>Субота:</b> \n"
        "09:30 – 11:00 🎭 Майстерність актора\n"
        "11:10 – 12:40 🖐️ Майстерність роботи з планшетною лялькою\n"
        "13:30 – 15:00 🎨 ТВТЛ\n"
        "15:10 – 16:40 💃 Танці\n\n"
        
        "🔸 <b>Неділя:</b> \n"
        "🌟 Вихідний! Відпочивай і надихайся! 😊", parse_mode='html', reply_markup=markup)
    elif callback.data == 'back_to_main':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        start(callback.message)
    elif callback.data == 'Notes':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_prepod = types.InlineKeyboardButton('Дні народження викладачів🥳', callback_data='prepod_dr')
        markup.row(btn_prepod)
        btn_stud_dr = types.InlineKeyboardButton('Дні народження студентів🥃🍭', callback_data='stud_dr')
        markup.row(btn_stud_dr)
        btn_sessia= types.InlineKeyboardButton('💀Розклад сессії💀', callback_data='sessia')
        markup.row(btn_sessia)
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id,"⏰ <b>Нагадування:</b>\n\n"
    "Ти готовий до нових досягнень? 😊\n\n"
    "Не забувай про важливі події та дедлайни! 📅\n\n"
    "Ми можемо нагадати про:\n",  parse_mode='html', reply_markup=markup )
    elif callback.data == 'sessia':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id,  "🎓 <b>Розклад сесії:</b>\n\n"
    "Розклад? Який розклад? Зараз же <b>канікули</b>! 🏖️✨\n"
    "Відпочивай, кайфуй і роби вигляд, що сесії не існує. 😎\n\n"
    "Але не хвилюйся, я тримаю все під контролем – як тільки щось з’явиться, ти дізнаєшся першим! 🚀", parse_mode='html', reply_markup=markup)
    elif callback.data == 'prepod_dr':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "🎉 <b>Дні народження викладачів кафедри:</b>\n\n"
    "🔹 <b>Січень:</b>\n"
    "05.01 – Іщенко\n"
    "12.01 – Погребняк\n"
    "23.01 – Сільченко\n"
    "29.01 – Огородній\n\n"
    "🔹 <b>Лютий:</b>\n"
    "27.02 – Овчієва\n\n"
    "🔹 <b>Березень:</b>\n"
    "06.03 – Гололобова\n"
    "13.03 – Попов\n"
    "25.03 – Івановська\n\n"
    "🔹 <b>Квітень:</b>\n"
    "19.04 – Бартко\n\n"
    "🔹 <b>Червень:</b>\n"
    "03.06 – Урицький\n"
    "04.06 – Волокушина\n\n"
    "🔹 <b>Липень:</b>\n"
    "03.07 – Задорожня Віра\n"
    "06.07 – Лукяненко\n\n"
    "🔹 <b>Серпень:</b>\n"
    "25.08 – Задорожня Даря\n"
    "28.08 – Войткович-Шевченко\n\n"
    "🔹 <b>Жовтень:</b>\n"
    "23.10 – Вальчук\n"
    "26.10 – Андрушкевич\n"
    "26.10 – Сніцар\n"
    "30.10 – Вороний\n\n"
    "🔹 <b>Листопад:</b>\n"
    "27.11 – Чуркін\n\n"
    "🔹 <b>Грудень:</b>\n"
    "06.12 – Неупокоєв\n"
    "10.12 – Мельник\n\n"
    "🎂 Не забудь привітати улюблених викладачів! 🥳", parse_mode='html', reply_markup=markup)
    elif callback.data == 'stud_dr_2':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "🎉 <b>Дні народження студентів:</b>\n\n"
    "✨ <b>Лютий:</b>\n"
    "18.02.2004 – Оля Камінська (ртл)\n\n"
    "✨ <b>Березень:</b>\n"
    "26.03.2006 – Толік Сергєєв (атл)\n\n"
    "✨ <b>Квітень:</b>\n"
    "09.04.2003 – Дарина Баранецька (ртл)\n"
    "29.04.2006 – Оля Білаш (ртл)\n\n"
    "✨ <b>Травень:</b>\n"
    "08.05.2006 – Марк Огородній (атл)\n"
    "10.05.2006 – Макар Кожушко (атл)\n\n"
    "✨ <b>Червень:</b>\n"
    "27.06 – Влад Сенцов (стл)\n\n"
    "✨ <b>Липень:</b>\n"
    "08.07.2006 – Маша Олійник (стл)\n\n"
    "✨ <b>Серпень:</b>\n"
    "01.08.2005 – Ліля Мойсеєнко (атл)\n"
    "20.08.2006 – Катя Ігнатенко (атл)\n"
    "21.08.2006 – Соня Волинець (атл)\n"
    "24.08.2006 – Настя Терехова (атл)\n"
    "29.08.2003 – Міша Мокрянин (атл)\n\n"
    "✨ <b>Жовтень:</b>\n"
    "07.10.2005 – Маша Момот (атл)\n"
    "22.10.2004 – Денис Примушко (атл)\n\n"
    "✨ <b>Листопад:</b>\n"
    "29.11.2005 – Рома Овчаренко (атл)\n\n"
    "✨ <b>Грудень:</b>\n"
    "28.12.2002 – Богдан Реплюк (атл)\n\n"
    "🎂 Не забудь привітати своїх одногрупників! 🥳", parse_mode='html', reply_markup=markup)
    elif callback.data == 'Media':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        first_course_med = types.InlineKeyboardButton('1 - АМТЛ', callback_data='1_media')
        markup.row(first_course_med)
        yt_first = types.InlineKeyboardButton('🎥 YouTube', url='https://www.youtube.com/@MaisterniaNeupokoieva')
        inst_first = types.InlineKeyboardButton('📸 Instagram', url='https://www.instagram.com/_neupokoi_/')
        tt_first = types.InlineKeyboardButton('🎶 TikTok', url='https://www.tiktok.com/@neupokoivtsi?_t=ZM-8sqJvecXxvp&_r=1')
        markup.row(yt_first,inst_first,tt_first)
        sec_course_med = types.InlineKeyboardButton('2 - АМТЛ', callback_data='2_media')
        markup.row(sec_course_med)
        yt_sec = types.InlineKeyboardButton('🎥 YouTube', url='https://www.youtube.com/@maysternya.si_')
        inst_sec = types.InlineKeyboardButton('📸 Instagram', url='https://www.instagram.com/maysternya.si_/')
        tt_sec = types.InlineKeyboardButton('🎶 TikTok', url='https://www.tiktok.com/@maysternya.si?_t=ZM-8sqJtLG0SrW&_r=1')
        markup.row(yt_sec, inst_sec, tt_sec)
        third_course_med = types.InlineKeyboardButton('3 - АМТЛ', callback_data='3_media')
        markup.row(third_course_med)
        yt_third = types.InlineKeyboardButton('🎥 YouTube', url='https://www.youtube.com/@popovtsi')
        inst_third = types.InlineKeyboardButton('📸 Instagram', url='https://www.instagram.com/popovtsi/')
        markup.row(yt_third, inst_third)
        four_course_med = types.InlineKeyboardButton('4 - АМТЛ', callback_data='4_media')
        markup.row(four_course_med)
        yt_four = types.InlineKeyboardButton('🎥 YouTube', url='https://www.youtube.com/@%D0%9C%D0%B0%D0%B9%D1%81%D1%82%D0%B5%D1%80%D0%BD%D1%8F%D0%9C.%D0%AF.%D0%A3%D1%80%D0%B8%D1%86%D1%8C%D0%BA%D0%BE%D0%B3%D0%BE')
        inst_four = types.InlineKeyboardButton('📸 Instagram', url='https://www.instagram.com/urytski/')
        markup.row(yt_four, inst_four)
        kafedra_med = types.InlineKeyboardButton('КАФЕДРА', callback_data='kafedra_med')
        markup.row(kafedra_med)
        site_kaf= types.InlineKeyboardButton('🌐WEB', url='https://knutkt.edu.ua/struktura/fakultet-teatralnoho-mystetstva/kafedra-mystetstva-teatru-lialok/pro-kafedru/')
        facebook_kaf = types.InlineKeyboardButton('📸 Instagram', url='https://www.instagram.com/knutkit_puppeteers/')
        inst_kaf = types.InlineKeyboardButton('💬Facebook', url='https://www.facebook.com/knutkitKarpenkoKary?locale=ru_RU')
        markup.row(site_kaf, facebook_kaf, inst_kaf)
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "🌐 <b>Соцмережі:</b>\n\n"
    "Я зібрав для вас посилання на усі сторінки наших студентів та кафедри. 📱\n\n"
    "Переглядайте акаунти кожного курсу, а також офіційні канали кафедри, щоб бути в курсі всіх подій! ✨\n\n"
    "Посилання нижче: 👇", parse_mode='html', reply_markup=markup)
    elif callback.data == 'Numbers':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "📞🔽🔽 <b>Важливі номери телефонів</b> 🔽🔽 📞\n\n"
        "👩‍🔬 <b>Завідувач навчальної лабораторії</b>\n"
        "Сніцар Людмила Олександрівна\n"
        "📱 +380503812155\n\n"
        "👨‍🏫 <b>Завідувач кафедри</b>\n"
        "Неупокоєв Руслан Валентинович\n"
        "📱 +380506682303\n\n"
        "🏛️ <b>Деканат</b>\n"
        "📞 +380442720227\n"
        "📞 +380442341190\n\n"
        "🔧 <b>Реквізиторський цех</b>\n"
        "Вороний Іван Валентинович\n"
        "📱 +380938502329\n"
        "📱 +380679980997\n\n"
        "Будь ласка, збережи ці контакти, щоб вони завжди були під рукою! 😊", parse_mode='html', reply_markup=markup)
    elif callback.data == 'us_web':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id,  "🌐 <b>Корисні посилання для студентів</b> 🌐\n\n"
        "1️⃣ <b>ChatGPT</b> — Твій незамінний помічник у навчанні та житті.\n"
        "<a href='https://chat.openai.com/'>https://chat.openai.com/</a>\n\n"
        "2️⃣ <b>Офіційний сайт КНУТКіТ</b> — Новини, розклад та вся необхідна інформація.\n"
        "<a href='https://knutkt.edu.ua/'>https://knutkt.edu.ua/</a>\n\n"
        "3️⃣ <b>Wepa UNIMA</b> — Міжнародний ресурс про театр ляльок.\n"
        "<a href='https://wepa.unima.org/'>https://wepa.unima.org/</a>\n\n"
        "Зберігай ці посилання та використовуй, коли потрібно! 😊", parse_mode='html', reply_markup=markup)
    elif callback.data == 'home_w':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_add_hw = types.InlineKeyboardButton('📝 Додати завдання', callback_data='add_homework')
        markup.row(btn_add_hw)
        btn_view_hw = types.InlineKeyboardButton('📖 Переглянути завдання', callback_data='view_homework')
        markup.row(btn_view_hw)
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "📚 <b>Домашнє завдання</b>\n\n"
        "Тут ти можеш:\n"
        "📝 <b>Додати</b> нове завдання.\n"
        "📖 <b>Переглянути</b> всі записані завдання.\n"
        "🗑️ <b>Видалити</b> виконані завдання.\n\n"
        "Обери дію нижче, і я допоможу! 😊", parse_mode='html', reply_markup=markup)
    elif callback.data == 'add_homework':
        handle_home_work(callback)
    elif callback.data == 'view_homework':
        handle_homework_view(callback)
    elif callback.data.startswith('delete_'):
        handle_homework_delete(callback)
    elif callback.data == 'games':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_add_hw = types.InlineKeyboardButton('🧩 2048', web_app=WebAppInfo(url='https://raw.githack.com/Chemarok/test-1/main/WEBAPP.html'))
        markup.row(btn_add_hw)
        #btn_view_hw = types.InlineKeyboardButton('📖 Переглянути завдання', callback_data='view_homework')
        #markup.row(btn_view_hw)
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "🎮 Знаю, знаю... іноді на парах може бути ну дуууже весело, правда? 😏\n\n"
        "Саме для таких моментів я підготував кілька ігор, щоб ти не нудьгував(-ла)!\n\n"
        "Обирай гру та насолоджуйся. Але не забувай про навчання, лялькарю! 😉\n", parse_mode='html', reply_markup=markup)
    elif callback.data == 'donate':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.ReplyKeyboardMarkup()

        support_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        support_btn = types.KeyboardButton('💸 Підтримати автора', web_app=WebAppInfo(url='https://raw.githack.com/Chemarok/test-1/main/WEBAPP.html'))
        support_markup.add(support_btn)

        bot.send_message(callback.message.chat.id, "<b>Підтримати творця бота !</b> 🎭✨\n\n"
    "Твій внесок допоможе створювати ще більше крутих матеріалів для студентів. 😮‍💨\n\n "
    "Обери суму, яка тобі підходить, та зроби свій внесок у розвиток мистецтва! 💙", parse_mode='html', reply_markup=support_markup)

    elif callback.data == 'Plans':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        plans_1 = types.InlineKeyboardButton('🎓 Перший курс', callback_data='no_info')
        markup.row(plans_1)
        plans_2 = types.InlineKeyboardButton('🎓 Другий курс', callback_data='Plans_2')
        markup.row(plans_2)
        plans_3 = types.InlineKeyboardButton('🎓 Третій курс', callback_data='no_info')
        markup.row(plans_3)
        plans_4 = types.InlineKeyboardButton('🎓 Четвертий курс', callback_data='no_info')
        markup.row(plans_4)
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id,"📚 Обери курс, розклад якого хочеш переглянути:\n\n"
        "🎓 Перший курс\n"
        "🎓 Другий курс\n"
        "🎓 Третій курс\n"
        "🎓 Четвертий курс\n\n"
        "Тисни на відповідну кнопку, і я одразу покажу потрібну інформацію! 😊" ,parse_mode='html', reply_markup=markup)
    elif callback.data == 'stud_dr':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        dr_1 = types.InlineKeyboardButton('1️⃣ Перший курс', callback_data='no_info')
        markup.row(dr_1)
        dr_2 = types.InlineKeyboardButton('2️⃣ Другий курс', callback_data='stud_dr_2')
        markup.row(dr_2)
        dr_3 = types.InlineKeyboardButton('3️⃣ Третій курс', callback_data='no_info')
        markup.row(dr_3)
        dr_4 = types.InlineKeyboardButton('4️⃣ Четвертий курс', callback_data='no_info')
        markup.row(dr_4)
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id,"🎂 Обери курс, щоб переглянути дні народжень студентів:\n\n"
        "1️⃣ Перший курс\n"
        "2️⃣ Другий курс\n"
        "3️⃣ Третій курс\n"
        "4️⃣ Четвертий курс\n\n"
        "Тисни на кнопку нижче, щоб дізнатися, хто сьогодні святкує! 🎉" ,parse_mode='html', reply_markup=markup)
    elif callback.data == 'no_info':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='back_to_main')
        markup.row(btn_back)
        bot.send_message(callback.message.chat.id, "На жаль, у мене поки що немає достовірної інформації для цього розділу. 😔\n\n"
        "Будь ласка, допоможи мені її отримати! Якщо в тебе є актуальні дані, "
        "надішли сюди @CHEMAROK, і я додам їх до бази. 💌", parse_mode='html', reply_markup=markup)

    # Обробка кнопок домашнього завдання
def handle_home_work(callback):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='home_w')
        markup.row(btn_back)
        msg = bot.send_message(callback.message.chat.id, "📚 Напиши своє домашнє завдання і я збережу його для тебе! ✨", reply_markup=markup)

        user_messages[callback.message.chat.id] = msg.message_id
        # Ось тут ініціюємо обробку тексту домашнього завдання
        bot.register_next_step_handler(msg, save_homework)

def save_homework(message):
        chat_id = message.chat.id

        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception as e:
            print(f"Помилка видалення тексту: {e}")

        if chat_id in user_messages:
            try:
                bot.delete_message(chat_id, user_messages[chat_id])
                del user_messages[chat_id]
            except Exception as e:
                print(f"Помилка видалення попереднього повідомлення: {e}")

        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='home_w')
        markup.row(btn_back)
        # Отримуємо текст завдання від користувача
        task = message.text

        # Збереження завдання в базі даних
        cursor.execute('''INSERT INTO tasks (user_id, task) VALUES (?, ?)''', (message.chat.id, task))
        conn.commit()

        # Повідомлення користувачу, що завдання збережено
        bot.send_message(message.chat.id, "✅ Твоє домашнє завдання успішно збережено!", reply_markup=markup)

    # Додамо ще одну функцію для перегляду збережених завдань

def handle_homework_view(callback):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('<<НАЗАД', callback_data='home_w')
        markup.row(btn_back)

        # Отримуємо завдання користувача з бази
        cursor.execute('''SELECT id, task, timestamp FROM tasks WHERE user_id = ? ORDER BY timestamp DESC''',
                       (callback.message.chat.id,))
        tasks = cursor.fetchall()

        if tasks:
            message_text = "📚 <b>Твоє домашнє завдання:</b>\n\n"
            for task_id, task, timestamp in tasks:
                # Кнопка для видалення завдання
                btn_delete = types.InlineKeyboardButton(f'❌ Видалити {task[:20]}...', callback_data=f'delete_{task_id}')
                markup.row(btn_delete)
                message_text += f"📅 {timestamp} — {task}\n"
            bot.send_message(callback.message.chat.id, message_text, parse_mode='html', reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, "❗ У тебе ще немає збережених домашніх завдань.",
                             reply_markup=markup)

    # Функція для видалення завдання

def handle_homework_delete(callback):
        task_id = callback.data.split('_')[1]

        # Видалення завдання з бази даних
        cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
        conn.commit()

        # Повідомлення користувачу про видалення
        msg = bot.send_message(callback.message.chat.id, "✅ Завдання було успішно видалено!")
        delete_message_after_delay(msg.chat.id, msg.message_id, delay=5)
        # Функція для перевірки днів народжень


def check_birthdays_7():
    while True:
        today = datetime.date.today()
        for date_str, name in birthdays.items():
            # Конвертуємо дату народження у формат MM-DD
            birthday_date = datetime.datetime.strptime(date_str, "%m-%d").date()
            # Додаємо рік поточного року
            birthday_date = birthday_date.replace(year=today.year)

            # Нагадування за тиждень
            reminder_date = birthday_date - datetime.timedelta(days=7)

            if today == reminder_date:
                send_birthday_reminder_7(name, birthday_date)

        sleep(86400)  # Перевірка раз на добу

    # Функція для відправки нагадування

def check_birthdays_1():
    while True:
        today = datetime.date.today()
        for date_str, name in birthdays.items():
            # Конвертуємо дату народження у формат MM-DD
            birthday_date = datetime.datetime.strptime(date_str, "%m-%d").date()
            # Додаємо рік поточного року
            birthday_date = birthday_date.replace(year=today.year)

            # Нагадування за тиждень
            reminder_date = birthday_date

            if today == reminder_date:
                send_birthday_reminder_1(name, birthday_date)

        sleep(86400)  # Перевірка раз на добу


def send_birthday_reminder_7(name, birthday_date):
    for chat_id in all_users:  # Перебираємо підписаних користувачів
        bot.send_message(chat_id,
                         f"📢 Нагадуємо, що {birthday_date.strftime('%d.%m')} святкує день народження <b>{name}</b>! 🥳", parse_mode='html')
        bot.send_message(chat_id, "Не забудь привітати!")

def send_birthday_reminder_1(name, birthday_date):
    for chat_id in all_users:  # Перебираємо підписаних користувачів
        bot.send_message(chat_id,
                         f"📢 Нагадуємо, що сьогоднія' святкує день народження <b>{name}</b>! 🥳",
                             parse_mode='html')
        bot.send_message(chat_id, "Не забудь привітати!")
    # Запуск окремого потоку для перевірки днів народжень


birthday_thread = threading.Thread(target=check_birthdays_7)
birthday_thread = threading.Thread(target=check_birthdays_1)
birthday_thread.start()


bot.polling(none_stop=True)