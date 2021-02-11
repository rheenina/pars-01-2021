# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutoyoulaItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    specifications = scrapy.Field()
    price = scrapy.Field()


class HHVacancyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    company_url = scrapy.Field()


class EmployerItem(scrapy.Item):
    _id = scrapy.Field()
    emp_name = scrapy.Field()
    url = scrapy.Field()
    area_of_activity = scrapy.Field()
    emp_description = scrapy.Field()
    emp_vacancy_offer = scrapy.Field()


class Insta(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    img = scrapy.Field()


class InstaTag(Insta):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    img = scrapy.Field()


class InstaPost(Insta):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    img = scrapy.Field()


class InstaFollow(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    follow_name = scrapy.Field()
    follow_id = scrapy.Field()


class InstaUser(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()