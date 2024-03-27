from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


class WarnsCommand(Command):
    def __init__(self, bot):
        super().__init__("warns", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "moderator"]):
            ID = get_warn()
            if ID:
                com = self.bot.get_command("get_user")
                com.function([str(ID), "keyboard2"], event)
            else:
                self.bot.send_message(event.user_id, "Нет предупреждений")
                self.bot.get_command("main").function([], event)


class BanCommand(Command):
    def __init__(self, bot):
        super().__init__("ban", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "moderator"]) and validation_int(self.bot, event, params):
            if ban_user(int(params[0])):
                self.bot.send_message(event.user_id, "Пользователь забанен")
            else:
                self.bot.send_message(event.user_id, "Пользователь не найден")
        self.bot.get_command("warns").function([], event)


class UnbanCommand(Command):
    def __init__(self, bot):
        super().__init__("unban", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "moderator"]) and validation_int(self.bot, event, params):
            if ban_user(int(params[0]), False):
                self.bot.send_message(event.user_id, "Пользователь разбанен")
            else:
                self.bot.send_message(event.user_id, "Пользователь не найден")
        self.bot.get_command("warns").function([], event)