import telebot
from telebot import types
import random
import wikipedia
import time
import sqlite3
import time
import re
from telebot import util
from dotenv import load_dotenv
import os

wikipedia.set_lang("ru")
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом. '


#admin
admins_id = 5668034921



#Admin_message
ad= None
ad2 = None
ad3 =None

#google
google_seach = 'https://www.google.com/search?q='

#time
result=time.localtime()

time='\n' +str(result.tm_mday) + '.' + str(result.tm_mon) + '.' + str(result.tm_year) + '    '  +str(result.tm_hour) + ':' + str(result.tm_min) + ':' + str(result.tm_sec ) 


connect = sqlite3.connect('users.db',check_same_thread=False) 
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS login_id(
        chat_id INT,
        name TEXT,
        surename TEXT,
        username TEXT,
        time INT
)''')
    
connect.commit()

chat_idd = None


#Start Code!
#---------------------------

time_test = 0000

load_dotenv()
# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv("TOKEN"))

if result.tm_hour == 7:
    bot.delete_message(5668034921, time_test)
    time_test = bot.send_message(5668034921, 'Техническая проверка...⚠️🛠️⏱️\nСервер проверен!👨‍💻 Бот работает исправно!🤖✅\nДата и время последней проверки:' + time + '.')
    time_test = time_test.id
    
@bot.message_handler(commands=['start'])
def start_message(message):
    
    #SQL info
    chats_id = message.chat.id
    usernames = message.chat.username
    names = message.chat.first_name
    surenames = message.chat.last_name
    SQLtime= f'{result.tm_mday}.{result.tm_mon}.{result.tm_year} {result.tm_hour}:{result.tm_min}:{result.tm_sec} '

    
    #SQL mehanik
    
    
    cursor.execute(f'SELECT chat_id FROM login_id WHERE chat_id = {chats_id}')
    data = cursor.fetchone()
    if data is None:
        if message.chat.type == 'private':
            cursor.execute("INSERT INTO login_id (chat_id, name, surename, username, time) VALUES (?,?,?,?,?)",[chats_id, names, surenames, usernames, SQLtime])
            if message.chat.id != admins_id :
                bot.send_message(5668034921, 'Админ, поздравляю! У нас новый пользователь!!!')
        connect.commit()
        
    
    bot.send_message(message.chat.id,     'Привет,' + str(message.chat.first_name) + '!')
    bot.send_message(message.chat.id, 'Чтож, познакомились и давай к делу!😉\n\nЯ - бот-словарь. Одним словом: Поисковик слов из Википедии.🔎📙 У меня есть определения почти на каждое слово или компанию! \n<span class = "tg-spoiler">(конечно же если оно слишком простое, несуществующее или если его нет в энциклопедии). </span> \n\n Так же я принимаю в поиск имена разных личностей и компаний на английском.', parse_mode='html')
    bot.send_message(message.chat.id, 'Напиши мне любое слово(существительное)👇')
    

def send_message_to_users(message):
    connect = sqlite3.connect('users.db',check_same_thread=False) 
    cursor = connect.cursor() 
    cursor.execute('SELECT chat_id FROM login_id')
    users = cursor.fetchall()
    info = ''
    for el in users:
        info = el[0]
        bot.send_message(info, message)
    connect.commit()
	
@bot.message_handler(commands=['send'])
def send(message): 	
    if message.chat.id == 5668034921:
        text = message.text.replace('/send', '').strip()
        send_message_to_users(text)
        bot.send_message(message.chat.id, 'Сообщение успешно отправлено')
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к этой команде')
  
    
# Админка(команды)
 
@bot.message_handler(commands=['admin'])
def admins_message(message):
    if message.chat.id == 5668034921:
        global ad3
        ad3 = message.id
        global ad
        ad = bot.send_message(5668034921, 'Рад видеть тебя, Админ!' )
        markup = types.InlineKeyboardMarkup()
        btn1 = markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data = 'users'))
        markup.add(telebot.types.InlineKeyboardButton('Вся информация', callback_data = 'users_all'))
        markup.add(telebot.types.InlineKeyboardButton('Назад', callback_data = 'back'))

        global ad2
        ad2= bot.send_message(message.chat.id, 'Команды', reply_markup = markup)
        
    if message.chat.id != 5668034921:
        bot.send_message(message.chat.id, 'Эта комадна админа! Вы не имеете эти права!')
 
# 1824053958


    





@bot.message_handler(commands=['autor'])
def send_message(message):
    bot.send_message(message.chat.id, 'Создатель этого бота: @NikolaGream\nАкаунт актуален и можно писать ему в случае сбоев или проблем с ботом.\nПросьба, не писать по пустякам или без причины!\n\n    С уважением,\n                 Администрация!')

@bot.message_handler(commands=['help'])
def send_message(message):
    bot.send_message(message.chat.id, 'Ответы на часто задаваемые вопросы👀:\n\n•Что это за бот и какие у него функции?\nДанный бот предназначен для быстрого поиска определения слов(возможно он даже поможет вам в учёбе или же для своих нужд и интересов). Так же у меня есть небольшая информация про разные компании(и на английском тоже), известные личности и т.д.\n\n•Кто автор бота?\nАвтор бота и являеться тех. поддержкой.\nНажмите /autor для более подробной информации!')
    
def handle_text(message):
    mil =0
    sus= bot.send_message(message.chat.id, 'Загрузка... |')
    for lop in range(1):
        
        bot.edit_message_text(chat_id=message.chat.id, message_id=sus.id,text='Загрузка... /') 
        bot.edit_message_text(chat_id=message.chat.id, message_id=sus.id, text='Загрузка... -')
        bot.edit_message_text(chat_id=message.chat.id, message_id=sus.id, text= 'Загрузка... \ ')
        bot.edit_message_text(chat_id=message.chat.id, message_id=sus.id, text='Загрузка... |')
        mil =+ 1
        if mil == 5:
            break
  

    bot.reply_to(message, getwiki(message.text) + f'\n--------------------\nПодробне можно узнать тут: {google_seach}{message.text}.')
    bot.delete_message(message.chat.id, sus.id)

sub_msg = None
'''
def nok(message):   
    global sub_msg    
    for k in status:
        if k != bot.get_chat_member(chat_id=-1001915322163, user_id = message.chat.id).status:  
            markup = types.InlineKeyboardMarkup() 
            markup= types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton(text='Канал', url='https://t.me/bhytrc')
            btn1 = telebot.types.InlineKeyboardButton(text='Я подписался', callback_data = 'sub')
            markup.add(btn,btn1) 
            sub_msg=bot.send_message(message.chat.id, 'Подпишитесь на канал!', reply_markup=markup)
            break

