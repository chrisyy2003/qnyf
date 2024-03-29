from flask import Flask, request, make_response
import datetime
from lib.qnyflib import qnyf
from lib.model import daka
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

logger.add('app.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.info('app start...')
app = Flask(__name__)

def check(yxdm, name, number, passwd, loc):
    try:
        stu = qnyf(yxdm, name, number, passwd, loc)
        return True
    except Exception as e:
        logger.error(e)
        return False


def resp(code=200, msg="", data=""):
    if code == 500:
        msg = "服务器出现问题"
    return make_response({
        "code": code,
        "msg": msg,
        "data": data
    }, 200)


@app.route('/api/hello', methods=["GET"])
def hello():
    return make_response({
        "code": 200,
        "msg": "hello",
        "data": ""
    }, 200)


@app.route('/api/count', methods=["GET"])
def dakacount():
    return resp(200, '', str(len(daka.select())))


@app.route('/api/query', methods=["GET"])
def query():
    try:
        args = request.args

        yxdm = args['yxdm']
        number = args['num'].strip()

        if not number or not yxdm:
            return resp(400, "字段不能为空")
        if not daka.select().where((yxdm == daka.yxdm) & (number == daka.number)).exists():
            return resp(400, "用户还未在数据库中")
        user = daka.get((daka.number == number))
        if not check(yxdm, user.name, number, user.passwd, loc = 'default'):
            return resp(400, user.name + '打卡状态不正常,请更新账号密码')
        return resp(200, f'用户: {user.name} \n\n 打卡状态: 正常 \n\n 打卡位置: {user.loc}')

    except Exception as e:
        logger.error(f"{args} - {e}")

        return resp(500)


@app.route('/api/stop', methods=["GET"])
def stophan():
    try:
        args = request.args
        yxdm = args['yxdm'].strip()
        number = args['num'].strip()

        if not daka.select().where((yxdm == daka.yxdm) & (number == daka.number)).exists():
            return resp(400, '用户不存在或者密码学号有误，请检查')
        daka.delete().where(number == daka.number).execute()
        return resp(200, "删除成功")
    except Exception as e:
        logger.error(f"{args} - {e}")
        return resp(500)


@app.route('/api/submit', methods=["GET"])
def add():

    args = request.args

    try:
        yxdm = args['yxdm'].strip()
        name = args['name'].strip()
        number = args['num'].strip()
        passwd = args['passwd'].strip()
        loc = args['address'].strip()

        if not name or not passwd or not number:
            return resp(400, "字段不能为空")

        if not loc:
            return resp(400, "没有地址信息")


        if not check(yxdm, name, number, passwd, loc):
            return resp(400, "学号或者密码有误，请检查")

        if daka.select().where(daka.number == number).exists():
            user = daka.get(daka.number == number)
            user.name = name
            user.passwd = passwd
            user.loc = loc
            user.save()
            return resp(200, "修改成功")
        else:
            daka.create(yxdm=yxdm, name=name, number=number,
                        passwd=passwd, loc=loc)
            return resp(200, "添加成功")

    except Exception as e:
        logger.error(f"{args} - {e}")
        return resp(500)

def daily_job():
    logger.info('Daily_job start...')

    for row in daka.select()[::-1]:
        try:
            stu = qnyf(row.yxdm, row.name, row.number, row.passwd, row.loc)
            res = stu.do_daka()

            if res == 1:
                logger.info(f"{row.name} - 打卡成功")
            elif res == 2:
                logger.info(f"{row.name} - 打卡失败")
            elif res == 3:
                logger.info(f"{row.name} - 已经打卡")

        except Exception as e:
            logger.error(f"{row.name} - {e}")

if __name__ == "__main__":
    # 每日打卡任务定时器
    sched = BackgroundScheduler()
    sched.add_job(daily_job, 'cron', hour=0, minute=0)
    sched.start()

    app.run(host='0.0.0.0', debug=False, port=4000, use_reloader=False)
