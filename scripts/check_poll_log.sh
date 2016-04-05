#!/bin/bash


logfsize=`stat -c "%s" ~/poll.log`
if  [ $logfsize -gt 500000 ]
then  	
	echo "fsize is $logfsize"
else
    echo "less that max"
fi	


