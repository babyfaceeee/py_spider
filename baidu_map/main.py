from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException
from PIL import Image
from io import BytesIO
import time
import os
import re

# 截图路线地图
def screenshot_line(scheme_name):
    mask_element = driver.find_element(By.ID, "mask")
    map_img_bytes = mask_element.screenshot_as_png
    img_file_dir = f"map_images/{start}-{end}"
    if not os.path.exists(img_file_dir):
        os.makedirs(img_file_dir)
        print(f"已创建图片目录：{img_file_dir}")
    image_obj = Image.open(BytesIO(map_img_bytes))
    img_file_path = f"{img_file_dir}/{scheme_name}.png"
    image_obj.save(img_file_path)

# 解析路线详情信息
def pares_route_detail(route_li_element):
    """
    详情列表：
    位于 class=info-table 的 table 标签下面的 tr 标签，每个 tr 标签的 data-type 表示步行或者公交/地铁。
    步行：
    <td class="transferDetail">
        <p class="walkdisinfo">步行&nbsp;
            <a class="cs">240米</a>
        </p>
    </td>
    BUS：
    上车站点：
    <div class="getonstop">
            <a class="ks" data-tindex="0" data-cindex="1">环球度假区</a>站
    </div>
    下车站点：
    <div class="getoffstop">
        <a class="ks" data-tindex="0" data-cindex="2">天安门西</a>站
        <span>（A西北口出）</span>
        下车&nbsp;&nbsp;
    </div>
    公交或地铁线路名称：
    <span class="line-name">地铁1号线八通线</span>
    线路起始结束站（行进方向）：
    <span class="l-grey direction">（环球度假区-福寿岭）</span>
    行驶站数：
    <span class="kl">
        <a class="cs tf">22站</a>
    </span>
    """
    route_li_element.click()
    time.sleep(1.5)
    table_element = route_li_element.find_element(By.CLASS_NAME, "info-table")
    tr_elements = table_element.find_elements(By.TAG_NAME, "tr")
    print("以下是路线的分段路径：")
    for tr_element in tr_elements:
        data_type = tr_element.get_attribute("data-type") # 获取data_type属性的值,不同的值代表了不同的交通方式
        transfer_detail_element = tr_element.find_element(By.CLASS_NAME, "transferDetail")
        if data_type.strip() == "walk":
            walk_distance_element = transfer_detail_element.find_element(By.CLASS_NAME, "walkdisinfo")
            walk_distance = walk_distance_element.text
            print(f"分段类型：{data_type}，距离：{walk_distance}")
        elif data_type.strip() == "bus":
            # 提取上车站
            getonstop_element = transfer_detail_element.find_element(By.CLASS_NAME, "getonstop")
            start_station = getonstop_element.text
            # 提取下车站
            getoffstop_element = transfer_detail_element.find_element(By.CLASS_NAME, "getoffstop")
            end_station = getoffstop_element.text
            # 提取路线信息
            kl_element = transfer_detail_element.find_element(By.CLASS_NAME, "kl")
            line_name_element = kl_element.find_element(By.CLASS_NAME, "line-name")
            line_name = line_name_element.text
            # 提取始发站和终点站
            line_direction = "未提供"
            try:
                line_direction_element = kl_element.find_element(By.CSS_SELECTOR, ".l-grey.direction")
                line_direction = line_direction_element.text
            except NoSuchElementException:
                print("地铁或公交没有提供始末站数据")
            # 提取沿途站点数
            line_via_station_element = kl_element.find_element(By.CSS_SELECTOR, ".cs.tf")
            line_via_station_cnt = line_via_station_element.text
            print(f"分段类型：{data_type}，线路名：{line_name}，上车站点：{start_station}，下车站点：{end_station}，"
                  f"线路始末站：{line_direction}，途经站点数：{line_via_station_cnt}")
        else:
            print(f"未知交通类型：{data_type=}")


