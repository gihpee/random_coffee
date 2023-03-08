import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import time
import psycopg2
from random import randint

bot = telebot.TeleBot('TOKEN')

conn = psycopg2.connect(host='host', user='user', password='pwd', database='db')
cur = conn.cursor()

cur.execute('SELECT * FROM users_demo')
counter = 0

users = cur.fetchall()

users_l = []

for user in users:
    users_l.append(list(user))

private = list(filter(lambda x: x[1] and x[9] and x[7] == 'yes', users_l))
open = list(filter(lambda x: (not x[1]) and x[9] and x[7] == 'yes', users_l))

pairs_private = []
pairs_open = []

length = len(private) - 1
while length != 0:
    first = private[0]
    flag = 0
    while flag != 1:
        second = private[randint(0, length)]
        if first != second and first[10] == second[10]:
            pairs_private.append([first, second])
            private.remove(first)
            private.remove(second)
            flag += 1
            if length == 1:
                length += 1
            length -= 2
    if length == 0:
        break


length = len(open) - 1
while length != 0:
    first = open[0]
    flag = 0
    while flag != 1:
        second = open[randint(0, length)]
        if first != second and first[10] == second[10]:
            pairs_open.append([first, second])
            open.remove(first)
            open.remove(second)
            flag += 1
            if length == 1:
                length += 1
            length -= 2
    if length == 0:
        break

print(pairs_open)
print(pairs_private)
print(open)
print(private)

for el in pairs_private:
    counter += 1

    try:
        kb1 = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Написать собеседнику', url=f'https://t.me/{el[0][2]}')
        kb1.add(btn1)

        kb2 = types.InlineKeyboardMarkup(row_width=1)
        btn2 = types.InlineKeyboardButton(text='Написать собеседнику', url=f'https://t.me/{el[1][2]}')
        kb2.add(btn2)
        bot.send_message(el[0][0],
                         f'✅Собеседник найден'
                         f'\n {el[1][3]}'
                         f'\nПрофиль: {el[1][5]}'
                         f'\n\n◽️Чем занимается: {el[1][4]}'
                         f'\n◽️Зацепки для начала разговора: {el[1][6]}', reply_markup=kb2)
        bot.send_message(el[0][0],
                               '❗️Напиши собеседнику для того, чтобы совместно согласовать встречу!'
                               '\n\n Посмотреть и поменять данные своего профиля\nты можешь в /help')

        bot.send_message(el[1][0],
                         f'✅Собеседник найден'
                         f'\n {el[0][3]}'
                         f'\nПрофиль: {el[0][5]}'
                         f'\n\n ◽️Чем занимается: {el[0][4]}'
                         f'\n◽️Зацепки для начала разговора: {el[0][6]}', reply_markup=kb1)
        bot.send_message(el[1][0],
                         '❗️Напиши собеседнику для того, чтобы совместно согласовать встречу!'
                         '\n\n Посмотреть и поменять данные своего профиля\nты можешь в /help')

    except Exception as e:
        print(e)

    if counter % 5 == 0:
        time.sleep(3)
        print(counter)


for el in pairs_open:
    counter += 1

    try:
        kb1 = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Написать собеседнику', url=f'https://t.me/{el[0][2]}')
        kb1.add(btn1)

        kb2 = types.InlineKeyboardMarkup(row_width=1)
        btn2 = types.InlineKeyboardButton(text='Написать собеседнику', url=f'https://t.me/{el[1][2]}')
        kb2.add(btn2)
        bot.send_message(el[0][0],
                         f'✅Собеседник найден'
                         f'\n {el[1][3]}'
                         f'\nПрофиль: {el[1][5]}'
                         f'\n\n ◽️Чем занимается: {el[1][4]}'
                         f'\n◽️Зацепки для начала разговора: {el[1][6]}', reply_markup=kb2)
        bot.send_message(el[0][0],
                               '❗️Напиши собеседнику для того, чтобы совместно согласовать встречу!'
                               '\n\n Посмотреть и поменять данные своего профиля\nты можешь в /help')

        bot.send_message(el[1][0],
                         f'✅Собеседник найден'
                         f'\n {el[0][3]}'
                         f'\nПрофиль: {el[0][5]}'
                         f'\n\n ◽️Чем занимается: {el[0][4]}'
                         f'\n◽️Зацепки для начала разговора: {el[0][6]}', reply_markup=kb1)
        bot.send_message(el[1][0],
                         '❗️Напиши собеседнику для того, чтобы совместно согласовать встречу!'
                         '\n\n Посмотреть и поменять данные своего профиля\nты можешь в /help')

    except Exception as e:
        print(e)

    if counter % 5 == 0:
        time.sleep(3)
        print(counter)

for el in open:
    counter += 1

    try:

        bot.send_message(el[0], 'Пары на эту неделю уже распределены. \n'
                                  'Попробую найти тебе партнера, но это может занять несколько дней.\n'
                                  'Буду держать в курсе! \n\n'
                                  'А в субботу я спрошу, участвуешь ли ты в Random Coffee на следующей неделе, не пропусти.')

    except Exception as e:
        print(e)

    if counter % 20 == 0:
        time.sleep(3)
        print(counter)


for el in private:
    counter += 1

    try:

        bot.send_message(el[0], 'Пары на эту неделю уже распределены. \n'
                                  'Попробую найти тебе партнера, но это может занять несколько дней.\n'
                                  'Буду держать в курсе! \n\n'
                                  'А в субботу я спрошу, участвуешь ли ты в Random Coffee на следующей неделе, не пропусти.')

    except Exception as e:
        print(e)

    if counter % 20 == 0:
        time.sleep(3)
        print(counter)