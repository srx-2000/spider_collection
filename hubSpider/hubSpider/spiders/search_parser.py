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
            first=response.xpath("//div[@class='pagination ']/ul/li[last()-1]/a/text()").extract()
            if len(first)==0:
                first = response.xpath("//div[@class='pagination']/ul/li[last()-1]/a/text()").extract()
            total_page=first[0]
            for i in range(1,int(total_page)):
                url_list.append(search_url+"&p="+str(i))
            yield scrapy.Request(url=search_url+"&p="+str(int(total_page)-1),callback=self.parse)
        else:
            with open('../video/video_url.txt', mode='w', encoding="utf-8") as f:
                for i in url_list:
                    f.write(i + "\n")
            f.close()

if __name__ == '__main__':
    cmdline.execute("scrapy crawl xhub".split())