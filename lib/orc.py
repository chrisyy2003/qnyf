import requests
import random


def get_access_token():
        host1 = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=2KoX0UzisGEleKfne0Q4R0Xk&client_secret=sQ3PW5m0u29S7FU4Di90sWoPYlKVk76e'
        host2 = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TUql6XvVAFreu6PQxjpWCHrs&client_secret=yGuiZdloTWszzXIFw7Un9co9kj7Z8mWR'
        host3 = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=WM12GuRCFKcznA1eeiu13bDE&client_secret=AbA1nHVWY3D3H1MaSuh53uvllcQZH3ac'

        token1 = requests.get(host1).json()['access_token']
        token2 = requests.get(host2).json()['access_token']
        # token3 = requests.get(host3).json()['access_token']
        return [token1,]

def recognize(img):
    '''
    通用文字识别(高精度版)
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    params = {"image": img}
    request_url = request_url + "?access_token=" + random.choice(get_access_token())
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


