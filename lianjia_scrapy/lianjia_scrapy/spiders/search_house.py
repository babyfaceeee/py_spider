import scrapy
from lianjia_scrapy.items import HouseItem

#  scrapy crawl search_house

class SearchHouseSpider(scrapy.Spider):
    name = "search_house"
    allowed_domains = ["bj.lianjia.com"]
    # start_urls = ["https://bj.lianjia.com/ershoufang/pg40rs%E5%A4%A9%E9%80%9A%E8%8B%91/"]
    # TODO 只有前33页有数据，可以按需要改成33
    max_page = 1

    async def start(self):
        yield self.create_page_requests(1)

    def create_page_requests(self, page):
        url = f'https://bj.lianjia.com/ershoufang/pg{page}rs%E5%A4%A9%E9%80%9A%E8%8B%91/'
        if page > self.max_page:
            return None
        return scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse,
            meta = {"page":page}
        )

    def parse(self, response):
        self.logger.debug(f'当前正在请求第{response.meta["page"]}页')
        try:
            house_element_list = response.xpath("//li[contains(@class, 'LOGCLICKDATA')]//div[@class='title']")
            self.logger.debug(f"页面中有{len(house_element_list)}个房源信息")
            # 解析每个信息卡片
            for house_element in house_element_list:
                house_title_list = house_element.xpath(".//a[1]/text()").getall()
                if len(house_title_list) == 0:
                    raise Exception("列表页解析失败")
                house_title = "".join(house_title_list)
                # 获取详情页url
                house_url = house_element.xpath(".//@href").get()
                if house_url is None or house_url.strip() == "":
                    raise Exception("列表页URL解析失败")
                house_url = house_url.strip()
                # 获取标签
                house_tag_list = house_element.xpath(".//span[contains(@class, 'tagBlock')]/text()").getall()
                house_tag = "".join(house_tag_list)
                # self.logger.debug(f"房子标题：{house_title}，url：{house_url}，标签：{house_tag}")
                yield scrapy.Request(
                    url=house_url,
                    method='GET',
                    callback=self.parse_house_detail,
                    meta={"house_title":house_title,
                          "house_tag":house_tag}
                )
            # 分页逻辑
            next_page = response.meta["page"] + 1
            if next_page <= self.max_page:
                yield self.create_page_requests(next_page)


        except Exception as e:
            self.logger.error(f'列表页解析异常：{e}')

    def parse_house_detail(self, response):
        item = HouseItem()
        house_title = response.meta["house_title"]
        item['title'] = house_title
        item['house_tag'] = response.meta["house_tag"]
        try:
            # 总价
            total_price_element = response.xpath("/html/body/div[5]/div[2]/div[3]/div/span[1]/text()").get()
            # total_price_element = response.xpath("//div[@class='price-container']//div[@class='price']/span[@class='total']/text()").get()
            item['total_price'] = total_price_element
            # 单价
            unit_price_element = response.xpath("/html/body/div[5]/div[2]/div[3]/div/div[1]/div[1]/span/text()").get()
            # unit_price_element = response.xpath("//div[@class='price-container']//div[@class='price']//div[@class='unitPrice']/span[@class='unitPriceValue']/text()").get()
            item['unit_price'] = unit_price_element
            # 小区名
            community_element = response.xpath("/html/body/div[5]/div[2]/div[5]/div[1]/a[1]/text()").get()
            item['community_name'] = community_element
            # 所处位置
            region_element = response.xpath("//div[@class='areaName']//span[@class='info']//text()").getall()
            item['region_name'] = region_element
            # 房屋格局
            lay_out_element = response.xpath("//div[@class='room']/div[@class='mainInfo']/text()").get()
            item['lay_out'] = lay_out_element
            # 房屋面积
            area_element = response.xpath("//div[@class='area']/div[@class='mainInfo']/text()").get()
            item['area'] = area_element
            # 朝向
            orientation_element = response.xpath("//div[@class='type']/div[@class='mainInfo']/text()").get()
            item['orientation'] = orientation_element
            # 装修状态
            decorate_status_element = response.xpath("//div[@class='type']/div[@class='subInfo']/text()").get()
            item['decorate_status'] = decorate_status_element
            # 楼层
            floor_element = response.xpath("//div[@class='room']/div[@class='subInfo']/text()").get()
            item['floor'] = floor_element
            # 楼栋类型
            # building_type_element = response.xpath("//div[@class='base']//div[@class='content']/ul/li[6]/text()").getall()
            building_type_element = response.xpath("//*[@id='introduction']/div/div/div[1]/div[2]/ul/li[6]/text()").getall()
            item['building_type'] = building_type_element
            # 是否近地铁
            is_near_subway_element = response.xpath("//div[@class='areaName']/a[@class='supplement']/text()").get()
            item['is_near_subway'] = is_near_subway_element
            # 免税类型
            tax_free_type_element = response.xpath("//div[contains(@class, 'tags')]//a[contains(@class, 'taxfree')]/text()").get()
            item['tax_free_type'] = tax_free_type_element
            # 是否随时看房
            is_has_key_element = response.xpath("//div[@class='visitTime']/span[@class='info']/text()").get()
            item['is_has_key'] = is_has_key_element

            yield item

        except Exception as e:
            self.logger.error(f"解析详情页失败：{e}")