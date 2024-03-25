import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import command_prefix
from controller.user import get_user_page, get_roles
from data import db_session

import requests
from requests import ReadTimeout

from korabelchik2.Command import Command


class Bot:
    def __init__(self, token, db_path):
        # VK bot init
        vk_session = vk_api.VkApi(token=token)
        self.__long_poll = VkLongPoll(vk_session)
        self.__vk = vk_session.get_api()

        # database init
        db_session.global_init(db_path)

        # VK bot for image
        self.__session = requests.Session()
        self.__upload = vk_api.VkUpload(self.__vk)

        # commands
        self.__commands = []

    # --- run ---
    def run(self):
        try:
            for event in self.__long_poll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    # check command
                    if event.message.startswith(command_prefix) or self.is_button_pressed(event):
                        self.run_command(event)
                    # check message
                    # return page
        except ReadTimeout:
            self.run()

    # --- commands ---
    def add_command(self, command):
        if issubclass(type(command), Command):
            self.__commands.append(command)
        else:
            raise TypeError(f"Тип команды не является наследником Command")

    def get_command(self, name):
        for command in self.__commands:
            if command.get_name() == name:
                return command
        return None

    def run_command(self, event):
        for command in self.__commands:
            if command.is_command(event):
                command.run_command(event)

    # --- buttons ---
    def is_button_pressed(self, event):
        return "payload" in event.extra_values and "command" in event.extra_values["payload"]

    # --- user data ---
    @staticmethod
    def get_page(user_id):
        return get_user_page(user_id)

    @staticmethod
    def get_roles(user_id):
        return get_roles(user_id)

    def get_vk_info(self, user_id):
        data = self.__vk.users.get(user_id=user_id, fields="crop_photo")
        if data:
            data = data[0]
            return data['crop_photo']["photo"]["sizes"][-1]["url"], data["first_name"], data["last_name"]
        return None

    # --- send ---
    def __send(self, user_id, data):
        data["random_id"] = get_random_id()
        # отправка фотографии
        if "attachment" in data:
            image = self.__session.get(data["attachment"], stream=True)
            photo = self.__upload.photo_messages(photos=image.raw)[0]
            data["attachment"] = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
        self.__vk.messages.send(user_id=user_id, **data)

    def send_message(self, user_id, message, **kwargs):
        kwargs["message"] = message
        self.__send(user_id, kwargs)

    def mark_as_read(self, event):
        self.__vk.messages.markAsRead(user_id=event.user_id, mark_conversation_as_read=True)
