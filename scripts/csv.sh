#!/bin/bash

###################################################################################################################################################################
#
#
#   This script facilitates for converting a large block of the html file of lvn affecting table in the wiki into CSV format for having the data inserted into a db for the R&D_Id_000035_35 As a R&D person, I want a dynamic web site that contains the ISU wiki related documentation 
#
###################################################################################################################################################################



if [ "$1" == "" ];then

    echo -e "Usage:You must provide an HTML file as input to the script\n"
    exit 1
fi


grep -n -P '(?<=name=")NG.+|Trunk' $1|grep -vi 'cd4\|cd5'|sed -n '2,$'p|awk -F: '{print $1}'>tables_start.log
i=0

while read line;do

    tables[$i]=`echo $line`

    let i++

done<tables_start.log

tables[9]=5385 #stop before PCD5 line



#tables contain the line numbers where the tables start in html file.


for ((i=0;i<=$((${#tables[*]} - 2));i++));do

    td_num=`sed -n ${tables[$i]},${tables[$i+1]}p $1|grep -c '<td'`

    td_start=`sed -n ${tables[$i]},${tables[$i+1]}p $1|grep -n -m 1 '<td'|awk -F: '{print $1}'`

    td_ends=`sed -n ${tables[$i]},${tables[$i+1]}p $1|grep -n '</td'|sed -n '$p'|awk -F: '{print $1}'`
    sed -n ${tables[$i]},${tables[$i+1]}p $1>file_st 2>/dev/null
 
    for ((j=$(($td_start));j<=$(($td_ends));j+=8))
    do
        #cat file_st|sed -n "$j","$(($j+7))p"
       
        cat file_st|sed -n "$j","$(($j+7))"p |grep -Po '(?<=> ).*(?=<)'|paste -s -d,|sed 's/&nbsp;//'>>LVN.csv 2>/dev/null
        
    done
    echo -e "\n" >> LVN.csv

done

sed -i 's/&nbsp;//g' LVN.csv

if [ -s LVN.csv ];then
    echo -e "All done\n"
fi

echo -e "removing reduntant info\n"

sed -e 's/<a href="\/twiki/http:\/\/viini.dev.salab.noklab.net\/twiki/g' LVN.csv > LVN1.csv
sed -e 's/<a href="//g' LVN1.csv > LVN2.csv
sed -e 's/" class="twikiLink">//g' LVN2.csv > LVN3.csv
sed -e 's/<\/a>//g' LVN3.csv > LVN4.csv
sed -e 's/" target="_top">//g' LVN4.csv > LVN5.csv

mv LVN5.csv LVN.csv
rm LVN1.csv LVN2.csv LVN3.csv LVN4.csv

