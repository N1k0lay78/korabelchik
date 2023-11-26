from UI.commands import add_role_commands, add_get_info, add_owner_commands, add_usual_commands
from UI.pages import add_profile_page, add_age_pages, add_gender_pages, add_faculty_pages, add_main_page, add_edit_page, \
    add_texts_for, add_test_page, add_my_for_friend
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
    add_for_friends_text_input(bot)
    add_for_interests_text_input(bot)

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
    add_texts_for(bot)

    # base pages
    add_main_page(bot)
    add_profile_page(bot)
    add_edit_page(bot)

    # test
    add_test_page(bot)
    add_my_for_friend(bot)


def add_commands(bot):
    add_role_commands(bot)
    add_get_info(bot)
    add_usual_commands(bot)
    add_owner_commands(bot)


def add_all(bot):
    add_inputs(bot)
    add_pages(bot)
    add_commands(bot)
