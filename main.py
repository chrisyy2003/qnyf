import sqlite3
from qnyflib import QNDK
import requests

con = sqlite3.connect('./studata.db')
cur = con.cursor()

count = 0
res = list(cur.execute('SELECT * FROM stu'))
for row in res:
    num, name, passwd, loc, valid = row
    if valid:
        try:
            # 10623 is your school code
            stu = QNDK(10623, num, name, passwd, loc)
            print(name, stu.USRID, count := count + 1 if stu.DK_action() else False, loc)
        except Exception as e:
            print(name, e)
    else:
        print(name, '不打卡')
        count += 1
