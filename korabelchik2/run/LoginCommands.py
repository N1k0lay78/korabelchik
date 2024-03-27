from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


# --- login ---
from smtu_info import faculty_keys


class StartCommand(Command):
    def __init__(self, bot):
        super().__init__("start", bot)

    def function(self, params, event):
        self.bot.send_message(event.user_id, f"Привет, это бот тестовичок!\nЯ работаю в тестовом режиме, все ваши данные могут быть просмотренны.")

        self.bot.save_image(event.user_id)

        com = self.bot.get_command("ask_age")
        com.function(["set"], event)

"""
Можно получить только пол пользователя - такое себе
https://dev.vk.com/ru/method/account.getProfileInfo
# profile info
class AskProfileInfoCommand(Command):
    def __init__(self, bot):
        super().__init__("ask_profile_info", bot)

    def function(self, params, event):
        if validation_str(self.bot, event, params):
            if params[0] in ["update", "set"]:
                set_page(event.user_id, f"set_profile_info {params[0]}")
            else:
                self.bot.send_message(event.user_id, "Неверный параметр")
                return None
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Из профиля", VkKeyboardColor.SECONDARY, {"command": "set_profile_info True"})
            keyboard.add_button("Введу сам", VkKeyboardColor.SECONDARY, {"command": "set_profile_info False"})
            self.bot.send_message(event.user_id, f"Использовать данные из вашего профиля ВК?", keyboard=keyboard.get_keyboard())


class SetProfileInfoCommand(Command):
    def __init__(self, bot):
        super().__init__("set_profile_info", bot)

    def function(self, params, event):
        if validate_page(self.bot, event, "set_profile_info", ["update", "set"]) and validation_str(self.bot, event, params):
            if params[0] == "True":
            self.bot.mark_as_read(event)
            if get_user_page(event.user_id).split()[1] == "update":
                set_page(event.user_id, "main")
            else:
                if params[0] == "True":
                    # com = self.bot.get_command("ask_gender")
                    # com.function(["set"], event)
                    pass
                else:
                    pass
"""


# age
class AskAgeCommand(Command):
    def __init__(self, bot):
        super().__init__("ask_age", bot)

    def function(self, params, event):
        if validation_str(self.bot, event, params):
            if params[0] in ["update", "set"]:
                set_page(event.user_id, f"set_age {params[0]}")
            else:
                self.bot.send_message(event.user_id, "Неверный параметр")
                return None
            self.bot.send_message(event.user_id, f"Введите ваш возраст:")


class SetAgeCommand(Command):
    def __init__(self, bot):
        super().__init__("set_age", bot)

    def function(self, params, event):
        if validate_page(self.bot, event, "set_age", ["update", "set"]) and validation_int(self.bot, event, params):
            set_user_age(event.user_id, int(params[0]))
            self.bot.mark_as_read(event)
            if get_user_page(event.user_id).split()[1] == "update":
                self.bot.get_command("edit").function([], event)
            else:
                com = self.bot.get_command("ask_gender")
                com.function(["set"], event)


# gender
class AskGenderCommand(Command):
    def __init__(self, bot):
        super().__init__("ask_gender", bot)

    def function(self, params, event):
        if validation_str(self.bot, event, params):
            if params[0] in ["update", "set"]:
                set_page(event.user_id, f"set_gender {params[0]}")
            else:
                self.bot.send_message(event.user_id, "Неверный параметр")
                return None
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Мужской", VkKeyboardColor.SECONDARY, {"command": "set_gender male"})
            keyboard.add_button("Женский", VkKeyboardColor.SECONDARY, {"command": "set_gender female"})
            self.bot.send_message(event.user_id, f"Выберите ваш пол:", keyboard=keyboard.get_keyboard())


class SetGenderCommand(Command):
    def __init__(self, bot):
        super().__init__("set_gender", bot)

    def function(self, params, event):
        if validate_page(self.bot, event, "set_gender", ["update", "set"]) and validation_str(self.bot, event, params):
            type_page = get_user_page(event.user_id).split()[1]
            if params[0] in ["male", "female"]:
                set_user_gender(event.user_id, params[0])
            else:
                com = self.bot.get_command("ask_gender")
                com.function([type_page], event)
                return None
            self.bot.mark_as_read(event)
            if type_page == "update":
                self.bot.get_command("edit").function([], event)
            else:
                com = self.bot.get_command("ask_faculty")
                com.function(["set"], event)


