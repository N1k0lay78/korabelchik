from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


# --- tester ---
class SetPageCommand(Command):
    def __init__(self, bot):
        super().__init__("set_page", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner"]) and validation_str(self.bot, event, params):
            set_page(event.user_id, params[0])
            self.bot.mark_as_read(event)


class GetFullUserInfoCommand(Command):
    def __init__(self, bot):
        super().__init__("get_full_user_info", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner"]) and validation_int(self.bot, event, params):
            info = get_user_full_info(int(params[0]))
            if info is not None:
                self.bot.send_message(event.user_id, f"fac_id: {info[0]}\nage: {info[1]}\ngender: {info[2]}\nvk_id: {info[3]}\npage: {info[4]}\nis_active: {info[5]}\nis_muted: {info[6]}")
            else:
                self.bot.send_message(event.user_id, f"пользователь не найден")