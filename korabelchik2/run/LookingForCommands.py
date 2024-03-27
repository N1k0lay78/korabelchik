from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import *
from korabelchik2.Command import Command
from korabelchik2.tools import *


class LikesThemCommand(Command):
    def __init__(self, bot):
        super().__init__("likes_them", bot)

    def function(self, params, event):
        ids = get_likes_them(event.user_id)
        if ids is not None:
            for ID in ids:
                self.bot.get_command("get_user").function([str(ID)], event)
            self.bot.get_command("looking_for_page").function([], event)
        else:
            self.bot.send_message(event.user_id, "Нет анкет ожидающих ответа")
            self.bot.get_command("looking_for_page").function([], event)


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
                self.bot.send_message(event.user_id, "Пользователь не указан")
                self.bot.get_command("main").function([], event)
                return None
            data1 = self.bot.get_vk_info(user_id)
            if data1 is None:
                self.bot.send_message(event.user_id, "Не удалось загрузить информацию о пользователе")
                self.bot.get_command("main").function([], event)
                return None
            name, _surname = data1
            img = get_user_image(user_id)
            if img is None:
                self.bot.save_image(user_id)
                img = get_user_image(user_id)
                if not img:
                    self.bot.send_message(event.user_id, "Не удалось найти изображение пользователя")
                    self.bot.get_command("main").function([], event)
                    return None
            data2 = get_for_people_info(user_id)
            if data2 is None:
                self.bot.send_message(event.user_id, "Не удалось найти информацию пользователе")
                self.bot.get_command("main").function([], event)
                return None
            text, fac, age, gender = data2
            # работает - не трогай, checked by rjkzavr at 1-100 yo
            if age is not None:
                yo = ("год" if age % 10 == 1 else "года") if (5 > age % 10 > 0) and age // 10 != 1 else "лет"
            else:
                yo = "лет"
            if "keyboard" in params:  # looking for
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("👎", VkKeyboardColor.PRIMARY, {"command": "reaction -1"})
                keyboard.add_button("🚨", VkKeyboardColor.SECONDARY, {"command": "reaction -2"})
                keyboard.add_button("👋", VkKeyboardColor.PRIMARY, {"command": "reaction 1"})
                keyboard.add_button("👀", VkKeyboardColor.PRIMARY, {"command": "reaction 0"})
                keyboard.add_line()
                keyboard.add_button("на главную", VkKeyboardColor.PRIMARY, {"command": "main"})
                if "moderator" in get_roles(event.user_id):
                    keyboard.add_button("БАН", VkKeyboardColor.NEGATIVE, {"command": f"ban {user_id}"})
                self.bot.send_message(event.user_id, f"{name}, {age} {yo}\n{fac}\nПол: {gender}\nО себе:\n{text}",
                                      attachment=img, keyboard=keyboard.get_keyboard())
            elif "keyboard2" in params:  # moderation
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("забанить", VkKeyboardColor.NEGATIVE, {"command": f"ban {user_id}"})
                keyboard.add_button("разбанить", VkKeyboardColor.POSITIVE, {"command": f"unban {user_id}"})
                keyboard.add_line()
                keyboard.add_button("на главную", VkKeyboardColor.PRIMARY, {"command": "main"})
                self.bot.send_message(event.user_id, f"{name}, {age} {yo}\n{fac}\nПол: {gender}\nО себе:\n{text}",
                                      attachment=img, keyboard=keyboard.get_keyboard())
            elif "keyboard3" in params:  # likes
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("👋", VkKeyboardColor.POSITIVE, {"command": f"accept 1"})
                keyboard.add_button("👎", VkKeyboardColor.NEGATIVE, {"command": f"accept 0"})
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


class LikesMeCommand(Command):
    def __init__(self, bot):
        super().__init__("likes_me", bot)

    def function(self, params, event):
        data = get_likes_me(event.user_id)
        if data:
            user_id, reaction_id = data
            set_page(event.user_id, f"likes_me {reaction_id}")
            self.bot.get_command("get_user").function([str(user_id), "keyboard3"], event)
            # self.bot.send_message(event.user_id, f"LikeID: {ID2}\n")
        else:
            self.bot.send_message(event.user_id, "Нет анкет ожидающих ответа")
            self.bot.get_command("looking_for_page").function([], event)


class AcceptCommand(Command):
    def __init__(self, bot):
        super().__init__("accept", bot)

    def function(self, params, event):
        if validation_int(self.bot, event, params) and validate_page_id(self.bot, event, "likes_me"):
            reaction_id = int(get_user_page(event.user_id).split()[1])
            reaction = int(params[0])
            data = get_like_vk_profiles(reaction_id, event.user_id)
            if data and reaction:  # like
                vk_id_1, vk_id_2 = data
                self.bot.send_message(vk_id_1, f"Пользователь @id{vk_id_2} принял вашу заявку")
                self.bot.send_message(vk_id_2, f"Пользователь @id{vk_id_1} принял вашу заявку")
                self.bot.get_command("likes_me").function([], event)
            elif data:  # dont like
                self.bot.get_command("likes_me").function([], event)
            else:
                self.bot.send_message(event.user_id, "Реакция не найдена")
                self.bot.get_command("looking_for_page").function([], event)


class ClearReactionStoryCommand(Command):
    def __init__(self, bot):
        super().__init__("clear_reaction_story", bot)

    def function(self, params, event):
        if clear_reaction_story(event.user_id):
            self.bot.mark_as_read(event)
        else:
            self.bot.send_message(event.user_id, "Не удалось отчистить историю сообщений")
