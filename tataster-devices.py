# -*- coding: utf-8 -*-
import telebot
from telebot import apihelper
from telebot import types
import constants
import tataster-connect
import ari

@bot.message_handler(commands=['devices'])
def handle_start(message):
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
   markup.row('SIP устройства')
   markup.row('SCCP устройства)
   bot.send_message(message.chat.id, 'Выберите тип устройств', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
   if message.text == u"SIP устройства":
       hide_markup = types.ReplyKeyboardRemove()
       bot.send_message(message.chat.id, devices.sip, reply_markup=hide_markup)
   elif message.text ==u'SCCP устройства':
       hide_markup = types.ReplyKeyboardRemove()
       bot.send_message(message.chat.id, devices.sccp, reply_markup=hide_markup)
    else:
        bot.send_message(message.chat.id, "Неправильная команда. Попробуй еще раз")
		
if __name__ == '__main__':
   bot.polling(none_stop=True, interval=0)