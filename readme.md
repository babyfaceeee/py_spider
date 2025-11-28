好的，我帮你写一个更简洁、易读、带截图示例的 `README.md`，适合新手快速上手：

````markdown
# Baidu Map 公交路线爬取与截图工具

一个使用 **Python + Selenium + PIL** 的百度地图路线爬取工具。  
可以获取两点间的公交/地铁路线信息，并将路线截图保存到本地。

---

## 功能特点

- 输入起点和终点，自动获取公交/地铁路线。
- 获取每条路线的：
  - 路线名称
  - 票价
  - 路线标签（如直达/无堵车风险）
  - 总耗时
  - 总距离与步行距离
- 分段路线信息：
  - 步行段：距离
  - 公交/地铁段：上车站、下车站、线路名、始末站、途经站数
- 保存路线地图截图，方便查看或做分析。

---

## 环境要求

- Python 3.8+
- Chrome 浏览器
- 对应版本 [ChromeDriver](https://chromedriver.chromium.org/downloads)
- Python 库：
  - `selenium`
  - `pillow`

安装依赖：

```bash
pip install selenium pillow
````

---

## 快速上手

1. 克隆仓库：

```bash
git clone https://github.com/你的用户名/baidu-map-route-scraper.git
cd baidu-map-route-scraper
```

2. 修改 `main.py` 中 ChromeDriver 路径：

```python
service = Service("/path/to/chromedriver")
```

3. 修改起点和终点：

```python
start = "环球影城"
end = "天安门"
```

4. 运行脚本：

```bash
python main.py
```

5. 查看截图：

* 路线截图保存在 `map_images/起点-终点/` 文件夹下
* 文件名对应路线名称，例如：

```
map_images/环球影城-天安门/地铁7号线→120路.png
```

---

## 输出示例

```text
路线名称：地铁7号线→120路，票价：8，标签：直达，耗时：1小时42分钟，总距离：35.2公里，步行距离：1.9公里
分段类型：walk，距离：步行240米
分段类型：bus，线路名：地铁7号线，起点站：环球影城，下车站：天安门，线路始末站：（环球影城-福寿岭），途经站点数：22站
```

截图示例：

![示例截图](map_images/example.png)  <!-- 运行后可替换为实际截图 -->

---

## 注意事项

* 脚本中有 `time.sleep()` 等等待时间，可根据网络状况调整。
* 路线名称包含特殊字符（如 `/`、`→` 等）会被自动处理，以防文件保存报错。
* 默认爬取公交/地铁路线，如果页面默认是驾车路线，会自动点击公交标签。

---

## 项目结构

```
├── main.py            # 主程序
├── map_images/        # 保存路线截图（运行时自动生成）
└── README.md
```

---

## 免责声明

本项目仅用于学习与技术交流，禁止商业用途。请遵守百度地图相关服务协议。

```

---

如果你愿意，我可以帮你再写一版 **GitHub 风格极简版**，让你的仓库首页更干净、更专业。  

你希望我做吗？
```
