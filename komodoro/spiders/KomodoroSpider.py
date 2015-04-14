# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from pyquery import PyQuery as pq
import scrapy
class KomodoroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    news_category = scrapy.Field()
    title = scrapy.Field()
    news_summary = scrapy.Field()
    news_text = scrapy.Field()
    news_date = scrapy.Field()
    
class KomodoroSpider(CrawlSpider):
    name = "hurriyet_demo"
    allowed_domains = ["hurriyet.com.tr"]
    start_urls = ['http://hurarsiv.hurriyet.com.tr/goster/Haberler.aspx?id=2403&tarih=2014-01-01']
    rules = (
            # Rule(LinkExtractor(allow=('\/.aberler\.aspx\?id=[0-9]+&tarih=201[4]-0[1-9]|1[012]-0[1-9]|[12][0-9]|3[01]'))),
            Rule(LinkExtractor(allow=('\/.aberler\.aspx\?id=[0-9]+\&tarih=2014-'))),
            Rule(LinkExtractor(allow=('[0-9]+\.asp')), callback = 'parse2'),
        )

    def parse2(self, response):
        item = KomodoroItem()

        extract = response.css('div[class=midLeft] a::attr(href)').extract()
        if len(extract) == 0:
            return None
        item['title'] = response.css('h1[class=title]::text').extract()
        item['url'] = response.url    
        item['news_category'] = extract[0][27:]
        item['news_summary'] = response.css('h2[class=dtlSpot]::text').extract()
        item['news_date'] = response.css('div[class=newsDate]::text').extract()
        interval = pq(response.body)   
        item['news_text'] = interval(".detailText").text()
        
        return item