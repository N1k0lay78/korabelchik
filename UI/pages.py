from korabelchik.output.Page import Page


def add_age_pages(bot):
    pg_age = Page("age")
    render_age = lambda event, bot: "Введите ваш возраст"
    pg_age.set_message(render_age)
    bot.add_page(pg_age)

    pg_edit_age = Page("edit age")
    pg_edit_age.set_message(render_age)
    pg_edit_age.set_keyboard(bot.get_keyboard("go to edit"))
    bot.add_page(pg_edit_age)


def add_gender_pages(bot):
    pg_gender = Page("gender")
    render_gender = lambda event, bot: "Выберите ваш пол"
    pg_gender.set_message(render_gender)
    pg_gender.set_keyboard(bot.get_keyboard("gender"))
    bot.add_page(pg_gender)

    pg_edit_gender = Page("edit gender")
    render_gender = lambda event, bot: "Выберите ваш пол"
    pg_edit_gender.set_message(render_gender)
    pg_edit_gender.set_keyboard(bot.get_keyboard("edit gender"))
    bot.add_page(pg_edit_gender)


def add_faculty_pages(bot):
    pg_faculty = Page("faculty")
    render_faculty = lambda event, bot: "Выберите ваш факультет"
    pg_faculty.set_message(render_faculty)
    pg_faculty.set_keyboard(bot.get_keyboard("faculty"))
    bot.add_page(pg_faculty)

    pg_edit_faculty = Page("edit faculty")
    pg_edit_faculty.set_message(render_faculty)
    pg_edit_faculty.set_keyboard(bot.get_keyboard("edit faculty"))
    bot.add_page(pg_edit_faculty)


def add_texts_for(bot):
    pg_for_friends = Page("for friends")
    render_for_friends = lambda event, bot: "Введите текст для поиска друга"
    pg_for_friends.set_message(render_for_friends)
    bot.add_page(pg_for_friends)

    pg_edit_for_friends = Page("edit for friends")
    pg_edit_for_friends.set_message(render_for_friends)
    bot.add_page(pg_edit_for_friends)

    pg_for_interests = Page("for interests")
    render_for_interests = lambda event, bot: "Введите текст для поиска по интересам"
    pg_for_interests.set_message(render_for_interests)
    bot.add_page(pg_for_interests)

    pg_edit_for_interests = Page("edit for interests")
    pg_edit_for_interests.set_message(render_for_interests)
    bot.add_page(pg_edit_for_interests)


def add_main_page(bot):
    pg_main = Page("main")
    render_main = lambda event, bot: "Главное меню"
    pg_main.set_message(render_main)
    pg_main.set_keyboard(bot.get_keyboard("main"))
    bot.add_page(pg_main)


def add_profile_page(bot):
    pg_profile = Page("profile")
    render_profile = lambda event, bot: "Ваш профиль"
    pg_profile.set_message(render_profile)
    pg_profile.set_keyboard(bot.get_keyboard("profile"))
    bot.add_page(pg_profile)


def add_edit_page(bot):
    pg_edit = Page("edit")
    render_edit = lambda event, bot: "Изменить данные вашего профиля"
    pg_edit.set_message(render_edit)
    pg_edit.set_keyboard(bot.get_keyboard("edit"))
    bot.add_page(pg_edit)


def add_test_page(bot):
    pg_text = Page("test")
    def render_test(bot, event):
        img, name, surname = bot.get_info_for_looking(event.user_id)
        return {"message": f"{name}, {surname}", "attachment": img}
    pg_text.set_message(render_test)
    bot.add_page(pg_text)


def add_my_for_friend(bot):
    pg_my_for_friends = Page("my for friends")

    def render_my_for_friends(bot, event):
        # bot.get_gender(event)
        img, name, surname = bot.get_info_for_looking(event.user_id)
        text, fac, age, gender = bot.get_for_friends_info(event)
        bot.send_full({"message": f"{name} {surname}\n{fac}\nВозраст: {age}\nПол: {gender}\nО себе:\n{text}", "attachment": img})

    pg_my_for_friends.set_message(render_my_for_friends)
    bot.add_page(pg_my_for_friends)