# 解析路线基本信息
def parse_route_basic(route_li_element):
    """
    票价：
    <span class="schemePrice"><font>票价<span class="yuanStance">¥</span>6</font></span>
    路线标签：
    <span class="schemeTag" style="background: #67C395"><font color="#ffffff">直达</font></span>
    路线名称div：
    class="schemeName"
    路线耗时：
    <span class="bus_time">1小时27分钟</span>
    距离：
    <span id="blDis_0">33.0公里</span> //blDis_0里最后的数字是序号，定位时要模糊匹配
    步行距离：
    最后一个span元素
    """
    route_head_element = route_li_element = route_li_element.find_element(By.CLASS_NAME, "route-head")
    # 提取票价
    scheme_price_element = route_head_element.find_element(By.CLASS_NAME, "schemePrice")
    scheme_price = scheme_price_element.text
    # 提取标签
    scheme_tag = "无"
    try:
        scheme_tag_element = route_head_element.find_element(By.CLASS_NAME, "schemeTag")
        scheme_tag = scheme_tag_element.text
    except NoSuchElementException:
        print("路线无标签")
    # 提取路线名称
    scheme_name_element = route_head_element.find_element(By.CLASS_NAME, "schemeName")
    scheme_name_text = scheme_name_element.text
    scheme_name_text = scheme_name_text.replace(" → ", "→")
    scheme_name_text_list = scheme_name_text.split(" ")
    scheme_name = scheme_name_text_list[-1]
    # 提取路线时长
    bus_time = route_head_element.find_element(By.CLASS_NAME, "bus_time")
    total_time = bus_time.text
    # 提取距离
    bl_dis_element = route_head_element.find_element(By.XPATH, "//span[contains(@id, 'blDis_')]")
    total_distance = bl_dis_element.text
    span_element = route_head_element.find_elements(By.TAG_NAME, "span")
    walk_distance_element = span_element[-1]
    walk_distance = walk_distance_element.text
    print(f"路线名称：{scheme_name}，票价：{scheme_price}，标签：{scheme_tag}，耗时：{total_time}，"
          f"距离：{total_distance}，步行距离：{walk_distance}")
    return scheme_name


# 解析路线列表
def parse_route_list():
    wait = WebDriverWait(driver, 10)
    route_list_element = wait.until(
        EC.visibility_of_element_located((By.ID, "route_list"))
    )
    route_li_elements = route_list_element.find_elements(By.TAG_NAME, "li")
    print(f"{len(route_li_elements)=}")
    for route_li_element in route_li_elements:
        # 1.解析路线基本信息
        scheme_name = parse_route_basic(route_li_element)
        # 2.解析路线详细信息
        pares_route_detail(route_li_element)
        # 3.截图保存
        screenshot_line(scheme_name)
        print()


# 输入起点和终点并点击公交车出行方式
def input_start_end(start, end):
    start_input = driver.find_element(By.CLASS_NAME, "route-start-input")
    start_input.send_keys(Keys.COMMAND+"a")
    start_input.send_keys(Keys.CONTROL, "a")
    start_input.send_keys(start)
    time.sleep(0.5)
    end_input = driver.find_element(By.CLASS_NAME, "route-end-input")
    end_input.send_keys(end)
    time.sleep(0.5)
    search_button = driver.find_element(By.ID, "search-button")
    search_button.click()
    time.sleep(2)
    # 默认出行方式是驾车，需要手动点击公共交通方式
    bus_tab = driver.find_element(By.CSS_SELECTOR, ".tab-item.bus-tab")
    bus_tab.click()
    time.sleep(1)

# 展开路线查询输入框
def show_search_box():
    route_button = driver.find_element(By.XPATH, '//div[@data-title="路线"]')
    route_button.click()
    time.sleep(1)

if __name__ == '__main__':
    service = Service("/Users/cy/Desktop/chromedriver/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get("https://map.baidu.com")

    # 1.展开路线查询输入框
    show_search_box()
    # 2.输入起点和终点，并点击搜索按钮
    start = "环球影城"
    end = "天安门"
    input_start_end(start, end)
    # 3.解析路线列表
    parse_route_list()

