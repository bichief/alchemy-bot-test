from sqlalchemy.exc import DatabaseError

from data.config import engine
from sqlalchemy.orm import Session

from utils.db_api.db_alchemy import Users, Registration

session = Session(engine)


def insert_users(message):
    try:
        user = Users(
            telegram_id=message.chat.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        session.add(user)
        session.commit()
    except DatabaseError:
        session.rollback()


def insert_reg(phone, email, telegram_id):
    global user_id
    try:
        result = session.query(Users.id).filter(Users.telegram_id == f'{telegram_id}')

        for row in result:
            user_id = row.id

        reg = Registration(
            users_id=user_id,
            phone=phone,
            email=email,
        )
        session.add(reg)
        session.commit()
    except DatabaseError:
        session.rollback()


def select_state(telegram_id):
    global state

    result = session.query(Users.state).filter(Users.telegram_id == telegram_id)

    for row in result:
        state = row.state
        print(state)

    return state

def update_state(telegram_id):
    global user_id
    result = session.query(Users.id).filter(Users.telegram_id == f'{telegram_id}')

    for row in result:
        user_id = row.id

    update = session.query(Users).get(user_id)
    update.state = 'true'
    session.add(update)
    session.commit()