from vk_api.keyboard import VkKeyboardColor
from korabelchik.Exceptions import ButtonLengthError, ButtonFuncError, ButtonPageIntersection, ButtonUnknownColor, \
    ButtonAccessDenied, TextInputFuncError, TextInputPageError, TextInputAccessDenied


class Command:
    def __init__(self, pref, func, roles=None):
        if roles is None:
            roles = {"user"}
        self.pref = pref
        self.func = func
        self.roles = roles

    def update(self, bot, event, page, roles):
        if any(role in self.roles for role in roles):
            self.func(event, bot, page)


if __name__ == '__main__':
    pass
