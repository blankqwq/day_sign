import requests
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    filename='current.txt',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

TOKEN = os.getenv("TOKEN").strip() if os.getenv("TOKEN") is not None else ''
SESSION = os.getenv("SESSION").strip() if os.getenv("SESSION") is not None else ''
ADDRESS = os.getenv("ADDRESS").strip() if os.getenv("ADDRESS") is not None else ''
PUBLISH_KEY = os.getenv("PUBLISH_KEY").strip() if os.getenv("PUBLISH_KEY") is not None else ''

host = "https://student.wozaixiaoyuan.com"
# 头部信息，只需要修改token值
headers = {
    "Host": "student.wozaixiaoyuan.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 "
                  "Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Referer": "https://servicewechat.com/wxce6d08f781975d91/147/page-frame.html",
    "Cookie": f"SESSION={SESSION}; path=/; HttpOnly",
    "token": f"{TOKEN}"
}


def getAddr(addr):
    keys = ['latitude', 'longitude', 'country', 'province', 'city', 'district', 'township', 'street', 'areacode']
    return dict(zip(keys, addr.split('|')))


addressData = getAddr(ADDRESS)


def getSignMessage(doSigning=True):
    url = "/sign/getSignMessage.json"
    data = {
        "page": 1,
        "size": 5
    }
    res = requests.post(host + url, headers=headers, data=data)
    resData = res.json()
    logger.info(f"获取签到信息成功")
    if resData['code'] == 0:
        if doSigning:
            reqData = resData['data'][0]
            doSign(reqData)
        else:
            return resData["data"]
    else:
        logger.error(f"获取签到内容 -- 失败")


def doSign(reqData):
    logger.info(f"{reqData['title']} -- 开始签到")
    if reqData['type']:
        logger.info(f"{reqData['title']} -- 已签到，跳过签到流程")
        return
    url = "/sign/doSign.json"
    data = {
        "id": reqData['logId'],
        "signId": reqData['id'],
        "latitude": addressData['latitude'],
        "longitude": addressData['longitude'],
        "country": addressData['country'],
        "province": addressData['province'],
        "city": addressData['city'],
        "district": addressData['district'],
        "township": addressData['township']
    }
    res = requests.post(host + url, headers=headers, json=data).json()
    if res['code'] == 0:
        logger.info(f"{reqData['title']} -- 签到成功!!")
    else:
        logger.error(f"健康签到失败：{res}")


def healty():
    url = "/health/getToday.json"
    res = requests.post(host + url, headers=headers).json()
    if res['code'] != 0:
        logger.error(f'异常错误')
        return
    country = res['data'].get('country')
    if country == '' or country is None:
        logger.info(f'开始签到')
        saveHealth()
    else:
        logger.error(f'已签到跳过签到')


def saveHealth():
    url = "/health/save.json"
    headers["content-type"] = "application/x-www-form-urlencoded"
    data = {
        "answers": '["0","0","2"]',
        "latitude": addressData['latitude'],
        "longitude": addressData['longitude'],
        "country": addressData['country'],
        "city": addressData['city'],
        "district": addressData['district'],
        "province": addressData['province'],
        "township": addressData['township'],
        "street": addressData['street'],
        "areacode": addressData['areacode']
    }
    res = requests.post(host + url, headers=headers, data=data).json()
    if res['code'] == 0:
        logger.info(f"健康签到成功{res}")
    else:
        logger.error(f"健康签到失败:{res}")


def getUserInfo():
    url = '/my/getUserInfo.json'
    res = requests.post(host + url, headers=headers).json()
    return res['code'] == 0, res['data']


def notify(content):
    url = f'https://sc.ftqq.com/{PUBLISH_KEY.strip()}.send'
    requests.get(url, params={"text": "我在校园打卡", "desp": content})


def main():
    infoOk, userInfo = getUserInfo()
    if infoOk:
        getSignMessage()
        healty()
        with open('./current.txt', 'r') as f:
            result = f"```\n姓名: {userInfo['name']}\n{f.read()}\n```"
    else:
        result = '签到失败,信息过期或错误'
    if PUBLISH_KEY is not None or PUBLISH_KEY != '':
        notify(result)
    else:
        print("请输入提醒KEY")


if __name__ == "__main__":
    main()
