from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


class MainPageCommand(Command):
    def __init__(self, bot):
        super().__init__("main", bot)

    def function(self, params, event):
        set_page(event.user_id, "main")
        # roles = get_roles(event.user_id)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Поиск людей", VkKeyboardColor.PRIMARY, {"command": "looking_for_page"})
        # if "moderator" in roles:
        #     keyboard.add_line()
        #     keyboard.add_button("Модерация", VkKeyboardColor.SECONDARY, {"command": "warns"})
        keyboard.add_line()
        keyboard.add_button("Профиль", VkKeyboardColor.SECONDARY, {"command": "profile"})

        self.bot.send_message(event.user_id, f"Главное меню", keyboard=keyboard.get_keyboard())


class LookingForPageCommand(Command):
    def __init__(self, bot):
        super().__init__("looking_for_page", bot)

    def function(self, params, event):
        set_page(event.user_id, "looking_for_page")
        roles = get_roles(event.user_id)
        c_like_me, c_like_them = get_reaction_statistic(event.user_id)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Искать людей", VkKeyboardColor.PRIMARY, {"command": "looking_for"})
        keyboard.add_line()
        keyboard.add_button(f"Кому интересна анкета ({min(99, c_like_me)})", VkKeyboardColor.PRIMARY,
                            {"command": "likes_me"})
        keyboard.add_line()
        keyboard.add_button(f"Чьи анкеты интересны ({min(99, c_like_them)})", VkKeyboardColor.PRIMARY,
                            {"command": "likes_them"})
        keyboard.add_line()
        if "moderator" in roles:
            keyboard.add_button("Модерация", VkKeyboardColor.SECONDARY, {"command": "warns"})
        keyboard.add_button("Главное меню", VkKeyboardColor.SECONDARY, {"command": "main"})

        self.bot.send_message(event.user_id, f"Поиск людей", keyboard=keyboard.get_keyboard())


class ProfilePageCommand(Command):
    def __init__(self, bot):
        super().__init__("profile", bot)

    def function(self, params, event):
        set_page(event.user_id, "profile")
        roles = get_roles(event.user_id)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Главное меню", VkKeyboardColor.PRIMARY, {"command": "main"})
        keyboard.add_line()
        keyboard.add_button("Редактировать", VkKeyboardColor.SECONDARY, {"command": "edit"})
        keyboard.add_line()
        keyboard.add_button("Моя анкета", VkKeyboardColor.SECONDARY,
                            {"command": f"view_my {get_ids(event.user_id)['id']}"})
        keyboard.add_line()
        if get_is_active_questionnaire(event.user_id):
            keyboard.add_button("Отключить анкету", VkKeyboardColor.SECONDARY, {"command": "toggle_questionnaire"})
        else:
            keyboard.add_button("Включить анкету", VkKeyboardColor.SECONDARY, {"command": "toggle_questionnaire"})

        self.bot.send_message(event.user_id, f"Профиль", keyboard=keyboard.get_keyboard())


class EditPageCommand(Command):
    def __init__(self, bot):
        super().__init__("edit", bot)

    def function(self, params, event):
        set_page(event.user_id, "edit")
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Профиль", VkKeyboardColor.PRIMARY, {"command": "profile"})
        keyboard.add_line()
        keyboard.add_button("Изменить возраст", VkKeyboardColor.SECONDARY, {"command": "ask_age update"})
        keyboard.add_line()
        keyboard.add_button("Изменить пол", VkKeyboardColor.SECONDARY, {"command": "ask_gender update"})
        keyboard.add_line()
        keyboard.add_button("Изменить факультет", VkKeyboardColor.SECONDARY, {"command": "ask_faculty update"})
        keyboard.add_line()
        keyboard.add_button("Изменить текст анкеты", VkKeyboardColor.SECONDARY, {"command": "ask_about_text update"})

        self.bot.send_message(event.user_id, f"Редактировать", keyboard=keyboard.get_keyboard())
