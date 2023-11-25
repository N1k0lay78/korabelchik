from vk_api.keyboard import VkKeyboardColor

from config import token
from controller.user import set_page
from test import Korabelchik, KorabelchikPage, generate_keyboard
from tools import get_command

korabel = Korabelchik(token)


def logic(event, bot):
    if get_command(event) == "hello":
        print("OPEN SETTINGS")
        set_page(event.user_id, "settings")


def view(event, bot):
    keyboard = [
        [("Привет Привет Привет Привет Привет Привет Привет", VkKeyboardColor.SECONDARY, "hello")]
    ]
    return "Привет пользователь!", generate_keyboard(keyboard)


hello_page = KorabelchikPage(logic, view)

korabel.add_page("age", hello_page)
korabel.add_page("main", hello_page)

korabel.run()
