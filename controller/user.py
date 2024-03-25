from data import db_session
from data.model.Roles import Role
from data.model.User import User
from data.model.Reaction import Reaction
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
        return None

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
        new_user.page = "start"

        new_role = Role()
        new_role.user = new_user
        new_role.role_name = "user"

        session.add(new_user)
        session.add(new_role)
        session.commit()

        if user_id == 318220914:
            add_role(user_id, "tester")
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
    if not user:
        return None
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
    user = session.query(User).filter(User.vk_id != user_id,
                                      User.is_muted_for_people is not False,
                                      User.is_active_questionnaire).order_by(func.random()).first()
    session.close()

    if user:
        return user.vk_id
    else:
        return user_id


def get_for_people_info(user_id):
    session = db_session.create_session()
    # user = session.query(User).filter(User.vk_id != user_id, User.for_people is not None).order_by(func.random()).first()
    user = session.query(User).filter(User.vk_id == user_id).first()
    res = user.for_people, get_faculty_longs_keys(user.faculty_id), user.age, "мужской" if user.is_male else "женский"
    session.close()

    return res


def add_reaction(from_user, to_user, reaction, is_answered=True):

    session = db_session.create_session()
    from_user = session.query(User).filter(User.vk_id == from_user).first()
    to_user = session.query(User).filter(User.vk_id == to_user).first()
    if not from_user or not to_user:
        session.close()
        return 0
    new_reaction = Reaction()
    new_reaction.from_user = from_user
    new_reaction.to_user = to_user
    new_reaction.reaction = reaction
    new_reaction.is_answered = is_answered
    new_reaction.message = ""
    res = 1
    session.add(new_reaction)
    session.commit()
    if reaction == -2:  # warn
        print("WARN")
        to_user.warns += 1
        if to_user.warns > 5:
            to_user.is_muted_for_people = True
            res = 2
        session.merge(to_user)
    session.commit()
    session.close()
    return res


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
    ID = user.vk_id
    session.close()
    return ID


def ban_user(user_id, ban=True):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
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
    reaction = session.query(Reaction).filter(Reaction.to_user == user,
                                              Reaction.is_answered is False).order_by(Reaction.id).first()
    if not reaction:
        session.close()
        return None
    ID = reaction.from_user_id
    ID2 = reaction.id
    session.close()
    return ID, ID2


def get_likes_them(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return None
    que = session.query(Reaction).filter(Reaction.from_user == user).filter(Reaction.accepted == False)
    count = que.count()
    reactions = que.order_by(-Reaction.id).limit(5)
    if not reactions:
        session.close()
        return None
    ids = set()
    for reaction in reactions:
        ids.add(reaction.to_user_id)
    session.close()
    return sorted(ids), count


def get_like_vk_profiles(like_id):
    session = db_session.create_session()
    reaction = session.query(Reaction).get(like_id)
    if not reaction:
        session.close()
        return None
    vk_id_1 = reaction.from_user.vk_id
    vk_id_2 = reaction.to_user.vk_id
    reaction.accepted = True
    session.merge(reaction)
    session.commit()
    session.close()
    return vk_id_1, vk_id_2


def get_is_active_questionnaire(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return None
    res = user.is_active_questionnaire
    session.close()
    return res


def toggle_is_active_questionnaire(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.vk_id == user_id).first()
    if not user:
        session.close()
        return False
    user.is_active_questionnaire = not user.is_active_questionnaire
    session.merge(user)
    session.commit()
    session.close()
    return True
