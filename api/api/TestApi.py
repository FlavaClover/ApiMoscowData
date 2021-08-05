import unittest
from requests import get
from moscowdataapi import ApiMoscowData


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api = ApiMoscowData("068b1c994457c79ff1f857bcd687b964")

    def test_base_url(self):
        response = get("https://apidata.mos.ru/version")
        version = response.json()["Version"]
        base_url = f"https://apidata.mos.ru/v{version}"
        self.assertEqual(self.api.base_url, base_url)

    def test_get_all_data_count(self):
        response = get(url=self.api.base_url + "/datasets", params={
            "api_key": "068b1c994457c79ff1f857bcd687b964",
            "$inlinecount": "allpages",
            "$top": 10,
        })
        datasets = response.json()
        actual = self.api.get_all_datasets(inline_count="allpages", top=10)

        self.assertEqual(int(datasets["Count"]), int(actual["Count"]))

    def test_get_all_data_value(self):
        response = get(url="https://apidata.mos.ru/v1/datasets", params={
            "api_key": "068b1c994457c79ff1f857bcd687b964",
            "$skip": 1,
            "$top": 10,
        })

        result = response.json()
        actual = self.api.get_all_datasets(skip=1, top=10)
        self.assertListEqual(result, list(actual))

        response = get(url="https://apidata.mos.ru/v1/datasets", params={
            "api_key": "068b1c994457c79ff1f857bcd687b964",
            "$skip": 1,
            "$top": 10,
            "$inlinecount": "allpages",
        })

        result = response.json()
        actual = self.api.get_all_datasets(skip=1, top=10, inline_count="allpages")
        self.assertDictEqual(result, actual)

    def test_get_dataset(self):
        response = get(url="https://apidata.mos.ru/v1/datasets/495", params={
            "api_key": "068b1c994457c79ff1f857bcd687b964",
        })

        result = response.json()
        actual = self.api.get_dataset_info(495)

        self.assertEqual(result, actual)

    def test_dataset_row_count(self):
        response = get(url="https://apidata.mos.ru/v1/datasets/495/count", params={
            "api_key": "068b1c994457c79ff1f857bcd687b964",
        })

        result = response.json()
        actual = self.api.get_dataset_count_row(495)

        self.assertEqual(result, actual)
