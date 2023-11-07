def is_button_pressed(event):
    """
    Возвращает:
    True - если нажали кнопку
    False - если отправили сообщение
    """
    return "payload" in event.extra_values and "command" in event.extra_values["payload"]


def get_command(event):
    """
    Возвращает какую кнопку нажали
    """
    if is_button_pressed(event):
        return event.extra_values["payload"][12:-2]
    else:
        return ""