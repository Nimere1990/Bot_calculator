
import telebot
from telebot import types

bot = telebot.TeleBot("5916857325:AAFg8c6yV39L51A1pThFWwxz6Kofs0IGx8I", parse_mode=None)
storage = {}

def init_storage(user_id):
  storage[user_id] = dict(first=None, znak=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Калькулятор")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Поздороваться":
        bot.send_message(message.chat.id, text="Привет!")
    
    elif message.text == "Калькулятор":
        init_storage(message.from_user.id)
        bot.send_message(message.chat.id, text="Введите первое число")
        bot.register_next_step_handler(message, calc1)

    elif message.text == "Вернуться":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Калькулятор")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")

def calc1(message): 
    first = message.text
    try:
        x = int(first)
    except:
        bot.send_message(message.chat.id, text="Вы ввели не число")
        return 
    store_number(message.from_user.id, "first", first)
    bot.send_message(message.chat.id, text="Выберите операцию + - * /")
    bot.register_next_step_handler(message, znak)
    

def znak(message):
    znak = message.text
    if znak == "+" or znak == "-" or znak == "*" or znak == "/":
        store_number(message.from_user.id, "znak", znak)
    else:
        bot.send_message(message.chat.id, text="Вы ввели неверную операцию")
        return
    bot.send_message(message.chat.id, text="Введите второе число")
    bot.register_next_step_handler(message, calc)
    

def calc(message):
    second = message.text
    try:
        y = int(second)
    except:
        bot.send_message(message.chat.id, text="Вы ввели не число")
        return 
    x = int(get_number(message.from_user.id, "first"))
    z = get_number(message.from_user.id, "znak")
    if z == "+":
        xy = x + y
    elif z == "-":
        xy = x - y 
    elif z == "*":
        xy = x * y
    elif z == "/" and y != 0:
        xy = x / y
    else:
        bot.send_message(message.chat.id, text="На ноль делить нельзя!")
        return
    bot.send_message(message.chat.id, text=xy)
    bot.register_next_step_handler(message, calc)

bot.polling(none_stop=False, interval=0)