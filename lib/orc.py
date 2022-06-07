import requests

def get_access_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TUql6XvVAFreu6PQxjpWCHrs&client_secret=yGuiZdloTWszzXIFw7Un9co9kj7Z8mWR'
    token = requests.get(host).json()['access_token']
    return token


def recognize(img):
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
    print(response)
    if len(response['words_result']) != 0:
        code = response['words_result'][0]['words']
        import string
        code = ''.join([i if i in string.ascii_letters +
                        string.digits else '' for i in code])
        return code
    else:
        raise ValueError
