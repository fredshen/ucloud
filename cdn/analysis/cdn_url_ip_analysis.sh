#!/bin/bash
#####################################################################################################
#                                                                                                   #
# Author: F.Shen                                                                                    #
# Version: 1.1                                                                                      #
# Release Date: 01/29/2021                                                                          #
# Features:Sort by URL > TOP3URL, sort the request IP of TOP3URL, analyze CDN abnormal requests     #
# Export: a/URL sort <url_sort.log>, b/TOP3URL request IP sort <top3url_ip_sort.log>                #
# *Let me know if there're any BUGs | fred.shen@ucloud.cn                                           #
#                                                                                                   #
#####################################################################################################

#####################################################################################################
# ------------Release Note------------                                                              #
# Version:1.0                                                                                       #
# Sort by URL, sort the request IP of TOP3URL, analyze CDN abnormal requests                        #
# Export unit time: a/URL sort <url_sort.log>, b/TOP3URL request IP sort <top3url_ip_sort.log>      #
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
log_name_00="替换为日志的文件名,不包含后缀.gz"
log_name_01="2021012907_static.xigou100.com_CDN.log_00"
log_name_02="2021012908_static.xigou100.com_CDN.log_00"
log_name_03="2021012909_static.xigou100.com_CDN.log_00"

gunzip ${log_name_00}.gz ${log_name_01}.gz ${log_name_02}.gz ${log_name_03}.gz
cat ${log_name_00} ${log_name_01} ${log_name_02} ${log_name_03} > initial.log
rm -rf ${log_name_00} ${log_name_01} ${log_name_02} ${log_name_03}

#截取日志文件的第5列（URL），并将其重复项合并，从大到小进行排序
awk '{print $5}' initial.log | sort |uniq -c | sort -n -r |less > url_sort.log
head -3 url_sort.log > url_sort_top3.log
awk '{print $2}' url_sort_top3.log > top3_url.log
rm -rf url_sort_top3.log

#通过TOP3的URL，在原始日志initial.log中过滤，导出TOP3URL的原始日志top3url_initial.log
cat top3_url.log | while read myline
do
        grep "$myline" initial.log > top3url_initial.log
done

#将TOP3URL的原始日志top3url_initial.log处理，将请求IP从大到小一次排序
awk '{print $3}' top3url_initial.log | sort |uniq -c | sort -n -r |less > top3url_ip_sort.log
rm -rf top3_url.log
rm -rf top3url_initial.log


echo "URL访问量前三为："
head -3 url_sort.log
echo "IP访问量前三为："
head -3 top3url_ip_sort.log

echo "日志分析完成，请在目录下查看分析结果：a/url_sort.log、b/top3url_ip_sort.log、c/initial.log"
