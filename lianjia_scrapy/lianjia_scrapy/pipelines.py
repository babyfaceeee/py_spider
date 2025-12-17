# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LianjiaScrapyPipeline:
    def process_item(self, item, spider):
        def clean_text(text):
            if isinstance(text, str):
                cleaned = text.strip()
                return cleaned if cleaned else None
            return None
        # 清洗数据
        # 总价
        item["total_price"] = int(item["total_price"]) * 10000
        # 单价
        item['unit_price'] = int(item["unit_price"])
        # 小区名
        item['community_name'] = item['community_name'].strip()
        # 所处位置
        region_name_list = [clean_text(t) for t in item['region_name'] if clean_text(t)]
        item['region_name'] = "".join(item['region_name'])
        item['region_name'] = item['region_name'].replace('\xa0', '')
        # 房屋格局
        item['lay_out'] = item['lay_out'].strip()
        # 房屋面积
        item['area'] = item['area'].strip()
        # 朝向
        item['orientation'] = item['orientation'].strip()
        # 装修状态
        item['decorate_status'] = item['decorate_status'].strip()
        # 楼层
        item['floor'] = item['floor'].strip()
        # 楼栋类型
        cleaned_list = [clean_text(t) for t in item['building_type'] if clean_text(t)]
        item['building_type'] = "".join(cleaned_list)
        # 是否近地铁
        item['is_near_subway'] = item.get('is_near_subway') not in [None, '', False]
        # 免税类型
        tax_free_type_list = [clean_text(t) for t in item['tax_free_type'] if clean_text(t)]
        item['tax_free_type'] = "".join(tax_free_type_list)
        # 是否随时看房
        item['is_has_key'] = (item['is_has_key'] == '提前预约随时可看')

        # spider.logger.debug(item)
        return item