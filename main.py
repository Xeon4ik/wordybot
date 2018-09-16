from fileinput import close

import telebot
import constants
import random
import urllib.request as urllib2
bot = telebot.TeleBot(constants.token)
#bot.config['api_key'] = constants.token
#bot.send_message(448513434, "ку ку")
print(bot.get_me())


def correction(word):
    word.lower()
    word2 = ''
    for i in range(len(word)):
        if word[i].isalpha():
            word2 = word2[:] + word[i]
    return word2


def diff(word1, word2):
    word1 = correction(word1)
    word2 = correction(word2)
    if len(word1) == len(word2):
        for i in range(min(len(word1), len(word2))):
            if word1[i] != word2[i]:
                return False
        return True


def isIt(word):
    f = open('wordlist.txt', 'r')
    for line in f:
        if diff(word, line):
            return True
            break
    return False


def _st(sw, pick):
    if not pick:
        constants.start = sw
    else:
        constants.switch = sw

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    #_st(False)
    user_markup.row('/Начать', '/Закончить')
    user_markup.row('','/Правила', '')
    user_markup.row('', '/Скрыть', '')
    bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)

@bot.message_handler(commands=['Правила'])
def handle_start(message):
    bot.send_message(message.from_user.id, 'Это обычная игра в слова.\nТы пишешь слово боту, а он отвечает словом начинающимся на последнюю букву твоего, а ты отвечаешь словом начинающимся на последнюю букву слова бота.\nПример:\nКовер - Ракета - Абажур')

@bot.message_handler(commands=['Скрыть'])
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Что бы включить клавиатуру наберите /start', reply_markup=hide_markup)

@bot.message_handler(commands=['Начать'])
def handle_start(message):
    _st(True, 0)
    _st(True, 1)
    bot.send_message(message.from_user.id, 'Начинай игру')

@bot.message_handler(commands=['Закончить'])
def handle_start(message):
    _st(False, 0)
    _st(False, 1)
    bot.send_message(message.from_user.id, 'Игра закончена')



@bot.message_handler(content_types=['text'])
def handle_text(message):
    mat = []
    _l = message.text
    _l = correction(_l)
    f = open('wordlist.txt', 'r')
    if not isIt(_l):
        bot.send_message(message.from_user.id, "Такого слова нет!")
    elif constants.start and constants.switch:
        for line in f:
            line = correction(line)
            if line[0] == _l[len(_l) - 1]:
                mat.append(line)
        line.title()
        random.shuffle(mat)
        bot.send_message(message.from_user.id, random.choice(mat))  # Здесь может быть ошибка
        mat.clear()
        _st(False, 0)  # Возможна ошибка
        constants._lastchar = line[len(line) - 1]
    elif constants.switch and constants._lastchar != _l[0]:
        bot.send_message(message.from_user.id, "Твое слово не проходит по правилу")
    elif constants.switch and constants._lastchar == _l[0]:
        for line in f:
            line = correction(line)
            if line[0] == _l[len(_l) - 1]:
                mat.append(line)
            line.title()
            random.shuffle(mat)
            bot.send_message(message.from_user.id, random.choice(mat)) #Здесь может быть ошибка
            mat.clear()
            constants._lastchar = line[len(line) - 1]
    else:
        bot.send_message(message.from_user.id, 'Ты не начал игру!')

bot.polling(none_stop=True, interval=0)
