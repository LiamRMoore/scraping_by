import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector


class NoticesSpider(CrawlSpider):
    name = 'notices'
    allowed_domains = ['www.publiccontractsscotland.gov.uk/', 'publiccontractsscotland.gov.uk']
    start_urls = ['https://www.publiccontractsscotland.gov.uk/Search/Search_MainPage.aspx']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'


    #"//tr[@class='pcs-tbl-row']"
    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=["//a[@class='ns-list-link pcs-focus']"]
            ),
            callback='parse_item',
            follow=True,
            process_request='set_user_agent'
        ),
    )


    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.publiccontractsscotland.gov.uk/Search/Search_MainPage.aspx',
            headers={'User-Agent': self.user_agent}
        )

    def parse_item(self, response):
        item = {}
        item["user-agent"] = response.request.headers["User-Agent"]
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        print("*\nfound contract: ", response.url)
        return item

# notice tab 1 (introduction) table rows
xpath_select_intro_table_rows = "//div[@class='rmpView MultiPage']//tr"
# header key, value
# /th[1] : /th[2] 
# other key, value
# /td[1] : /td[2]

# export to HTML selector
xpath_select_html_download = (
    "//a[@id='ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_"
    "notice_introduction1_cmdExportHTML']"
)
# 

# convert html text to selector object
# from scrapy.Selector import selector
# s = Selector(text=r2text)
# //h2[5]