from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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


class RolesCommand(Command):
    def __init__(self, bot):
        super().__init__("roles", bot)

    def function(self, params, event):
        roles = self.bot.get_roles(event.user_id)
        self.bot.send_message(event.user_id, f"Ваши роли: {roles}")


class DinoCommand(Command):
    def __init__(self, bot):
        super().__init__("dino", bot)

    def function(self, params, event):
        roles = self.bot.get_roles(event.user_id)
        self.bot.send_message(event.user_id, f"Динозавр выглядит так:", attachment="photo318220914_1711374849")


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