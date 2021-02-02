#!/bin/bash
#####################################################################################################
#                                                                                                   #
# Author: F.Shen                                                                                    #
# Version: 1.1                                                                                      #
# Release Date: 02/02/2021                                                                          #
# Features:                                                                                         #
# 1.Sort URLs in the original log                                                                   #
# 2.Sort the top three URLs by IP                                                                   #
# Export:                                                                                           #
# a/Original log<initial.log>, b/URL sorting log<url_sort_top20.log>,                               #
# c/IP sorting of the top three URLs <top3url_ip_sort_top20.log>,                                   #
#                                                                                                   #
# ** Let me know if there're any BUGs | fred.shen@ucloud.cn                                         #
#                                                                                                   #
#####################################################################################################

#####################################################################################################
# ------------Release Note------------                                                              #
# Version:1.0                                                                                       #
# 1.Sort URLs in the original log                                                                   #
# 2.Sort the top three URLs by IP                                                                   #
# Export:                                                                                           #
# a/Original log<initial.log>, b/URL sorting log<url_sort_top20.log>,                               #
# c/IP sorting of the top three URLs <top3url_ip_sort_top20.log>,                                   #
#                                                                                                   #
# Version:1.1                                                                                       #
# Added notifications                                                                               #
#                                                                                                   #
#                                                                                                   #
#                                                                                                   #
#                                                                                                   #
#                                                                                                   #
#                                                                                                   #
#####################################################################################################

#合并解压UCloud Console下载的原始日志
log_name_00="替换为日志的文件名,不包含后缀(.gz)"
log_name_01="2021012907_static.xigou100.com_CDN.log_00"
log_name_02="2021012908_static.xigou100.com_CDN.log_00"
log_name_03="2021012909_static.xigou100.com_CDN.log_00"

gunzip ${log_name_00}.gz ${log_name_01}.gz ${log_name_02}.gz ${log_name_03}.gz
cat ${log_name_00} ${log_name_01} ${log_name_02} ${log_name_03} > initial.log
rm -rf ${log_name_00} ${log_name_01} ${log_name_02} ${log_name_03}
echo "Step 1/4: 原始日志已合并完毕，即将进行URL排序..."

#截取日志文件的第5列（URL），并将其重复项合并，从大到小进行排序
awk '{print $5}' initial.log | sort |uniq -c | sort -n -r |less > url_sort.log
head -20 url_sort.log > url_sort_top20.log
head -3 url_sort_top20.log > url_sort_top3.log
awk '{print $2}' url_sort_top3.log > top3_url.log
rm -rf url_sort.log url_sort_top3.log
echo "Step 2/4: URL已排序完成，即将从原始日志<initial.log>中获取TOP3URL的完整日志..."

#通过TOP3的URL，在原始日志<initial.log>中过滤，导出TOP3URL的原始日志<top3url_initial.log>
cat top3_url.log | while read myline
do
        grep "$myline" initial.log > top3url_initial.log
done
rm -rf top3_url.log
echo "Step 3/4: TOP3URL完整日志已获取完成，即将进行IP排序..."

#将TOP3URL的原始日志top3url_initial.log处理，将请求IP从大到小一次排序
awk '{print $3}' top3url_initial.log | sort |uniq -c | sort -n -r |less > top3url_ip_sort.log
head -20 top3url_ip_sort.log > top3url_ip_sort_top20.log
rm -rf top3url_initial.log top3url_ip_sort.log
echo "Step 4/4: TOP3URL对应的IP已排序完成，所有任务已完成！！"

echo -e "\nURL访问量前三为："
head -3 url_sort_top20.log
echo "IP访问量前三为："
head -3 top3url_ip_sort_top20.log

echo -e "\n请在目录下查看分析结果：a/initial.log、b/url_sort_top20.log、c/top3url_ip_sort_top20.log"
