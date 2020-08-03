import telebot
import config
import coincap_pars

bot = telebot.TeleBot(config.token)

result = coincap_pars.start()


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = f'<b>Привет, {message.from_user.first_name}!</b>\n'\
            f'Меня зовут <b>Doge</b> и я показываю '\
            f'информацию о ТОП-10 криптовалют. '\
            f'Выбери одну из криптовалют ниже:'
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    key = []
    for name in result.keys():
        if len(key) == 2:
            keyboard.add(key[0], key[1])
            key.clear()
        key.append(telebot.types.KeyboardButton(text=name))
    keyboard.add(key[0], key[1])
    bot.send_message(message.from_user.id, msg, parse_mode='html', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text in result.keys():
        up_result = coincap_pars.start()
        sym = u"\U0001F4CB"
        msg = f'{sym}<u>Информация о криптовалюте <b>{message.text}</b>:</u>\n'
        for value in up_result[message.text].keys():
            if value == 'price':
                # sym = u"\U0001F4B5"
                sym = b'\xF0\x9F\x92\xB8'.decode()
                msg += f'{sym} Цена на данный момент: ' \
                       f'<b>&#36; {up_result[message.text][value]}</b>\n'
            elif value == 'market_cap':
                sym = u"\U0001F4B0"
                msg += f'{sym} Капитализация на рынке: ' \
                       f'<b>&#36; {up_result[message.text][value]:,}</b>'
            elif value == 'percent_change_24h':
                sym = u"\u2B07\uFE0F"
                if up_result[message.text][value] > 0:
                    sym = u"\u2B06\uFE0F"
                msg += f'{sym} Колебание цены за последние 24 часа: ' \
                       f'<b>{up_result[message.text][value]:,} &#37;</b>\n'
        bot.send_message(message.from_user.id, msg, parse_mode='html')
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери одну из криптовалют ниже:')


if __name__ == '__main__':
    bot.infinity_polling()
