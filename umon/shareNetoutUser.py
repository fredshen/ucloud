# -*- coding: utf-8 -*-

import requests
import json
import time

netId = ["bwshare-oi3vgl5z"]
fruits = []
for netId in netId :
  startTime = 0
  endTime = -1
  while startTime<4 and endTime<3:
      startTime+=1
      endTime+=1
      url='http://internal.api.ucloud.cn'
      data = {
        "Backend": "UMON3-INNER-API",
        "Action" : "GetMetricStats",
        "AccountId" : 1,
        "Metric" : 'resource.ustats2.thirdpart.bwshare_outbw',
        "Uuid" : netId,
        "StartTime" : int(time.time()) - 604800*startTime - 172800,
        "EndTime" : int(time.time())  - 604800*endTime - 172800,
      }
      res = requests.post(url,json=data).json()
      res = json.dumps(res)
      res = json.loads(res)
      s0 = res['Data']['Results'][0]['Max']
      fruits.append(s0)
  print (fruits)

  # for i in `cat eipoutUser.txt` ; do printf "%.5f\n" `echo "scale=17;$i/1558363980*100"|bc` ; done > percent.txt
# for i in `cat percent.txt` ;do printf "%.2f\n" `echo "scale=17; 5850*$i/100"|bc`; done > cost.txt