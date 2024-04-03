#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

import time
#修改为个人秘钥
#账号：shenchaook@gmail.com
Pubulic_Key = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
Private_Key = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"
Project_ID = "org-qvzj4o"#沈超

ULHostID_List = []

client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

Counts = int(input("输入需要开通的机器数量："))
for i in range(Counts):
	try:
		resp = client.invoke("CreateULHostInstance", {
			"Region": "cn-sh2",
			"ImageId": "uimage-ltvsjca0q65",
			"BundleId": "ulh.c2m2s40b4t1000",
			"Password": "VUNsb3VkLmNu",
			"Name": "API_test"
	})
	except exc.RetCodeException as e:
		resp = e.json()
	print("已创建完成第"+str(i+1)+"台，\n")
	print("共有"+str(Counts)+"台，\n")
	ULHostID = resp.get("ULHostId")
	ULHostID_List.append(ULHostID)
	#time.sleep(1)
print("所有轻量云主机已创建完成，资源ID为：\n")
for a in ULHostID_List:
	print(a)