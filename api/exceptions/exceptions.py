class UnAuthorizationError(Exception):
    def __init__(self):
        self.message = "Maybe API-key is invalid"

    def __str__(self):
        return self.message


class InValidRequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

