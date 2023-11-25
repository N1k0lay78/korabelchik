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
