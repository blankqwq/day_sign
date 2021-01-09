
# 我在校园自动打卡

> 感谢 [ruicky/jd_sign_bot](https://github.com/ruicky/jd_sign_bot) 项目，提供灵感

- 功能

 1. 检测今日是否打卡并打卡
 2. 检测今日是否健康签到并签到
 3. 发送提醒到方糖
 4. 每天检测签到三次
 
教程： [京东定时签到-GitHub 实现](https://ruicky.me/2020/06/05/jd-sign/)

与教程不同的是,需要添加四个变量
```
TOKEN           #抓取的token
SESSION         #抓取的session的值
ADDRESS         #例如 '28.682976|115.857972|中国|江西省|南昌市|红谷滩区|沙井街道|世贸路|360113'
                  对应关系 'latitude', 'longitude', 'country', 'province', 'city', 'district', 'township', 'street', 'areacode'
PUBLISH_KEY     #方糖的密钥
```

