# coding=utf-8
import hashlib
import requests
import random
import time
from .orc import recognize_img


success_daka = 1
failed_daka = 2
alredy_daka = 3


request_timecap = 2

def cap():
    time.sleep(request_timecap)

class qnyf():
    USERID = None       # 用户id

    YXDM = None         # 学校代码
    USER_NAME = None    # 姓名
    USER_NUMBER = None  # 学号
    USER_PASSWD = None  # 密码
    USER_LOC = None     # 打卡位置

    def __init__(self, YXDM, name, number, passwd, loc):
        self.YXDM = YXDM
        self.USER_NAME = name
        self.USER_NUMBER = number
        self.USER_PASSWD = passwd
        self.USER_LOC = loc

        self.USERID = self.getid()

    def sendpost(self, _url, _jsonusr):
        r = requests.post(_url, headers=self.getheader(), json=_jsonusr).json()
        if r['code'] == 200:
            if 'data' in r:
                return r['data']
        elif r['code'] == 400:
            msg = r['info']
            raise Exception(msg)
        else:
            raise Exception("Status Code Error")

    def sendget(self, _url, _params=None):
        if _params:
            r = requests.get(_url, headers=self.getheader(),
                             params=_params,  timeout=2).json()
        else:
            r = requests.get(_url, headers=self.getheader(), timeout=2).json()

        if r['code'] == 200:
            if 'data' in r:
                return r['data']
        elif r['code'] == 400:
            msg = r['info']
            raise Exception(msg)
        else:
            raise Exception("Status Code Error")

    def getid(self):
        pwd = hashlib.md5(self.USER_PASSWD.encode()).hexdigest()
        jsonusr = {
            'YXDM': self.YXDM,
            'UserType': 1,
            'XGH': self.USER_NUMBER,
            'Name': self.USER_NAME,
            'PassWord': pwd,
        }
        _url = 'https://yqfkapi.zhxy.net/api/User/CheckUser'
        return self.sendpost(_url, jsonusr)['ID']

    def getheader(self):
        random_str = ['154G8M6ASHE', 'N2LV8OLP5MM', 'TBZTEOA0E2',
                      'J75J2WS1QHL', 'X9QI7ZBQXR', '9N195OC0EUU']
        time_str = int(time.time()) + 300
        sign_str_o = random.choice(random_str).upper(
        ) + str(time_str) + 'Q9y1Vr5sbjGwR8gekNCzELhZioQb9UZw'
        sign_str = hashlib.md5(sign_str_o.encode(
            encoding="utf-8")).hexdigest().upper()
        return {
            'pragma': 'no-cache',
            'origin': 'https://wxyqfk.zhxy.net',
            'referer': 'https://wxyqfk.zhxy.net/?yxdm=' + str(self.YXDM),
            'timestamp': str(time_str),
            'sign': sign_str,
            'noncestr': random.choice(random_str),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'
        }

    def isclockin(self):
        '''
        判断是否已经打卡
        return bool
        '''
        cap()
        if not self.USERID:
            raise Exception(f"{self.USER_NAME} 未登录")
            
        params = {
            'uid': self.USERID,
            'usertype': 1,
            'yxdm': self.YXDM
        }
        _url = 'https://yqfkapi.zhxy.net/api/ClockIn/IsClockIn'
        return self.sendget(_url, params)['isclockin']

    def getverifycode(self):
        '''
        获得验证码
        return code key
        '''
        cap()
        code = None
        while not code:
            _url = 'https://yqfkapi.zhxy.net/api/common/getverifycode'
            r = self.sendget(_url)
            key, img = r['key'], r['img']
            try:
                code = recognize_img(img)
            except Exception as e:
                print(f'识别验证码发生错误: {e}')
                code = None
        return code, key, img

    def get_version(self):
        cap()
        url = 'https://yqfkapi.zhxy.net/api/School/GetInfo?YXDM=' + \
            str(self.YXDM)
        r = requests.get(url).json()
        return r['version']  # "v1.3.2"

    def do_daka(self):
        '''
        打卡
        return bool
        '''
        # 判断是否已经打卡
        if self.isclockin():
            return alredy_daka
            
        # 尝试30次
        count = 0
        while count < 30:
            count += 1

            code, key, img = self.getverifycode()

            _json = {
                "UID": self.USERID,
                "UserType": 1,
                "JWD": "30.664565,104.096446",  # 成都市经纬度
                "key": key,
                "code": code,
                "ZZDKID": 37,
                "A1": "正常",
                "A4": "无",
                "A2": "全部正常",
                "A3": self.USER_LOC,
                "A11": "不在校",
                "A12": "未实习",
                "YXDM": self.YXDM,
                "version": self.get_version()
            }
            cap()
            r = requests.post(
                'https://yqfkapi.zhxy.net/api/ClockIn/Save', headers=self.getheader(), json=_json).json()
            if r['code'] == 200:
                return success_daka
            if r['code'] == 400:
                continue
        return failed_daka
