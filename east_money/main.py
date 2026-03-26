import requests
import json
import time
import re
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from data_handler import write_stock_data



PAGE_SIZE = 20
DEBUG = True          # 调试开关
DEBUG_MAX_PAGE = 3    # 调试时最多爬 3 页
MAX_WORKERS = 3       # 最大并发数

# 记录时间
def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")
log("spider start")

def convert_response_text_to_json(response_text):
    match = re.search(r"\((\{.*\})\)", response_text)
    if not match:
        return None
    return json.loads(match.group(1))

def get_stock_sector_list(stock_code, page_size=50):
    import requests
    url = f"https://push2.eastmoney.com/api/qt/slist/get?fltt=1&invt=2&cb=jQuery35106940878247661206_1766135609725&fields=f14%2Cf12%2Cf13%2Cf3%2Cf152%2Cf4%2Cf128%2Cf140%2Cf141&secid=1.{stock_code}&ut=fa5fd1943c7b386f172d6893dbfba10b&pi=0&po=1&np=1&pz={page_size}&spt=3&wbp2u=%7C0%7C0%7C0%7Cweb&_=1766135609726"
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://quote.eastmoney.com/kcb/688807.html',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Cookie': 'qgqp_b_id=0f6f97e2b65025a1f4377cec795b5e39; websitepoptg_api_time=1766127185627; st_si=37663920679155; st_nvi=SYgIxcdX6IyjDLH0EkXZidbd6; nid18=07b56f3cfb6c8f651ff3a37d1bda4fc7; nid18_create_time=1766127187656; gviem=CIX38v7KzzKGuxVuMfdBr4d61; gviem_create_time=1766127187656; fullscreengg=1; fullscreengg2=1; st_asi=delete; rskey=pP4kWQ0E0cXdNNVV4ZjhsSytnSFIvVStzZz09bQgUl; st_pvi=34903235960971; st_sp=2025-12-19%2014%3A53%3A05; st_inirUrl=https%3A%2F%2Fcn.bing.com%2F; st_sn=47; st_psi=20251219171326515-111000300841-2583043577'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        result_json = convert_response_text_to_json(response.text)
        data = result_json['data']
        total_cnt = int(data['total'])
        if total_cnt > page_size:
            return get_stock_sector_list(stock_code, total_cnt)
        sector_list = data['diff']
        sector_dict_list = []
        for sector in sector_list:
            sector_dict = {
                "sector_code": sector['f12'],
                "sector_name": sector['f14']
            }
            sector_dict_list.append(sector_dict)
        print(f"从属于{len(sector_dict_list)}个板块")
        return sector_dict_list

    except requests.exceptions.RequestException as e:
        print(f"获取所属板块失败：{e}")

def get_stock_detail(stock_code):
    url = f"https://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=1&cb=jQuery35102059772792351109_1766132978362&fields=f58%2Cf734%2Cf107%2Cf57%2Cf43%2Cf59%2Cf169%2Cf301%2Cf60%2Cf170%2Cf152%2Cf177%2Cf111%2Cf46%2Cf44%2Cf45%2Cf47%2Cf260%2Cf48%2Cf261%2Cf279%2Cf277%2Cf278%2Cf288%2Cf19%2Cf17%2Cf531%2Cf15%2Cf13%2Cf11%2Cf20%2Cf18%2Cf16%2Cf14%2Cf12%2Cf39%2Cf37%2Cf35%2Cf33%2Cf31%2Cf40%2Cf38%2Cf36%2Cf34%2Cf32%2Cf211%2Cf212%2Cf213%2Cf214%2Cf215%2Cf210%2Cf209%2Cf208%2Cf207%2Cf206%2Cf161%2Cf49%2Cf171%2Cf50%2Cf86%2Cf84%2Cf85%2Cf168%2Cf108%2Cf116%2Cf167%2Cf164%2Cf162%2Cf163%2Cf92%2Cf71%2Cf117%2Cf292%2Cf51%2Cf52%2Cf191%2Cf192%2Cf262%2Cf294%2Cf181%2Cf295%2Cf748%2Cf747%2Cf803&secid=1.{stock_code}&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=%7C0%7C0%7C0%7Cweb&dect=1&_=1766132978363"
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        result_json = convert_response_text_to_json(response.text)
        data = result_json['data']
        # 提取数据值
        price = data['f43']
        if "-" in str(price):
            print(f"股票已退市，跳过爬取，股票代码：{stock_code}")
            return None
        trading_volume = data['f48']            # 成交额
        stock_code = data['f57']                # 代码
        stock_name = data['f58']                # 股票名
        update_time = data['f86']               # 更新时间
        total_market_cap = data['f116']         # 总市值
        circulating_market_cap = data['f117']   # 流通市值
        dynamic_pe_ratio = data['f162']         # 动态市盈率
        static_pe_ratio = data['f163']          # 静态市盈率
        rolling_pe_ratio = data['f164']         # 滚动市盈率
        pb_ratio = data['f167']                 # 市净率
        turnover_rate = data['f168']            # 交易日换手率
        price_change_percent = data['f170']     # 交易日涨跌幅
        is_profitable = data['f288']            # 是否盈利，0是1否

        # 转换数据值
        price = float(int(price) / 100)
        price_change_percent = float(int(price_change_percent) / 100)
        turnover_rate = float(int(turnover_rate) / 100)
        dynamic_pe_ratio = float(int(dynamic_pe_ratio) / 100)
        static_pe_ratio = float(int(static_pe_ratio) / 100)
        rolling_pe_ratio = float(int(rolling_pe_ratio) / 100)
        pb_ratio = float(int(pb_ratio) / 100)
        is_profitable = "是" if is_profitable == 0 else "否"
        update_time = datetime.fromtimestamp(update_time)


        # 获取股票所属板块列表
        time.sleep(2)
        sector_dict_list = get_stock_sector_list(stock_code)
        stock_dict = {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "update_time": update_time,
            "price": price,
            "price_change_percent": price_change_percent,
            "trading_volume": trading_volume,
            "turnover_rate": turnover_rate,
            "total_market_cap": total_market_cap,
            "circulating_market_cap": circulating_market_cap,
            "is_profitable": is_profitable,
            "dynamic_pe_ratio": dynamic_pe_ratio,
            "static_pe_ratio": static_pe_ratio,
            "rolling_pe_ratio": rolling_pe_ratio,
            "pb_ratio": pb_ratio,
            "sector_dict_list": sector_dict_list
        }
        return stock_dict

    except Exception as e:
        print(f"获取详情页失败，e：{e}")

