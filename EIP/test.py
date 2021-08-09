 #!/usr/bin/env python3
 # -*- coding: utf-8 -*-
 2 # 定义一个字典
 3 dic = {'剧情': 11, '犯罪': 10, '动作': 8, '爱情': 3, '喜剧': 2, '冒险': 2, '悬疑': 2, '惊悚': 2, '奇幻': 1}
 4 #通过list将字典中的keys和values转化为列表
 5 keys = list(dic.keys())
 6 values = list(dic.values())
 7 # 结果输出
 8 print("keys列表为：",end='')
 9 print(keys)
10 print("values列表为：",end='')
11 print(values)