import schedule
import time
from lib.model import *
from lib.qnyflib import qnyf


print("start daka...")


def dakafun(row):
    try:
        print(row)
        # 10623 is your school code
        stu = qnyf(row.yxdm, row.number, row.name, row.passwd, row.loc)
        res = stu.Daka()
        if res == 1:
            print(row.name, '打卡成功', )
        elif res == 2:
            print(row.name, '已经打卡', )
        else:
            print(row.name, '打卡失败')
    except Exception as e:
        print(row.name, e)


def job():
    for i in daka.select()[::-1]:
        dakafun(i)


# schedule.every().day.at('00:05').do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
job()
