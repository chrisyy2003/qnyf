# coding=utf-8 

import json
from qnyflib import QNDK
import os

path = os.path.dirname(os.path.abspath(__file__))
with open(path + '/studata.json', 'rb') as f:
    studata = json.loads(f.read())


for row in studata:
    num  = row['num']
    name = row['name']
    passwd = row['passwd']
    loc = row['loc']

    try:
        # 10623 is your school code
        stu = QNDK(10623, num, name, passwd, loc)
        print(stu.USRID)
        
        # if stu.Daka():
        #     print(name, '打卡成功')
    except Exception as e:
        print(name, e)