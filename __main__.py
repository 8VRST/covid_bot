# -*- coding: utf-8 -*-
import os
import sys
import telebot
from telebot import types
import TelegramBotAPI
import random
import time
from datetime import datetime
from data.text_data import belarus_main_virologist_adviser
from data.text_data import fatal_error_quotes
from data.text_data import countries_dictionary
import data.reply_blanks
from data.reply_blanks import replace_values
import neverpushit

TOKEN = neverpushit.bot_token

bot = telebot.TeleBot(TOKEN)


class BotKeyboards:

    def bot_main_keyboard():

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn0 = types.KeyboardButton('⬜️🟥⬜️')
        btn1 = types.KeyboardButton('👴🏻 мнения и советы ¿главного вирусолога¿')
        btn2 = types.InlineKeyboardButton('💳 донат медработникам')
        btn3 = types.KeyboardButton('🌏🌎🌍')
        btn4 = types.KeyboardButton('Другие регионы')
        
        markup.add(btn0, btn3, btn4)
        markup.add(btn1)
        markup.add(btn2)
        return markup

    def bot_countries_keyboard():

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

        btn0 = types.KeyboardButton('🚶 в главное меню')
        markup.add(btn0)

        for btn, btn1 in zip(list(countries_dictionary[0].values())[0::2], list(countries_dictionary[0].values())[1::2]):
            markup.add(btn, btn1)

        markup.add(btn0)

        return markup


@bot.message_handler(commands=['start'])
def start_sender(message):
    bot.send_message(message.chat.id, 'Доброго времени суток, ' + message.from_user.first_name + '. Приглашаю понажимать на кнопки!', reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)

@bot.message_handler(func=lambda message: message.text == '⬜️🟥⬜️')
def belarus_data_sender(message):
    bot.send_message(message.chat.id, data.reply_blanks.return_belarus_data('Belarus'), reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)

@bot.message_handler(func=lambda message: message.text == '🌏🌎🌍')
def world_data_sender(message):
    bot.send_message(message.chat.id, data.reply_blanks.return_world_data(), reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)

@bot.message_handler(func=lambda message: message.text == 'Другие регионы')
def country_data_sender(message):
    reply_message = message.from_user.first_name + ', выбери страну/регион!' + '\nТакже название можно попробовать ввести вручную на русском в любом регистре.' 
    bot.send_message(message.chat.id, reply_message, reply_markup=BotKeyboards.bot_countries_keyboard())
    time.sleep(2)

@bot.message_handler(func=lambda message: message.text == '🚶 в главное меню')
def return_to_main_menu(message):
    reply_message = message.from_user.first_name + ', с возвращением в главное меню!' 
    bot.send_message(message.chat.id, reply_message, reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)

@bot.message_handler(func=lambda message: message.text == '👴🏻 мнения и советы ¿главного вирусолога¿')
def send_advice(message):
    bot.send_message(message.chat.id, belarus_main_virologist_adviser(message), reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)

@bot.message_handler(func=lambda message: message.text == '💳 донат медработникам')
def donatation_to_doctors_command(message):
    donation_links = message.from_user.first_name + ', помочь медработникам можно на страницах:\n👉' + '[MolaMola](https://molamola.by/be/campaigns?sort=popular&category_id=10)' + '\n👉' + '[МЗ РБ](http://minzdrav.gov.by/ru/sobytiya/minzdrav-prinyal-reshenie-po-otkrytiyu-blagotvoritelnogo-scheta/)'
    bot.send_message(message.chat.id, donation_links, parse_mode='MarkdownV2', disable_web_page_preview = True,  reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)

@bot.message_handler()
def handler_for_everything(message):

    if str(message.text).title() == 'Беларусь':
        bot.send_message(message.chat.id, data.reply_blanks.return_belarus_data('Belarus'), reply_markup=BotKeyboards.bot_countries_keyboard())

    elif str(data.reply_blanks.multiple_replace(str(message.text).title(), replace_values)) in countries_dictionary[0].values():
        for english_country_name in countries_dictionary[1]:
            if english_country_name == str(data.reply_blanks.multiple_replace(str(message.text).title(), replace_values)):
                english_country_name = countries_dictionary[1][str(data.reply_blanks.multiple_replace(str(message.text).title(), replace_values))]
                bot.send_message(message.chat.id, data.reply_blanks.return_country_data(english_country_name), reply_markup=BotKeyboards.bot_countries_keyboard())
    
    else:
        bot.send_message(message.chat.id, fatal_error_quotes(message), reply_markup=BotKeyboards.bot_main_keyboard())
    time.sleep(2)



while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(10)



