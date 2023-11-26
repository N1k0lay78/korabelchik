from controller.user import add_role, remove_role, get_roles, get_ids, remove_user
from korabelchik.input.Command import Command


def add_role_commands(bot):
    def add_roles(event, bot, page):
        args = event.message.split()[1:]
        if args[0].isdigit() and args[1] in {"moderator", "admin", "user", "tester"}:
            bot.send_message(event, add_role(args[0], args[1]))

    def remove_roles(event, bot, page):
        args = event.message.split()[1:]
        if args[0].isdigit() and args[1] in {"moderator", "admin", "user", "tester"}:
            bot.send_message(event, remove_role(args[0], args[1]))

    def get_role(event, bot, page):
        args = event.message.split()[1:]
        if args[0].isdigit():
            bot.send_message(event, str(get_roles(args[0])))

    cmd_add_role = Command("add_role", add_roles, {"owner"})
    cmd_remove_role = Command("remove_role", remove_roles, {"owner"})
    cmd_get_roles = Command("get_roles", get_role, {"owner"})
    bot.add_command(cmd_add_role)
    bot.add_command(cmd_remove_role)
    bot.add_command(cmd_get_roles)


def add_usual_commands(bot):
    pass


def add_owner_commands(bot):
    def func1(event, bot, page):
        args = event.message.split()[1:]
        bot.set_page(event, " ".join(args))

    def func2(event, bot, page):
        args = event.message.split()[1:]
        if args[0].isdigit():
            bot.send_message(event, remove_user(args[0]))

    cmd_1 = Command("set_page", func1, {"owner", "tester"})
    bot.add_command(cmd_1)
    cmd_2 = Command("remove_user", func2, {"owner"})
    bot.add_command(cmd_2)


def add_get_info(bot):
    def log_get_ids(event, bot, page):
        args = event.message.split()[1:]
        bot.send_message(event, str(get_ids(event.user_id)))

    def log_get_info(event, bot, page):
        bot.send_message(event, str(get_ids(event.user_id)) + '\n' + str(get_roles(event.user_id))+ '\n' + f"страница: {page}")

    cmd_get_ids = Command("get_id", log_get_ids, {"user", "ban"})
    cmd_get_info = Command("get_info", log_get_info, {"user", "ban"})
    cmd_get_info1 = Command("info", log_get_info, {"user", "ban"})
    bot.add_command(cmd_get_ids)
    bot.add_command(cmd_get_info)
    bot.add_command(cmd_get_info1)

    def func1(event, bot, page):
        bot.send_message(event, page)

    cmd_1 = Command("get_page", func1, {"user"})
    bot.add_command(cmd_1)
