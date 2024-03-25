from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


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


class ReactionCommand(Command):
    def __init__(self, bot):
        super().__init__("reaction", bot)

    def function(self, params, event):
        if validation_int(self.bot, event, params) and validate_page_id(self.bot, event, "looking_for"):
            page_id = int(get_user_page(event.user_id).split()[1])
            if add_reaction(event.user_id, page_id, int(params[0]), int(params[0]) != 1) == 2:
                # mute notification
                self.bot.send_message(get_ids(page_id)["vk_id"], "Ваша анкета отключена на время проверки")
            self.bot.get_command("looking_for").function([], event)


class ToggleQuestionnaireCommand(Command):
    def __init__(self, bot):
        super().__init__("toggle_questionnaire", bot)

    def function(self, params, event):
        if not toggle_is_active_questionnaire(event.user_id):
            self.bot.send_message(event.user_id, "Не удалось найти пользователя")
        self.bot.mark_as_read(event)
        self.bot.get_command("profile").function([], event)


class GetUserCommand(Command):
    def __init__(self, bot):
        super().__init__("get_user", bot)

    def function(self, params, event):
        if validation_int(self.bot, event, params):
            user_id = int(params[0])
            if not user_id:
                self.bot.send_message(event.user_id, "Пользователь не найден")
                return None
            img, name, _surname = self.bot.get_vk_info(user_id)
            text, fac, age, gender = get_for_people_info(user_id)
            # работает - не трогай, checked by rjkzavr at 1-100 yo
            yo = ("год" if age % 10 == 1 else "года") if (5 > age % 10 > 0) and age // 10 != 1 else "лет"
            if "keyboard" in params:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("👎", VkKeyboardColor.PRIMARY, {"command": "reaction -1"})
                keyboard.add_button("🚨", VkKeyboardColor.SECONDARY, {"command": "reaction -2"})
                keyboard.add_button("👋", VkKeyboardColor.PRIMARY, {"command": "reaction 1"})
                keyboard.add_button("👀", VkKeyboardColor.PRIMARY, {"command": "reaction 0"})
                keyboard.add_line()
                keyboard.add_button("на главную", VkKeyboardColor.PRIMARY, {"command": "main"})
                if "moderator" in get_roles(event.user_id):
                    keyboard.add_button("БАН", VkKeyboardColor.NEGATIVE, {"command": "edit"})
                self.bot.send_message(event.user_id, f"{name}, {age} {yo}\n{fac}\nПол: {gender}\nО себе:\n{text}",
                                      attachment=img, keyboard=keyboard.get_keyboard())
            elif "keyboard2" in params:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("забанить", VkKeyboardColor.NEGATIVE, {"command": f"ban {user_id}"})
                keyboard.add_button("разбанить", VkKeyboardColor.POSITIVE, {"command": f"unban {user_id}"})
                keyboard.add_line()
                keyboard.add_button("на главную", VkKeyboardColor.PRIMARY, {"command": "main"})
                self.bot.send_message(event.user_id, f"{name}, {age} {yo}\n{fac}\nПол: {gender}\nО себе:\n{text}",
                                      attachment=img, keyboard=keyboard.get_keyboard())
            else:
                self.bot.send_message(event.user_id, f"{name}, {age} {yo}\n{fac}\nПол: {gender}\nО себе:\n{text}",
                                      attachment=img)


class ViewMyCommand(Command):
    def __init__(self, bot):
        super().__init__("view_my", bot)

    def function(self, params, event):
        if validation_int(self.bot, event, params):
            self.bot.get_command("get_user").function([str(event.user_id)], event)
            self.bot.get_command("profile").function([], event)


class LookingForCommand(Command):
    def __init__(self, bot):
        super().__init__("looking_for", bot)

    def function(self, params, event):
        look_id = get_random_for_people(event.user_id)
        if not look_id:
            self.bot.send_message(event.user_id, "Не найдено ни одной анкеты")
            self.bot.get_command("main").function([], event)
            return
        set_page(event.user_id, f"looking_for {look_id}")
        self.bot.get_command("get_user").function([str(look_id), "keyboard"], event)
