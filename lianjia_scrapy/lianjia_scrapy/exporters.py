from scrapy.exporters import CsvItemExporter
class CsvExportPipeline:
    def open_spider(self, spider):
        # 打开 CSV 文件
        self.file = open("lianjia_tiantongyuan.csv", "wb")
        # 初始化 CsvItemExporter
        self.exporter = CsvItemExporter(
            self.file,
            encoding="utf-8-sig",
            fields_to_export = [
            "title", "total_price", "unit_price", "community_name", "region_name",
            "lay_out", "area", "orientation", "decorate_status", "floor",
            "building_type", "house_tag", "is_near_subway", "tax_free_type", "is_has_key"
            ] # 指定表头的顺序
        )
        self.exporter.start_exporting()  # 写入表头

    def process_item(self, item, spider):
        # 将每个 item 写入 CSV
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 结束导出并关闭文件
        self.exporter.finish_exporting()
        self.file.close()

