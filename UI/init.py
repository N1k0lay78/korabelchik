from UI.pages import add_profile_page, add_age_pages, add_gender_pages, add_faculty_pages, add_main_page, add_edit_page
from UI.inputs import add_age_text_input, add_start_button, add_some, add_gender_keyboard, add_faculty_keyboard, \
    add_for_interests_text_input, add_main_keyboard, add_profile_keyboard, add_edit_keyboard, add_for_friends_text_input


def add_inputs(bot):
    # base
    add_start_button(bot)
    add_some(bot)

    # set/update user info
    add_age_text_input(bot)
    add_gender_keyboard(bot)
    add_faculty_keyboard(bot)
    # add_for_friends_text_input(bot)
    # add_for_interests_text_input(bot)

    # base pages
    add_main_keyboard(bot)
    add_profile_keyboard(bot)
    add_edit_keyboard(bot)

    # looking for pages


def add_pages(bot):
    # set/update user info
    add_age_pages(bot)
    add_gender_pages(bot)
    add_faculty_pages(bot)

    # base pages
    add_main_page(bot)
    add_profile_page(bot)
    add_edit_page(bot)


def add_all(bot):
    add_inputs(bot)
    add_pages(bot)
