from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from .items import HHVacancyItem, EmployerItem


class HHVacancyLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = "".join
    description_out = TakeFirst()
    salary_in = "".join
    salary_out = TakeFirst()


class EmployerLoader(ItemLoader):
    default_item_class = EmployerItem
    emp_name_out = TakeFirst()
    url_out = TakeFirst()
    area_of_activity_out = TakeFirst()
    emp_description_in = ''.join
    emp_description_out = TakeFirst()
