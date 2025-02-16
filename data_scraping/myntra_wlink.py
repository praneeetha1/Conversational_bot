import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MyntraJobSpider(CrawlSpider):
    name = 'myntra_spider'
    allowed_domains = ["careers.myntra.com"]
    start_urls = ["https://careers.myntra.com/jobs/operations/"]

    rules = (
        Rule(LinkExtractor(allow=r'/job-detail/'), callback='parse_job_listings', follow=True),
    )

    def parse_job_listings(self, response):
        yield {
            'job_url': response.url,
            'job_title': response.css('div.container h1::text').get(),
            'company_name': 'Myntra',  
            'job_description': ' '.join(response.css('div.container p::text').getall()).strip()
        }