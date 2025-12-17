# 爬虫项目 README

本 README 用来**复习整个爬虫的设计思路和关键代码**，重点放在三件事上：

1. 多线程（ThreadPoolExecutor）是怎么工作的

2. 数据是如何稳定地写入 CSV / Excel 的

3. 为什么这套写法 **几乎不会触发网站 500 状态码**

   

---

## 一、项目整体结构（先有全局概念）

爬虫逻辑分为三层：

```
列表页（分页）
   ↓
详情页（并发抓取）
   ↓
数据汇总 → CSV → Excel
```

对应到代码里就是：

* `parse_list_page`：

  * 请求列表页
  * 提取所有详情页 URL
  * 控制分页 + 休眠

* `parse_detail_page`：

  * 请求详情页
  * 解析字段
  * 返回一条完整数据 dict

* `ThreadPoolExecutor`：

  * 只用于「详情页」并发
  * 列表页始终是 **单线程顺序执行**

---

## 二、为什么要“列表页单线程，详情页多线程”？

这是**防 500 的第一关键点**。

### 1️⃣ 列表页为什么不用多线程？

列表页 URL 非常规律：

```
/Cases/Latest/1
/Cases/Latest/2
/Cases/Latest/3
...
```

如果你并发请求这些页面：

* 短时间内命中大量分页
* 服务器容易判定为异常流量
* **直接返回 500 或临时封禁**

所以设计原则是：

> ✅ 列表页：慢一点，顺序来

---

### 2️⃣ 详情页为什么可以并发？

详情页的特点：

* URL 分散
* 单页数据量大
* 响应时间不一致

并发的好处：

* 提高整体效率
* 不会集中轰炸同一个接口

但前提是：

> ⚠️ 并发数量必须受控

代码里：

```python
MAX_WORKERS = 2
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    ...
```

`2 ~ 3` 是一个**非常安全的值**。

---

## 三、多线程核心代码逐行讲解（重点）

### 1️⃣ 提交任务

```python
futures = [pool.submit(parse_detail_page, url) for url in detail_urls]
```

这行代码做的事情：

* 不执行函数
* 只是把任务“交给线程池排队”
* 返回的是 `Future` 对象（任务凭证）

等价的低级写法：

```python
futures = []
for url in detail_urls:
    future = pool.submit(parse_detail_page, url)
    futures.append(future)
```

---

### 2️⃣ 收集执行结果

```python
for f in as_completed(futures):
    r = f.result()
    if r:
        results.append(r)
```

逐行解释：

* `as_completed(futures)`

  * 谁先执行完，谁先返回
  * 不按提交顺序

* `f.result()`

  * 拿到 `parse_detail_page` 的返回值
  * 等价于同步调用函数的结果

* `if r:`

  * 失败时返回 `None`
  * 避免把失败数据写入文件

这段逻辑的本质是：

> ✅ 并发爬取
> ✅ 顺序、安全地收结果

---

## 四、为什么不会频繁遇到 500 状态码（最重要）

这是设计层面的结果，不是运气。

### ✅ 原因一：请求节奏被“人为放慢”

```python
BATCH_PAGE_SIZE = 30
BATCH_SLEEP_SECONDS = 120
```

含义：

* 每爬 30 页
* 主动休息 2 分钟

这在服务器眼里是：

> 一个很有耐心的人

---

### ✅ 原因二：详情页失败立即降速

```python
DETAIL_FAIL_THRESHOLD = 3
DETAIL_FAIL_SLEEP = 300
```

逻辑是：

* 连续 3 个详情页失败
* 判定为被限制
* **主动休息 5 分钟**

这一步非常关键：

> 不是硬刚服务器
> 是见势不妙立刻停

---

### ✅ 原因三：所有请求都有重试 + 超时

```python
def fetch_with_retry(url, retries=3):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.text
        except Exception:
            time.sleep(2 + i)
```

好处：

* 网络抖动不会立刻失败
* 请求不会无限挂起

---

### ✅ 原因四：并发数量极低

```python
ThreadPoolExecutor(max_workers=2)
```

这几乎是：

> “我不是爬虫，我只是手快一点的人”

服务器基本不会防你。

---

## 五、字段解析逻辑（FIELD_MAP 的意义）

```python
FIELD_MAP = {
    '案例编号：': 'case_id',
    '案例名称：': 'case_title',
    ...
}
```

设计思想：

* 页面上的中文字段名
* 映射为程序里的英文 key

统一由一个函数处理：

```python
def extract_fields(content_element):
    case_data = {}
    for label, field_name in FIELD_MAP.items():
        case_data[field_name] = get_value(content_element, label)
    return case_data
```

好处：

* 增字段只改 `FIELD_MAP`
* 解析逻辑完全不用动

---

## 六、CSV → Excel 的安全写入逻辑

### 1️⃣ 先写 CSV（最稳）

```python
write_to_csv_append(results)
```

原因：

* CSV 写入快
* 追加安全
* 中断不容易坏文件

---

### 2️⃣ 最后统一转 Excel

```python
csv_to_excel("cases.csv", "cases.xlsx")
```

这样做的好处：

* 爬虫过程中不频繁操作 Excel
* Excel 文件完整、干净

---

## 七、你现在应该掌握的核心能力

如果你能理解这份 README，说明你已经掌握：

* 多线程爬虫的**安全用法**
* 如何控制请求节奏
* 如何写一个**不会被服务器讨厌**的爬虫

这已经超过「入门爬虫」的水平了。

---

## 八、复习建议（很重要）

复习顺序建议：

1. 先看 **整体流程图**
2. 再看 `parse_list_page`
3. 最后精读这三行：

```python
pool.submit
as_completed
f.result()
```

把这三句吃透，
你之后看到任何并发爬虫代码，
都不会再慌。

---

（这份 README 就是给未来的你看的，不是给别人交差用的）
