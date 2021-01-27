from urllib.parse import urljoin

import bs4
import requests
from dotenv import load_dotenv

from database import Database


class GbParse:
    def __init__(self, start_url, database):
        self.start_url = start_url
        self.done_urls = set()
        self.tasks = [self.parse_task(self.start_url, self.pag_parse)]
        self.done_urls.add(self.start_url)
        self.database = database

    @staticmethod
    def _get_soup(*args, **kwargs):
        response = requests.get(*args, **kwargs)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup

    def parse_task(self, url, callback):
        def wrap():
            soup = self._get_soup(url)
            return callback(url, soup)

        return wrap

    def run(self):
        for task in self.tasks:
            result = task()
            if result:
                self.database.create_post(result)

    def post_parse(self, url, soup: bs4.BeautifulSoup) -> dict:
        author_name_tag = soup.find("div", attrs={"itemprop": "author"})
        data = {
            "post_data": {
                "url": url,
                "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
            },
            "author": {
                "url": urljoin(url, author_name_tag.parent.get("href")),
                "name": author_name_tag.text,
            },
            "tags": [
                {
                    "name": tag.text,
                    "url": urljoin(url, tag.get("href")),
                }
                for tag in soup.find_all("a", attrs={"class": "small"})
            ],
            "comments": self.__get_post_comments(soup),
        }
        return data

    def pag_parse(self, url, soup: bs4.BeautifulSoup):
        gb_pagination = soup.find("ul", attrs={"class": "gb__pagination"})
        a_tags = gb_pagination.find_all("a")
        for a in a_tags:
            pag_url = urljoin(url, a.get("href"))
            if pag_url not in self.done_urls:
                task = self.parse_task(pag_url, self.pag_parse)
                self.tasks.append(task)
                self.done_urls.add(pag_url)

        posts_urls = soup.find_all("a", attrs={"class": "post-item__title"})
        for post_url in posts_urls:
            post_href = urljoin(url, post_url.get("href"))
            if post_href not in self.done_urls:
                task = self.parse_task(post_href, self.post_parse)
                self.tasks.append(task)
                self.done_urls.add(post_href)

    def __get_post_comments(self, soup):
        post_id = soup.find(
            "div", attrs={"class": "referrals-social-buttons-small-wrapper"}).get("data-minifiable-id")
        params = {
            "commentable_type": "Post",
            "commentable_id": int(post_id),
            "order": "desc",
        }
        j_data = requests.get(
            urljoin(self.start_url, "/api/v2/comments"), params=params
        )
        return j_data.json()


if __name__ == "__main__":
    load_dotenv(".env")
    db_url = 'sqlite:///db_blog.db'
    parser = GbParse("https://geekbrains.ru/posts", Database(db_url))
    parser.run()
