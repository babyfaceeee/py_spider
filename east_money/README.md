# 东方财富股票数据爬虫与分析项目

## 项目简介

本项目基于 **Python + MySQL + Jupyter Notebook** 构建，实现了从 **东方财富网** 获取股票数据、存储数据库，并进行数据分析与可视化的完整流程。

项目主要功能包括：

* 股票列表数据爬取
* 股票详细信息抓取
* 股票所属板块信息抓取
* 数据清洗与结构化
* MySQL 数据库存储
* 历史数据与最新数据维护
* 数据分析与可视化

该项目适合作为：

* Python 爬虫学习项目
* 数据分析练习项目
* 金融数据处理示例

---

# 项目结构

```
.
main.py                  # 爬虫主程序
data_handler.py          # MySQL数据写入模块
data_analysis.ipynb      # 数据分析与可视化
README.md                # 项目说明
```

---

# 技术栈

* Python
* requests
* peewee ORM
* MySQL
* Jupyter Notebook
* pandas
* matplotlib / seaborn

---

# 数据采集流程

整体流程如下：

```
东方财富接口
      │
      ▼
获取股票列表
      │
      ▼
获取股票详情
      │
      ▼
获取股票所属板块
      │
      ▼
数据清洗
      │
      ▼
写入 MySQL 数据库
      │
      ▼
Jupyter 数据分析与可视化
```

---

# 爬虫功能说明

## 1 获取股票列表

通过东方财富接口获取股票列表，并按分页进行抓取。

获取内容包括：

* 股票代码
* 股票名称
* 股票数量统计

示例返回结构：

```
{
    "stock_cnt": 5000,
    "stock_code_list": ["600000", "600004", "600006"]
}
```

---

## 2 获取股票详情

针对每只股票获取详细数据，包括：

* 股票代码
* 股票名称
* 最新价格
* 涨跌幅
* 换手率
* 成交额
* 总市值
* 流通市值
* 市盈率
* 市净率
* 盈利情况
* 更新时间

示例数据结构：

```
{
    "stock_code": "600000",
    "stock_name": "浦发银行",
    "price": 10.52,
    "price_change_percent": 1.23,
    "turnover_rate": 0.45,
    "trading_volume": 123456789,
    "total_market_cap": 1000000000,
    "circulating_market_cap": 800000000,
    "dynamic_pe_ratio": 10.5,
    "static_pe_ratio": 11.2,
    "rolling_pe_ratio": 9.8,
    "pb_ratio": 1.2,
    "is_profitable": "是",
    "update_time": "2026-03-26"
}
```

---

## 3 获取股票所属板块

每只股票可能属于多个板块，例如：

* 银行
* 金融服务
* 上证50

示例结构：

```
[
    {
        "sector_code": "BK0481",
        "sector_name": "银行"
    }
]
```

---

# 数据库存储设计

项目使用 **Peewee ORM** 管理 MySQL 数据库。

数据库名：

```
spider_eastmoney
```

---

# 数据库表结构

## 1 股票历史数据表

表名：

```
stock_info_history
```

用途：

存储 **每日股票历史数据**

主键：

```
(history_date, stock_code)
```

主要字段：

| 字段                     | 说明    |
| ---------------------- | ----- |
| history_date           | 数据日期  |
| stock_code             | 股票代码  |
| stock_name             | 股票名称  |
| price                  | 当前价格  |
| price_change_percent   | 涨跌幅   |
| turnover_rate          | 换手率   |
| trading_volume         | 成交额   |
| total_market_cap       | 总市值   |
| circulating_market_cap | 流通市值  |
| dynamic_pe_ratio       | 动态市盈率 |
| static_pe_ratio        | 静态市盈率 |
| rolling_pe_ratio       | 滚动市盈率 |
| pb_ratio               | 市净率   |
| is_profitable          | 是否盈利  |
| spider_time            | 爬取时间  |

---

## 2 股票最新数据表

表名：

```
stock_info_latest
```

用途：

存储 **最新股票数据**

主键：

```
stock_code
```

每次爬虫执行会更新该表。

---

## 3 板块信息表

表名：

```
sector_info
```

字段：

| 字段          | 说明   |
| ----------- | ---- |
| sector_code | 板块代码 |
| sector_name | 板块名称 |

---

## 4 股票板块关系表

表名：

```
stock_sector
```

用于建立：

```
股票 ↔ 板块
```

多对多关系。

主键：

```
(stock_code, sector_code)
```

---

# 数据写入逻辑

写入数据时：

1. 写入 **历史表**
2. 更新 **最新数据表**
3. 写入 **板块信息**
4. 写入 **股票板块关系**

所有操作使用 **数据库事务**：

```
with db.atomic():
```

保证数据一致性。

---

# 数据分析与可视化

项目包含一个 `Jupyter Notebook` 文件：

```
stock_analysis.ipynb
```

用于：

* 从 MySQL 读取数据
* 使用 pandas 进行数据处理
* 数据统计分析
* 股票数据可视化

常见分析包括：

* 市值分布
* 市盈率分布
* 板块股票数量统计
* 涨跌幅分析

示例分析流程：

```
MySQL
  │
  ▼
pandas读取数据
  │
  ▼
数据清洗
  │
  ▼
数据统计
  │
  ▼
matplotlib / seaborn 可视化
```

---



# 数据库配置

修改 `data_handler.py` 中数据库连接配置：

```
db = MySQLDatabase(
    database="spider_eastmoney",
    host="localhost",
    port=3306,
    user="admin",
    passwd="12345678",
)
```

请根据自己的 MySQL 环境修改。

---

# 运行项目

## 1 创建数据库

在 MySQL 中创建数据库：

```
CREATE DATABASE spider_eastmoney;
```

---

## 2 运行爬虫

```
python spider.py
```

程序执行流程：

```
获取股票列表
      │
      ▼
获取股票详情
      │
      ▼
获取股票板块
      │
      ▼
写入 MySQL
```

---

## 3 数据分析

启动 Jupyter：

```
jupyter notebook
```

打开：

```
stock_analysis.ipynb
```

即可运行数据分析代码。

---

# 项目特点

* 使用 **多线程爬虫**
* 使用 **ORM 管理数据库**
* 支持 **历史数据与最新数据双表结构**
* 支持 **股票与板块多对多关系**
* 支持 **数据分析与可视化**

---

# 注意事项

1. 本项目仅用于 **学习与研究**。
2. 请勿高频访问目标网站接口。
3. 使用数据请遵守相关法律法规。

---

# 后续优化方向

可扩展功能：

* 增加代理池
* 请求重试机制
* 日志系统
* 定时任务（Airflow / cron）
* 分布式爬虫
* Web 数据展示

---

# License

MIT License
