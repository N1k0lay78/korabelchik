from data import db_session
from data.model.User import User
from smtu_info import get_faculty_id, get_faculty_is_technical


def is_user_authenticated(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    session.close()

    return user is not None


def signin_user(user_id):
    if not is_user_authenticated(user_id):
        session = db_session.create_session()

        new_user = User()
        new_user.vk_id = user_id
        new_user.page = "age"

        session.add(new_user)
        session.commit()

        print(f"signin user with {user_id = }")

        session.close()


def get_user_page(user_id):
    if not is_user_authenticated(user_id):
        signin_user(user_id)

    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    session.close()

    return user.page


def set_user_age(user_id, age):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.age = int(age)
    session.add(user)
    session.commit()

    session.close()


def set_user_gender(user_id, male):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.is_male = male == "male"
    session.add(user)
    session.commit()

    session.close()


def set_user_faculty(user_id, faculty):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.faculty_id = get_faculty_id(faculty)
    user.is_technical = get_faculty_is_technical(faculty)
    session.add(user)
    session.commit()

    session.close()


def set_page(user_id, page):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.page = page
    session.add(user)
    session.commit()

    session.close()