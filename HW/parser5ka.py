import json
import requests
import time


class ParseError(Exception):
    def __init__(self, txt):
        self.txt = txt


class Parse5ka:
    params: dict = {
        'records_per_page': 50
    }
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Safari/537.36 ',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    def __init__(self, start_url: str):
        self.start_url = start_url

    @staticmethod
    def __get_response(url: str, *args, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(url, *args, **kwargs)
                if response.status_code > 399:
                    raise ParseError(response.status_code)
                time.sleep(0.1)
                return response
            except (requests.RequestException, ParseError):
                time.sleep(0.5)
                continue

    def run(self):
        for products in self.parse(self.start_url):
            for product in products:
                self.save(product, product["id"])

    def parse(self, url: str):
        if not url:
            url = self.start_url

        params = self.params

        while url:
            response = self.__get_response(url, params=params, headers=self.headers)
            if params:
                params = {}

            data: dict = response.json()
            url = data.get('next')

            yield data.get("results")

    @staticmethod
    def save(data: dict, file_name: str):
        with open(f"{file_name}.json", "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    parser = Parse5ka(url)
    parser.run()

    # cleans up parsed json-files
    # import os
    #
    # listdir = os.listdir()
    # while listdir:
    #     cnt = listdir.pop()
    #     if 'json' in cnt:
    #         os.remove(f'{os.getcwd()}\{cnt}')
