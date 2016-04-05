if [ ! -d /home/hudson/lvnproject/Weblvn/my_media/lvn_change ] &&  [ ! -d ../my_media/isu_compact ];then
    echo "Creating lvn_change and isu_compact directories..."
    mkdir -v /home/django/lvnproject/Weblvn/my_media/lvn_change && mkdir -v /home/django/lvnproject/Weblvn/my_media/isu_compact
fi

date
#rsync -i kalyvas@10.23.50.7://scratch/isu/ISU_dmn_2011_12_12/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db*.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_trunk.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng30_13a.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng31_pt9.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng31.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_14a_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_14b_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng3120_14a.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
#rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng33_14b.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_15a_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_15b_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng15.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng15_15a.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng16_global_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng16_atca.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng16_15b.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng16_cloud.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_16a_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/
rsync -i kalyvas@10.23.50.7://scratch/isu_cgr/ISU_dmn_2014_03_07/daemon_work/svn_follower/troubleshoot/layout_work/svn_follower_work/rev_db_cache_ng165_global_isu_pretest.txt /home/django/lvnproject/Weblvn/scripts/rev_dbs/


#rsync -i  kalyvas@10.23.50.7://home/isu/ISU_dmn_2014_03_07/daemon_work/lvn_follower/troubleshoot/layout_work/lvn_follower_work/gen_report/LVN_change_reason*.txt /home/django/lvnproject/Weblvn/my_media/lvn_change/
rsync -i  kalyvas@10.23.50.7://home/isu_cgr/ISU_dmn_2014_03_07/daemon_work/lvn_follower/troubleshoot/layout_work/lvn_follower_work/gen_report/LVN_change_reason*.txt /home/django/lvnproject/Weblvn/my_media/lvn_change/

##compact versions are in a crontab in home dir since isu user runs it with sudo privileges
#rsync -i kalyvas@10.23.50.7://home/kalyvas/compact_versions_of_cache_db/compact*.txt /home/django/lvnproject/Weblvn/my_media/isu_compact/
rsync -i kalyvas@10.23.50.7://home/isu_cgr/compact_versions_of_cache_db/compact*.txt /home/django/lvnproject/Weblvn/my_media/isu_compact/
#rsync -i kalyvas@10.23.50.7://home/isu/compact_versions_of_cache_db/compact*.txt /home/django/lvnproject/Weblvn/my_media/isu_compact/
date
