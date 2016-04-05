ssh autocom@10.23.50.211 'bash -s' < cpInfoBuild_trunk.sh $1 
scp autocom@10.23.50.211:~/$1/a.txt . 
ssh autocom@10.23.50.211 'bash -s' < cleanInfoBuild_trunk.sh $1 
mv a.txt build_cre_dt_$2.txt
