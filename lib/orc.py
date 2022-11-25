import requests
import string
import os


cliend_id = os.getenv('baidu_orc_id')
client_secret = os.getenv('baidu_orc_secret')
if cliend_id == None or client_secret == None:
    raise Exception("没有配置orc")

def get_access_token():
    # fake client id
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TUql6XvVAFreu6PQxjpWCHrs&client_secret=yGuiZdloTWszzXIFw7Un9co9kj7Z8mWR'

    # get from env
    cliend_id = os.getenv('baidu_orc_id')
    client_secret = os.getenv('baidu_orc_secret')

    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={cliend_id}&client_secret={client_secret}'
    res = requests.get(host).json()
    if 'access_token' in res:
        return res['access_token']
    else:
        raise Exception("orc access_token 无效")



def recognize_img(img):
    # 通用文字识别(高精度版)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 通用文字识别(普通版)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    params = {"image": img}
    request_url = request_url + "?access_token=" + \
        get_access_token()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers).json()
    
    if 'words_result' in response:
        code = response['words_result'][0]['words']
        code = ''.join([i if i in string.ascii_letters +
                        string.digits else '' for i in code])
        return code
    else:
        raise Exception("验证码识别错误")


if __name__ == "__main__":
    url = 'https://yqfkapi.zhxy.net/api/common/getverifycode'
    r = requests.get(url).json()['data']['img']
    print(recognize_img(r))