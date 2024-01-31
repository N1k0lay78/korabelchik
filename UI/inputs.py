from korabelchik.KeyBoard import Keyboard
from korabelchik.input.Button import Button
from korabelchik.input.NewLine import NewLine
from korabelchik.input.TextInput import TextInput
from smtu_info import faculty_short, get_faculties
from tools import get_command

new_line = NewLine()


# --- start ---
def add_start_button(bot):
    void_func = lambda event, bot, page: bot.send_message(event, "Привет, я бот Тестовичок!\nЯ создан, чтобы помогать "
                                                                 "студентам)\n*Сейчас я работаю в отладочном режиме, "
                                                                 "ваша информация может быть просмотрена!")

    btn_start = Button("start", "Начать")
    btn_start.page("", void_func)

    bot.add_button(btn_start)


# ----- SOME -----
go_to_main = lambda event, bot, page: bot.set_page(event, "main")
go_to_edit = lambda event, bot, page: bot.set_page(event, "edit")
go_to_profile = lambda event, bot, page: bot.set_page(event, "profile")


def add_some(bot):
    """go_to_edit = lambda event, bot, page: bot.set_page(event, "edit")

    btn_go_to_edit = Button("go to edit", "Назад")
    btn_go_to_edit.page("", go_to_edit)

    bot.add_button(btn_go_to_edit)"""

    # main
    kb_go_to_main = Keyboard("go to main", bot)

    btn_go_to_main = Button("go to main", "На главную", color="blue")
    btn_go_to_main.page("", go_to_main)

    bot.add_button(btn_go_to_main)
    kb_go_to_main.add_element(btn_go_to_main)

    bot.add_keyboard(kb_go_to_main)

    # edit
    kb_go_to_edit = Keyboard("go to edit", bot)

    btn_go_to_edit = Button("go to edit", "Редактирование", color="blue")
    btn_go_to_edit.page("", go_to_edit)

    bot.add_button(btn_go_to_edit)
    kb_go_to_edit.add_element(btn_go_to_edit)

    bot.add_keyboard(kb_go_to_edit)

    # profile
    btn_profile = Button("profile", "Профиль", color="blue")
    btn_profile.page("", go_to_profile)

    bot.add_button(btn_profile)


# --- age ---
def add_age_text_input(bot):
    def set_age(event, bot, page):
        text = event.text
        # получаем первое число из строки
        res = [subline for subline in text.split() if subline.isdigit()]
        # проверяем валидность возраста
        if res and 15 < int(res[0]) < 100:
            bot.set_age(event, int(res[0]))
            # если задаём возраст в первый раз переходи на страницу задания пола
            print(page)
            if page == "age":
                bot.set_page(event, "gender")
            else:
                go_to_edit(event, bot, page)
        else:
            bot.send_message(event, f"Мне не удалось считать ваш возраст :(")

    ti_age = TextInput({"age", "edit age"}, set_age)

    bot.add_text_input(ti_age)


# --- male ---
def add_gender_keyboard(bot):
    def set_gender(event, bot, page):
        gender = get_command(event)
        if gender in ["male", "female"]:
            bot.set_gender(event, gender)
        if page == "gender":
            bot.set_page(event, "faculty")
        else:
            go_to_edit(event, bot, page)

    btn_male = Button("male", "мужской")
    btn_male.page("", set_gender)

    bot.add_button(btn_male)

    btn_female = Button("female", "женский")
    btn_female.page("", set_gender)

    bot.add_button(btn_female)

    kb_gender = Keyboard("gender", bot)
    kb_gender.add_element(btn_male)
    kb_gender.add_element(btn_female)

    kb_edit_gender = Keyboard("edit gender", bot)
    kb_edit_gender.add_element(btn_male)
    kb_edit_gender.add_element(btn_female)
    kb_edit_gender.add_element(new_line)
    kb_edit_gender.add_element(bot.get_button("go to edit"))

    bot.add_keyboard(kb_gender)
    bot.add_keyboard(kb_edit_gender)


# --- faculty ---
def add_faculty_keyboard(bot):
    def set_faculty(event, bot, page):
        bot.set_faculty(event)
        if page == "faculty":
            go_to_main(event, bot, page)
        else:
            go_to_edit(event, bot, page)

    btns_faculty = []
    kb_faculty = Keyboard("faculty", bot)
    kb_edit_faculty = Keyboard("edit faculty", bot)

    for i, fac in enumerate(faculty_short.items()):
        fac_en, fac_ru = fac
        btn = Button(fac_en, fac_ru)
        btn.page("faculty", set_faculty)
        btn.page("edit faculty", set_faculty)

        bot.add_button(btn)

        if i % 4 == 0 and i != 0:
            kb_faculty.add_element(new_line)
            kb_edit_faculty.add_element(new_line)
        kb_faculty.add_element(btn)
        kb_edit_faculty.add_element(btn)
        btns_faculty.append(btn)

    kb_edit_faculty.add_element(new_line)
    kb_edit_faculty.add_element(bot.get_button("go to edit"))

    bot.add_keyboard(kb_faculty)
    bot.add_keyboard(kb_edit_faculty)


