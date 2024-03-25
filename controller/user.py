from data import db_session
from data.model.Roles import Role
from data.model.User import User
from data.model.Like import Like
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


def get_vk_id(id):
    session = db_session.create_session()

    user = session.query(User).get(id)
    if not user:
        session.close()
        return "Пользователь не найден"

    vk_id = user.vk_id

    session.close()
    return vk_id


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


def user_is_ready_for_looking_for_people(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()

    session.close()
    return user.for_people is not None


def set_for_people(user_id, text):
    session = db_session.create_session()

    user = session.query(User).filter(User.vk_id == user_id).first()
    user.for_people = text
    session.add(user)
    session.commit()

    session.close()


def get_random_for_people(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id != user_id, User.for_people is not None).order_by(
        func.random()).first()
    session.close()

    if user:
        return user.vk_id


def get_for_people_info(user_id):
    session = db_session.create_session()
    # user = session.query(User).filter(User.vk_id != user_id, User.for_people is not None).order_by(func.random()).first()
    user = session.query(User).filter(User.vk_id == user_id).first()
    res = user.for_people, get_faculty_longs_keys(user.faculty_id), user.age, "мужской" if user.is_male else "женский"
    session.close()

    return res


def add_like(from_user, to_user):
    session = db_session.create_session()
    from_user = session.query(User).filter(User.vk_id == from_user).first()
    to_user = session.query(User).get(to_user)
    if not from_user or not to_user:
        session.close()
        return False
    new_like = Like()
    new_like.from_user = from_user
    new_like.to_user = to_user
    new_like.message = ""
    session.add(new_like)
    session.commit()
    session.close()
    return True


def add_warn(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return False
    user.warns += 1
    if user.warns > 5:
        user.is_muted_for_people = True
    session.merge(user)
    session.commit()
    session.close()
    return True


def get_is_muted(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    is_muted = user.is_muted_for_people
    session.close()
    return is_muted


def get_warn():
    session = db_session.create_session()
    user = session.query(User).filter(User.warns > 0).order_by(User.warns).first()
    if not user:
        session.close()
        return None
    ID = user.id
    session.close()
    return ID


def ban_user(user_id, ban=True):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return False
    user.is_muted_for_people = ban
    user.warns = 0
    session.merge(user)
    session.commit()
    session.close()
    return True


def get_likes_me(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return None
    like = session.query(Like).filter(Like.to_user == user).filter(Like.accepted == False).order_by(Like.id).first()
    if not like:
        session.close()
        return None
    ID = like.from_user_id
    ID2 = like.id
    session.close()
    return ID, ID2


def get_likes_them(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return None
    que = session.query(Like).filter(Like.from_user == user).filter(Like.accepted == False)
    count = que.count()
    likes = que.order_by(-Like.id).limit(5)
    if not likes:
        session.close()
        return None
    ids = set()
    for like in likes:
        ids.add(like.to_user_id)
    session.close()
    return sorted(ids), count


def get_like_vk_profiles(like_id):
    session = db_session.create_session()
    like = session.query(Like).get(like_id)
    if not like:
        session.close()
        return None
    vk_id_1 = like.from_user.vk_id
    vk_id_2 = like.to_user.vk_id
    like.accepted = True
    session.merge(like)
    session.commit()
    session.close()
    return vk_id_1, vk_id_2
