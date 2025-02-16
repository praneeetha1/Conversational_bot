from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class GoogleJobSpider(CrawlSpider):
    name = "google_spider"
    allowed_domains = ["google.com"]
    start_urls = [
        "https://www.google.com/about/careers/applications/jobs/results/"
    ]

    rules = (
        Rule(
            LinkExtractor(
                restrict_css="a.WpHeLc.VfPpkd-mRLv6",
                deny=[
                    r'https://accounts\.google\.com',  # Exclude sign-in URLs
                    r'/about/careers/applications/apply'  # Exclude apply job URLs
                ]
            ),
            callback='parse_job_details',
            follow=True
        ),
    )
    
    custom_settings = {
        'DEPTH_LIMIT': 30, 
    }

    def parse_job_details(self, response):
        job_title = response.css("h2.p1N2lc::text").get()
        location = response.css("div.op1BBf span.r0wTof::text").get()

        if not job_title or not location:
            self.logger.info(f"Skipping page without job details: {response.url}")
            return
        
        job_url = response.url
        company_name = "Google"
        about_the_job = response.css("div.aG5W3 p::text").getall()

        responsibilities = []
        responsibilities_container = response.css("div.BDNOWe")
        if responsibilities_container:
            responsibilities_list = responsibilities_container.css("ul li::text").getall()
            responsibilities = "\n".join(responsibilities_list)

        qualifications = []
        qualifications_container = response.css("div.KwJkGe")
        if qualifications_container:
            qualifications_list = qualifications_container.css("ul li::text").getall()
            qualifications = "\n".join(qualifications_list)

        job_details = {
            'job_url': job_url,
            'job_title': job_title,
            'location': location,
            'company': company_name,
            'responsibilities': responsibilities,
            'qualifications': qualifications,
            'about the job': about_the_job
        }

        yield job_details

