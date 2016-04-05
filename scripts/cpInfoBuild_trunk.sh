cd $1
stat -c "%y %n" * | grep "R_FPT" | grep -v latest > a.txt