# faculty
class AskFacultyCommand(Command):
    def __init__(self, bot):
        super().__init__("ask_faculty", bot)

    def function(self, params, event):
        if validation_str(self.bot, event, params):
            if params[0] in ["update", "set"]:
                set_page(event.user_id, f"set_faculty {params[0]}")
            else:
                self.bot.send_message(event.user_id, "Неверный параметр")
                return None
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("ФЦПТ", VkKeyboardColor.SECONDARY, {"command": "set_faculty fcpt"})
            keyboard.add_button("ФМП", VkKeyboardColor.SECONDARY, {"command": "set_faculty fmp"})
            keyboard.add_button("ФКиО", VkKeyboardColor.SECONDARY, {"command": "set_faculty fkio"})
            keyboard.add_button("ФКЭиА", VkKeyboardColor.SECONDARY, {"command": "set_faculty fkeia"})
            keyboard.add_line()
            keyboard.add_button("ФЕНГО", VkKeyboardColor.SECONDARY, {"command": "set_faculty feigo"})
            keyboard.add_button("ИЭФ", VkKeyboardColor.SECONDARY, {"command": "set_faculty ief"})
            # keyboard.add_line()
            # keyboard.add_button("Назад", VkKeyboardColor.PRIMARY, {"command": "set_page edit"})
            self.bot.send_message(event.user_id, f"Выберите ваш факультет:", keyboard=keyboard.get_keyboard())


class SetFacultyCommand(Command):
    def __init__(self, bot):
        super().__init__("set_faculty", bot)

    def function(self, params, event):
        if validate_page(self.bot, event, "set_faculty", ["update", "set"]) and validation_str(self.bot, event, params):
            type_page = get_user_page(event.user_id).split()[1]
            if params[0] in faculty_keys:
                set_user_faculty(event.user_id, params[0])
            else:
                com = self.bot.get_command("ask_faculty")
                com.function([type_page], event)
                return None
            self.bot.mark_as_read(event)
            if type_page == "update":
                self.bot.get_command("edit").function([], event)
            else:
                com = self.bot.get_command("ask_about_text")
                com.function(["set"], event)


# about text
class AskAboutTextCommand(Command):
    def __init__(self, bot):
        super().__init__("ask_about_text", bot)

    def function(self, params, event):
        if validation_str(self.bot, event, params):
            if params[0] in ["update", "set"]:
                set_page(event.user_id, f"set_about_text {params[0]}")
            else:
                self.bot.send_message(event.user_id, "Неверный параметр")
                return None
            self.bot.send_message(event.user_id, f"Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию.")


class SetAboutTextCommand(Command):
    def __init__(self, bot):
        super().__init__("set_about_text", bot)

    def function(self, params, event):
        if validate_page(self.bot, event, "set_about_text", ["update", "set"]) and validation_str(self.bot, event, params):
            set_for_people(event.user_id, params[0])
            self.bot.mark_as_read(event)
            if get_user_page(event.user_id).split()[1] == "update":
                self.bot.get_command("edit").function([], event)
            else:
                com = self.bot.get_command("main")
                com.function([], event)


"""# image
class AskImageCommand(Command):
    def __init__(self, bot):
        super().__init__("ask_image", bot)

    def function(self, params, event):
        if validation_str(self.bot, event, params):
            if params[0] in ["update", "set"]:
                set_page(event.user_id, f"set_image {params[0]}")
            else:
                self.bot.send_message(event.user_id, "Неверный параметр")
                return None
            self.bot.send_message(event.user_id, f"Отправьте своё изображение:")


class SetImageCommand(Command):
    def __init__(self, bot):
        super().__init__("set_image", bot)

    def function(self, params, event):
        if validate_page(self.bot, event, "set_image", ["update", "set"]):
            if "attach1" in event.attachments and event.raw[-2][f"attach1_type"] == "photo":
                self.bot.save_image(event.raw[-2]["attach1"])  # 318220914_457245392

            #     photo = self.__upload.photo_messages(photos=image.raw)[0]
            type_page = get_user_page(event.user_id).split()[1]
            if True:
                com = self.bot.get_command("ask_image")
                com.function([type_page], event)
                return None
            else:
                com = self.bot.get_command("ask_image")
                com.function([type_page], event)
                return None
            set_for_people(event.user_id, params[0])
            self.bot.mark_as_read(event)
            if get_user_page(event.user_id).split()[1] == "update":
                set_page(event.user_id, "main")
            else:
                # com = self.bot.get_command("ask_image")
                # com.function(["set"], event)
                pass"""
