from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


class HelpCommand(Command):
    def __init__(self, bot):
        super().__init__("help", bot)

    def function(self, params, event):
        roles = self.bot.get_roles(event.user_id)
        text = "Команды:\n"
        if "user" in roles:
            text += """/roles - узнать свои роли
            /page - узнать свою страницу
            /ids - узнать свои ID
            /info - метаинформация о пользователе\n\n"""
        if "moderator" in roles or "owner" in roles:
            text += """/warns - пользователи на которых оставили жалобы
            /ban <id> - забанить человека
            /unban <id> - разбанить человека\n\n"""
        if "tester" in roles or "owner" in roles:
            text += """/set_page <page> - перейти на страницу
            /get_user - получить случайного пользователя
            /get_user <id> - получить пользователя
            /like <id> - поставить лайк пользователю
            /likes - люди, которым вы понравились
            /accept <like_id> - принять запрос дружбы
            /cancel <like_id> - отклонить запрос дружбы
            /warn <id> - пожаловаться на пользователя\n\n"""
        if "owner" in roles:
            text += """/add_role <id> <role> - добавить роль
            /remove_role <id> <role> - убрать роль
            /roles <id> - роль человека\n\n"""
        self.bot.send_message(event.user_id, text)


# --- login ---
class StartCommand(Command):
    def __init__(self, bot):
        super().__init__("start", bot)

    def function(self, params, event):
        self.bot.send_message(event.user_id, f"Привет, это бот тестовичок!\nЯ работаю в тестовом режиме, все ваши данные могут быть просмотренны.")


# --- user ---
class RolesCommand(Command):
    def __init__(self, bot):
        super().__init__("roles", bot)

    def function(self, params, event):
        roles = self.bot.get_roles(event.user_id)
        self.bot.send_message(event.user_id, f"Ваши роли: {roles}")


class PageCommand(Command):
    def __init__(self, bot):
        super().__init__("page", bot)

    def function(self, params, event):
        page = self.bot.get_page(event.user_id)
        self.bot.send_message(event.user_id, f"Вы на странице: {page}")


class IDCommand(Command):
    def __init__(self, bot):
        super().__init__("ids", bot)

    def function(self, params, event):
        ids = get_ids(event.user_id)
        self.bot.send_message(event.user_id, f"ID: {ids['id']}\nVK_ID: {ids['vk_id']}")


class InfoCommand(Command):
    def __init__(self, bot):
        super().__init__("info", bot)

    def function(self, params, event):
        roles = self.bot.get_roles(event.user_id)
        page = self.bot.get_page(event.user_id)
        ids = get_ids(event.user_id)
        is_ready_for_search = user_is_ready_for_looking_for_people(event.user_id)
        self.bot.send_message(event.user_id, f"""Ваши роли: {roles}
        Ваша страница: {page}
        Готов к поиску людей: {is_ready_for_search}
        ID: {ids['id']}
        VK_ID: {ids['vk_id']}""")


# --- tester ---
class SetPageCommand(Command):
    def __init__(self, bot):
        super().__init__("set_page", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]) and validation_str(self.bot, event, params):
            set_page(event.user_id, params[0])
            self.bot.mark_as_read(event)


class GetUserCommand(Command):
    def __init__(self, bot):
        super().__init__("get_user", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]):
            if len(params) > 0 and params[0].isdigit():
                random_user_id = get_vk_id(int(params[0]))
                if type(random_user_id) != int:
                    random_user_id = get_random_for_people(event.user_id)
            else:
                random_user_id = get_random_for_people(event.user_id)
            img, name, _surname = self.bot.get_vk_info(random_user_id)
            text, fac, age, gender = get_for_people_info(random_user_id)
            # работает - не трогай, checked by rjkzavr at 1-100 yo
            yo = ("год" if age % 10 == 1 else "года") if (5 > age % 10 > 0) and age // 10 != 1 else "лет"
            # debug
            ID = get_ids(random_user_id)['id']
            self.bot.send_message(event.user_id, f"{name}, {age} {yo}\n{fac}\nПол: {gender}\n\nО себе:\n{text}\n\nID: {ID}\nIsMuted: {get_is_muted(ID)}",
                                  attachment=img)


class LikeCommand(Command):
    def __init__(self, bot):
        super().__init__("like", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]) and validation_int(self.bot, event, params):
            if not add_like(event.user_id, params[0]):
                self.bot.send_message(event.user_id, "Пользователь не найден")
            self.bot.mark_as_read(event)


class WarnCommand(Command):
    def __init__(self, bot):
        super().__init__("warn", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]) and validation_int(self.bot, event, params):
            if not add_warn(params[0]):
                self.bot.send_message(event.user_id, "Пользователь не найден")
            self.bot.mark_as_read(event)


class WarnsCommand(Command):
    def __init__(self, bot):
        super().__init__("warns", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "moderator"]):
            ID = get_warn()
            if ID:
                com = self.bot.get_command("get_user")
                com.function(str(ID), event)
            else:
                self.bot.send_message(event.user_id, "Нет предупреждений")


class BanCommand(Command):
    def __init__(self, bot):
        super().__init__("ban", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "moderator"]) and validation_int(self.bot, event, params):
            if ban_user(int(params[0])):
                self.bot.send_message(event.user_id, "Пользователь забанен")
            else:
                self.bot.send_message(event.user_id, "Пользователь не найден")


class UnbanCommand(Command):
    def __init__(self, bot):
        super().__init__("unban", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "moderator"]) and validation_int(self.bot, event, params):
            if ban_user(int(params[0], False)):
                self.bot.send_message(event.user_id, "Пользователь разбанен")
            else:
                self.bot.send_message(event.user_id, "Пользователь не найден")


class LikesMeCommand(Command):
    def __init__(self, bot):
        super().__init__("likes_me", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]):
            data = get_likes_me(event.user_id)
            if data:
                ID, ID2 = data
                com = self.bot.get_command("get_user")
                com.function(str(ID), event)
                self.bot.send_message(event.user_id, f"LikeID: {ID2}\n")
            else:
                self.bot.send_message(event.user_id, "Нет анкет ожидающих ответа")


class LikesThemCommand(Command):
    def __init__(self, bot):
        super().__init__("likes_them", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]):
            data = get_likes_them(event.user_id)
            if data:
                ids, count = data
                self.bot.send_message(event.user_id, f"Ожидают ответа {count}")
                print(ids)
                for ID in ids:
                    com = self.bot.get_command("get_user")
                    com.function(str(ID), event)
            else:
                self.bot.send_message(event.user_id, "Нет анкет ожидающих ответа")


class AcceptCommand(Command):
    def __init__(self, bot):
        super().__init__("accept", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]) and validation_int(self.bot, event, params):
            data = get_like_vk_profiles(int(params[0]))
            if data:
                vk_id_1, vk_id_2 = data
                self.bot.send_message(vk_id_1, f"Пользователь @id{vk_id_2} принял вашу заявку")
                self.bot.send_message(vk_id_2, f"Пользователь @id{vk_id_1} принял вашу заявку")
            else:
                self.bot.send_message("Реакция не найдена")
