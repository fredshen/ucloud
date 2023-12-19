# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

#修改为个人秘钥
#账号：1349826830@qq.com
Pubulic_Key = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
Private_Key = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"

#基础信息配置
Package_ID = "bw-rmq0ks7rv2e"
UGN_ID = "ugn-qr34zqz4xuh"
Project_ID = "org-en5c1p"
Log_Path = "/Users/fredshen/Downloads/uwork/API_test"


client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

try:
	resp = client.invoke("ModifyUGNBandwidth", {
		"ProjectId": Project_ID,
		"PackageID": Package_ID,
		"UGNID": UGN_ID,
		"BandWidth": 2
})
except exc.RetCodeException as e:
	resp = e.json()
	