"""
# --- for friends ---
# не обязательное поле. Указывается перед поиском друзей, если не задано
def add_for_friends_text_input(bot):
    def set_for_friends(event, bot, page):
        text = event.text
        # проверяем валидность текста
        text = text.replace("SELECT", "").replace("FROM", "").replace("WHERE", "").replace("GROUP BY", "").replace("HAVING", "") \
            .replace("ORDER BY", "")
        # TODO: проверка текста
        if len(text) <= 250:
            bot.set_for_friends(event, text)
            if page == "for friends":
                bot.set_page(event, "looking for friends")
            else:
                go_to_edit(event, bot, page)
        else:
            bot.send_message(event, f"Ваш текст слишком длинный: {len(text)} символов, максимум 250.")

    ti_for_friends = TextInput({"for friends", "edit for friends"}, set_for_friends)
    bot.add_text_input(ti_for_friends)
"""

# --- for ppl ---
# не обязательное поле. Указывается перед поиском людей, если не задано
def add_for_people_text_input(bot):
    def set_for_people(event, bot, page):
        text = event.text
        text = text.replace("SELECT", "").replace("FROM", "").replace("WHERE", "").replace("GROUP BY", "").replace("HAVING", "") \
            .replace("ORDER BY", "")
        # проверяем валидность текста
        # TODO: проверка текста
        if len(text) < 250:
            bot.set_for_people(event, text)
            # TODO: выбор пола пользователя которого мы ищем
            if page == "for people":
                bot.set_page(event, "looking for people")
            else:
                go_to_edit(event, bot, page)
        else:
            bot.send_message(event, f"Ваш текст слишком длинный: {len(text)} символов, максимум 250.")

    ti_for_people = TextInput({"for people", "edit for people"}, set_for_people)
    bot.add_text_input(ti_for_people)


# --- main ---
def add_main_keyboard(bot):

    def go_to_for_people(event, bot, page):
        if bot.user_is_ready_for_looking_for_people(event):
            user_id = bot.get_random_for_people(event)
            bot.send_for_people(event.user_id, user_id)
        else:
            bot.set_page(event, "for people")

    btn_for_people = Button("for people", "Искать людей")
    btn_for_people.page("main", go_to_for_people)

    bot.add_button(btn_for_people)
    """
    def go_to_for_interests(event, bot, page):
        if bot.user_is_ready_for_looking_for_interests(event):
            user_id = bot.get_random_for_interests(event)
            img, name, surname = bot.get_info_for_looking(user_id)
            text, fac, age, gender = bot.get_for_interests_info(user_id)
            bot.send_full(event.user_id, None, {"message": f"{name} {surname}\n{fac}\nВозраст: {age}\nПол: {gender}\nО себе:\n{text}", "attachment": img})
        else:
            bot.set_page(event, "for interests")

    btn_for_interests = Button("for interests", "Найти по интересам")
    btn_for_interests.page("main", go_to_for_interests)

    bot.add_button(btn_for_interests)
    """

    go_to_moderation = lambda event, bot, page: bot.set_page(event, "moderation")

    btn_moderation = Button("moderation", "Модерация", roles={"moderator"}, role_error=False)
    btn_moderation.page("main", go_to_moderation)

    bot.add_button(btn_moderation)

    kb_main = Keyboard("main", bot)
    kb_main.add_element(btn_for_people)
    # kb_main.add_element(new_line)
    # kb_main.add_element(btn_for_interests)
    kb_main.add_element(new_line)
    kb_main.add_element(btn_moderation)
    kb_main.add_element(new_line)
    kb_main.add_element(bot.get_button("profile"))

    bot.add_keyboard(kb_main)


