from korabelchik.KeyBoard import Keyboard
from korabelchik.input.Button import Button
from korabelchik.input.NewLine import NewLine
from korabelchik.input.TextInput import TextInput
from smtu_info import faculty_short

new_line = NewLine()

# --- start ---
void_func = lambda event, bot, page: 0

btn_start = Button("start", "Начать")
btn_start.page("", void_func)

kb_start = Keyboard("start")
kb_start.add_element(btn_start)

# ----- EDIT -----
go_to_edit = lambda event, bot, page: bot.set_page(event, "edit")

btn_go_to_edit = Button("go to edit", "Назад")
btn_go_to_edit.page("", go_to_edit)

kb_go_to_edit = Keyboard("go to edit")
kb_go_to_edit.add_element(btn_go_to_edit)

# --- age ---
def set_age(event, bot, page):
    text = event.text
    # получаем первое число из строки
    age = int([subline for subline in text.split() if subline.isdigit()][0])
    # проверяем валидность возраста
    if 16 < age < 80:
        bot.set_age(event, age)
        # если задаём возраст в первый раз переходи на страницу задания пола
        if page == "age":
            bot.set_page(event, "male")


ti_age = TextInput("age", set_age)

# --- male ---
set_male = lambda event, bot, page: bot.set_gender(event, "male")
set_female = lambda event, bot, page: bot.set_gender(event, "female")

btn_male = Button("male", "мужской")
btn_male.page("", set_male)

btn_female = Button("female", "женский")
btn_female.page("", set_female)

kb_male = Keyboard("male")
kb_male.add_element(btn_male)
kb_male.add_element(btn_female)

# --- faculty ---
set_faculty = lambda event, bot, page: bot.set_faculty(event)

btns_faculty = []
kb_faculty = Keyboard("faculty")
for i, fac_en, fac_ru in enumerate(faculty_short.items()):
    btn = Button(fac_en, fac_ru)
    btn.page("faculty", set_faculty)
    btn.page("edit faculty", set_faculty)
    if i % 4 == 0 and i != 0:
        kb_faculty.add_element(new_line)
    kb_faculty.add_element(btn)
    btns_faculty.append(btn)

# TODO: сделать добавление кнопки назад для страницы редактирования

# --- for friends ---
# не обязательно, указывается перед поиском друзей, если не задано
def set_for_friends(event, bot, page):
    text = event.text
    text = text.replace("SELECT", "").replace("FROM", "").replace("WHERE", "").replace("GROUP BY", "").replace("HAVING", "")\
        .replace("ORDER BY", "")
    # проверяем валидность текста
    if len(text) < 250:
        bot.set_for_friends(event, text)
        # если задаём возраст в первый раз переходи на страницу поиска друзей
        # TODO: выбор пола пользователя которого мы ищем
        if page == "for friends":
            bot.set_page(event, "looking for friends")
        else:
            go_to_edit(event, bot, page)


ti_for_friends = TextInput("age", set_for_friends)

# --- for interests ---
# не обязательно, указывается перед поиском по интересам, если не задано
def set_for_interests(event, bot, page):
    text = event.text
    text = text.replace("SELECT", "").replace("FROM", "").replace("WHERE", "").replace("GROUP BY", "").replace("HAVING", "")\
        .replace("ORDER BY", "")
    # проверяем валидность текста
    if len(text) < 250:
        bot.set_for_interests(event, text)
        # если задаём возраст в первый раз переходи на страницу поиска друзей
        # TODO: выбор пола пользователя которого мы ищем
        if page == "for interests":
            bot.set_page(event, "looking for interests")
        else:
            go_to_edit(event, bot, page)


ti_for_interests = TextInput("age", set_for_interests)

# --- main ---
# TODO: сделать кнопку для модерации


# --- settings ---


# --- edit ---


# --- looking for friends ---


# --- looking for interests ---
