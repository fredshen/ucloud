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
#账号：ibu_cretec@ucloud.cn  16c3f8B01
pubulicKey = "4eXvtltJL2h30eiaGMPsi37tu0Wi2UKFz"
privateKey = "29SOSFBqNRR5lvo5gKQ5ovAuFXZjNQoXJ1vHSsHokY40"

def main():
	client = Client({
	"region": "cn-sh2",
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "org-ww0gsd",
	"base_url": "https://api.ucloud.cn"
})
	

	try:
		resp = client.uhost().poweroff_uhost_instance({
			"Zone": "cn-sh2-01",
			"UHostId": "uhost-fwylm23y"
			
		})

	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
	print("------------------------------\n正在断电，请稍等。。。")
	time.sleep(5)
	print("------------------------------\n断电成功，正在启动。。。")
	try:
		resp = client.uhost().start_uhost_instance({
			"Zone": "cn-sh2-01",
			"UHostId": "uhost-fwylm23y"
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
	print("------------------------------\n启动成功，请10s之后使用")
		
if __name__ == '__main__':
	main()
	
