from vk_api.keyboard import VkKeyboardColor

from korabelchik.Exceptions import ButtonLengthError, ButtonFuncError, ButtonPageIntersection, ButtonUnknownColor, \
    ButtonAccessDenied, TextInputFuncError, TextInputPageError, TextInputAccessDenied


class TextInput:
    def __init__(self, pages, func, roles=None, role_error=True):
        if roles is None:
            roles = {"user"}
        self.pages = pages
        self.func = func
        self.roles = roles
        self.role_error = role_error

    def update(self, bot, event, page, roles):
        if any(role in self.roles for role in roles):
            self.func(event, bot, page)
        elif self.role_error:
            raise TextInputAccessDenied("Не хватает прав доступа для выполнения логики текстового поля")

    # --- getters and setters ---

    def get_pages(self):
        return self.pages

    # --- checkers ---

    def check(self, page=None):
        self.check_funcs(page)

    def check_funcs(self, page):
        if page is not None and  page != self.page:
            raise TextInputPageError(f"Нет обработчика событий для страницы {page}")
        if not self.func:
            raise TextInputFuncError("Нет обработчиков событий")


if __name__ == '__main__':
    pass
