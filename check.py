from lib.model import daka
from lib.qnyflib import qnyf


def daily_job():

    for row in daka.select()[::-1]:
        try:
            stu = qnyf(row.yxdm, row.name, row.number, row.passwd, row.loc)
            res = stu.do_daka()

            if res == 1:
                print(f"{row.name} - 打卡成功")
            elif res == 2:
                print(f"{row.name} - 打卡失败")
            elif res == 3:
                print(f"{row.name} - 已经打卡")

        except Exception as e:
            print(f"{row.name} - {e}")