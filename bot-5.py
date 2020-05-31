from typing import Any
import socks
import telebot
import requests
import re
import os
import socks
import socket


socks.set_default_proxy(socks.SOCKS5, "3.132.226.33")
socket.socket = socks.socksocket

token = os.environ['TOKEN']

PORT = int(os.environ.get('PORT', '8443'))

HEROKU_APPNAME = 'my-book-bot'

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет':
        msg = bot.send_message(message.from_user.id,
                               'Привет! Скажи мне, какая книга тебя интересует :) Поиск будет корректнее, если ты назовешь не только название произведения, но и его автора.')
        bot.register_next_step_handler(msg, which_book)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши мне Привет')
    else:
        bot.send_message(message.from_user.id, 'Я не понимаю :( Попробуй /help.')


global book


def which_book(message):
    global book
    book = message.text.split()
    book = '+'.join(book)

    msg = bot.send_message(message.from_user.id, 'Отлично! Может быть, стоит отсортировать книги по цене? (Да/Нет)')
    bot.register_next_step_handler(msg, book_price)


def book_price(message):
    global book
    if message.text == 'Да':
        msg = bot.send_message(message.from_user.id, 'Хорошо, скажи, от скольки и до скольки должна стоить книга.')
        bot.register_next_step_handler(msg, fromtoprice)
    elif message.text == 'Нет':
        url = 'https://www.ozon.ru/category/knigi-16500/?text=' + book
        msg = bot.send_message(message.from_user.id,
                               'Хорошо, тогда вот все книги, удовлетворяющие запросу: ' + url)
    else:
        bot.send_message(message.from_user.id, 'Я не понимаю :( Попробуй ответить Да или Нет')


def fromtoprice(message):
    global book
    price = message.text.split()
    if price[0] < price[1]:
        url = 'https://www.ozon.ru/category/knigi-16500/' + '?price=' + price[0] + '.000%3B' + price[
            1] + '.000&' + 'text=' + book
    else:
        url = 'https://www.ozon.ru/category/knigi-16500/' + '?price=' + price[1] + '.000%3B' + price[
            0] + '.000&' + 'text=' + book
    bot.send_message(message.from_user.id, 'Вот результаты, соответствующие запросу: ' + url)


def main():
    new_offset = 0
    print('launching...')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

    bot.polling(none_stop=True, interval=0)
