import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import token, db_path
from controller.user import get_user_page, set_page, set_user_gender, set_user_age, set_user_faculty
from data import db_session
from korabelchik.Exceptions import ButtonNameIntersection, ButtonNameNotFound, KeyboardNameIntersection, \
    KeyboardNameNotFound, ButtonAccessDenied, PageNameNotFound, PageNameIntersection, PageAccessDenied, \
    TextInputPageIntersection
from korabelchik.input.NewLine import NewLine
from tools import get_command


class Korabelchik:
    def __init__(self, token, db_path):
        self.token = token
        self.db_path = db_path
        vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

        self.buttons = {}
        self.text_inputs = {}
        self.new_line = NewLine()
        self.keyboards = {}

        self.pages = {}
        # TODO
        # self.commands = {}

    def send(self, user_id, message, keyboard):
        if keyboard is not None:
            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=get_random_id(),
                keyboard=keyboard
            )
        else:
            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=get_random_id()
            )

    def send_message(self, event, message, **kwargs):
        self.vk.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=get_random_id(),
            **kwargs
        )

    def run(self):
        db_session.global_init(self.db_path)
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                page, roles, button_name, text = self.get_info_for_logic(event)
                if button_name:
                    try:
                        self.get_button(button_name).update(self, event, page, roles)
                    except ButtonAccessDenied as e:
                        # debug
                        print(e)
                    except Exception as e:
                        # exception
                        print(e)
                else:
                    text = text.strip()
                    if text.startswith("/"):
                        # TODO: commands
                        pass
                    else:
                        try:
                            self.get_text_input(page).update(self, event, page, roles)
                        except AttributeError:
                            print("Нету обработчика")

                while True:
                    page, roles = self.get_info_for_view(event)
                    try:
                        self.get_page(page).render(self, event, roles)
                        break
                    except PageAccessDenied:
                        # debug
                        # print(e)
                        self.set_page(event, "main")
                        print("CHANGE PAGE AT MAIN", self.get_user_page(event))
                    except PageNameNotFound:
                        # debug
                        # print(e)
                        self.set_page(event, "main")
                        print("CHANGE PAGE AT MAIN", self.get_user_page(event))
                    # except Exception as e:
                    #     # exception
                    #     print(e)
                    #     break

    # --- getters and setters ---

    def set_age(self, event, age):
        set_user_age(event.user_id, age)

    def set_gender(self, event, male):
        set_user_gender(event.user_id, male)

    def set_faculty(self, event):
        set_user_faculty(event.user_id, get_command(event))

    def set_page(self, event, page):
        set_page(event.user_id, page)

    def get_info_for_view(self, event):
        return (
            self.get_user_page(event),
            self.get_user_roles(event),
        )

    def get_info_for_logic(self, event):
        return (
            self.get_user_page(event),
            self.get_user_roles(event),
            self.get_command(event),
            self.get_text(event),
        )

    def get_user_page(self, event):
        return get_user_page(event.user_id)

    def get_user_roles(self, event):
        # TODO: получение ролей из БД
        return {"user"}

    def get_text(self, event):
        return event.message

    def is_button_pressed(self, event):
        """
        Возвращает:
        True - если нажали кнопку
        False - если отправили сообщение
        """

        return "payload" in event.extra_values and "command" in event.extra_values["payload"]

    def get_command(self, event):
        """
        Возвращает какую кнопку нажали
        """

        if self.is_button_pressed(event):
            return event.extra_values["payload"][12:-2]
        else:
            return ""

    def add_page(self, page):
        if page.get_name() in self.pages:
            raise PageNameIntersection("Страница с таким названием уже существует")
        else:
            self.pages[page.get_name()] = page

    def get_page(self, name):
        if name in self.pages:
            return self.pages[name]
        else:
            raise PageNameNotFound("Нет страницы с таким названием")

    def add_text_input(self, text_input):
        for page in text_input.get_pages():
            if page in self.text_inputs:
                raise TextInputPageIntersection("Для этой страницы уже задано текстовое поле")
            else:
                self.text_inputs[page] = text_input

    def get_text_input(self, page):
        print(page, self.text_inputs)
        if page in self.text_inputs:
            return self.text_inputs[page]

    def add_button(self, button):
        if button.get_name() in self.buttons:
            raise ButtonNameIntersection("Кнопка с таким названием уже существует")
        else:
            self.buttons[button.get_name()] = button

    def get_button(self, name):
        if name in self.buttons:
            return self.buttons[name]
        else:
            raise ButtonNameNotFound("Нет кнопки с таким названием")

    def add_keyboard(self, keyboard):
        if keyboard.get_name() in self.keyboards:
            raise KeyboardNameIntersection("Клавиатура с таким названием уже существует")
        else:
            self.keyboards[keyboard.get_name()] = keyboard

    def get_keyboard(self, name):
        if name in self.keyboards:
            return self.keyboards[name]
        else:
            raise KeyboardNameNotFound("Нет клавиатуры с таким названием")
