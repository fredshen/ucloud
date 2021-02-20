#!/bin/bash
LogFile=/root/CallEipInfo.log

# 目标IP的id，运行时指定
EIPIds=$1

# 目标IP所在区域，运行时指定
Region=$2

# 客户所在项目ID，需要修改
ProjectId="org-lkmnzr"


# 客户的公钥，需要修改
PublicKey="kzje7oFRHFz6POmZ=="

# 客户的私钥，需要修改
PrivateKey="c1f28ce16d8a42"

# 客户URL编码后的公钥，需要修改
PublicKeyURL="kzje7oFRHFz6POmZhBhvqs"

ts=`date +%s`;

Endpoint=`hostname`

# 带宽使用率上调的阈值,默认70
highthreshold=80  

# 带宽上调的步伐，默认1.2
uprate=1.2

# 带宽使用率下调的阈值，默认60
lowthreshold=60

# 带宽下调的步伐，默认0.5
downrate=0.8

# 最低带宽，调整不允许超过改值
normalBandWidth=2

# 监控带宽使用率的时间周期，即每次查看近一分钟内的带宽使用率,单位s，请勿修改
monitorInterval=119


error()

{

        echo "STATUS:ERROR:""$1" >> $LogFile

        #echo "$1" 1>&2

        exit 1

}

info()

{

        echo "STATUS:INFO:""$1" >> $LogFile


}

writeLog()

