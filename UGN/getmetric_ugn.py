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
#	"project_id": "Input project ID at here",
	"base_url": "https://api.ucloud.cn"
})

try:
	resp = client.invoke("GetMetric", {
		"Region": "cn-sh2",
		"Zone": "cn-sh2-01",
		"ProjectId": "org-en5c1p",
		"ResourceType": "ugnbw",
		"ResourceId": "default-bw-qr350bs9ywh",
		"MetricName.0": "UgnBWOutPeakUsage"
})
except exc.RetCodeException as e:
	resp = e.json()



ResourceType: ugnbw
中文名：云联网带宽包

MetricName：
UgnBWOutPeakUsage 出向峰值带宽使用率
UgnBWOutbps 出向带宽
UgnBWOutPeakbps 出向峰值带宽
UgnBWOutUsage 出向带宽使用率
