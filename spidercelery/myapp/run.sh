#!/bin/bash


#Mioji2016@Spider

stop(){
	#ps aux |grep celery |awk -F' ' {'print $2'}|xargs kill -9
	idnum=$(ps aux |grep celery |awk -F' ' {'print $2'})
	for eid in idnum
	do
	kill -9 $idnum
	printf $idnum
	done
}


keeping(){

	while true
	do
	    procnum=` ps -ef|grep "celery"|grep -v grep|wc -l`
	   if [ $procnum -eq 0 ]; then
	       nohup celery -A myapp worker -c 100   -Q machine1 &
	   fi
	   sleep 30
	done
}

st_1="stop"
st_2="start"

if [ $1 == $st_1 ]; then
	stop

elif [ $1 == $st_2 ];then
	keeping
fi



