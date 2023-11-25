from config import db_path, token
from korabelchik.Bot import Korabelchik
from korabelchik.KeyBoard import Keyboard
from korabelchik.input.Button import Button
from korabelchik.output.Page import Page

bot = Korabelchik(token, db_path)

btn_1 = Button("aloha", "aloha")


def aloha_button(event, bot, page):
    bot.set_page(event, "hello")


btn_1.page("aloha", aloha_button)
btn_1.page("main", aloha_button)

btn_2 = Button("hello", "hello")


def hello_button(event, bot, page):
    bot.set_page(event, "aloha")


btn_2.page("hello", hello_button)
btn_2.page("main", hello_button)

bot.add_button(btn_1)
bot.add_button(btn_2)

kb_1 = Keyboard("aloha", bot)
kb_1.add_element(btn_1)
kb_2 = Keyboard("hello", bot)
kb_2.add_element(btn_2)

bot.add_keyboard(kb_1)
bot.add_keyboard(kb_2)

pg_1 = Page("aloha")
pg_1.set_message(lambda bot, event: "Aloha amigo")
pg_1.set_keyboard(kb_1)
pg_2 = Page("hello")
pg_2.set_message(lambda bot, event: "Hello my friend")
pg_2.set_keyboard(kb_2)

bot.add_page(pg_1)
bot.add_page(pg_2)

btn_3 = Button("main", "go to hello")


def go_to_hello_button(event, bot, page):
    bot.set_page(event, "hello")


btn_3.page("main", go_to_hello_button)

kb_3 = kb_1 + kb_2

pg_3 = Page("main")
pg_3.set_message(lambda bot, event: "go to hello")
pg_3.set_keyboard(kb_3)

bot.add_button(btn_3)
bot.add_keyboard(kb_3)
bot.add_page(pg_3)

bot.run()