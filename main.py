import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import psycopg2
import time

bot = telebot.TeleBot('TOKEN')

conn = psycopg2.connect(host='host', user='user', password='pwd', database='db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users_demo(
    userid BIGINT PRIMARY KEY,
    closed_club BOOLEAN,
    username VARCHAR,
    name VARCHAR,
    activity VARCHAR, 
    social_media VARCHAR,
    interests VARCHAR,
    this_week VARCHAR, 
    dates VARCHAR,
    finished BOOLEAN,
    format VARCHAR
)""")
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()
        print(message.chat.id)

        if info is None:
            kb = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Закрытый Клуб', callback_data='closed')
            btn2 = types.InlineKeyboardButton('Друзья Клуба', callback_data='friend')
            kb.add(btn1)
            kb.add(btn2)

            cur.execute(f"INSERT INTO users_demo VALUES('{message.from_user.id}', {False}, '{message.from_user.username}',"
                        f" '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{False}', '{0}')")
            conn.commit()
            bot.send_photo(message.chat.id, open('памятка.png', 'rb'), 'Привет!👋\n\nЯ Random Coffee бот Бизнес-клуба'
                                                                       ' ВШЭ!\n\nКаждую неделю я'
                                              ' буду предлагать тебе для встречи интересного человека, случайно'
                                              ' выбранного среди других резидентов Клуба.\n\n'
                                              'Выбери, к какой части Клуба ты относишься:', reply_markup=kb)

        else:
            if not info[9]:
                kb = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Закрытый Клуб', callback_data='closed')
                btn2 = types.InlineKeyboardButton('Друзья Клуба', callback_data='friend')
                kb.add(btn1)
                kb.add(btn2)

                cur.execute(f"""UPDATE users_demo SET closed_club={False}, username='{message.from_user.username}', name='{0}', activity='{0}', 
                social_media='{0}', interests='{0}', this_week='{0}', dates='{0}', finished='{False}', format='{0}' 
                WHERE userid={message.chat.id}""")
                conn.commit()
                bot.send_photo(message.chat.id, open('памятка.png', 'rb'),
                               'Привет!👋\n\nЯ Random Coffee бот Бизнес-клуба'
                               ' ВШЭ!\n\nКаждую неделю я'
                               ' буду предлагать тебе для встречи интересного человека, случайно'
                               ' выбранного среди других резидентов Клуба.\n\n'
                               'Выбери, к какой части Клуба ты относишься:', reply_markup=kb)
            else:
                ask_remake(message)

    except ApiTelegramException:
        pass


@bot.message_handler(commands=['restart'])
def ask_remake(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data='yes_remake')
    kb.add(btn1)
    bot.send_message(message.chat.id, 'Хочешь перезаполнить анкету?', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data == 'yes_remake')
def remake(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    name(call.message)


@bot.message_handler(commands=['help'])
def help_bk(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text='Поменять данные профиля')
    btn2 = types.KeyboardButton(text='Приостановить участие')
    kb.add(btn1)
    kb.add(btn2)

    bot.send_message(message.chat.id, 'Выбери подходящую опцию ниже.\nЕсли у тебя запрос посложнее, просто напиши его'
                                      ' в ответ, и (может и не сразу, но обязательно) сотрудник HSE BC Random Coffee'
                                      ' увидит его и ответит тебе.\n\nЧтобы перезапустить это меню, ты в любой момент'
                                      ' можешь ввести /help', reply_markup=kb)
    bot.register_next_step_handler(message, help_raspr)


def help_raspr(message):
    if message.text == 'Поменять данные профиля':
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Своё имя', callback_data='name')
        btn2 = types.InlineKeyboardButton('Ссылка на соц. сеть', callback_data='social')
        btn3 = types.InlineKeyboardButton('Кем работаю', callback_data='work')
        btn4 = types.InlineKeyboardButton('О себе', callback_data='about')
        btn5 = types.InlineKeyboardButton('Формат', callback_data='form')
        kb.add(btn1)
        kb.add(btn2)
        kb.add(btn3)
        kb.add(btn4)
        kb.add(btn5)

        bot.send_message(message.chat.id, 'Ок, выбери что хочешь сменить', reply_markup=kb)

    elif message.text == 'Приостановить участие':

        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Пауза на месяц🚫', callback_data='miss_month')
        btn2 = types.InlineKeyboardButton('Бессрочно', callback_data='inf')
        btn3 = types.InlineKeyboardButton('Назад', callback_data='back1')
        kb.add(btn1)
        kb.add(btn2)
        kb.add(btn3)
        bot.send_message(message.chat.id, 'Выбери период, на который хочешь приостановить встречи.\n\nПри любом варианте бот на это'
                                          ' время перестанет присылать все рассылки', reply_markup=kb)

    else:
        bot.send_message(message.chat.id, 'Спасибо! Ответ записан')


@bot.callback_query_handler(func=lambda call: call.data == 'back1')
def change(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    help_bk(call.message)


@bot.callback_query_handler(func=lambda call: call.data in ['name', 'social', 'work', 'about', 'form'])
def change(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'name':
        bot.send_message(chat_id=call.message.chat.id, text='Напиши на что хочешь заменить')
        bot.register_next_step_handler(call.message, change_name)
    elif call.data == 'social':
        bot.send_message(chat_id=call.message.chat.id, text='Напиши на что хочешь заменить')
        bot.register_next_step_handler(call.message, change_social)
    elif call.data == 'work':
        bot.send_message(chat_id=call.message.chat.id, text='Напиши на что хочешь заменить')
        bot.register_next_step_handler(call.message, change_work)
    elif call.data == 'about':
        bot.send_message(chat_id=call.message.chat.id, text='Напиши на что хочешь заменить')
        bot.register_next_step_handler(call.message, change_about)
    elif call.data == 'form':
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Онлайн', callback_data='change_online')
        btn2 = types.InlineKeyboardButton('Оффлайн', callback_data='change_offline')
        kb.add(btn1)
        kb.add(btn2)

        bot.send_message(call.message.chat.id, 'В каком формате ты бы предпочёл встречу?', reply_markup=kb)


def change_name(message):
    cur.execute(f"""UPDATE users_demo SET name='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=message.chat.id, text="Данные изменены!\n\nВот так теперь выглядит твоя анкета⏬")
    show(message)


