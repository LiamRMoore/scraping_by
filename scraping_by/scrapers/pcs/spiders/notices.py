import scrapy

# from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from scraping_by.scrapers.pcs.items import PcsItem


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
)
p = PcsItem()


class NoticesSpider(scrapy.Spider):
    name = "notices"
    allowed_domains = [
        "www.publiccontractsscotland.gov.uk",
        "publiccontractsscotland.gov.uk",
    ]
    base_url = allowed_domains[0]
    starting_url = (
        "https://www.publiccontractsscotland.gov.uk/Search/Search_MainPage.aspx"
    )
    user_agent = USER_AGENT  # (
    # "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
    # )

    wait_load: float = 0.5
    wait_next_page: float = 2.5
    contract_link_xpath = "//a[@class='ns-list-link pcs-focus']"

    def start_requests(self):
        yield SplashRequest(
            url=self.starting_url,
            callback=self.parse,  # method to interpret html response
            headers={"User-Agent": self.user_agent},
        )

    def parse(self, response):
        """
        N.B. - recursive
        """
        print("** top level parse **")
        for ix, link in enumerate(response.xpath(self.contract_link_xpath)):
            title = link.xpath("./text()").get()
            rel_link = link.xpath("./@href").get()
            full_link = self.base_url + rel_link
            print("found project:", title, "\n->", full_link)
        else:
            print("on to next page...")
            print(response.url)
            print(type(response), dir(response))
            # print(self.next_page_lua)
            yield SplashRequest(
                url=response.url,
                callback=self.parse,  # recursive
                endpoint="execute",  # run a lua script
                args=dict(
                    lua_source=self.next_page_lua
                ),  # source for script to run,
                dont_filter=False,
                # cookies=response.cookies
            )

    @property
    def next_page_lua(self):
        s = (
            """
            function main(splash, args)
                splash:init_cookies(splash.args.cookies)
                splash:set_user_agent("{user_agent}")
                splash.private_mode_enabled = true
                url = args.url
                assert(
                    splash:go{{
                        url,
                        headers=splash.args.headers,
                        http_method=splash.args.http_method,
                        body=splash.args.body
                    }}
                )
                assert(splash:wait({wait_load}))
                --
                --
                next_page_btn = assert(
                    splash:select(
                        "#ctl00_maincontent_PagingHelperTop_btnNext"
                    )
                )
                assert(next_page_btn:mouse_click())
                assert(splash:wait({wait_next_page}))

                local entries = splash:history()
                local last_response = entries[#entries].response

                return {{
                    url = splash:url(),
                    html = splash:html(),
                    headers = last_response.headers,
                    cookies = splash:get_cookies(),
                    http_status = last_response.status
                }}
            end
            """
        ).format(
            user_agent=self.user_agent,
            wait_load=self.wait_load,
            wait_next_page=self.wait_next_page,
        )
        return s


# # notice tab 1 (introduction) table rows
# xpath_select_intro_table_rows = "//div[@class='rmpView MultiPage']//tr"
# # header key, value
# # /th[1] : /th[2]
# # other key, value
# # /td[1] : /td[2]

# # export to HTML selector
# xpath_select_html_download = (
#     "//a[@id='ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_"
#     "notice_introduction1_cmdExportHTML']"
# )
#

# convert html text to selector object
# from scrapy.Selector import selector
# s = Selector(text=r2text)
# //h2[5]

# JS prev/next
# //a[@id="ct100_maincontent_PagingHelperTop_btnPrevious"]
# //a[@id="ct100_maincontent_PagingHelperTop_btnNext"]
