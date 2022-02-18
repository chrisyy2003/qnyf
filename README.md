# 青柠疫服自动打卡



基于解析青柠的`api`，青柠接口写在`qnyflib`中

按照字段依次填入信息到`studata.json`最后运行`python3 main.py`即可

| num  | name | passwd |             loc              |
| ---- | ---- | :----: | :--------------------------: |
| 学号 | 姓名 |  密码  | 打卡地址（不填默认西华大学） |

代码很简单，稍微阅读即可，功能包含：

1. 体温打卡
2. 每日打卡
2. 在不审批的情况下获得通行凭证

hints: 

1. YXDM字段是学校代码，在本学校网址可以看见
2. 需要百度[ocr](https://cloud.baidu.com/doc/OCR/s/1k3h7y3db)来自动识别验证码，可以免费申请且有免费额度，申请后[修改](https://github.com/chrisyang2003/qnyf/blob/master/qnyflib.py#L17)为自己的即可