# --- profile ---
def add_profile_keyboard(bot):
    kb_profile = Keyboard("profile", bot)

    # на главную
    kb_profile.add_element(bot.get_button("go to main"))
    kb_profile.add_element(new_line)
    # редактирование
    kb_profile.add_element(bot.get_button("go to edit"))

    def view_my_form_for_people(event, bot, page):
        bot.send_for_people(event.user_id, event.user_id)

    btn_view_my_form_for_people = Button("view my form for people", "Моя анкета для поиска людей", color="green")
    btn_view_my_form_for_people.page("profile", view_my_form_for_people)

    # моя анкета для поиска людей
    bot.add_button(btn_view_my_form_for_people)
    kb_profile.add_element(new_line)
    kb_profile.add_element(btn_view_my_form_for_people)

    """
    def view_my_form_for_interests(event, bot, page):
        img, name, _surname = bot.get_info_for_looking(event.user_id)
        text, fac, age, gender = bot.get_for_interests_info(event.user_id)
        yo = ("год" if age % 10 == 1 else "года") if (5 > age % 10 > 0) and age // 10 != 1 else "лет"
        bot.send_full(event.user_id, None,
                      {"message": f"{name}, {age} {yo}, {fac}\nПол: {gender}\n\nО себе:\n{text}", "attachment": img})

    btn_view_my_form_for_interests = Button("view my form for interests", "Моя анкета для поиска по интересам", color="green")
    btn_view_my_form_for_interests.page("profile", view_my_form_for_interests)

    # моя анкета для поиска по интересам
    bot.add_button(btn_view_my_form_for_interests)
    kb_profile.add_element(new_line)
    kb_profile.add_element(btn_view_my_form_for_interests)
    """
    def disable_my_form_for_people(event, bot, page):
        bot.disable_form_for_people(event.user_id)
        bot.send_message(event, "Ваша форма по поиску людей отключена")
        bot.set_page(event, "main")

    btn_disable_my_form_for_people = Button("disable my form for people", "Выключить поиск людей", color="red")
    btn_disable_my_form_for_people.page("profile", disable_my_form_for_people)

    # выключить поиск людей
    bot.add_button(btn_disable_my_form_for_people)
    kb_profile.add_element(new_line)
    kb_profile.add_element(btn_disable_my_form_for_people)

    """
    def disable_my_form_for_interests(event, bot, page):
        bot.disable_form_for_interests(event.user_id)
        bot.send_message(event, "Ваша форма для поиска по интересам отключена")
        bot.set_page(event, "main")

    btn_disable_my_form_for_interests = Button("disable my form for interests", "Выключить поиск по интересам", color="red")
    btn_disable_my_form_for_interests.page("profile", disable_my_form_for_interests)

    # выключить поиск по интересам
    bot.add_button(btn_disable_my_form_for_interests)
    kb_profile.add_element(new_line)
    kb_profile.add_element(btn_disable_my_form_for_interests)
    """

    bot.add_keyboard(kb_profile)


# --- edit ---
def add_edit_keyboard(bot):
    kb_edit = Keyboard("edit", bot)

    kb_edit.add_element(bot.get_button("profile"))

    # age
    go_to_edit_age = lambda event, bot, page: bot.set_page(event, "edit age")

    btn_go_to_edit_age = Button("go to edit age", "Изменить возраст")
    btn_go_to_edit_age.page("edit", go_to_edit_age)

    bot.add_button(btn_go_to_edit_age)
    kb_edit.add_element(new_line)
    kb_edit.add_element(btn_go_to_edit_age)

    # gender
    go_to_edit_gender = lambda event, bot, page: bot.set_page(event, "edit gender")

    btn_go_to_edit_gender = Button("go to edit gender", "Изменить пол")
    btn_go_to_edit_gender.page("edit", go_to_edit_gender)

    bot.add_button(btn_go_to_edit_gender)
    kb_edit.add_element(new_line)
    kb_edit.add_element(btn_go_to_edit_gender)

    # faculty
    go_to_edit_faculty = lambda event, bot, page: bot.set_page(event, "edit faculty")

    btn_go_to_edit_faculty = Button("go to edit faculty", "Изменить факультет")
    btn_go_to_edit_faculty.page("edit", go_to_edit_faculty)

    bot.add_button(btn_go_to_edit_faculty)
    kb_edit.add_element(new_line)
    kb_edit.add_element(btn_go_to_edit_faculty)

    # course
    go_to_edit_course = lambda event, bot, page: bot.set_page(event, "edit course")

    btn_go_to_edit_course = Button("go to edit course", "Изменить курс")
    btn_go_to_edit_course.page("edit", go_to_edit_course)

    bot.add_button(btn_go_to_edit_course)
    kb_edit.add_element(new_line)
    kb_edit.add_element(btn_go_to_edit_course)

    # for people
    go_to_edit_for_people = lambda event, bot, page: bot.set_page(event, "edit for people")

    btn_go_to_edit_for_people = Button("go to edit for people", "Изменить текст для поиска людей")
    btn_go_to_edit_for_people.page("edit", go_to_edit_for_people)

    bot.add_button(btn_go_to_edit_for_people)
    kb_edit.add_element(new_line)
    kb_edit.add_element(btn_go_to_edit_for_people)

    """
    # for interests
    go_to_edit_for_interests = lambda event, bot, page: bot.set_page(event, "edit for interests")

    btn_go_to_edit_for_interests = Button("go to edit for interests", "Изменить текст для поиска по интересам")
    btn_go_to_edit_for_interests.page("edit", go_to_edit_for_interests)

    bot.add_button(btn_go_to_edit_for_interests)
    kb_edit.add_element(new_line)
    kb_edit.add_element(btn_go_to_edit_for_interests)
    """

    bot.add_keyboard(kb_edit)


# --- looking for people ---
def add_looking_for_people_keyboard(bot):
    # TODO
    kb_looking_for_people = Keyboard("looking for people", bot)

    kb_looking_for_people.add_element(bot.get_button("profile"))

    # отправить заявку
    send_requiest = lambda event, bot, page: bot.send_requiest(event, "edit age")

    btn_go_to_edit_age = Button("go to edit age", "Изменить возраст")
    btn_go_to_edit_age.page("edit", send_requiest)

    bot.add_button(btn_go_to_edit_age)
    kb_looking_for_people.add_element(btn_go_to_edit_age)


# --- looking for interests ---
