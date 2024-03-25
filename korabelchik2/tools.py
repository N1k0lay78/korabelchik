from controller.user import get_user_page


def validation_role(bot, event, roles, alert=True):
    for role in bot.get_roles(event.user_id):
        if role in roles:
            return True
    if alert:
        bot.send_message(event.user_id, "Недостаточно прав доступа")
    return False


def validation_int(bot, event, params, alert=True):
    if len(params) > 0 and len(params[0]) > 0 and (params[0].isdigit() or
                                                   params[0][1:].isdigit() and params[0][0] == "-"):
        return True
    if alert:
        bot.send_message(event.user_id, "Пропущен аргумент - число")
    return False


def validation_str(bot, event, params, alert=True):
    if len(params) > 0:
        return True
    if alert:
        bot.send_message(event.user_id, "Пропущен аргумент - строка")
    return False


def validate_page(bot, event, page, req_params=None, alert=True):
    args = get_user_page(event.user_id).split()
    if len(args) == 1:
        if args[0] == page and req_params is None:
            return True
        else:
            if alert:
                bot.send_message(event.user_id, "Неправильная страница")
            return False
    elif len(args) == 2:
        if args[0] == page and args[1] in req_params:
            return True
        else:
            if alert:
                bot.send_message(event.user_id, "Неправильная страница или пропущен обязательный аргумент")
            return False
    else:
        if alert:
            bot.send_message(event.user_id, "Вы не находитесь на странице и пропущен обязательный аргумент")
        return False


def validate_page_id(bot, event, page, alert=True):
    args = get_user_page(event.user_id).split()
    if len(args) == 1:
        if alert:
            bot.send_message(event.user_id, "Неправильная страница и/или отсутствует аргумент")
        return False
    elif len(args) == 2:
        if args[0] == page and args[1].isdigit():
            return True
        else:
            if alert:
                bot.send_message(event.user_id, "Неправильная страница или аргумент")
            return False
    else:
        if alert:
            bot.send_message(event.user_id, "Вы не находитесь на странице и пропущен обязательный аргумент")
        return False
