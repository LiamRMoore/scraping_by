import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector



# lua script for splash to get list of links
show_ortho_links_lua = ("""
function main(splash, args)
  splash.private_mode_enabled = false
  splash:set_user_agent("{user_agent}")
  url = args.url
  assert(splash:go(url))
  assert(splash:wait(1))
  download_button = assert(splash:select(
  	"{sel_download_button_css}"
  ))
  download_button:mouse_click()
  assert(splash:wait(1))
  -- click all folders
  local elems = splash:select_all("{sel_folder_css}")
  for i, elem in ipairs(elems) do
    elem:mouse_click()
    splash:wait(0.5)
  end
  splash:set_viewport_full()
  return splash:html()
end
""")




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

    def expand_folders(self, response):
        """ parse the html of the individual ortho pages
        """
        # grab the title (name of dataset e.g. Ortho Vlaanderen 2012...)
        title = response.xpath(
            '//section[@class="region"]/div/div/div/h1/text()'
        ).get()
        # parse it to resolve individual fields
        title_meta = parse_title(title, meta_keys=self.title_meta_keys)
        # submit splash JS req to expand downloadable folders and extract html
        # feed this to extract_orthos, passing the dataset title
        yield SplashRequest(
            url=response.url,
            callback=self.extract_orthos,
            endpoint="execute",
            args={
                'lua_source':show_ortho_links_lua.format(
                    user_agent=self.user_agent,
                    sel_download_button_css=sel_download_button_css,
                    sel_folder_css=sel_folder_css
                ),
                'wait':2
            },
            meta = title_meta
        )

    def extract_orthos(self, response):
        # find all file classes in expanded download folders
        sel_file_links = response.xpath('//span[@class="file"]')
        # loop over selectorlist, getting ortho links, names and filesizes
        for file in sel_file_links:
            item = VLOrthoItem()
            loader = ItemLoader(item=item,
                                selector=file)
            loader.add_value('page_url', response.url)
            loader.add_xpath('suffix', './/a/text()')
            loader.add_xpath('filesize', './/child::node()[2]')
            loader.add_xpath('filename', './/a/text()')
            loader.add_xpath('download_url', './/a/@href')
            # tag on the metadata associated with the whole dataset: year etc
            loader.add_value('dataset', response.request.meta.get('dataset'))
            for k in self.title_meta_keys:
                if k in response.request.meta and k in item.fields.keys():
                    loader.add_value(k, response.request.meta[k])
            yield loader.load_item()        
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

# JS prev/next
# //a[@id="ct100_maincontent_PagingHelperTop_btnPrevious"]
# //a[@id="ct100_maincontent_PagingHelperTop_btnNext"]
