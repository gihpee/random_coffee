import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import time
import psycopg2

bot = telebot.TeleBot('TOKEN')

conn = psycopg2.connect(host='host', user='user', password='pwd', database='db')
cur = conn.cursor()

kb = types.InlineKeyboardMarkup(row_width=1)
btn = types.InlineKeyboardButton(text='учавствую')

cur.execute('SELECT * FROM users_demo')
info = cur.fetchall()
counter = 0

cur.execute(f"""UPDATE users_demo SET this_week='no'""")
conn.commit()

#проводим рассылку с опросом\

#тем кто ответил учавствую высталяем в БД True

#рассылка
for el in info:
    print(el[0])
    counter += 1

    try:
        #тут обработчик нажатия кнопки -> переход на функцию которая в БД выставит True
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Да, конечно👍', callback_data='participate')
        btn2 = types.InlineKeyboardButton('Пропущу неделю🔂', callback_data='miss')
        btn3 = types.InlineKeyboardButton('Пропускаю месяц🚫', callback_data='miss_month')
        kb.add(btn1)
        kb.add(btn2)
        kb.add(btn3)
        bot.send_message(el[0], 'Встречи Random Coffee продолжаются.\n\nПодскажи, планируешь ли ты участвовать на'
                                ' следующей неделе?', reply_markup=kb)

    except Exception as e:
        print(e)

    if counter % 20 == 0:
        time.sleep(3)
        print(counter)