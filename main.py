import telebot
from sqlalchemy.exc import IntegrityError

from data import config
from keyboards.inline.reg import reg
from utils.commands import insert_users, insert_reg, select_state, update_state

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands='get')
def get_cmd(message):
    res = select_state(message.chat.id)
    bot.send_message(message.chat.id, res)

@bot.message_handler(commands='state')
def state_cmd(message):
    bot.send_message(message.chat.id, 'ok')
    update_state(message.chat.id)

@bot.message_handler(commands='start')
def start_cmd(message):
    global chat_id
    try:
        chat_id = message.chat.id
        insert_users(message)
        bot.send_message(chat_id, 'Привет, добро пожаловать в бота для регистрации в нашем проекте.\n'
                                  'Чтобы начать регистрацию, нажми на кнопку ниже', reply_markup=reg)
    except IntegrityError:
        bot.send_message(chat_id, 'Ты уже авторизовался для регистрации. нажми кнопку ниже.', reply_markup=reg)


@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    if call.data == 'start_reg':
        if select_state(call.message.chat.id) == 'false':
            msg = bot.edit_message_text(
                text='Окей, укажите ваш номер телефона, начиная с +7',
                chat_id=call.message.chat.id,
                message_id=call.message.id
            )
            bot.register_next_step_handler(msg, add_number)
        else:
            bot.edit_message_text(
                text='Вы уже зарегестрированы',
                chat_id=call.message.chat.id,
                message_id=call.message.id
            )

def add_number(message):
    global phone
    phone = message.text
    if phone.startswith('+79') and len(phone) == 12:
        msg = bot.send_message(message.chat.id, 'Отлично, отправь теперь мне свой email')
        bot.register_next_step_handler(msg, add_email)
    else:
        msg = bot.send_message(message.chat.id, 'Неверный формат.\n'
                                                'Пример номера:\n'
                                                '+79059494949')
        bot.register_next_step_handler(msg, add_number)


def add_email(message):
    email = message.text
    if email.find('@') != -1 and email.endswith('.ru') or email.endswith('.com'):
        insert_reg(phone, email, telegram_id=message.chat.id)
        update_state(message.chat.id)
        bot.send_message(message.chat.id, 'Отлично, я зарегистрировал тебя в Базе Данных.\n'
                                          'Твои данные:\n'
                                          f'Имя: {message.from_user.first_name}\n'
                                          f'Телефон: {phone}\n'
                                          f'Email: {email}\n\n'
                                          f'В скором времени с тобой свяжутся, будь на связи.')
    else:
        msg = bot.send_message(message.chat.id, 'Ты что-то напутал..\n'
                                                'Пример Email:\n'
                                                'example@mail.ru')
        bot.register_next_step_handler(msg, add_email)


if __name__ == '__main__':
    bot.infinity_polling(allowed_updates=True)
