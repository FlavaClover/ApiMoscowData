from exceptions.exceptions import *
import collections


def check_response_decorator(func):
    """
    Декоратор, который обрабатывает ответ функций, взаимодействующих с API

    :param func: функция, которая возвращает Response
    """
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        if response.status_code == 403:
            raise UnAuthorizationError()
        if response.status_code == 413:
            raise InValidRequestError("Максимальное количество записей можно узнать с помощью функции"
                                      " get_dataset_count_rows(id_dataset)")
        datasets = response.json()
        if isinstance(datasets, dict) and "Message" in datasets:
            raise InValidRequestError(datasets["Message"])
        else:
            return datasets

    return wrapper

