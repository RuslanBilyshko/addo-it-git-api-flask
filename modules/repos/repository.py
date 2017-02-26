import csv

import requests
from modules.repos.lang.trans import trans
import json
import xlwt
import os.path

"""
Класс для работы с данными репозиториев пользователя
Работает по принципу цепных вызовов методов
что дает определенное удобство в построении запросов
Пример:
    repo = Repository('username')
    ---------------------------------------------
    - Загрузить все репозитории пользователя
        repo.all().get()
    - Выборка полей:
        repo.all().select(['field1, ...'field_n']).get()
    - Загрузить информацию о конкретном репозитории:
        repo.find('repos_name').first()
"""


class Repository:
    _base_url = "https://api.github.com/"
    status = "Status: 200 OK"

    def __init__(self, username: str):
        self.username = username
        self.url = self._base_url + "users/" + self.username + "/repos"
        self._collection = []

    def __getattr__(self, item):
        return self._collection[0].get(item)

    def find(self, repository: str):
        """Поиск конкретного репозитория из коллекции. Изменяет коллекцию оставляя найденый репозиторий"""
        self.url = self._base_url + "repos/" + self.username + "/" + repository
        self.all()
        self._collection = [self._collection]

        for r in self._collection:
            if repository == r.get("name"):
                self._collection = [r]
        return self

    def select(self, fields: list):
        """Выборка определенных полей из репозитория. Изменяет коллекцию оставляя только отфильтрованые данные"""

        result = []

        for repos in self._collection:

            f = {}

            for field in fields:
                f.update({field: repos.get(field)})

            result.append(f)

        self._collection = result
        return self

    def get(self) -> list:
        """Возвращает коллекцию. Рекомендуеться вызывать после всех выборок"""

        return self._collection

    def count(self) -> int:
        """Подсчитывает колличество элементов в коллекции"""

        return len(self._collection)

    def first(self) -> dict:
        """Возвращает первый элемент коллекции"""

        return self._collection[0]

    def all(self):
        """Загружает полный список в коллекцию"""

        response = requests.get(self.url)
        self.status = response.headers.get("status")
        self._collection = response.json()
        # from repos_data import repos_data
        # self._collection = repos_data

        return self

    def create(self, **request) -> int:
        """Создание репозитория"""

        repo = request["name"]
        secret = request["secret"]

        url = "https://api.github.com/user/repos"

        data = {
            "name": repo,
            "description": "Testting a creating repository " + repo,
            "auto_init": True,
        }

        response_create = requests.post(url, data=json.dumps(data), auth=(self.username, secret))
        status = response_create.headers.get("status")

        if status == "201 Created":
            return 201

        if status == "401 Unauthorized":
            return 401

        if status == "422 Unprocessable Entity":
            return 422

    def export(self, ext: str, path: str, file_name=None):
        """Экспорт репозитория в файл"""

        if file_name is None:
            file_name = self.name

        path_to_file = path + "/" + file_name + "." + ext

        if ext == "csv":
            self.__export_to_csv(path_to_file)
        elif ext == "xls":
            self.__export_to_exel(path_to_file)

        if os.path.exists(path_to_file):
            return True
        else:
            return False

    def __export_to_exel(self, path: str):

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Statistic of repo')

        ws.write(0, 0, 'key')
        ws.write(0, 1, 'value')

        index = 1
        for key, value in self._collection[0].items():
            ws.write(index, 0, "{}".format(key))
            ws.write(index, 1, "{}".format(value))
            index += 1

        wb.save(path)

    def __export_to_csv(self, path: str):

        toCSV = self._collection
        keys = toCSV[0].keys()
        with open(path, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)

    def __str__(self):
        """Строковое представление репозиториев"""

        result = ""
        for repos in self._collection:
            for key, value in repos.items():
                result += "{}: {}\n".format(trans(key), value)

            result += "---------------------------------\n"

        return result


"""
Класс расширяющий Repository
для работы с коммитами
"""


class Commit(Repository):
    def __init__(self, repository: str, username: str):
        Repository.__init__(self, username)
        self.repository = repository
        self.url = self._base_url + "repos/" + self.username + "/" + self.repository + "/commits"


"""
Класс для работы с данными пользователя
"""


class Owner(Repository):
    def __init__(self, username):
        Repository.__init__(self, username)

        # from repos_data import repos_data
        # self._collection = [repos_data[0].get("owner")]

        response = requests.get(self.url)
        self.status = response.headers.get("status")
        self._collection = [response.json()[0].get("owner")]

    def all(self): pass
