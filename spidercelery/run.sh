#!/bin/sh

#sleep 25000

idnum=$(ps aux |grep test|awk -F' ' {'print $2'})
for eid in idnum
do
kill -9 $idnum
printf $idnum
done
