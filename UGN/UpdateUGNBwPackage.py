#!/usr/bin/env python3

#修改为个人秘钥
#账号：1349826830@qq.com
pubulicKey = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
privateKey = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"


# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

client = Client({
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "Input project ID at here",
	"base_url": "https://api.ucloud.cn"
})

try:
	resp = client.invoke("UpdateUGNBwPackage", {
		"ProjectId": "org-en5c1p",
		"PackageID": "bw-qv7mfeyujk3",
		"UGNID": "ugn-qr34zqz4xuh",
		"RegionA": "cn-sh2",
		"RegionABwMax": 4,
		"RegionABwMin": 4,
		"RegionB": "cn-gd",
		"RegionBBwMax": 4,
		"RegionBBwMin": 4,
		"ChargeType": "Month",
		"Quantity": 0,
		"BwBidRate": 1,
		"BwULRate": 1,
		"PayMode": "FixedBw",
		"Qos": "Gold",
		"Path": "IGP"
})
except exc.RetCodeException as e:
	resp = e.json()
	