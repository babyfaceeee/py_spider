## 流程
1. `search_house.py`爬取列表页+详情页数据并封装到`item`并`yield`
2. 在`items.py`中定义要爬取的字段，并将爬取到的数据存放进去
3. 在`pipelines.py`中对`Item`各字段数据进行清洗
4. 在`settings.py`中启用`exporters`管道
5. 在`exporters.py`中把`item`保存下来
### 总结
Spider 抓取 item → Pipeline 处理 → 下一个 Pipeline（exporters）保存数据 → 最终输出
