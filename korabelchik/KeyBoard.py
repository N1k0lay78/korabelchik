from vk_api.keyboard import VkKeyboard

from korabelchik.input.NewLine import NewLine


class Keyboard:
    def __init__(self, name,  bot, one_time=True):
        self.__name = name
        self.one_time=one_time
        self.__elements = []
        self.bot = bot

    def __add__(self, other):
        keyboard = Keyboard(self.bot, self.one_time)

        for elem in self.get_elements():
            keyboard.add_element(elem)

        for elem in other.get_elements():
            keyboard.add_element(elem)

        return keyboard

    def remove_element(self, name):
        for elem in self.__elements:
            if elem.get_name == name:
                self.__elements.remove(elem)
                break

    def get_name(self):
        return self.__name

    def get_elements(self):
        return self.__elements

    def add_element(self, element):
        self.__elements.append(element)

    def check_page(self, page):
        for elem in self.__elements:
            elem.check(page)

    def get_keyboard(self, roles):
        keyboard = VkKeyboard(one_time=self.one_time)
        last_is_new_line = True
        for elem in self.__elements:
            if type(elem) == NewLine and last_is_new_line:
                pass
            else:
                elem.add_element(keyboard, roles)
            last_is_new_line = type(elem) == NewLine
        self.check_keyboard(keyboard)  # TODO
        return keyboard.get_keyboard()

    # --- checkers ---

    def check_keyboard(self, keyboard):
        # TODO проверка что нету больше 4х кнопок в одном ряду
        # нету 4х Button подряд
        # raise KeyboardLineError("больше 4х кнопок в одном ряду")
        pass
