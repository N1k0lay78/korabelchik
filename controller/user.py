from data import db_session
from data.model.Roles import Role
from data.model.User import User
from smtu_info import get_faculty_id, get_faculty_is_technical, get_faculty_longs_keys
from sqlalchemy.sql.expression import func


def is_user_authenticated(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    session.close()

    return user is not None


def add_role(user_id, role_name):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return "Пользователь не найден"

    # у пользователя нет этой роли
    if all(role.role_name != role_name for role in user.roles):
        new_role = Role()
        new_role.user = user
        new_role.role_name = role_name
        session.add(new_role)
        session.commit()
        session.close()
        return "Роль добавлена"

    session.close()
    return "У пользователя уже есть эта роль"


def remove_role(user_id, role_name):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return "Пользователь не найден"

    # у пользователя есть эта роль
    role = [role for role in user.roles if role.role_name == role_name]
    if role:
        user.roles = [role for role in user.roles if role.role_name != role_name]
        session.add(user)
        session.commit()
        session.close()
        return "Роль удалена"

    session.close()
    return "У пользователя нет этой роли"


def get_roles(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return {}

    role = [role.role_name for role in user.roles]

    session.close()
    return role


def get_ids(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return "Пользователь не найден"

    resp = {"id": user.id, "vk_id": user.vk_id}

    session.close()
    return resp


def remove_user(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return "Пользователь не найден"

    roles = session.query(Role).filter(Role.user_id == user.id).all()
    for role in roles:
        session.delete(role)
    session.delete(user)
    session.commit()

    session.close()
    return "Пользователь удалён"


def signin_user(user_id):
    if not is_user_authenticated(user_id):
        session = db_session.create_session()

        new_user = User()
        new_user.vk_id = user_id
        new_user.page = "age"

        new_role = Role()
        new_role.user = new_user
        new_role.role_name = "user"

        session.add(new_user)
        session.add(new_role)
        session.commit()

        if user_id == 318220914:
            add_role(user_id, "moderator")
            add_role(user_id, "owner")

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


def user_is_ready_for_looking_for_friends(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()

    session.close()
    return user.for_friends is not None



def set_for_friends(user_id, text):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.for_friends = text
    session.add(user)
    session.commit()

    session.close()


def set_for_interests(user_id, text):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.for_interests = text
    session.add(user)
    session.commit()

    session.close()


def user_is_ready_for_looking_for_interests(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()

    session.close()
    return user.for_interests is not None


def get_random_for_friend(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id != user_id, User.for_friends is not None).order_by(func.random()).first()
    session.close()

    if user:
        return user.id

def get_random_for_interests(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id != user_id, User.for_interests is not None).order_by(func.random()).first()
    session.close()

    if user:
        return user.id


def get_for_friends_info(user_id):
    session = db_session.create_session()
    # user = session.query(User).filter(User.vk_id != user_id, User.for_friends is not None).order_by(func.random()).first()
    user = session.query(User).filter(User.vk_id == user_id).first()
    res = user.for_friends, get_faculty_longs_keys(user.faculty_id), user.age, "мужской" if user.is_male else "женский"
    session.close()

    return res


def get_for_interests_info(user_id):
    session = db_session.create_session()
    # user = session.query(User).filter(User.vk_id != user_id, User.for_friends is not None).order_by(func.random()).first()
    user = session.query(User).filter(User.vk_id == user_id).first()
    res = user.for_interests, get_faculty_longs_keys(user.faculty_id), user.age, "мужской" if user.is_male else "женский"
    session.close()

    return res