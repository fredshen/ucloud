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


def main():
	client = Client({
	"public_key": "Input public key at here",
	"private_key": "Input private key at here",
	"project_id": "org-en5c1p",
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().modify_udpn_bandwidth({
			"UDPNId": "xxyy",
			"Bandwidth": 4
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		
if __name__ == '__main__':
	main()
	