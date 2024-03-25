def validation_role(bot, event, roles, alert=True):
    for role in bot.get_roles(event.user_id):
        if role in roles:
            return True
    if alert:
        bot.send_message(event.user_id, "Недостаточно прав доступа")
    return False


def validation_int(bot, event, params, alert=True):
    if len(params) > 0 and params[0].isdigit():
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
