from peewee import MySQLDatabase, Model
from peewee import CharField, DecimalField, DateField, DateTimeField, CompositeKey
import datetime

# 连接数据库
db = MySQLDatabase(
    database = "spider_eastmoney",
    host = "localhost",
    port = 3306,
    user = "admin",
    passwd = "12345678",
)


# 创建数据库表的模型类
class StockInfoHistory(Model):      # 对应 stock_info_history 表
    history_date = DateField()
    stock_code = CharField()
    stock_name = CharField()
    update_time = DateTimeField()
    price = DecimalField()
    price_change_percent = DecimalField()
    turnover_rate = DecimalField()
    trading_volume = DecimalField()
    total_market_cap = DecimalField()
    circulating_market_cap = DecimalField()
    dynamic_pe_ratio = DecimalField()
    static_pe_ratio = DecimalField()
    rolling_pe_ratio = DecimalField()
    pb_ratio = DecimalField()
    is_profitable = CharField()
    spider_time = DateTimeField()

    @classmethod
    def get_instance(cls, stock_dict):
        return cls(
            history_date=stock_dict['update_time'].date(),
            stock_code=stock_dict['stock_code'],
            stock_name=stock_dict['stock_name'],
            update_time=stock_dict["update_time"],
            price=stock_dict["price"],
            price_change_percent=stock_dict["price_change_percent"],
            turnover_rate=stock_dict['turnover_rate'],
            trading_volume=stock_dict['trading_volume'],
            total_market_cap=stock_dict['total_market_cap'],
            circulating_market_cap=stock_dict['circulating_market_cap'],
            dynamic_pe_ratio=stock_dict["dynamic_pe_ratio"],
            static_pe_ratio=stock_dict["static_pe_ratio"],
            rolling_pe_ratio=stock_dict["rolling_pe_ratio"],
            pb_ratio=stock_dict["pb_ratio"],
            is_profitable=stock_dict["is_profitable"],
            spider_time=datetime.datetime.now()
        )

    class Meta:
        database = db
        table_name = 'stock_info_history'
        primary_key = CompositeKey('history_date', 'stock_code')


# 个股信息表模型类
class StockInfoLatest(Model):
    stock_code = CharField(primary_key=True)
    stock_name = CharField()
    update_time = DateTimeField()
    price = DecimalField()
    price_change_percent = DecimalField()
    turnover_rate = DecimalField()
    trading_volume = DecimalField()
    total_market_cap = DecimalField()
    circulating_market_cap = DecimalField()
    dynamic_pe_ratio = DecimalField()
    static_pe_ratio = DecimalField()
    rolling_pe_ratio = DecimalField()
    pb_ratio = DecimalField()
    is_profitable = CharField()
    spider_time = DateTimeField()

    @classmethod
    def get_instance(cls, stock_dict):
        return cls(
            stock_code=stock_dict['stock_code'],
            stock_name=stock_dict['stock_name'],
            update_time=stock_dict["update_time"],
            price=stock_dict["price"],
            price_change_percent=stock_dict["price_change_percent"],
            turnover_rate=stock_dict['turnover_rate'],
            trading_volume=stock_dict['trading_volume'],
            total_market_cap=stock_dict['total_market_cap'],
            circulating_market_cap=stock_dict['circulating_market_cap'],
            dynamic_pe_ratio=stock_dict["dynamic_pe_ratio"],
            static_pe_ratio=stock_dict["static_pe_ratio"],
            rolling_pe_ratio=stock_dict["rolling_pe_ratio"],
            pb_ratio=stock_dict["pb_ratio"],
            is_profitable=stock_dict["is_profitable"],
            spider_time=datetime.datetime.now()
        )

    class Meta:
        database = db
        db_table = "stock_info_latest"


# 板块信息模型类
class SectorInfo(Model):
    sector_code = CharField(primary_key=True)
    sector_name = CharField()

    class Meta:
        database = db
        db_table = "sector_info"


# 个股与板块关系模型类
class StockSector(Model):
    stock_code = CharField()
    sector_code = CharField()

    class Meta:
        database = db
        db_table = "stock_sector"
        primary_key = CompositeKey('stock_code', 'sector_code')

# 写入个股数据历史表或个股数据表
def write_stock_info(stock_info_history):
    if type(stock_info_history) is StockInfoHistory:
        select_result = StockInfoHistory.select().where(
            (StockInfoHistory.stock_code == stock_info_history.stock_code) &
            (StockInfoHistory.history_date == stock_info_history.history_date)
        )
    else:
        select_result = StockInfoLatest.select().where(
            (StockInfoLatest.stock_code == stock_info_history.stock_code)
        )

    # 判断数据是否已经存在，如果存在则更新，不存在则插入
    is_insert = True
    if len(select_result) > 0:
        is_insert = False
    save_result = stock_info_history.save(force_insert=is_insert)
    print(f"是否插入：{is_insert}，模型类型：{stock_info_history}，保存结果：{save_result=}")

# 写入板块信息表
def write_sector_info(sector_code, sector_name):
    select_result = SectorInfo.select().where(SectorInfo.sector_code == sector_code)
    if len(select_result) == 0:
        create_result = SectorInfo.create(sector_code=sector_code, sector_name=sector_name)
        if create_result:
            print(f"板块信息写入成功，板块代码：{sector_code}，板块名称：{sector_name}")

# 写入个股与板块信息表
def write_stock_sector(stock_code, sector_code):
    select_result = StockSector.select().where(
        (StockSector.stock_code == stock_code) &
        (StockSector.sector_code == sector_code)
    )
    if len(select_result) == 0:
        create_result = StockSector.create(
            stock_code=stock_code,
            sector_code=sector_code
        )
        if create_result:
            print(f"个股与板块关系写入成功，股票代码：{stock_code}，板块代码：{sector_code}")



def write_stock_data(stock_dict):
    try:
        # 连接数据库
        try:
            db.connect(reuse_if_open=True)
        except Exception as e:
            raise
        # 开启事务
        with db.atomic():
            # 写入个股信息历史表
            stock_info_history = StockInfoHistory.get_instance(stock_dict)
            write_stock_info(stock_info_history)
            # 写入个股数据表
            stock_info_latest = StockInfoLatest.get_instance(stock_dict)
            write_stock_info(stock_info_latest)
            # 循环板块列列表，如果不存在则写入
            sector_dict_list = stock_dict['sector_dict_list']
            for sector_dict in sector_dict_list:
                sector_code, sector_name = sector_dict['sector_code'], sector_dict['sector_name']
                write_sector_info(sector_code, sector_name)
                # 写入个股与板块关系表
                write_stock_sector(stock_info_history.stock_code, sector_code)

    except Exception as e:
        print(f"写入mysql失败：{e}")
