from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


# --- tester ---
class SetPageCommand(Command):
    def __init__(self, bot):
        super().__init__("set_page", bot)

    def function(self, params, event):
        if validation_role(self.bot, event, ["owner", "tester"]) and validation_str(self.bot, event, params):
            set_page(event.user_id, params[0])
            self.bot.mark_as_read(event)
