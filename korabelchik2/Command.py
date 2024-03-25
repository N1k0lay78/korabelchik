class Command:
    def __init__(self, command, bot):
        self.__command = command
        self.bot = bot
        self.__command_prefix = "/"

    def function(self, params, event):
        self.bot.send_message(event, f"Я функция c параметрами {params}")

    def is_command(self, event):
        if event.message.split()[0] == self.__command_prefix + self.__command:
            return True
        elif self.bot.is_button_pressed(event) and self.__get_command(event).split()[0] == self.__command:
            return True
        return False

    def run_command(self, event):
        self.function(event.message.split()[1:], event)

    def get_name(self):
        return self.__command

    def __get_command(self, event):
        return event.extra_values["payload"][12:-2]