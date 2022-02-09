import datetime
import hashlib
import random
from select import select
import time

import requests
from requests.models import requote_uri


def recognize2(img):
    import requests
    '''
    通用文字识别（高精度版）
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    def get_access_token():
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=2KoX0UzisGEleKfne0Q4R0Xk&client_secret=sQ3PW5m0u29S7FU4Di90sWoPYlKVk76e'
        response = requests.get(host)
        if response:
            return response.json()
    access_token = get_access_token()['access_token']

    params = {"image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers).json()
    if len(response['words_result']) != 0:
        code = response['words_result'][0]['words']
        import string
        code = ''.join([i if i in string.ascii_letters +
                        string.digits else '' for i in code])
        return code
    else:
        raise ValueError


def get_version(yxdm):
    time.sleep(1)
    url = 'https://yqfkapi.zhxy.net/api/School/GetInfo?YXDM=' + str(yxdm)
    r = requests.get(url).json()
    return r['version']


class QNDK():
    YXDM = None
    USRID = None
    USRNAME = None
    USRXH = None
    USRPSW = None
    USRLOC = None

    ZCTW = None
    ZCTJSJ = None
    ZWTW = None
    ZWTJSJ = None
    WSTW = None
    WSTJSJ = None
    tb_now = None
    flag = True

    def __init__(self, YXDM, USRXH, USRNAME, USRPSW, USRLOC = '中国四川省成都市西华大学'):
        self.YXDM = YXDM
        self.USRXH = USRXH
        self.USRNAME = USRNAME
        self.USRPSW = USRPSW
        self.USRLOC = USRLOC
        self.USRID = self.getid()

    def send(self, _url, _jsonusr):
        r = requests.post(_url, headers=self.getheader(), json=_jsonusr).json()
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
        r = self.send(_url, jsonusr)
        return r['ID']

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
        if not self.USRID:
            raise Exception("未登录")
        time.sleep(2)
        params = {
            'uid': self.USRID,
            'usertype': 1,
            'yxdm': self.YXDM
        }
        r = requests.get('https://yqfkapi.zhxy.net/api/ClockIn/IsClockIn',
                         params=params, headers=self.getheader()).json()
        return r['data']['isclockin']

    def getverifycode(self):
        time.sleep(2)
        code, key = None, None
        while (code, key) == (None, None):
            r = requests.get(
                'https://yqfkapi.zhxy.net/api/common/getverifycode', headers=self.getheader()).json()
            try:
                code = recognize2(r['data']['img'])
                key = r['data']['key']
                img = r['data']['img']
            except ValueError:
                code, key = None, None
        return code, key, img

    def check(self):
        self.now = datetime.datetime.now()
        params = {
            'uid': self.USRID,
            'usertype': 1,
            'yxdm': self.YXDM,
            'date': self.now.strftime("%Y-%m-%d")
        }
        r1 = requests.get('https://yqfkapi.zhxy.net/api/ClockIn/gettem',
                          params=params, headers=self.getheader())
        try:
            self.ID = r1.json()['data']['ID']
            self.ZCTW = r1.json()['data']['ZCTW']
            self.ZWTW = r1.json()['data']['ZWTW']
            self.WSTW = r1.json()['data']['WSTW']
            self.tb_now = self.now.strftime("%Y-%m-%d %H:%M:%S")
            self.first_flag = False
        except:
            self.first_flag = True
        tem_list = ['36.{}'.format(i) for i in range(2, 8)]
        if self.ZCTW == None:
            self.ZCTJSJ = self.tb_now
            self.ZCTW = random.choice(tem_list)
        else:
            if self.ZWTW == None:
                self.ZWTJSJ = self.ZCTJSJ = self.tb_now
                self.ZWTW = random.choice(tem_list)
            if self.WSTW == None:
                self.WSTJSJ = self.ZWTJSJ = self.ZCTJSJ = self.tb_now
                self.WSTW = random.choice(tem_list)
            else:
                self.flag = False  # 用于判断是否继续填写温度
        return self.flag

    def Tem_action(self):
        if not self.check():
            return True
        for i in range(2):
            if self.flag:
                if self.first_flag:
                    self.json2 = {
                        'UID': self.USRID,
                        'UType': 1,
                        'YXDM': self.YXDM,
                        'ZCTJSJ': self.ZCTJSJ,
                        'ZCTW': self.ZCTW,
                    }
                    self.first_flag = False
                else:
                    self.check()
                    self.json2 = {
                        'ID': self.ID,
                        'SBRQ': self.now.strftime("%Y-%m-%d") + " 00:00:00",
                        'UID': self.USRID,
                        'UType': 1,
                        'YXDM': self.YXDM,

                        'ZCTJSJ': self.ZCTJSJ,
                        'ZCTW': self.ZCTW,

                        'ZWTJSJ': self.ZWTJSJ,
                        'ZWTW': self.ZWTW,

                        'WSTJSJ': self.WSTJSJ,
                        'WSTW': self.WSTW
                    }
                time.sleep(2)
                requests.post('https://yqfkapi.zhxy.net/api/ClockIn/SaveTem',
                              headers=self.getheader(), json=self.json2)
        if not self.check():
            return True
        else:
            return False

    def DK_action(self):
        if self.isclockin():
            return True
        count = 0
        while count < 25:
            count += 1

            code, key, img = self.getverifycode()
            self.json1 = {
                "UID": self.USRID,
                "UserType": 1,
                "JWD": "30.664565,104.096446",
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
                "version": get_version(self.YXDM)
            }
            time.sleep(2)
            r = requests.post(
                'https://yqfkapi.zhxy.net/api/ClockIn/Save', headers=self.getheader(), json=self.json1).json()
            if r['code'] == 200:
                return True
            if r['code'] == 400:
                continue
        return False
    
    def GetOncePassCard(self):
        self.saveApplication()
        res = self.GetPassCard()

        if len(res) == 2 and res[1] != None:
            key = res[1]
            context = {}
            img = "https://yqfkapi.zhxy.net/api/access/GetPassCardQRCode?code=" + key
            if self.DeletePassCard():
                return img

    def saveApplication(self, reson='有事回家'):
        jsonParams = {
            "ID": self.USRID,
            "UID": self.USRID,
            "Utype": 1,
            "WCYY": reson,
            "WCSJ": datetime.datetime.now().strftime("%Y-%m-%d"),
            "YJFHSJ": datetime.datetime.now().strftime("%Y-%m-%d"),
            "CPBC": reson,
            "JKZT": "健康",
            "YXDM": self.YXDM
        }

        r = requests.post('https://yqfkapi.zhxy.net/api/Access/Save', headers=self.getheader(), json=jsonParams).json()
        if r['code'] == 200:
            return True
        else:
            return False

    def GetPassCard(self):
        url = f'https://yqfkapi.zhxy.net/api/Access/GetPassCard?yxdm={self.YXDM}&UID={self.USRID}&usertype=1'
        r = requests.get(url, headers=self.getheader()).json()
        if r['code'] == 200:
            if 'KEY' in r['data']:
                return (r['data']['ID'], r['data']['KEY'])
            else:
                return r['data']['ID']

    def DeletePassCard(self):
        jsonParams = {
            "ID": self.GetPassCard()[0],
            "UID": self.USRID,
            "Utype": 1,
            "YXDM": self.YXDM
        }
        r = requests.post('https://yqfkapi.zhxy.net/api/Access/Delete', headers=self.getheader(),
                          json=jsonParams).json()
        if r['code'] == 200 and r['info'] == '操作成功':
            return True
