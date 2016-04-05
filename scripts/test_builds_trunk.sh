#!/usr/bin/expect -f
set arg1 [lindex $argv 1]
spawn ssh autocom@10.23.50.211 'bash -s' < cpInfoBuild_trunk.sh $arg1
expect  "autocom@10.23.50.211's password:"
send    "abc123\r"
sleep 1
send "exit\r"
spawn scp autocom@10.23.50.211:~/$arg1/a.txt . 
expect  "autocom@10.23.50.211's password:"
send    "abc123\r"
send "exit\r"
#ssh autocom@10.23.50.211 'bash -s' < cleanInfoBuild_trunk.sh $1 
#mv a.txt build_cre_dt_$2.txt
