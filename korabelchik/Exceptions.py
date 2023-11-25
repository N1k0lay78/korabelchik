class ButtonLengthError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ButtonFuncError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ButtonNameIntersection(Exception):
    def __init__(self, message):
        super().__init__(message)


class KeyboardNameIntersection(Exception):
    def __init__(self, message):
        super().__init__(message)


class PageNameIntersection(Exception):
    def __init__(self, message):
        super().__init__(message)


class ButtonNameNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class KeyboardNameNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class PageNameNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class ButtonPageIntersection(Exception):
    def __init__(self, message):
        super().__init__(message)


class ButtonUnknownColor(Exception):
    def __init__(self, message):
        super().__init__(message)


class ButtonAccessDenied(Exception):
    def __init__(self, message):
        super().__init__(message)


class PageAccessDenied(Exception):
    def __init__(self, message):
        super().__init__(message)


class PageMessageIsNone(Exception):
    def __init__(self, message):
        super().__init__(message)


class TextInputAccessDenied(Exception):
    def __init__(self, message):
        super().__init__(message)


class TextInputPageError(Exception):
    def __init__(self, message):
        super().__init__(message)


class TextInputFuncError(Exception):
    def __init__(self, message):
        super().__init__(message)
