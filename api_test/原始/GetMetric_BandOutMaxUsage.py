#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

#修改为个人秘钥
#账号：shenchaook@gmail.com
pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"

client = Client({
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "Input project ID at here",
	"base_url": "https://api.ucloud.cn"
})

try:
	resp = client.invoke("GetMetric", {
		"Region": "cn-gd",
		"Zone": "cn-gd-02",
		"ProjectId": "org-fye3q5",
		"ResourceType": "udpn",
		"ResourceId": "udpn-r3qv8h1dkau",
		"TimeRange": 200,
		"MetricName.0": "BandOutMaxUsage"
})
except exc.RetCodeException as e:
	resp = e.json()