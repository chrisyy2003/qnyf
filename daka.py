import schedule
import time
from lib.model import daka
from lib.qnyflib import qnyf

def daily_job():
    format_time = time.asctime( time.localtime(time.time()))
    print(f'[+] Daily_job at {format_time} start...')
    for row in daka.select()[::-1]:
        try:
            stu = qnyf(row.yxdm, row.name, row.number, row.passwd, row.loc)
            res = stu.do_daka()

            if res == 1:
                print(row.name, '打卡成功', )
            elif res == 2:
                print(row.name, '打卡失败', )
            elif res == 3:
                print(row.name, '已经打卡')

        except Exception as e:
            print(row.name, e)

schedule.every().day.at('00:01').do(daily_job)
while True:
    schedule.run_pending()
    time.sleep(1)
