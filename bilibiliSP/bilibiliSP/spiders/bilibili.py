import scrapy


class BilibiliSpider(scrapy.Spider):
    base_url = "https://www.bilibili.com/video/BV1dK41137mr"
    up_uid = "7487399"

    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    base_up_url = "//space.bilibili.com/"
    up_url = base_up_url + up_uid + "/"
    start_urls = [base_url]
    allList = []
    file_handle = open('bilbili_Output.txt', mode='w', encoding='utf-8')

    def parse(self, response):
        up_url_list = response.xpath("//div[@class='count up']/a/@href").extract()
        video_url_list = response.xpath("//div[@class='video-page-card']/div/div/a[@class='title']/@href").extract()
        # print(video_url_list)

        if up_url_list:
            for i in range(0, len(up_url_list)):
                if up_url_list[i] == self.up_url:
                    video_url_list[i] = "https://www.bilibili.com" + video_url_list[i].split("?")[0]
                    # print(video_url_list[i])
                    if not self.allList.__contains__(video_url_list[i]):
                        self.allList.append(video_url_list[i])
                        self.file_handle.write(str(video_url_list[i]) + '\n')
                    yield scrapy.Request(video_url_list[i], callback=self.parse)
