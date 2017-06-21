import scrapy
from links.items import LinksItem

class LinksSpider(scrapy.Spider):
    name = "6080"
    hostname = "http://www.6080.tv"             # 站点域名
    allowed_domains = ["6080.tv"]
    start_urls = [
        "http://www.6080.tv/book/movie/"    # 6080的电影标签页
    ]

    def parse(self, response):
        """
        爬取电影标签列表，将每个电影链接传递给 parse_item 进行爬取电影具体信息
        """
        # 获取包含内容的部分
        list_movie = response.css("#body > div.imagewall_nav")
        # 该站将视频列表分为4列，按列进行获取
        for col in list_movie.css("#imagewall_container > div.share_col"):
            # 获取每一列的视频项
            for url_item in col.css("a::attr(href)").extract():
                #print("-------------------- Item --------------------")
                #print(url_item)
                #print("----------------------------------------------")
                # 将获取到的每一项链接转交给 parse_item 进行解析
                yield scrapy.http.Request(self.hostname + url_item, callback=self.parse_item)
        # 下一页按钮链接
        url_page_next = response.css("a.page_next::attr(href)").extract()[0]
        #print("-------------------- Next --------------------")
        #print(url_page_next)
        #print("----------------------------------------------")
        # 爬取下一页
        yield scrapy.http.Request(self.hostname + url_page_next, callback=self.parse)

    def parse_item(self, response):
        """
        搜集电影的具体信息，存储进 LinksItem 并返回
        """
        link = LinksItem()
        movie = response.css("#content > div.note_content")     # 获取视频详情内容部分
        link["name"] = movie.css("span.tit::text").extract()    # 视频名称
        link["url"] = response.url                              # 视频所在 url
        link["acts"] = movie.css("div.detail-info > span:nth-child(1) > a::text").extract() # 演员列表
        link["categorys"] = movie.css("div > span:nth-child(3) > a::text").extract()        # 视频分类
        link["description"] = movie.css("div.juqing > p::text").extract()                   # 视频描述
        link["hot"] = movie.css("div.vodplay > span.playcount > em::text").extract()[1]     # 人气
        link["rank"] = movie.css("div.vodplay > span.playcount > em::text").extract()[0]    # 评分
        link["download_url"] = movie.css("#vodlist > ul > li > input.durl::attr(value)").extract()  # 下载链接
        link["size"] = movie.css("div > div.detail-info > span:nth-child(4) > span:nth-child(6)::text").extract()   # 视频时长
        yield link