{

        if [ $# -eq 1 ];then

                echo $1 >> $LogFile

                echo "##########################################################" >> $LogFile

        else

                echo "CallEIPWidthTime :"$1 >> $LogFile

                echo "CallTotalBandwidthResult :"$2 >> $LogFile

                echo "TotalBandwidth: "$3 >> $LogFile

                echo "CallEIPWidthCosttime :"$4 >> $LogFile

                echo " " >> $LogFile

                echo "CallNetworkOutUsageTime :"$5 >> $LogFile

                echo "CallNetworkOutUsageResult :"$6 >> $LogFile

                echo "NetworkOut :"$7 >> $LogFile

                echo "NetworkOutUsage :"$8 >> $LogFile

                echo "NowNetworkOutUsage :"$9 >> $LogFile

                echo "NetworkIn :"${10} >> $LogFile

                echo "NetworkInUsage :"${11} >> $LogFile

                echo "NowNetworkInUsage :"${12} >> $LogFile

                echo "CallNetworkOutUsageCosttime :"${13} >> $LogFile

                echo " " >> $LogFile

                echo "CallSetEIPWidthTime :"${14} >> $LogFile

                echo "SetEipBandWidthResult :"${15} >> $LogFile

                echo "CurrentBandwidth is :"${16}"Mb" >> $LogFile

                echo "UpdateBandwidth to :"${17}"Mb" >> $LogFile

                echo "SetEipBandWidtStatudCode :"${18} >> $LogFile

                echo "CallSetEipBandWidthCosttime :"${19} >> $LogFile

        fi

}

echo "########################################" >> $LogFile

echo `date "+%Y-%m-%d %H:%M:%S"` >> $LogFile

if [ $# != 2 ];then

        error "Parameter's count is false,should be two,example: EIPIds Region"

fi

#######################################################################################################################################

# 获取IP的总带宽

EIPURLEncrypt="ActionDescribeEIPEIPIds.0${EIPIds}ProjectId${ProjectId}PublicKey${PublicKey}Region${Region}${PrivateKey}"

EIPURLSign=`echo -n $EIPURLEncrypt|sha1sum |awk '{print $1}'`

EIPCALLURL="https://api.ucloud.cn/?Action=DescribeEIP&EIPIds.0=$EIPIds&ProjectId=$ProjectId&PublicKey=$PublicKeyURL&Region=$Region&Signature=$EIPURLSign"

CallEIPWidthTime=`date "+%Y-%m-%d %H:%M:%S"`

start_time=$(date +%s)

CallTotalBandwidthResult=`curl -s -k $EIPCALLURL`

# echo $CallTotalBandwidthResult

end_time=$(date +%s)

TotalBandwidth=`echo $CallTotalBandwidthResult|awk -F "," '{for(i=1;i<=NF;i++) {print $i}}'|grep "TotalBandwidth"|cut -d : -f 2|awk 'gsub(/^ *| *$/,"")'`

EIPStatus=`echo $CallTotalBandwidthResult|sed 's/ResourceName/\n/g'|tail -1|sed 's/ResourceType/\n/g'|head -1|sed 's/://g'|sed 's/,//g'|sed 's/"//g'`


Metric="susuan_php"

CallEIPWidthCost=$(($end_time - $start_time))

isNumber=`echo $TotalBandwidth|sed -n '/^[0-9][0-9]*$/p'|wc -l`

newTotalBandwidth=`echo $TotalBandwidth|sed -n '/^[0-9][0-9]*$/p'`

if [ $isNumber -eq 0 ] || [ $newTotalBandwidth != $TotalBandwidth ]; then

        error "Get TotalBandwidth is false!!!"

fi

#######################################################################################################################################
# 获取IP的带宽使用率

Seconds=$monitorInterval

# 计算签名
NetworkOutUsageURLEncrypt="ActionGetMetricMetricName.0NetworkOutUsageMetricName.1NetworkInUsageMetricName.2NetworkOutMetricName.3NetworkInProjectId${ProjectId}PublicKey${PublicKey}Region${Region}ResourceId${EIPIds}ResourceTypeeipTimeRange${Seconds}$PrivateKey"

NetworkOutUsageURLSign=`echo -n $NetworkOutUsageURLEncrypt|sha1sum |awk '{print $1}'`

# 拼接url
#NetworkOutUsageCallURL="https://api.ucloud.cn/?Action=GetMetric&MetricName.0=NetworkOutUsage&MetricName.1=NetworkInUsage&MetricName.2=NetworkOut&MetricNa#me.3=NetworkIn&PublicKey=$PublicKeyURL&Region=$Region&ResourceId=$EIPIds&ResourceType=eip&TimeRange=$Seconds&Signature=$NetworkOutUsageURLSign"

NetworkOutUsageCallURL="https://api.ucloud.cn/?Action=GetMetric&MetricName.0=NetworkOutUsage&MetricName.1=NetworkInUsage&MetricName.2=NetworkOut&MetricName.3=NetworkIn&ProjectId=${ProjectId}&PublicKey=$PublicKeyURL&Region=$Region&ResourceId=$EIPIds&ResourceType=eip&TimeRange=$Seconds&Signature=$NetworkOutUsageURLSign"

#echo $NetworkOutUsageCallURL

CallNetworkOutUsageTime=`date "+%Y-%m-%d %H:%M:%S"`

start_time=$(date +%s)

# 发送请求
CallNetworkOutUsageResult=`curl -s -k $NetworkOutUsageCallURL`

#echo $CallNetworkOutUsageResult
end_time=$(date +%s)

CallNetworkOutUsageCosttime=$(($end_time - $start_time))

# 结果处理
valueNums=`echo $CallNetworkOutUsageResult|grep -o "Value"|wc -l`

#echo $valueNums
if [ $valueNums -eq 4 ]; then

        NetworkOutUsage=`echo $CallNetworkOutUsageResult|cut -d : -f 6|cut -d , -f 1`

        NetworkInUsage=`echo $CallNetworkOutUsageResult|cut -d : -f 9|cut -d , -f 1`

        NetworkOut=`echo $CallNetworkOutUsageResult|cut -d : -f 12|cut -d , -f 1`

        NetworkIn=`echo $CallNetworkOutUsageResult|cut -d : -f 15|cut -d , -f 1`

fi

if [ $valueNums -eq 6 ]; then

        NetworkOutUsage=`echo $CallNetworkOutUsageResult|cut -d : -f 8|cut -d , -f 1`

        NetworkInUsage=`echo $CallNetworkOutUsageResult|cut -d : -f 11|cut -d , -f 1`

        NetworkOut=`echo $CallNetworkOutUsageResult|cut -d : -f 16|cut -d , -f 1`

        NetworkIn=`echo $CallNetworkOutUsageResult|cut -d : -f 19|cut -d , -f 1`

fi

if [ $valueNums -eq 8 ]; then

        NetworkOutUsage=`echo $CallNetworkOutUsageResult|cut -d : -f 8|cut -d , -f 1`

        NetworkInUsage=`echo $CallNetworkOutUsageResult|cut -d : -f 11|cut -d , -f 1`

        NetworkOut=`echo $CallNetworkOutUsageResult|cut -d : -f 18|cut -d , -f 1`

        NetworkIn=`echo $CallNetworkOutUsageResult|cut -d : -f 21|cut -d , -f 1`

fi

# echo "debug info request:"+ $NetworkOutUsageCallURL+",  result :" + $CallNetworkOutUsageResult >> $LogFile

isNumber=`echo $NetworkOutUsage|sed -n '/^[0-9][0-9]*$/p'|wc -l`

newNetworkOutUsage=`echo $NetworkOutUsage|sed -n '/^[0-9][0-9]*$/p'`

info "NetworkOutusage : $newNetworkOutUsage"

if [ $isNumber -eq 0 ] || [ $newNetworkOutUsage != $NetworkOutUsage ]; then

        error "Get NetworkOutUsage is false!!!""@@@@@""$CallNetworkOutUsageResult""@@@@@""$NetworkOutUsage""@@@@@""$newNetworkOutUsage"
	
	echo "debug info request:"+ $NetworkOutUsageCallURL+",  result :" + $CallNetworkOutUsageResult >> $LogFile

fi

isNumber=`echo $NetworkInUsage|sed -n '/^[0-9][0-9]*$/p'|wc -l`

newNetworkInUsage=`echo $NetworkInUsage|sed -n '/^[0-9][0-9]*$/p'`

if [ $isNumber -eq 0 ] || [ $newNetworkInUsage != $NetworkInUsage ]; then

        error "Get NetworkInUsage is false!!!""@@@@@""$CallNetworkOutUsageResult""@@@@@""$NetworkInUsage""@@@@@""$newNetworkInUsage"

fi

isNumber=`echo $NetworkOut|sed -n '/^[0-9][0-9]*$/p'|wc -l`

newNetworkOut=`echo $NetworkOut|sed -n '/^[0-9][0-9]*$/p'`

if [ $isNumber -eq 0 ] || [ $newNetworkOut != $NetworkOut ]; then

        error "Get NetworkOut is false!!!""@@@@@""$CallNetworkOutUsageResult""@@@@@""$NetworkOut""@@@@@""$NetworkOut"

fi
# NetworkOut 为出口带宽使用量，单位为b/s，转换成Mb/s
NetworkOut=`awk 'BEGIN{printf "%.2f\n",'$NetworkOut' / 1000000}'`

# 通过Networkout/TotalBandwidth来计算网络出口带宽使用率，保留两位小数
NowNetworkOutUsage=`awk 'BEGIN{printf "%.2f\n",'$NetworkOut'/'$TotalBandwidth'}'`

# 使用率乘100
NowNetworkOutUsage=`awk -v x=$NowNetworkOutUsage -v y=100 'BEGIN{printf "%i\n",x*y }'`

info "NowNetworkOutUsage : $NowNetworkOutUsage"

isNumber=`echo $NetworkIn|sed -n '/^[0-9][0-9]*$/p'|wc -l`

newNetworkIn=`echo $NetworkIn|sed -n '/^[0-9][0-9]*$/p'`

if [ $isNumber -eq 0 ] || [ $newNetworkIn != $NetworkIn ]; then

        error "Get NetworkIn is false!!!""@@@@@""$CallNetworkOutUsageResult""@@@@@""$NetworkIn""@@@@@""$newNetworkIn"

fi

NetworkIn=`awk 'BEGIN{printf "%.2f\n",'$NetworkIn' / 1000000}'`

NowNetworkInUsage=`awk 'BEGIN{printf "%.2f\n",'$NetworkIn'/'$TotalBandwidth'}'`

NowNetworkInUsage=`awk -v x=$NowNetworkInUsage -v y=100 'BEGIN{printf "%i\n",x*y }'`

#######################################################################################################################################

# 进行带宽调整
 
ExecUpate="YES"

ExecHoure=`date +'%H%m'`

# 如果当前带宽使用率高于设定好的阈值，默认70,则调高带宽到一定比例（默认是1.2倍）
if [ $ExecUpate == "YES" ] && [ $NowNetworkOutUsage -gt $highthreshold ]; then

        Rate=$uprate

        # 计算目标带宽，即为当前实际使用带宽的uprate倍,当不足1m时，向上取整
	temp=`awk -v x=$Rate -v y=$NetworkOut 'BEGIN{printf "%.1f\n",x*y }'`
	Bandwidth=`awk -v x=$temp 'BEGIN{printf "%i\n",(x * 10 + 9) / 10 }'`

	# 如果目标带宽小于当前带宽，则不需要上调
	if [ $Bandwidth -lt $TotalBandwidth ]; then
		info  "There is no need to modify the width of ip"
		exit
	fi
	
	# 拼接URL
      	SetEipBandWidthURLEncrypt=ActionModifyEIPBandwidthBandwidth${Bandwidth}EIPId${EIPIds}ProjectId${ProjectId}PublicKey${PublicKey}Region${Region}${PrivateKey}

	SetEipBandWidthURLSign=`echo -n $SetEipBandWidthURLEncrypt|sha1sum |awk '{print $1}'`

        SetEipBandWidthCallURL="https://api.ucloud.cn/?Action=ModifyEIPBandwidth&Bandwidth=$Bandwidth&EIPId=$EIPIds&ProjectId=${ProjectId}&PublicKey=$PublicKeyURL&Region=$Region&Signature=$SetEipBandWidthURLSign"

        CallSetEIPWidthTime=`date "+%Y-%m-%d %H:%M:%S"`

        start_time=$(date +%s)

	# 调用获取结果
        SetEipBandWidthResult=`curl -s -k $SetEipBandWidthCallURL`
        
	end_time=$(date +%s)

        CallSetEipBandWidthCosttime=$(($end_time - $start_time))

	# 得到操作状态码，0表示成功
        SetEipBandWidtStatudCode=`echo $SetEipBandWidthResult|sed 's/{\|}//g'|awk -F "," '{for(i=1;i<=NF;i++) {print $i}}'|grep RetCode|cut -d : -f 2|awk 'gsub(/^ *| *$/,"")'`

	# 写日志
        writeLog "$CallEIPWidthTime" "$CallTotalBandwidthResult" "$TotalBandwidth" "$CallEIPWidthCost" "$CallNetworkOutUsageTime" "$CallNetworkOutUsageResult" "$NetworkOut" "$NetworkOutUsage" "$NowNetworkOutUsage" "$NetworkIn" "$NetworkInUsage" "$NowNetworkInUsage" "$CallNetworkOutUsageCosttime" "$CallSetEIPWidthTime" "$SetEipBandWidthResult" "$TotalBandwidth" "$Bandwidth" "$SetEipBandWidtStatudCode" "$CallSetEipBandWidthCosttime"

	# 获取调整后的带宽
        CallTotalBandwidthResult=`curl -s -k $EIPCALLURL`

        UpdatedTotalBandwidth=`echo $CallTotalBandwidthResult|awk -F "," '{for(i=1;i<=NF;i++) {print $i}}'|grep "TotalBandwidth"|cut -d : -f 2|awk 'gsub(/^ *| *$/,"")'`

        #sleep 5
	
	# 如果状态码为0，且查询带宽确实为调整目标后，反馈成功
        if [ $SetEipBandWidtStatudCode -eq 0 ] && [ $UpdatedTotalBandwidth -eq $Bandwidth ]; then

                writeLog "BEHAVIOR:UP:STATUS:SUCCESSFUL:INFO:"$SetEipBandWidtStatudCode:$TotalBandwidth"MB":$UpdatedTotalBandwidth"MB"

                Value=$(($UpdatedTotalBandwidth - $TotalBandwidth))
		
		# 如果需要将调整结果通知给客户需要实现下面代码
                #curl -X POST -d "[{\"metric\": \"$Metric\", \"endpoint\": \"$Endpoint\", \"timestamp\": $ts,\"step\": 180,\"value\": $Value,\"counterType#\": \"GAUGE\",\"tags\": \"status=$EIPStatus\"}]" http://*.*.*.*:1988/v1/push

        else

                writeLog "BEHAVIOR:UP:STATUS:ERROR:INFO:"$SetEipBandWidtStatudCode:$TotalBandwidth"MB"

        fi

# 如果当前带宽使用率很低，低于指定阈值（默认30），且高于用户设定的带宽最低值（该值如果过低，会造成来回调整带宽）
elif [ $ExecUpate == "YES" ] && [ $NowNetworkOutUsage -lt $lowthreshold ] && [ $TotalBandwidth -gt $normalBandWidth ]; then

        Rate=$downrate

	# 计算目标调整带宽，不能低于用户设置的最低带宽
        Bandwidth=`awk -v x=$Rate -v y=$TotalBandwidth 'BEGIN{printf "%i\n",x*y }'`

        if [ $Bandwidth -lt $normalBandWidth ]; then

                Bandwidth=$normalBandWidth

        fi
	
	# 拼接URL
	SetEipBandWidthURLEncrypt=ActionModifyEIPBandwidthBandwidth${Bandwidth}EIPId${EIPIds}ProjectId${ProjectId}PublicKey${PublicKey}Region${Region}${PrivateKey}
        
	SetEipBandWidthURLSign=`echo -n $SetEipBandWidthURLEncrypt|sha1sum |awk '{print $1}'`

        SetEipBandWidthCallURL="https://api.ucloud.cn/?Action=ModifyEIPBandwidth&Bandwidth=$Bandwidth&EIPId=$EIPIds&ProjectId=${ProjectId}&PublicKey=$PublicKeyURL&Region=$Region&Signature=$SetEipBandWidthURLSign"

        CallSetEIPWidthTime=`date "+%Y-%m-%d %H:%M:%S"`

        start_time=$(date +%s)

        SetEipBandWidthResult=`curl -s -k $SetEipBandWidthCallURL`

        end_time=$(date +%s)

	# 请求调用
        CallSetEipBandWidthCosttime=$(($end_time - $start_time))

	# 调用结果
        SetEipBandWidtStatudCode=`echo $SetEipBandWidthResult|sed 's/{\|}//g'|awk -F "," '{for(i=1;i<=NF;i++) {print $i}}'|grep RetCode|cut -d : -f 2|awk 'gsub(/^ *| *$/,"")'`
	
	# 写日志
        writeLog "$CallEIPWidthTime" "$CallTotalBandwidthResult" "$TotalBandwidth" "$CallEIPWidthCost" "$CallNetworkOutUsageTime" "$CallNetworkOutUsageResult" "$NetworkOut" "$NetworkOutUsage" "$NowNetworkOutUsage" "$NetworkIn" "$NetworkInUsage" "$NowNetworkInUsage" "$CallNetworkOutUsageCosttime" "$CallSetEIPWidthTime" "$SetEipBandWidthResult" "$TotalBandwidth" "$Bandwidth" "$SetEipBandWidtStatudCode" "$CallSetEipBandWidthCosttime"

	# 获取调整后的带宽
        CallTotalBandwidthResult=`curl -s -k $EIPCALLURL`

        UpdatedTotalBandwidth=`echo $CallTotalBandwidthResult|awk -F "," '{for(i=1;i<=NF;i++) {print $i}}'|grep "TotalBandwidth"|cut -d : -f 2|awk 'gsub(/^ *| *$/,"")'`

        #sleep 5

	# 如果反馈码为0，且调整后的带宽等于目标带宽，则调整成功
        if [ $SetEipBandWidtStatudCode -eq 0 ] && [ $UpdatedTotalBandwidth -eq $Bandwidth ]; then

                writeLog "BEHAVIOR:DOWN:STATUS:SUCCESSFUL:INFO:"$SetEipBandWidtStatudCode:$TotalBandwidth"MB":$UpdatedTotalBandwidth"MB"

                Value=$(($UpdatedTotalBandwidth - $TotalBandwidth))

                #curl -X POST -d "[{\"metric\": \"$Metric\", \"endpoint\": \"$Endpoint\", \"timestamp\": $ts,\"step\": 180,\"value\": $Value,\"counterType# \": \"GAUGE\",\"tags\": \"status=$EIPStatus\"}]" http://*.*.*.*:1988/v1/push

        else

                writeLog "BEHAVIOR:DOWN:STATUS:ERROR:INFO:"$SetEipBandWidtStatudCode:$TotalBandwidth"MB"

        fi

else

        # curl -X POST -d "[{\"metric\": \"$Metric\", \"endpoint\": \"$Endpoint\", \"timestamp\": $ts,\"step\": 180,\"value\": 0,\"counterType\": \"GAUGE\# ",\"tags\": \"status=$EIPStatus\"}]" http://*.*.*.*:1988/v1/push
	
	info  "There is no need to modify the width of ip"

fi



