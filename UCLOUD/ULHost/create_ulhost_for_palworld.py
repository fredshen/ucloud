#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client


#账号：shenchaook@gmail.com
Pubulic_Key = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
Private_Key = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"
Project_ID = "org-fye3q5"

client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

try:
	resp = client.invoke("CreateULHostInstance", {
		"Region": "cn-sh2",
		"ProjectId": "org-fye3q5",
		"ImageId": "uimage-t3ukgedv9pc",
		"BundleId": "ulh.c2m8s100b8t2000",
		"Password": "VUNsb3VkLmNu",
		"Name": "api_131",
		"Count": 3
})
except exc.RetCodeException as e:
	resp = e.json()
	