status = ['creator', 'administrator', 'member']
'''

@bot.message_handler(content_types=["text"])
def reg(message):
    handle_text(message)
    '''
    num_s = 0
    for i in status:
        num_s = num_s + 1
        if i == bot.get_chat_member(chat_id=-1001915322163, user_id = message.chat.id).status:
            num_s =0
            handle_text(message)
            break
        
        if num_s == 3:
            nok(message)
'''
            
  
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global txt
    #-----------------------назад
    if call.data == 'back':
        bot.delete_message(call.message.chat.id, ad2.id)
        bot.delete_message(call.message.chat.id, ad3.id)
   #------------------------не назад
    if call.data != 'back':
        connect = sqlite3.connect('users.db',check_same_thread=False) 
        cursor = connect.cursor()
        #----------------------таблица
        if call.data == 'users_all':
            cursor.execute('SELECT * FROM login_id')
            users = cursor.fetchall()
            info = ' '
            for el in users:
                info += f'{el[0]} - {el[1]} - {el[2]} - @{el[3]} - {el[4]} \n-------------\n'
            for message1 in util.smart_split(info, 3000):
                bot.send_message(call.message.chat.id, f'Список всех пользователей: \n{message1}')
            bot.delete_message(call.message.chat.id, ad.id)
            bot.delete_message(call.message.chat.id, ad2.id)
            bot.delete_message(call.message.chat.id,ad3 ) 
            connect.commit()
            
            cursor.execute('SELECT chat_id FROM login_id')
            users = cursor.fetchall()
            info = ' '
            for el in users:
                info = f'{el[0]}'
                
       #-----------------------список
        elif call.data == 'users':
            cursor.execute('SELECT name, username FROM login_id')
            users = cursor.fetchall()
            info = ' '
            for el in users:
                info += f'{el[0]} - @{el[1]}\n-------------\n'
            for message2 in util.smart_split(info, 3000):
                bot.send_message(call.message.chat.id, f'Список всех пользователей: \n{message2}')
            bot.delete_message(call.message.chat.id, ad.id)
            bot.delete_message(call.message.chat.id, ad2.id)
            bot.delete_message(call.message.chat.id,ad3 ) 
    connect.commit()
'''
    if call.data == 'sub':
        status = ['creator', 'administrator', 'member']
        for i in status:
            if i == bot.get_chat_member(chat_id=-1001915322163, user_id = call.message.chat.id).status:
                bot.delete_message(call.message.chat.id, sub_msg.id)
                handle_text(call.message)
                break
        bot.answer_callback_query(callback_query_id=call.id, text='Вы не подписаны!')
            '''    

      
        
            
bot.polling()