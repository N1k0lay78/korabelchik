class Command:
    def __init__(self, command, bot):
        self.__command = command
        self.bot = bot
        self.__command_prefix = "/"

    def function(self, params, event):
        self.bot.send_message(event, f"Я функция c параметрами {params}")

    def is_command(self, event, type_command=1):
        # press button
        if type_command == 0 and self.__get_command(event).split()[0] == self.__command:
            return True
        # classic command with /
        elif type_command == 1 and event.message.split()[0] == self.__command_prefix + self.__command:
            return True
        # write text on page
        elif type_command == 2 and self.bot.get_page(event.user_id).split()[0] == self.__command:
            return True
        return False

    def run_command(self, event, type_command=1):
        self.function(((event.message.split()[1:]
                        if type_command == 1 else
                        event.extra_values["payload"][12:-2].split()[1:]
                        )
                       if type_command < 2 else
                       [event.message]), event)

    def get_name(self):
        return self.__command

    def __get_command(self, event):
        return event.extra_values["payload"][12:-2]
