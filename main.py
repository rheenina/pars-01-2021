import os
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.inst import InstSpider

if __name__ == "__main__":
    tags = ['foxhome_', 'redroom_boutique']
    load_dotenv('.env')
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(InstSpider, login=os.getenv('USERNAME'), password=os.getenv('ENC_PASSWORD'), tags=tags)
    crawler_process.start()
