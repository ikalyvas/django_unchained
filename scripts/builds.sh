ssh autocom@10.23.50.211 'bash -s' < cpInfoBuild.sh $1 
scp autocom@10.23.50.211:~/$1/b.txt . 
scp autocom@10.23.50.211:~/$1/a.txt . 
ssh autocom@10.23.50.211 'bash -s' < cleanInfoBuild.sh $1 
mv b.txt build_dir_dt_$2.txt
mv a.txt build_cre_dt_$2.txt
