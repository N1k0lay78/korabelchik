import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor

from config import token
from controller.user import is_user_authenticated, signin_user, get_user_page, set_user_age, set_user_gender, \
    set_user_faculty, set_page
from data import db_session
from tools import is_button_pressed, get_command

db_session.global_init("db/korabelchik.sqlite")

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

print("start")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        page = get_user_page(event.user_id)
        if get_command(event) == "start":
            pass
        if page == "age" and is_button_pressed(event) and get_command(event).isdigit():
            set_user_age(event.user_id, get_command(event))
        elif page == "male" and is_button_pressed(event):
            set_user_gender(event.user_id, get_command(event))
        elif page == "faculty" and is_button_pressed(event):
            set_user_faculty(event.user_id, get_command(event))
        elif page == "main" and is_button_pressed(event):
            if get_command(event) == "settings":
                set_page(event.user_id, "settings")
        elif page == "settings" and is_button_pressed(event):
            if get_command(event) == "main":
                set_page(event.user_id, "main")
            elif get_command(event) == "edit profile":
                set_page(event.user_id, "edit profile")
        elif page == "edit profile" and is_button_pressed(event):
            if get_command(event) == "main":
                set_page(event.user_id, "main")

        page = get_user_page(event.user_id)
        print(page, page == "settings")
        if page == "age":
            #TODO: сделать ввод через сообщение
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("17 лет", VkKeyboardColor.SECONDARY, {"command": "17"})
            keyboard.add_button("18 лет", VkKeyboardColor.SECONDARY, {"command": "18"})
            keyboard.add_button("19 лет", VkKeyboardColor.SECONDARY, {"command": "19"})
            keyboard.add_button("20 лет", VkKeyboardColor.SECONDARY, {"command": "20"})
            keyboard.add_line()
            keyboard.add_button("21 год", VkKeyboardColor.SECONDARY, {"command": "21"})
            keyboard.add_button("22 года", VkKeyboardColor.SECONDARY, {"command": "22"})
            keyboard.add_button("23 года", VkKeyboardColor.SECONDARY, {"command": "23"})
            keyboard.add_button("24 года", VkKeyboardColor.SECONDARY, {"command": "24"})
            keyboard.add_line()
            keyboard.add_button("25 лет", VkKeyboardColor.SECONDARY, {"command": "25"})
            keyboard.add_button("26 лет", VkKeyboardColor.SECONDARY, {"command": "26"})
            keyboard.add_button("27 лет", VkKeyboardColor.SECONDARY, {"command": "27"})
            keyboard.add_button("28 лет", VkKeyboardColor.SECONDARY, {"command": "28"})
            keyboard.add_line()
            keyboard.add_button("29 лет", VkKeyboardColor.SECONDARY, {"command": "29"})
            keyboard.add_button("30 лет", VkKeyboardColor.SECONDARY, {"command": "30"})
            keyboard.add_button("31 год", VkKeyboardColor.SECONDARY, {"command": "31"})
            keyboard.add_button("32 года", VkKeyboardColor.SECONDARY, {"command": "32"})
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Сколько вам лет?',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        elif page == "male":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("мужской", VkKeyboardColor.SECONDARY, {"command": "male"})  # Факультет цифровых промышленных технологий
            keyboard.add_button("женский", VkKeyboardColor.SECONDARY, {"command": "female"})
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Какой пол?',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        elif page == "faculty":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("ФЦПТ", VkKeyboardColor.SECONDARY, {"command": "fcpt"})
            keyboard.add_button("ФМП", VkKeyboardColor.SECONDARY, {"command": "fmp"})
            keyboard.add_button("ФКиО", VkKeyboardColor.SECONDARY, {"command": "fkio"})
            keyboard.add_button("ФКЭиА", VkKeyboardColor.SECONDARY, {"command": "fkeia"})  # Факультет корабельной энергетики и автоматики
            keyboard.add_line()
            keyboard.add_button("ФЕНГО", VkKeyboardColor.SECONDARY, {"command": "feigo"})  # Факультет естественнонаучного и гуманитарного образования
            keyboard.add_button("ИЭФ", VkKeyboardColor.SECONDARY, {"command": "ief"})  # Инженерно-экономический факультет
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Какой факультет?',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        elif page == "main":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Подобрать пару", VkKeyboardColor.PRIMARY, {"command": "search"})
            keyboard.add_line()
            keyboard.add_button("Настройки", VkKeyboardColor.SECONDARY, {"command": "settings"})
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Меню',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        elif page == "settings":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("На главную", VkKeyboardColor.PRIMARY, {"command": "main"})
            keyboard.add_line()
            keyboard.add_button("Просмотреть мою анкету", VkKeyboardColor.POSITIVE, {"command": "view my form"})
            keyboard.add_line()
            keyboard.add_button("Изменить мои данные", VkKeyboardColor.SECONDARY, {"command": "edit profile"})
            keyboard.add_line()
            keyboard.add_button("Отключить мою анкету", VkKeyboardColor.NEGATIVE, {"command": "close my form"})
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Настройки',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        elif page == "edit profile":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("На главную", VkKeyboardColor.PRIMARY, {"command": "main"})
            keyboard.add_line()
            keyboard.add_button("Изменить возраст", VkKeyboardColor.SECONDARY, {"command": "edit my age"})
            keyboard.add_line()
            keyboard.add_button("Изменить пол", VkKeyboardColor.SECONDARY, {"command": "edit my gender"})
            keyboard.add_line()
            keyboard.add_button("Изменить факультет", VkKeyboardColor.SECONDARY, {"command": "edit my faculty"})
            keyboard.add_line()
            keyboard.add_button("Изменить курс", VkKeyboardColor.SECONDARY, {"command": "edit my course"})
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Изменить профиль',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )




        """if is_button_pressed(event):
            print(event.user_id)
            print(f"user now auth is {is_user_authenticated(event.user_id)}")
            signin_user(event.user_id)
            print(f"command: '{get_command(event)}'")
        elif event.text:
            print(f"message: '{event.text}'")
            if event.text.lower() == 'первый вариант фразы' or event.text == 'Второй вариант фразы':  # Если написали заданную фразу
                if event.from_user:  # Если написали в ЛС
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        message='Ваш текст 1',
                        random_id=get_random_id()
                    )
                elif event.from_chat:  # Если написали в Беседе
                    vk.messages.send(  # Отправляем собщение
                        chat_id=event.chat_id,
                        message='Ваш текст 2',
                        random_id=get_random_id()
                    )"""
