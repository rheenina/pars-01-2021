import requests
from parser5ka import Parse5ka


class ParseCat(Parse5ka):
    def __init__(self, start_url, cat_url):
        self.cat_url = cat_url
        super().__init__(start_url)

    def get_cat(self, url):
        response = requests.get(url, headers=self.headers)
        return response.json()

    def run(self):
        for cat in self.get_cat(self.cat_url):
            data = {
                "name": cat["parent_group_name"],
                "code": cat["parent_group_code"],
                "products": [],
            }

            self.params["categories"] = cat["parent_group_code"]

            for products in self.parse(self.start_url):
                data["products"].extend(products)
                print(f'extended {products}')
            self.save(data, cat["parent_group_code"])


if __name__ == '__main__':
    parser = ParseCat("https://5ka.ru/api/v2/special_offers/", "https://5ka.ru/api/v2/categories/")
    parser.run()
