# coding=utf-8 

import sqlite3
from qnyflib import QNDK
import requests
import os

path = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(path + '/studata.db')
cur = con.cursor()

count = 0
res = list(cur.execute('SELECT * FROM stu'))
for row in res:
    num, name, passwd, loc, valid = row
    if valid:
        try:
            # 10623 is your school code
            stu = QNDK(10623, num, name, passwd, loc)
            if stu.DK_action():
                count += 1
                print(name, '打卡成功')
        except Exception as e:
            print(name, e)
    else:
        print(name, '不打卡')
        count += 1
