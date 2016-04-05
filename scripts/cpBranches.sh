user=`whoami`
echo $user but is not used ...
date
scp kalyvas@10.23.50.7://scratch/isu/ISU_dmn_2011_12_12/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db*.txt rev_dbs/
scp kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2012_06_29/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_trunk.txt rev_dbs/
rsync -i  kalyvas@10.23.50.7://scratch/isu/ISU_dmn_2011_12_12/daemon_work/lvn_follower/troubleshoot/layout_work/lvn_follower_work/gen_report/LVN_change_reason*.txt lvn_change/.
rsync -i  kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2012_06_29/daemon_work/lvn_follower/troubleshoot/layout_work/lvn_follower_work/gen_report/LVN_change_reason*.txt lvn_change/.
scp kalyvas@10.23.50.7://scratch/isu/ISU_dmn_2011_12_12/daemon_work/svn_follower/troubleshoot/msgmon/conf/svn_follower_branches.conf rev_dbs/.
date
