import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from controller.user import get_user_page, set_page
from data import db_session


class KorabelchikPage:
    def __init__(self, logic, view):
        self.logic = logic
        self.view = view
        self.bot = None

    def is_ready_page(self):
        return self.logic is not None and self.view is not None

    def set_bot(self, bot):
        self.bot = bot

    def logic_page(self, event):
        self.logic(event, self.bot)

    def view_page(self, event):
        message, keyboard = self.view(event, self.bot)
        self.bot.send(event, message, keyboard)


class KorabelchikCommand:
    def __init__(self):
        self.logic = None
        self.bot = None

    def is_ready_page(self):
        return self.logic is not None

    def set_bot(self, bot):
        self.bot = bot


def generate_keyboard(buttons):
    keyboard = VkKeyboard()
    for button_line in buttons:
        for button in button_line:
            print("ADD button")
            keyboard.add_button(button[0], button[1], {"command": button[2]})
        if button_line != buttons[-1]:
            print("ADD line")
            keyboard.add_line()
    return keyboard


class Korabelchik:
    def __init__(self, token):
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()
        # для новых сообщений
        # self.pages[<page>] -> [<roles:set>, <logic:KorabelchikPage>]
        self.pages = {}
        # self.commands[<command>] -> [<roles:set>, <logic:KorabelchikCommand>]
        self.commands = {}

        # info
        """
        user - обычный пользователь
        admin - админ (пока хз что будет делать)
        smm - может написать пост
        smm leader - может отправить пост пользователям
        owner - может управлять ролями
        """
        self.all_roles = {"user", "admin", "smm", "smm leader", "owner"}

    def send(self, event, message, keyboard=None):
        print("SEND PAGE")
        if keyboard is not None:
            self.vk.messages.send(
                user_id=event.user_id,
                message=message,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )

    def add_page(self, name, page, roles={"user"}):
        self.check_page_name(name)
        self.check_roles(roles)
        self.check_page(page)
        self.pages[name] = [set(roles), page]
        page.set_bot(self)

    def add_command(self, name, command, roles={"user"}):
        self.check_command_name(name)
        self.check_roles(roles)
        self.check_command(command)
        self.commands[name] = [set(roles), command]
        command.set_bot(self)

    def get_page(self, name, roles):
        if name not in self.pages:
            raise KeyError(f"Страница {name} не существует")
        page = self.pages[name]
        if not any(role in page[0] for role in roles):
            raise KeyError(f"Отказано в доступе к странице {name}")
        return page[1]

    def get_command(self, name, roles):
        if name not in self.commands:
            raise KeyError(f"Команда {name} не существует")
        command = self.commands[name]
        if not any(role in command[0] for role in roles):
            raise KeyError(f"Отказано в доступе к команде {name}")
        return command[1]

    def run(self):
        db_session.global_init("../../db/korabelchik_bu4.sqlite")
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                # TODO: commands

                page = get_user_page(event.user_id)
                try:
                    self.get_page(page, {"user"}).logic_page(event)
                except KeyError as e:
                    # debug
                    print(e)
                except Exception as e:
                    # exception
                    print(e)

                while True:
                    page = get_user_page(event.user_id)
                    try:
                        self.get_page(page, {"user"}).view_page(event)
                        break
                    except KeyError as e:
                        # debug
                        print(e)
                        set_page(event.user_id, "main")
                        print("CHANGE PAGE AT MAIN", get_user_page(event.user_id))
                    except Exception as e:
                        # exception
                        print(e)

    # --- checkers ---
    def check_name(self, name):
        if type(name) != str:
            raise TypeError("Название страницы может быть только строкой")
        if not name.replace("_", "").isalpha():
            raise KeyError("Название страницы может содержать только буквы и символ нижнего подчёркивания")

    def check_page_name(self, name):
        self.check_name(name)
        if name in self.pages:
            raise KeyError("Такая страница уже существует")

    def check_command_name(self, name):
        self.check_name(name)
        if name in self.commands:
            raise KeyError("Такая команда уже существует")

    def check_roles(self, roles):
        if type(roles) not in [list, set, tuple]:
            raise TypeError("Роли должны быть в виде списка")
        for role in roles:
            if role not in self.all_roles:
                raise KeyError(f"Роль '{role}' не существует")

    def check_page(self, page):
        if type(page) != KorabelchikPage:
            raise TypeError("Неправильный тип страницы")
        if not page.is_ready_page():
            raise TypeError("Страница не готова к использованию, не хватает логики или интерфейса")

    def check_command(self, command):
        if type(command) != KorabelchikCommand:
            raise TypeError("Неправильный тип команды")
        if not command.is_ready_page():
            raise TypeError("Команда не готова к использованию, не хватает логики")
