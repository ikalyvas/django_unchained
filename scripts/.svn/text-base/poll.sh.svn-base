#!/bin/bash





if [ ! -d ~/lvnproject/Weblvn/my_media/svnhistory ];then

    mkdir -v ~/lvnproject/Weblvn/my_media/svnhistory >> ~/poll.log

fi


if [[ -e head.txt ]] && [[ "cat head.txt|grep -P '\d+'" ]];then
    
    true
    echo "head is not empty at `date`.It has: `cat head.txt`" >> ~/poll.log
else 
   
    echo "emtpy head.txt." >> ~/poll.log
   

fi

#gia na parw to HEAD sto opoio ekana to prwto log against.





var=`cat ~/head.txt`
cur_var=`svn info svn+ssh://svne1.access.nokiasiemensnetworks.com/isource/svnroot/flexi_bng/ --revision HEAD|grep Revision|awk -F: '{print $2}'`


if [ "$var" == "$cur_var" ];then
    
    
    true


else
   echo "Running svn info to get the HEAD @ `date`" >> ~/poll.log
   svn log -v -r $var:HEAD svn+ssh://svne1.access.nokiasiemensnetworks.com/isource/svnroot/flexi_bng/ > ~/commit_messages.txt 
   svn info svn+ssh://svne1.access.nokiasiemensnetworks.com/isource/svnroot/flexi_bng/ --revision HEAD|grep Revision|awk -F: '{print $2}' > ~/head.txt #edw to var einai to palio HEAD
   while read line;do
	  if [ ! -f ~/lvnproject/Weblvn/my_media/svnhistory/$line.txt ]
	  then	 
		      echo "file does not exist" $line >> ~/poll.log
              awk '/'$line' \|/,/------/' commit_messages.txt > ~/lvnproject/Weblvn/my_media/svnhistory/$line.txt #throw them in my_media
	  else 
		  if [ ! -s ~/lvnproject/Weblvn/my_media/svnhistory/$line.txt ]
		  then 	  
			  echo "file has 0 size" $line >> ~/poll.log
              awk '/'$line' \|/,/------/' commit_messages.txt > ~/lvnproject/Weblvn/my_media/svnhistory/$line.txt #throw them in my_media
		  fi
	  fi
   done< <(grep -Po '(?<=r)\d{6}(?= \|)' ~/commit_messages.txt)
   rm ~/commit_messages.txt

fi

logfsize=`stat -c "%s" ~/poll.log`
if  [ $logfsize -gt 4000000 ]
then  	
    rm ~/poll.log
else
    echo "fsize is $logfsize not removing"
fi	

