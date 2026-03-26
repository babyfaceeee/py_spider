import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Current-Site': '510100',
    'Origin': 'https://zw.cdzjryb.com',
    'Request-Source': 'WEB',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
    'X-EIS-DOWN-ORG-ID': 'fd45fe77-98d2-487a-a785-dea0e925f6da',
    'X-EIS-REQUEST-HASH': 'c6912f41da6607e5a5ed5f8d48a202bf3f3a10a835d618861c89b88fe0981931',
    'X-EIS-REQUEST-ID': 'abd91e24-e1b3-9f03-663c-17b3911626c7',
    'X-EIS-TIMESTAMP': '1774420825480',
    'X-Eis-Authorization': '',
    'X-Eis-Tenant-id': 'chengdu',
    'business-source': 'WEB',
    'hsweb-auth': '',
    'portal-auth': 'undefined',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

json_data = {
    'dicHsipTypeCode': 'TH',
    'pageNo': 1,
    'pageSize': 5,
    'total': 0,
    'regionCode': '',
    'houseTypes': [],
    'unitPrices': [],
    'statusList': [],
    'regionCodes': [],
}

response = requests.post(
    'https://zw.cdzjryb.com/cd_jcfw_gateway/hsweb/buyHouse/findProjectRegistrationList',
    headers=headers,
    json=json_data,
)

print(response.json())

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"dicHsipTypeCode":"TH","pageNo":1,"pageSize":5,"total":0,"regionCode":"","houseTypes":[],"unitPrices":[],"statusList":[],"regionCodes":[]}'
#response = requests.post(
#    'https://zw.cdzjryb.com/cd_jcfw_gateway/hsweb/buyHouse/findProjectRegistrationList',
#    headers=headers,
#    data=data,
#)