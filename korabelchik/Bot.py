import vk_api
from requests import ReadTimeout
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload

from config import token, db_path
from controller.user import get_user_page, set_page, set_user_gender, set_user_age, set_user_faculty, get_roles, \
    user_is_ready_for_looking_for_people, set_for_people, \
    get_for_people_info, get_random_for_people
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
        self.commands = {}
        self.pages = {}

        self.upload = vk_api.VkUpload(self.vk)
        # TODO
        # self.commands = {}

    def send_for_people(self, to_user_id, about_user_id):
        img, name, _surname = self.get_info_for_looking(about_user_id)
        text, fac, age, gender = self.get_for_people_info(about_user_id)
        # работает - не трогай, checked by rjkzavr at 1-100 yo
        yo = ("год" if age % 10 == 1 else "года") if (5 > age % 10 > 0) and age // 10 != 1 else "лет"
        self.send_full(to_user_id, None,
                      {"message": f"{name}, {age} {yo}\n{fac}\nПол: {gender}\n\nО себе:\n{text}", "attachment": img})

    def send_full(self, user_id, keyboard, kwargs):
        if keyboard is not None:
            self.vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                keyboard=keyboard,
                **kwargs
            )
        else:
            self.vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                **kwargs
            )

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
        try:
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
                            try:
                                self.get_commandd(text[1:].split()[0]).update(self, event, page, roles)
                            except AttributeError:
                                print("Команда не существует")
                            except Exception as e:
                                # exception
                                print(e)
                        else:
                            try:
                                self.get_text_input(page).update(self, event, page, roles)
                            except AttributeError:
                                print("Нет обработчика")
                            except Exception as e:
                                # exception
                                print(e)
    
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
                            print(f"CHANGE PAGE FROM '{page}' AT MAIN", self.get_user_page(event))
                        # except Exception as e:
                        #     # exception
                        #     print(e)
                        #     break
        except ReadTimeout:
            pass

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
        return get_roles(event.user_id)

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
        if page in self.text_inputs:
            return self.text_inputs[page]

    def add_command(self, command):
        if command.pref in self.commands:
            raise AttributeError("Такая команда уже существует")
        else:
            self.commands[command.pref] = command

    def get_commandd(self, name):
        if name in self.commands:
            return self.commands[name]

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

    def user_is_ready_for_looking_for_people(self, event):
        return user_is_ready_for_looking_for_people(event.user_id)

    # def user_is_ready_for_looking_for_interests(self, event):
    #     return user_is_ready_for_looking_for_interests(event.user_id)

    def get_random_for_people(self, event):
        return get_random_for_people(event.user_id)

    # def get_random_for_interests(self, event):
    #     return get_random_for_interests(event.user_id)

    def set_for_people(self, event, text):
        set_for_people(event.user_id, text)

    # def set_for_interests(self, event, text):
    #     set_for_interests(event.user_id, text)

    def get_gender_api(self, event):
        data = self.vk.users.get(user_id=event.user_id, fields="sex")[0]
        if data["sex"] == 2:
            return "male"
        else:
            return "female"

    def get_for_people_info(self, user_id):
        return get_for_people_info(user_id)

    """def get_for_interests_info(self, user_id):
        return get_for_interests_info(user_id)"""

    def get_info_for_looking(self, user_id):
        data = self.vk.users.get(user_id=user_id, fields="crop_photo")[0]
        print(data)
        # upload_image  = self.upload.photo_messages("C:/2023/Bot/korabelchik/Chess Game.png")
        # return 'photo{}_{}'.format(upload_image['owner_id'], upload_image['id']), data["first_name"], data["last_name"]
        return data['crop_photo']["photo"]["sizes"][-1]["url"], data["first_name"], data["last_name"]
        # return data['photo_200'], data["first_name"], data["last_name"]
        # print(self.vk.photos.get(owner_id=-1, album_id="profile"))