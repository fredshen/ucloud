# -*- coding: utf-8 -*-
 #!/usr/bin/env python3
import requests
import json
import time,datetime

udpn_id = input('Enter your UDPN ID:')
month = int(input('Enter the month:'))

#Judge the number of days in the month by 'month'
if month in [1,3,5,7,8,10,12]:
    day = 31
elif month in [4,6,9,11]:
    day = 30
elif month == 2:
    day = 28
else:
    print('Incorrect input, please try again')


start_time =('20210'+str(month)+'01')
startTime = time.mktime((time.strptime(start_time, "%Y%m%d")))
startList = [];endList = [];y = []


for x in range(day):
  
  startList.append(int(startTime+x*86400))
  endList.append(int(startTime+(x+1)*86400))

 

  url='http://internal.api.ucloud.cn'
  data = {
    "Backend": "UMON3-INNER-API",
    "Action" : "GetMetricStats",
    "AccountId" : 1,
    "Metric" : 'resource.ustats2.thirdpart.unet_dpn_outbw',
    "Uuid" : 'udpn-mnwjlcej',
    "StartTime" : startList[x],
    "EndTime" : endList[x],
  }

  res = requests.post(url,json=data).json()
  res = json.dumps(res)
  res = json.loads(res)

  t = res['Data']['Results'][0]['Values']

  
  for x in t.values():
    y.append(x)

  y.sort(reverse=True)
  a = int(len(y)*0.05)
  print(y[a])