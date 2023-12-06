#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""

#修改为个人秘钥
#账号：shenchaook@gmail.com
pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"


from ucloud.core import exc
from ucloud.client import Client


def main():
	client = Client({
	"region": "cn-gd",
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "org-fye3q5",
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().describe_udpn({
			"UDPNId": "udpn-r3qv8h1dkau"
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		#print(resp.get("DataSet",[],"Bandwidth"))
		
if __name__ == '__main__':
	main()
	