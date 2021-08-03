from requests import get, post
from simplejson import JSONDecodeError


class UnAuthorizationError(Exception):
    pass


class Data:

    class __Department:
        def __init__(self, department_id: int, caption: str):
            self.__id = department_id
            self.__caption = caption

        @property
        def id(self):
            return self.__id

        @property
        def caption(self):
            return self.__caption

    class __Category:
        def __init__(self, category_id: int, caption: str):
            self.__id = category_id
            self.__caption = caption

        @property
        def id(self):
            return self.__id

        @property
        def caption(self):
            return self.__caption

    class __Version:
        def __init__(self, number: str, date: str):
            self.__number = number
            self.__date = date

        @property
        def number(self):
            return self.__number

        @property
        def date(self):
            return self.__date

    class __Column:
        def __init__(self, name: str, caption: str, visible: bool, sub_columns: list):
            self.__name = name
            self.__caption = caption
            self.__visible = visible
            self.__sub_columns = sub_columns

        @property
        def name(self):
            return self.__name

        @property
        def caption(self):
            return self.__caption

        @property
        def visible(self):
            return self.__visible

        @property
        def sub_columns(self):
            return self.__sub_columns

        def __repr__(self):
            return f"{self.__class__.__name__}({self.name}, {self.caption}, {self.visible}, {self.sub_columns})"

    def __init__(self, **kwargs):
        try:
            self.id = int(kwargs["Id"])
            self.category = self.__Category(int(kwargs["CategoryId"]), kwargs["CategoryCaption"])
            self.department = self.__Department(int(kwargs["DepartmentId"]), kwargs["DepartmentCaption"])
            self.caption = kwargs["Caption"]
            self.desc = kwargs["Description"]
            self.contains_geodata = kwargs["ContainsGeodata"]
            self.version = self.__Version(kwargs["VersionNumber"], kwargs["VersionDate"])
            self.items_count = int(kwargs["ItemsCount"])

            def get_columns(columns):

                result = []
                for c in columns:
                    if c["SubColumns"]:
                        sub_columns = get_columns(c["SubColumns"])
                    else:
                        sub_columns = None

                    result.append(self.__Column(c["Name"], c["Caption"], c["Visible"], sub_columns))

                return result
            self.columns = get_columns(kwargs["Columns"])

        except Exception:
            raise ValueError("Some value is wrong")

    def __repr__(self):
        return f"{Data.__name__}({self.id}, {self.category.caption}, {self.caption})"


class ApiMoscowData:
    def __init__(self, api_key: str):
        """ Стандартный конструктор """
        self.__api_key = api_key
        self.__base_url = "https://apidata.mos.ru"
        self.__get_version()

    def __get_version(self) -> None:
        """ Добавление верссии в базовый url """
        response = get(self.__base_url + "/version")
        version = response.json()["Version"]
        self.__base_url = self.__base_url + f"/v{version}"

    @property
    def base_url(self) -> str:
        """ Геттер для базового url'a """
        return self.__base_url

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

    def get_all_data(self, **kwargs) -> dict:
        """
        Взятие информации о данных

        Опциональные аргументы:\n
        top:	Ограничивает количество возвращаемых записей. Без указания данного параметра выводятся все записи.\n
        skip:	Позволяет указать количество записей, которые следует пропустить в ответе.\n
        inlinecount:	Принимает значение allpages для того, чтобы в ответе получить общее количество записей.\n
        orderby:	Указывает поле для сортировки результирующего списка.\n
        filter:	Поддерживает операторы протокола OData v2.0
        (https://www.odata.org/documentation/odata-version-2-0/uri-conventions/).\n
        foreign:	true - возвращает список англоязычных наборов данных;
        false- возвращает список русскоязычных наборов данных (значение по умолчанию).
        """
        params = self.__get_params(**kwargs)
        params["api_key"] = self.__api_key

        response = get(url=self.__base_url + "/datasets", params=params)

        if response.status_code == 403:
            raise UnAuthorizationError("Maybe API-key is invalid")
        else:
            data = response.json()
            return data

    def get_all_data_with_specific_fields(self, fields: list, **kwargs):
        """
        Взятие информации о данных c определенными полями

        Обязательные аргументы:\n
        fields: Список полей

        Опциональные аргументы:\n
        top:	Ограничивает количество возвращаемых записей. Без указания данного параметра выводятся все записи.\n
        skip:	Позволяет указать количество записей, которые следует пропустить в ответе.\n
        inlinecount:	Принимает значение allpages для того, чтобы в ответе получить общее количество записей.\n
        orderby:	Указывает поле для сортировки результирующего списка.\n
        filter:	Поддерживает операторы протокола OData v2.0
        (https://www.odata.org/documentation/odata-version-2-0/uri-conventions/).\n
        foreign:	true - возвращает список англоязычных наборов данных;
        false- возвращает список русскоязычных наборов данных (значение по умолчанию).
        """
        params = self.__get_params(**kwargs)
        params["api_key"] = self.__api_key

        response = post(url=self.__base_url + "/datasets", params=params, json=fields)

        if response.status_code == 403:
            raise UnAuthorizationError("Maybe API-key is invalid")
        else:
            data = response.json()
            return data

    def get_data(self, id_data, fields=None):

        if not fields:
            response = get(url=self.__base_url + f"/datasets/{id_data}", params={"api_key": self.__api_key})
        else:
            response = post(url=self.__base_url + f"/datasets/{id_data}", params={"api_key": self.__api_key},
                            json=fields)

        if response.status_code == 403:
            raise UnAuthorizationError("Maybe API-key is invalid")
        else:
            data = response.json()
            return data

    def get_data_object(self, id_data) -> Data:
        response = get(url=self.__base_url + f"/datasets/{id_data}", params={"api_key": self.__api_key})

        if response.status_code == 403:
            raise UnAuthorizationError("Maybe API-key is invalid")
        else:
            data = Data(**response.json())
            return data

    def get_data_count_row(self, id_data):
        response = get(url=self.__base_url + f"/datasets/{id_data}/count", params={"api_key": self.__api_key})

        if response.status_code == 403:
            raise UnAuthorizationError("Maybe API-key is invalid")
        else:
            data = response.json()
            return data
