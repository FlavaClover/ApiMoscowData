from requests import get, post
from decorators import *


class ApiMoscowData:
    def __init__(self, api_key: str):
        """ Стандартный конструктор """
        self.__api_key = api_key
        self.__base_url = "https://apidata.mos.ru"

    def get_version(self) -> None:
        """ Добавление верссии в базовый url """
        response = get(self.__base_url + "/version")
        version = response.json()["Version"]
        return version

    @property
    def base_url(self) -> str:
        """ Геттер для базового url'a """
        return self.__base_url + f"/v{self.get_version()}"

    @staticmethod
    def __get_params(**kwargs) -> dict:
        params = dict()
        if "top" in kwargs:
            params["$top"] = kwargs["top"]
        if "skip" in kwargs:
            params["$skip"] = kwargs["skip"]
        if "inlinecount" in kwargs:
            params["$inlinecount"] = kwargs["inlinecount"]
        if "orderby" in kwargs:
            params["$orderby"] = kwargs["orderby"]
        if "filter" in kwargs:
            params["$filter"] = kwargs["filter"]
        if "foreign" in kwargs:
            params["foreign"] = kwargs["foreign"]

        return params

    @check_response_decorator
    def get_all_datasets(self, top=None, skip=None,
                         inline_count=None, order_by=None, filter=None, foreign=None):
        """
        Взятие наборов данных

        :param top:	Ограничивает количество возвращаемых записей. Без указания данного параметра выводятся все записи.
        :param skip:	Позволяет указать количество записей, которые следует пропустить в ответе.
        :param inline_count:	Принимает значение allpages для того, чтобы в ответе получить общее количество записей.
        :param order_by:	Указывает поле для сортировки результирующего списка.
        :param filter:	Поддерживает операторы протокола OData v2.0
        (https://www.odata.org/documentation/odata-version-2-0/uri-conventions/).
        :param foreign:	true - возвращает список англоязычных наборов данных;
        false- возвращает список русскоязычных наборов данных (значение по умолчанию).

        :return: список наборов данных
        """
        params = self.__get_params(top=top, skip=skip, inlinecount=inline_count,
                                   orderby=order_by, filter=filter, foreign=foreign)
        params["api_key"] = self.__api_key

        return get(url=self.base_url + "/datasets", params=params)

    @check_response_decorator
    def get_all_dataset_with_specific_fields(self, fields: list, top=None, skip=None,
                                             inline_count=None, order_by=None, filter=None, foreign=None):
        """
        Взятие наборов данных c определенными полями

        :param fields: Список полей
        :param top:	Ограничивает количество возвращаемых записей. Без указания данного параметра выводятся все записи.
        :param skip:	Позволяет указать количество записей, которые следует пропустить в ответе.
        :param inline_count:	Принимает значение allpages для того, чтобы в ответе получить общее количество записей.
        :param order_by:	Указывает поле для сортировки результирующего списка.
        :param filter:	Поддерживает операторы протокола OData v2.0
        (https://www.odata.org/documentation/odata-version-2-0/uri-conventions/).
        :param foreign:	true - возвращает список англоязычных наборов данных;
        false- возвращает список русскоязычных наборов данных (значение по умолчанию).

        :return: список наборов данных с определенными полями
        """
        params = self.__get_params(top=top, skip=skip, inlinecount=inline_count,
                                   orderby=order_by, filter=filter, foreign=foreign)

        params["api_key"] = self.__api_key

        return post(url=self.base_url + "/datasets", params=params, json=fields)

    @check_response_decorator
    def get_dataset_info(self, id_data, fields=None):
        """
        Взятие информации о конкретном наборе данных

        :param id_data: номер набора
        :param fields: нужные поля
        :return: информация о наборе данных
        """
        if not fields:
            return get(url=self.base_url + f"/datasets/{id_data}", params={"api_key": self.__api_key})
        else:
            return post(url=self.base_url + f"/datasets/{id_data}", params={"api_key": self.__api_key},
                        json=fields)

    @check_response_decorator
    def get_dataset_object(self, id_data):
        return get(url=self.base_url + f"/datasets/{id_data}", params={"api_key": self.__api_key})

    @check_response_decorator
    def get_dataset_count_row(self, id_data):
        return get(url=self.base_url + f"/datasets/{id_data}/count", params={"api_key": self.__api_key})



