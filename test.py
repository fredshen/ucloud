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
    "region": "cn-sh2",
    "public_key": pubulicKey,
    "private_key": privateKey,
    "project_id": "org-fye3q5",
    "base_url": "https://api.ucloud.cn"
})

    try:
        resp = client.unet().describe_share_bandwidth({
			"ShareBandwidthIds": [
				"bwshare-lh6pdg70syn"
			]
		
        })
    except exc.UCloudException as e:
        print(e)
    else:
        print(resp)

if __name__ == '__main__':
    main()
    
    
    
if usage < 60:
    new_bandwith = old_bandwith * 0.8
elif usage > 60 and usage <80:
    new_bandwith = old_bandwith * 0.9
elif usage >= 80:
    new_bandwith = real_usage * 1.2
    