def change_social(message):
    cur.execute(f"""UPDATE users_demo SET social_media='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=message.chat.id, text="Данные изменены!\n\nВот так теперь выглядит твоя анкета⏬")
    show(message)


def change_work(message):
    cur.execute(f"""UPDATE users_demo SET activity='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=message.chat.id, text="Данные изменены!\n\nВот так теперь выглядит твоя анкета⏬")
    show(message)


def change_about(message):
    cur.execute(f"""UPDATE users_demo SET interests='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=message.chat.id, text="Данные изменены!\n\nВот так теперь выглядит твоя анкета⏬")
    show(message)


@bot.callback_query_handler(func=lambda call: call.data in ['change_online', 'change_offline'])
def change_form(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'change_online':
        cur.execute(f"""UPDATE users_demo SET format='online' WHERE userid={call.message.chat.id}""")
        conn.commit()
    else:
        cur.execute(f"""UPDATE users_demo SET format='offline' WHERE userid={call.message.chat.id}""")
        conn.commit()

    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Назад', callback_data='back1')
    btn2 = types.InlineKeyboardButton('Посмотреть анкету', callback_data='sshow')
    kb.add(btn2)
    kb.add(btn1)

    bot.send_message(chat_id=call.message.chat.id, text="Данные изменены!", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data in ["closed", "friend"])
def closed(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'closed':
        bot.send_message(chat_id=call.message.chat.id, text="Это сообщество защищено паролем 🔐, для доступа нужен"
                                                            " <b>специальный код</b>", parse_mode='HTML')
        bot.register_next_step_handler(call.message, check_secret_code_closed)
    elif call.data == 'friend':
        bot.send_message(chat_id=call.message.chat.id, text="Это сообщество защищено паролем 🔐, для доступа нужен"
                                                            " <b>специальный код</b>", parse_mode='HTML')
        bot.register_next_step_handler(call.message, check_secret_code_friend)


def check_secret_code_closed(message):
    if message.text == '1111':
        cur.execute(f"""UPDATE users_demo SET closed_club={True} WHERE userid={message.chat.id}""")
        conn.commit()

        bot.send_message(message.chat.id, 'Успешно!')
        name(message)
    else:
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Назад', callback_data='back')
        kb.add(btn1)
        bot.send_message(message.chat.id, 'Неверный код доступа, вернитесь назад или введите код заново!', reply_markup=kb)
        bot.register_next_step_handler(message, check_secret_code_closed) #&&&&&


def check_secret_code_friend(message):
    if message.text == '1111':
        cur.execute(f"""UPDATE users_demo SET closed_club={False} WHERE userid={message.chat.id}""")
        conn.commit()

        bot.send_message(message.chat.id, 'Успешно!')
        name(message)
    else:
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Назад', callback_data='back')
        kb.add(btn1)
        bot.send_message(message.chat.id, 'Неверный код доступа, вернитесь назад или введите код заново!', reply_markup=kb)
        bot.register_next_step_handler(message, check_secret_code_closed) #&&&&&


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Закрытый Клуб', callback_data='closed')
    btn2 = types.InlineKeyboardButton('Друзья Клуба', callback_data='friend')
    kb.add(btn1)
    kb.add(btn2)

    bot.send_message(call.message.chat.id, 'Выбери, к какой части Клуба ты относишься:', reply_markup=kb)


def name(message):
    bot.send_message(message.chat.id, '☕️ Напиши Имя и Фамилию')
    bot.register_next_step_handler(message, save_name_and_turn_to_social_media)


def save_name_and_turn_to_social_media(message):
    cur.execute(f"""UPDATE users_demo SET name='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()

    bot.send_message(message.chat.id, '🤳 Пришли ссылку на свой профиль в любой соц. сети, где есть наиболее подробная'
                                      ' информация о тебе\n\nТак вы в паре сможете лучше узнать друг о друге до встречи')
    bot.register_next_step_handler(message, save_social_media_and_turn_to_activity)


def save_social_media_and_turn_to_activity(message):
    cur.execute(f"""UPDATE users_demo SET social_media='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()

    bot.send_message(message.chat.id, '👨‍🔬 Кем ты работаешь и чем занимаешься?')
    bot.register_next_step_handler(message, save_activity_abd_turn_to_interests)


def save_activity_abd_turn_to_interests(message):
    cur.execute(f"""UPDATE users_demo SET activity='{message.text}' WHERE userid={message.chat.id}""")
    conn.commit()

    bot.send_message(message.chat.id, '👀 Какие у тебя есть рабочие и нерабочие интересы?\n\n💡 Напиши через запятую'
                                      ' слова, за которые можно зацепиться и развернуть из этого интересный разговор!'
                                      ' Например, увлечения, названия книг, любимый вид спорта')
    bot.register_next_step_handler(message, save_interests_abd_turn_to_format)


def save_interests_abd_turn_to_format(message):
    cur.execute(f"""UPDATE users_demo SET interests='{message.text}' WHERE userid={message.from_user.id}""")
    conn.commit()

    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Онлайн', callback_data='online')
    btn2 = types.InlineKeyboardButton('Оффлайн', callback_data='offline')
    kb.add(btn1)
    kb.add(btn2)

    bot.send_message(message.chat.id, 'В каком формате ты бы предпочёл встречу?', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data in ['online', 'offline'])
def save(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'online':
        cur.execute(f"""UPDATE users_demo SET format='online' WHERE userid={call.message.chat.id}""")
        conn.commit()
    elif call.data == 'offline':
        cur.execute(f"""UPDATE users_demo SET format='offline' WHERE userid={call.message.chat.id}""")
        conn.commit()
    cur.execute(f"""UPDATE users_demo SET finished={True} WHERE userid={call.message.chat.id}""")
    bot.send_message(chat_id=call.message.chat.id, text="Получилось! 🙌\n\nТеперь ты — участник встреч HSE BC"
                                                        " Random Coffee ☕️\n\nВот так будет выглядеть твой профиль"
                                                        " в сообщении, которое мы пришлем твоему собеседнику:\n\n⏬")
    show(call.message)


@bot.message_handler(commands=['show'])
def show(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    cur.execute(f'SELECT * FROM users_demo WHERE userid={message.chat.id}')
    info = cur.fetchone()
    #print(message.from_user.id)

    bot.send_message(chat_id=message.chat.id, text=f"{info[3]}\nПрофиль: {info[5]}\n\n◽ Чем занимается:"
                                                   f" {info[4]}\n◽ Зацепки для начала разговора: {info[6]}\n\nЕсли"
                                                   f" нужно что-то поменять - /help")


@bot.callback_query_handler(func=lambda call: call.data == "sshow")
def sshow(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    cur.execute(f'SELECT * FROM users_demo WHERE userid={call.message.chat.id}')
    info = cur.fetchone()
    # print(message.from_user.id)
    print(info)

    bot.send_message(chat_id=call.message.chat.id, text=f"{info[3]}\nПрофиль: {info[5]}\n\n◽ Чем занимается:"
                                                   f" {info[4]}\n◽ Зацепки для начала разговора: {info[6]}\n\nЕсли"
                                                   f" нужно что-то поменять - /help")


@bot.callback_query_handler(func=lambda call: call.data == "participate")
def participate(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    cur.execute(f"""UPDATE users_demo SET this_week='yes' WHERE userid={call.message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=call.message.chat.id, text="Участие подтверждено!")


@bot.callback_query_handler(func=lambda call: call.data == "miss")
def miss(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    cur.execute(f"""UPDATE users_demo SET this_week='no' WHERE userid={call.message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=call.message.chat.id, text="Будем ждать на следующей неделе!")


@bot.callback_query_handler(func=lambda call: call.data == "miss_month")
def miss_month(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    cur.execute(f"""UPDATE users_demo SET this_week='month' WHERE userid={call.message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=call.message.chat.id, text="Встретимся через месяц!")


@bot.callback_query_handler(func=lambda call: call.data == "inf")
def miss_inf(call: types.CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    cur.execute(f"""UPDATE users_demo SET this_week='inf' WHERE userid={call.message.chat.id}""")
    conn.commit()
    bot.send_message(chat_id=call.message.chat.id, text="Подтверждено!")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(5)