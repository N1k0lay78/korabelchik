class NewLine:
    def __init__(self):
        pass

    def get_name(self):
        return ""

    def check(self, page):
        pass

    def add_element(self, keyboard, roles):
        keyboard.add_line()

    def check_roles(self, roles):
        return True

    def __repr__(self):
        return f"NEW LINE"