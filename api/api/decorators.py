from exceptions.exceptions import *


def check_response_decorator(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        if response.status_code == 403:
            raise UnAuthorizationError()

        datasets = response.json()
        if "Message" in datasets:
            raise InValidRequestError(datasets["Message"])
        else:
            return datasets

    return wrapper
