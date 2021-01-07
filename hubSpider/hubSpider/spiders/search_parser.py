import scrapy
from scrapy import cmdline

key="teenager"


search_url="https://www.xvideos.com/?k={key}".format(key=key)
url_list=[search_url]


class xhub(scrapy.Spider):
    base_url="https://www.xvideos.com"
    start_urls = [search_url]
    name = "xhub"
    allowed_domains = ['xvideos.com']

    def parse(self, response):
        next=response.xpath("//a[@class='no-page next-page']/@href").extract()
        if next!=None and len(next)!=0:
            next_url=self.base_url + next[0]
            print(next_url)
            url_list.append(next_url)
            yield scrapy.Request(url=next_url,callback=self.parse)
        else:
            # print(url_list)
            with open('../video/video_url.txt', mode='w', encoding="utf-8") as f:
                for i in url_list:
                    # print(i)
                    f.write(i + "\n")
            f.close()

if __name__ == '__main__':
    cmdline.execute("scrapy crawl xhub".split())