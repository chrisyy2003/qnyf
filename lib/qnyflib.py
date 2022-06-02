# coding=utf-8
import hashlib
import requests
import random
import time
import lib.orc as orc


class qnyf():
    YXDM = None    # 学校代码
    USRID = None   # 用户id
    USRNAME = None  # 姓名
    USRXH = None   # 学号
    USRPSW = None  # 密码
    USRLOC = None  # 打卡位置

    def __init__(self, YXDM, USRXH, USRNAME, USRPSW, USRLOC='中国四川省成都市西华大学'):
        self.YXDM = YXDM
        self.USRXH = USRXH
        self.USRNAME = USRNAME
        self.USRPSW = USRPSW
        self.USRLOC = USRLOC
        self.USRID = self.getid()

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
        pwd = hashlib.md5(self.USRPSW.encode()).hexdigest()
        jsonusr = {
            'YXDM': self.YXDM,
            'UserType': 1,
            'XGH': self.USRXH,
            'Name': self.USRNAME,
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

    def GetPassCard(self):
        '''
        通过提交的申请获取通行凭证
        '''
        _url = f'https://yqfkapi.zhxy.net/api/Access/GetPassCard?yxdm={self.YXDM}&UID={self.USRID}&usertype=1'
        r = self.sendget(_url)
        if 'KEY' in r:
            return r['KEY'], r['TJSJ'], r['WCSJ'], r['YJFHSJ']

    def isclockin(self):
        '''
        判断是否已经打卡
        return bool
        '''
        if not self.USRID:
            raise Exception("未登录")
        time.sleep(2)
        params = {
            'uid': self.USRID,
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
        time.sleep(2)
        code = None
        while not code:
            _url = 'https://yqfkapi.zhxy.net/api/common/getverifycode'
            r = self.sendget(_url)
            key, img = r['key'], r['img']
            try:
                code = orc.recognize(img)
            except Exception as e:
                code = None
        return code, key, img

    def get_version(self):
        time.sleep(1)
        url = 'https://yqfkapi.zhxy.net/api/School/GetInfo?YXDM=' + \
            str(self.YXDM)
        r = requests.get(url).json()
        return r['version']  # "v1.3.2"

    def Daka(self):
        '''
        打卡
        return bool
        '''
        # 判断是否已经打卡
        if self.isclockin():
            return 2

        count = 0
        while count < 25:
            count += 1
            code, key, img = self.getverifycode()

            _json = {
                "UID": self.USRID,
                "UserType": 1,
                "JWD": "30.664565,104.096446",  # 成都市经纬度
                "key": key,
                "code": code,
                "ZZDKID": 37,
                "A1": "正常",
                "A4": "无",
                "A2": "全部正常",
                "A3": self.USRLOC,
                "A11": "不在校",
                "A12": "未实习",
                "YXDM": self.YXDM,
                "version": self.get_version()
            }
            time.sleep(2)
            r = requests.post(
                'https://yqfkapi.zhxy.net/api/ClockIn/Save', headers=self.getheader(), json=_json).json()
            if r['code'] == 200:
                return 1
            if r['code'] == 400:
                continue
        return False
