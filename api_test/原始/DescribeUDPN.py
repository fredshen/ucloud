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

def main():
	client = Client({
	"region": "cn-bj2",
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "org-fye3q5",
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().describe_udpn({
			"UDPNId": "udpn-r3qv8h1dkau",
			"Limit": 1000
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		
if __name__ == '__main__':
	main()
	