def get_stock_list(market_type, page_num):
    log(f"request page {page_num}")
    url = f"https://push2.eastmoney.com/api/qt/clist/get?np=1&fltt=1&invt=2&cb=jQuery37108075555763970431_1766133682788&fs={market_type}&fields=f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23&fid=f3&pn={page_num}&pz=20&po=1&dect=1&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=|0|0|0|web&_=1766133682791"

    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(f"url:{url}")
        response.raise_for_status()
        result_json = convert_response_text_to_json(response.text)
        data = result_json['data']
        stock_cnt = data['total']       # 股票总数
        stock_list = data['diff']       # 股票列表
        stock_code_list = []            # 股票代码
        for stock in stock_list:
            stock_code_list.append(stock['f12'])
        # 返回字典数据
        stock_list_dict = {
            "stock_cnt": stock_cnt,
            "stock_code_list": stock_code_list
        }
        print(f"{stock_list_dict=}")
        time.sleep(2.5)
        return stock_list_dict
    except requests.exceptions.RequestException as e:
        print(e)
        traceback.print_exc()
        print('获取股票列表失败，e：',{e})

def crawl_detail(stock_code_list):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(get_stock_detail, code): code for code in stock_code_list}
        for future in as_completed(futures):
            try:
                data = future.result()
                if data:
                    results.append(data)
            except Exception as e:
                print(f"解析详情页失败：{e}")

    return results

def spider_stock_data(market_type, _start_page):
    try:
        stock_dict = get_stock_list(market_type, _start_page)
        stock_cnt = stock_dict['stock_cnt']                 # 股票总数
        stock_code_list = stock_dict['stock_code_list']     # 股票代码列表
        print(f'股票总数：{stock_cnt}')
        # 根据股票总数实现分页循环
        total_page = (stock_cnt+PAGE_SIZE-1)//PAGE_SIZE
        print(f"总共有 {total_page} 页")
        end_page = total_page
        if DEBUG:
            end_page = min(total_page, DEBUG_MAX_PAGE)
            print(f"【调试模式】只爬前 {end_page} 页")
        for page_num in range(_start_page, end_page + 1):
            print(f"\n===== 正在爬取第 {page_num} 页 =====")
            stock_list_dict = get_stock_list(market_type, page_num)
            stock_code_list = stock_list_dict['stock_code_list']
            print(f"本页共 {len(stock_code_list)} 支股票，正在开始并发抓取详情")
            detail_results = crawl_detail(stock_code_list)
            print(f"本页成功抓到 {len(stock_code_list)} 条数据")
            for detail in detail_results:
                write_stock_data(detail)
            time.sleep(2)
    except Exception as e:
        current_time = datetime.datetime.now()
        print(f"程序遇到异常！当前页码：第{page_num}页。异常时间：{current_time}")




if __name__ == '__main__':
    # 上证A股：m:1+t:2+f:!2,m:1+t:23+f:!2
    # 深证A股：m:0+t:6+f:!2,m:0+t:80+f:!2
    start_page = 1
    spider_stock_data('m:1+t:2+f:!2,m:1+t:23+f:!2', start_page)
    log("spider finished")
