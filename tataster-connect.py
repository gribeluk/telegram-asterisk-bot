# -*- coding: utf-8 -*-
import telebot
from telebot import apihelper
from telebot import types
import MySQLdb
import socket
import hashlib
import constants
import ari

class Aster:
    def __init__(self):
        self.ip = None
        self.port = 8088
        self.user = None
        self.pas = None
        self.pas512 = None

aster_dict = {}

start_text = 'Данный бот умеет присылать уведомления и отправлять команды серверу телефонии Asterisk.\n'
comand_list = 'Список команд:\n/login - подключиться к серверу\n/events - настройка оповещений событий\n/devices - просмотр состояния устройств\n/cli - режим консоли\n/logout - отключиться от сервера\n/help - список всех команд'
ami_text = 'Необходимо настроить AMI-user для управления сервером Asterisk. В файле manager.conf \n `[general]`\n`enabled = yes`\n`port = (5038 по-умолчанию)`\n`bindaddr = 163.172.176.72 (принимать соеднинение с данного IP-адреса)`\n\n`[username] (имя пользователя)`\n`secret = (пароль пользователя)`\n`deny = 0.0.0.0/0.0.0.0 (запрещенные ip-адреса)`\n`permit = 163.172.176.72/255.255.255.0 (разрешенные ip-адреса)`\n`read = system, call, log, verbose, command, agent, user`\n`(список передаваемых пользователю классов событий)`\n`write = system, call, log, verbose, command, agent, user`\n`(список разрешенных классов команд)`\n[Подробнее про опции read и write](http://www.pbxware.ru/wiki/asterisk_managment_interface_ami/)'

apihelper.proxy = {'https':'socks5://' + str(constants.proxy_user) + ':' + str(constants.proxy_pass) + '@' + str(constants.proxy_host) + ':' str(constants.proxy_port)}

bot = telebot.TeleBot(constants.token)

@bot.message_handler(commands=['start'])
def handle_start(message):
   bot.send_sticker(message.chat.id, 'CAADAgADcQAD6VUFGA7eUnLkYgnmAg')
   bot.send_message(message.chat.id, start_text)
   bot.send_message(message.chat.id, comand_list)
   bot.send_message(message.chat.id, 'Для того, чтобы начать работу подключитесь к серверу Asterisk.')
    
@bot.message_handler(commands=['help'])
def handle_help(message):
   bot.send_message(message.chat.id, comand_list)

@bot.message_handler(commands=['login'])
def handle_login(message):
   bot.send_message(message.chat.id, ami_text)
   bot.send_message(message.chat.id, 'Введите IP-адрес сервера Asterisk:')
   bot.register_next_step_handler(message, process_check_ip)
    
def process_check_ip(message):
   chat_id = message.chat.id
   aster = Aster()
   aster_dict[chat_id] = aster
   ip = message.text
   try:
       socket.inet_aton(ip)
   except socket.error:
       bot.send_message(message.chat.id, "Данный IP некорректен. Попробуйте еще раз")
       bot.register_next_step_handler(message, process_wrong_ip)
   else:
       aster.ip = ip
       bot.send_message(message.chat.id, ssh_text)
       bot.send_message(message.chat.id, "Введите username")
       bot.register_next_step_handler(message, process_add_name)
    
def process_wrong_ip(message):
   chat_id = message.chat.id
   aster = Aster()
   aster_dict[chat_id] = aster
   ip = message.text
   try:
       socket.inet_aton(ip)
   except socket.error:
       bot.send_message(message.chat.id, "Данный IP некорректен. Попробуйте еще раз")
       bot.register_next_step_handler(message, process_wrong_ip)
   else:
       aster.ip = ip
       bot.send_message(message.chat.id, ssh_text)
       bot.send_message(message.chat.id, "Введите username")
       bot.register_next_step_handler(message, process_add_name)
    
def process_add_name(message):
    chat_id = message.chat.id
    aster = aster_dict[chat_id]
    aster.user = message.text
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, process_add_pass)

def process_add_pass(message):
    chat_id = message.chat.id
    aster = aster_dict[chat_id]
    aster.pas = message.text
    aster.pas512 = hashlib.sha512(aster.pas).hexdigest()
    bot.register_next_step_handler(message, aster_connect)

# делалось для расширения   
#def db_connect(chat_id):
#    aster = aster_dict[chat_id]
#    try: 
#        db = MySQLdb.connect(host=constants.db_host, user=constants.db_user, passwd=constants.db_pass, db=constants.db_name, charset='utf8')
#        cursor = db.cursor()
#        cursor.execute("""
#            INSERT INTO aster (host, port, user, password) VALUES
#            (%s, %s, %s, %s)
#        """, (str(aster.ip), int(aster.port), str(aster.user), str(aster.pas512)))
#        db.commit()
#    except: 
#        bot.send_message(message.chat.id, "Ошибка подключения к БД")

def aster_connect(chat_id):
    aster = aster_dict[chat_id]
    try:
        client_ast = ari.connect('http://' + str(aster.ip) + ':' + str(aster.port) + '/', str(aster.user), str(aster.pas))
    except:
        bot.send_message(chat_id, "Ошибка соединения")
    else:
        bot.send_message(chat_id, "Соединение установлено")
        
if __name__ == '__main__':
   bot.polling(none_stop=True, interval=0)