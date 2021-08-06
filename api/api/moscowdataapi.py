from requests import get, post, Response
from decorators import *


class ApiMoscowData:
    def __init__(self, api_key: str):
        """
        Стандартный конструктор

        :param api_key: ключ для доступа к API
        """
        self.__api_key = api_key
        self.__base_url = "https://apidata.mos.ru"

    def get_version(self) -> str:
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
        """
        Функция для обработки параметров запроса к API. Принятые параметры возвращаются ввиде словаря

        :param kwargs: параметры запроса
        """
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
                         inline_count=None, order_by=None, filter=None, foreign=None) -> Response:
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
        """
        params = self.__get_params(top=top, skip=skip, inlinecount=inline_count,
                                   orderby=order_by, filter=filter, foreign=foreign)
        params["api_key"] = self.__api_key

        return get(url=self.base_url + "/datasets", params=params)

    @check_response_decorator
    def get_all_dataset_with_specific_fields(self, fields: list, top=None, skip=None,
                                             inline_count=None, order_by=None, filter=None, foreign=None) -> Response:
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
        """
        params = self.__get_params(top=top, skip=skip, inlinecount=inline_count,
                                   orderby=order_by, filter=filter, foreign=foreign)

        params["api_key"] = self.__api_key

        return post(url=self.base_url + "/datasets", params=params, json=fields)

    @check_response_decorator
    def get_dataset_info(self, id_dataset, fields=None) -> Response:
        """
        Взятие информации о конкретном наборе данных

        :param id_dataset: номер набора
        :param fields: нужные поля
        """
        if not fields:
            return get(url=self.base_url + f"/datasets/{id_dataset}", params={"api_key": self.__api_key})
        else:
            return post(url=self.base_url + f"/datasets/{id_dataset}", params={"api_key": self.__api_key},
                        json=fields)

    @check_response_decorator
    def get_dataset_count_rows(self, id_dataset: int) -> Response:
        """
        Получения количества строк в наборе информации
        :param id_dataset: номер набора информации
        :return:
        """
        return get(url=self.base_url + f"/datasets/{id_dataset}/count", params={"api_key": self.__api_key})

    @check_response_decorator
    def get_dataset_rows(self, id_dataset, field=None, top=None, skip=None, order_by=None, filter=None) -> Response:
        """
        Получение данных определенного набора

        :param id_dataset: Номер набора
        :param field: Список нужных полей. Если параметр пустой, то будут получены все поля
        :param top: Ограничивает количество возвращаемых записей. Без указания данного параметра выводятся все записи.
        :param skip: Позволяет указать количество записей, которые следует пропустить в ответе.
        :param order_by: Указывает поле для сортировки результирующего списка.
        :param filter: Позволяет производить фильтрацию данных по указанным значениям в конкретных атрибутах.
        Атрибут в фильтре должен начинается с "Cells/". Используется оператор "eq", который ищет по частичному вхождению
        (поиск чисел осуществляется по полному вхождению).
        """
        params = self.__get_params(top=top, skip=skip, orderby=order_by, filter=filter)
        params["api_key"] = self.__api_key
        if not field:
            return get(url=self.base_url + f"/datasets/{id_dataset}/rows", params=params)
        else:
            return post(url=self.base_url + f"/datasets/{id_dataset}/rows", params=params, json=field)


if __name__ == "__main__":
    api = ApiMoscowData("068b1c994457c79ff1f857bcd687b964")
    data = api.get_dataset_rows(658, top=3, field=["global_id"])
    for d in data:
        print(d)