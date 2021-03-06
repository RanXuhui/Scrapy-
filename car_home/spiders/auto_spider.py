# -*- coding: utf-8 -*-
import scrapy
from car_home.items import CarHomeItem
import re

class AutoSpiderSpider(scrapy.Spider):
    name = 'auto_spider'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['http://autohome.com.cn/']

    def start_requests(self):
        reqs = []
        req = scrapy.Request("https://www.autohome.com.cn/beijing/")
        reqs.append(req)
        return reqs

    def parse(self, response):

        # hotcar-content → hatcar-n → list → name（车类型） → box(具体车名)
        Car_Calss_Web = response.xpath('//div[@class="hotcar-content"]')  # 选取所有所有div元素，且这些元素拥有值为homepage-hotcar的class属性

        # 热门车之外的豪华车、小型/其他....是动态界面
        # Car_Luxury = Car_Calss_Web.xpath('div[2]/div[1]')

        Car_Name = Car_Calss_Web.xpath('div[1]/div/div[2]/div/ul/li/div/p[@data-gcjid]') # 第二个div对应    # 具体到车的名字

        i = 0
        for Car in Car_Name:
            item = CarHomeItem()
            # 车名
            item['Car_Name'] = Car.xpath('string(a)').extract()[0]

            if i < 25:
                # 车的类型
                # item['Car_Class'] = Car_Class.xpath('div[1]/text()')[0].extract() bug
                item['Car_Class'] = Car_Calss_Web.xpath('div[1]/div[1]/div[1]/a/text()').extract()[0]  # item['Car_Class'] = Car_Class.xpath('div[1]/text()')[0].extract() bug

            elif 24 < i < 49:
                # 车的类型
                # item['Car_Class'] = Car_Class.xpath('div[1]/text()')[0].extract() bug
                item['Car_Class'] = Car_Calss_Web.xpath('div[1]/div[2]/div[1]/a/text()').extract()[0]  # item['Car_Class'] = Car_Class.xpath('div[1]/text()')[0].extract() bug

            elif 48 < i < 75:
                # 车的类型
                # item['Car_Class'] = Car_Class.xpath('div[1]/text()')[0].extract() bug
                item['Car_Class'] = Car_Calss_Web.xpath('div[1]/div[3]/div[1]/a/text()').extract()[0]  # item['Car_Class'] = Car_Class.xpath('div[1]/text()')[0].extract() bug

            i += 1

            Car_url_1 = Car.xpath('a').re('(?<=\/)\d+(?=\/)')      # 注意这里的Car_url_1是一个列表
            Car_url_2 = Car.xpath('a').re('=\d+')
            item['Car_url'] = Car_url_1 if 'https:' in Car_url_1 else ('https://www.autohome.com.cn/' + Car_url_1[0] + '/#pvareaid' +Car_url_2[0])

            yield scrapy.Request(url=item['Car_url'], meta={'item': item}, callback=self.parse_detail, dont_filter=True)


    def parse_detail(self, response):
        item = response.meta['item']
        # 新车指导价
        item['New_car_guide'] = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dt[1]/a[1]/text()').extract()[0]

        # 下面两项车商城报价和二手车报价是js/ajax动态生成的数据使用上面的方法无法爬取
        # item['Mall_price'] = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dt[2]/a[1]/text()')[0].extract()
        # item['Secondhand_price'] = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dt[3]/a[1]/text()')[0].extract()

        # item['Engine'] = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[2]/a/text()').extract()
        engines = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[2]/a/text()').extract()
        Engine = ''
        for i in range(len(engines)):
            Engine += engines[i] + ','
        item['Engine'] = Engine

        # a[0:-1]是变速箱属性
        # item['Speed_Changing_Box'] = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[3]/a/text()').extract()[:-1]
        Speeds = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[3]/a/text()').extract()[:-1]
        Speed = ''
        for i in range(len(Speeds)):
            Speed += Speeds[i] + ','
        item['Speed_Changing_Box'] = Speed

        # a[-1]是车体结构
        # item['Body_structure'] = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[3]/a/text()')[-1].extract()
        bodies = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[3]/a/text()')[-1].extract()
        Body = ''
        for i in range(len(bodies)):
            Body += bodies[i]
        item['Body_structure'] = Body

        colors =response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]/dl/dd[1]/div/a/div/div/text()').extract()
        Car_Color = ''
        for i in range(len(colors)):
            Car_Color += colors[i] + ','
        item['Car_Color'] = Car_Color

        yield item




