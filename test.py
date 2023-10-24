# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client


pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"


def main():
    client = Client({
    "region": "cn-sh2",
    "public_key": "Input public key at here",
    "private_key": "Input private key at here",
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
    