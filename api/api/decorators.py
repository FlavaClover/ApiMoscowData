from exceptions.exceptions import *
import collections


def check_response_decorator(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        if response.status_code == 403:
            raise UnAuthorizationError()

        datasets = response.json()
        if isinstance(datasets, dict) and "Message" in datasets:
            raise InValidRequestError(datasets["Message"])
        else:
            return datasets

    return wrapper
