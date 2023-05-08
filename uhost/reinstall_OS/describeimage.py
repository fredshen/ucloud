#!/usr/bin/env python3


# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

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
		resp = client.uhost().describe_image({
			"Zone": "cn-sh2-01",
			"ImageId": "uimage-yeg3lc"
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		#x = resp.get("ImageSet",[])[0].get("ImageName",[])
		#print (x)
		print(resp.get("ImageSet",[])[0].get("ImageName",[]))
		print(resp.get("RetCode",[]))
		print(resp.get("request_uuid",[]))
		
		#print(resp)
if __name__ == '__main__':
	main()
	