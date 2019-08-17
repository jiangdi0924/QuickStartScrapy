import scrapy
from demo.items import Jobs

class JobsSpider(scrapy.spiders.Spider):
    name = 'jobs'
    start_urls = ['https://learnku.com/laravel/c/jobs']

    def parse(self, response):
        list_urls = response.selector.xpath(
            "//*[contains(@class, 'content pl-3 pr-3')]//*[contains(@class, 'topic-title-wrap rm-tdu')]/@href").extract()
        next_page = response.selector.xpath(
            "//*[contains(@class, 'page-link')]/@href"
        )[-1].extract()

        for info_url in list_urls:
            yield scrapy.Request(info_url, callback=self.content)
            
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
    def content(self, response):
        item = Jobs()
        item['title'] = response.selector.xpath(
            '/html/body/div[2]/div[1]/div/div[1]/div[1]/div/h1/div[1]/span/text()').extract_first()
        item['created_at'] = response.selector.xpath(
            '/html/body/div[2]/div[1]/div/div[1]/div[1]/div/p/a[2]/@data-tooltip').extract_first()
        yield item    
