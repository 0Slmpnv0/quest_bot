import telebot
import level_1
import level_2
import level_3
from telebot import async_telebot
from telebot import util
import dotenv
import random
import asyncio
import json


def load_data():
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_data(user_data: dict):
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file, indent=2, ensure_ascii=False)


def get_img(path):
    with open(path, 'r') as img:
        return img


repeats_count = 0
token = dotenv.get_key('.env', 'TELEGRAM_BOT_TOKEN')

bot = async_telebot.AsyncTeleBot(token)
start_kb = util.quick_markup({'Начать': {'callback_data': '1'}})
data = load_data()


@bot.message_handler(commands=['start', 'help'])
async def start_help(message: telebot.types.Message):
    global repeats_count
    if message.text == '/start':
        if message.from_user.username in data:
            text = (f'Снова здравствуйте, {message.from_user.username}! Добро пожаловать в бот-квест. Чтобы начать '
                    'нажмите "Начать". Чтобы продолжить с места на котором вы остановились нажмите "Продолжить"')
            reply = util.quick_markup({
                'Начать снова': {'callback_data': '1'},
                'Продолжить': {'callback_data': data[message.from_user.username]['call']}
            })
            repeats_count = data[message.from_user.username]['shouts']
        else:
            save_data({message.from_user.username: {'call': '1', 'shouts': '0'}})
            text = (f'Здравствуйте, {message.from_user.username}! Добро пожаловать в бот-квест. Чтобы начать нажмите '
                    f'"Начать"')
            reply = start_kb
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=reply)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Данный бот является платформой для прохождения текстового '
                                    'квеста. Чтобы сделать выбор просто нажмите на кнопку под '
                                    'сообщением. Удачи! Чтобы начать квест нажмите "Начать"',
                               reply_markup=start_kb)


@bot.callback_query_handler(lambda x: str(x.data)[0] == '1')
async def handle_level_1(call: telebot.types.CallbackQuery):
    await bot.edit_message_reply_markup(message_id=call.message.id, chat_id=call.from_user.id)
    global repeats_count
    save_data({call.from_user.username: {'call': call.data, 'shouts': repeats_count}})
    path = 'media/level_1/start_location.png'
    match str(call.data):
        case '1':
            text = level_1.greeting
            reply = util.quick_markup({
                '1': {'callback_data': '1.1'},
                '2': {'callback_data': '1.2'},
                '3': {'callback_data': '1.3'}
            })
        case '1.1':
            repeats_count += 1
            if repeats_count == 5:
                repeats_count = 0
                text = level_1.shout_repeat
                reply = util.quick_markup({'Перейти ко второму уровню': {'callback_data': '2'}})
                path = 'media/level_1/tired.png'
            else:
                text = level_1.if_shout_for_help
                reply = util.quick_markup({
                    '1': {'callback_data': '1.1'},
                    '2': {'callback_data': '1.2'}
                })
            save_data({call.from_user.username: {'call': call.data, 'shouts': repeats_count}})

        case '1.2':
            text = level_1.if_look_around
            reply = util.quick_markup({
                '1': {'callback_data': '1.2.1'},
                '2': {'callback_data': '1.2.2'}
            })
        case '1.3':
            text = level_1.sleep
            reply = start_kb
            path = 'media/level_1/falling.png'
        case '1.2.1':
            text = level_1.choice_door + '\n чтобы начать сначала нажмите "Начать"'
            reply = start_kb
            path = 'media/level_1/door.png'
        case '1.2.2':
            text = random.choice([level_1.choice_hatch_good, level_1.choice_hatch_bad])
            if text == level_1.choice_hatch_good:
                reply = util.quick_markup({'Перейти к следующему уровню': {'callback_data': '2'}})
            else:
                text = level_1.choice_hatch_bad + '\n чтобы начать сначала нажмите "Начать"'
                reply = start_kb
            path = 'media/level_1/jumper.png'
    with open(path, 'rb') as photo:
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=reply)


@bot.callback_query_handler(lambda x: str(x.data)[0] == '2')
async def handle_level_2(call: telebot.types.CallbackQuery):
    save_data({call.from_user.username: {'call': call.data, 'shouts': repeats_count}})
    await bot.edit_message_reply_markup(message_id=call.message.id, chat_id=call.from_user.id)
    match call.data:
        case '2':
            text = level_2.greeting
            reply = util.quick_markup({
                '1': {'callback_data': '2.1'},
                '2': {'callback_data': '2.2'}
            })
            path = 'media/level_2/hall.png'
        case '2.1':
            text = level_2.choice_left
            reply = util.quick_markup({
                '1': {'callback_data': '2.1.1'},
                '2': {'callback_data': '2.1.2'}
            })
            path = 'media/level_2/room_and_table.png'
        case '2.2':
            text = level_2.choice_right + '\nЧтобы начать снова нажмите "Начать"'
            reply = util.quick_markup({'Начать': {'callback_data': '2'}})
            path = 'media/level_2/hehehehehe.jpg'
        case '2.1.1':
            text = level_2.if_look_at_the_table
            reply = util.quick_markup({
                'Перейти на новый уровень': {'callback_data': '3'}
            })
            path = 'media/level_2/map.png'
        case '2.1.2':
            text = level_2.if_look_around
            reply = util.quick_markup({
                '1': {'callback_data': '2.1.1'},
                '2': {'callback_data': '2.1.2.2'}
            })
            path = 'media/level_2/room_and_table.png'
        case '2.1.2.2':
            text = level_2.if_red_button + '\nЧтобы начать уровень снова нажмите "Начать"'
            reply = util.quick_markup({
                'Начать': {'callback_data': '2'}
            })
            path = 'media/level_2/room_and_table.png'
    with open(path, 'rb') as photo:
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=reply)


@bot.callback_query_handler(lambda x: str(x.data)[0] == '3')
async def handle_level_3(call: telebot.types.CallbackQuery):
    save_data({call.from_user.username: {'call': call.data, 'shouts': repeats_count}})
    await bot.edit_message_reply_markup(message_id=call.message.id, chat_id=call.from_user.id)
    match call.data:
        case '3':
            text = level_3.greeting
            reply = util.quick_markup({
                '1': {'callback_data': '3.1'},
                '2': {'callback_data': '3.2'},
                '3': {'callback_data': '3.3'}
            })
            path = 'media/level_3/forest.png'
        case '3.1':
            text = level_3.if_catacombs + '\nВы прошли игру! Чтобы пройти весь квест снова нажмите "Начать"'
            reply = start_kb
            path = 'media/level_3/bad_room.png'
        case '3.2':
            text = level_3.if_forest + '\nВы прошли игру! Чтобы пройти весь квест снова нажмите "Начать"'
            reply = start_kb
            path = 'media/level_3/christmass_tree.png'
        case '3.3':
            text = level_3.forest_immediate + '\nВы прошли игру! Чтобы пройти весь квест снова нажмите "Начать"'
            reply = start_kb
            path = 'media/level_3/forest_bad.png'

    with open(path, 'rb') as photo:
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=reply)


asyncio.run(bot.polling(non_stop=True))
