import datetime as dt
import json
import scrapy
from ..items import InstaTag, InstaPost


class InstSpider(scrapy.Spider):
    name = 'inst'
    allowed_domains = ['www.instagram.com']
    start_urls = ['http://www.instagram.com/']
    tag_path = '/explore/tags/'
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    api_url = "/graphql/query/"
    query_hash = {
        "posts": "2c4c2e343a8f64c625ba02b2aa12c7f8",
        "tag_posts": "845e0309ad78bd16fc862c04ff9d8939",
    }

    def __init__(self, login, password, tags: list, *args, **kwargs):
        self.tags = tags
        self.__login = login
        self.__enc_passwd = password
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.__login,
                    'password': self.__enc_passwd,
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError:
            if response.json().get('authenticated'):
                for tag in self.tags:
                    tag_url = f'{self.tag_path}{tag}'
                    yield response.follow(tag_url, callback=self.tag_parse)

    def tag_parse(self, response):
        tag = self.js_data_extract(response)["entry_data"]["TagPage"][0]["graphql"]["hashtag"]

        yield InstaTag(
            date_parse=dt.datetime.utcnow(),
            data={
                "id": tag["id"],
                "name": tag["name"],
                "profile_pic_url": tag["profile_pic_url"],
            },
        )
        yield from self.get_tag_posts(tag, response)

    def tag_api_parse(self, response):
        yield from self.get_tag_posts(response.json()["data"]["hashtag"], response)

    def get_tag_posts(self, tag, response):
        if tag["edge_hashtag_to_media"]["page_info"]["has_next_page"]:
            variables = {
                "tag_name": tag["name"],
                "first": 100,
                "after": tag["edge_hashtag_to_media"]["page_info"]["end_cursor"],
            }
            url = f'{self.api_url}?query_hash={self.query_hash["tag_posts"]}&variables={json.dumps(variables)}'
            yield response.follow(
                url,
                callback=self.tag_api_parse,
            )

        yield from self.get_post_item(tag["edge_hashtag_to_media"]["edges"])

    @staticmethod
    def get_post_item(edges):
        for node in edges:
            yield InstaPost(date_parse=dt.datetime.utcnow(), data=node["node"])

    @staticmethod
    def js_data_extract(response) -> dict:
        script = response.xpath("/html/body/script[contains(text(), 'window._sharedData = ')]/text()").get()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])
