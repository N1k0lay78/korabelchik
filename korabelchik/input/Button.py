from vk_api.keyboard import VkKeyboardColor

from korabelchik.Exceptions import ButtonLengthError, ButtonFuncError, ButtonPageIntersection, ButtonUnknownColor, \
    ButtonAccessDenied


class Button:
    def __init__(self, name, text, color="grey", roles=None, role_error=True):
        if roles is None:
            roles = {"user"}
        self.name = name
        self.text = text
        self.color = None
        self.roles = roles
        self.role_error = role_error
        self.funcs = {}
        self.set_color(color)

    def page(self, page, func):
        if page in self.funcs:
            raise ButtonPageIntersection("Такая страница уже обрабатывается")
        self.funcs[page] = func

    def update(self, bot, event, page, roles):
        if any(role in self.roles for role in roles):
            if page in self.funcs:
                self.funcs[page](event, bot, page)
            else:
                self.funcs[""](event, bot, page)
        elif self.role_error:
            raise ButtonAccessDenied("Не хватает прав доступа для выполнения логики кнопки")

    def add_element(self, keyboard, roles):
        if any(role in self.roles for role in roles):
            keyboard.add_button(self.text, self.color, {"command": self.name})
        elif self.role_error:
            raise ButtonAccessDenied("Не хватает прав доступа для добавления кнопки")

    # --- getters and setters ---

    def get_name(self):
        return self.name

    def set_color(self, color):
        colors = {
            "grey": VkKeyboardColor.SECONDARY,
            "blue": VkKeyboardColor.PRIMARY,
            "green": VkKeyboardColor.POSITIVE,
            "red": VkKeyboardColor.NEGATIVE,
        }
        if color not in colors:
            raise ButtonUnknownColor(f"Неизвестный цвет {color}")
        self.color = colors[color]

    # --- checkers ---

    def check(self, page=None):
        self.check_text()
        self.check_funcs(page)

    def check_text(self):
        if len(self.text) > 40:
            # print(self.text)
            raise ButtonLengthError("Текст кнопки больше 40 символов")

    def check_funcs(self, page):
        if page is not None and page not in self.funcs and "" not in page:
            raise ButtonFuncError(f"Нет обработчика событий для страницы {page}")
        if not self.funcs:
            raise ButtonFuncError("Нет обработчиков событий")


if __name__ == '__main__':
    btn = Button("start", "HELLO")

    def hello(event, bot, page):
        return f"Change page from '{page}' to 'main'"

    btn.page("main", hello)
