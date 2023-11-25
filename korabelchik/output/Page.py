from korabelchik.Exceptions import PageAccessDenied, PageMessageIsNone


class Page:
    def __init__(self, name, roles=None):
        if roles is None:
            roles = {"user"}
        self.__name = name
        self.__roles = roles
        self.__message = None
        self.__keyboard = None

    def render(self, bot, event, roles):
        if any(role in self.__roles for role in roles):
            if self.__keyboard:
                bot.send(event.user_id, self.__message(bot, event), self.__keyboard.get_keyboard(roles))
            else:
                bot.send(event.user_id, self.__message(bot, event), self.__keyboard)
        else:
            raise PageAccessDenied("Не хватает прав доступа для открытия страницы")

    # --- getters and setters ---

    def get_name(self):
        return self.__name

    def set_message(self, func):
        self.__message = func

    def set_keyboard(self, keyboard):
        self.__keyboard = keyboard
        self.__keyboard.check_page(self.get_name())

    # --- checkers ---

    def check(self):
        self.check_message()

    def check_message(self):
        if self.__message is None:
            raise PageMessageIsNone("Нет генератора сообщения")