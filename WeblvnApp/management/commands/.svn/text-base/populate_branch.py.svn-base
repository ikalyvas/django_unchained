from django.core.management.base import AppCommand, BaseCommand, CommandError
from Weblvn.WeblvnApp.models import *
from Weblvn.WeblvnApp.views import *
import os
import pwd
import shutil
from django.db.models import Q
from optparse import * 



class Command(AppCommand):
    help = "Command to import or update a branch"
    option_list = BaseCommand.option_list + ( 
        make_option(
              "-i", 
              "--insert", 
              dest = "ins_branch",
              action = "store",  
              help = "insert a new branch", 
              metavar = "STRING"
        ),
        make_option(
            "-u", 
            "--update", 
            dest = "upd_branch",
            action= "store", 
            help = "update a branch", 
            metavar = "STRING"
        ),
        make_option(
              "-d", 
              "--display", 
              dest = "disp_branch",
              action = "store",  
              help = "display a branch", 
              metavar = "STRING"
        ),
        make_option(
              "-b", 
              "--bfrev", 
              dest = "bfr",
              action = "store",  
              help = "bfr of the branch", 
              metavar = "STRING"
        ),
        make_option(
              "-f", 
              "--flag", 
              dest = "flag",
              action = "store",  
              help = "specifies if branch is to be displayed", 
              metavar= "STRING"
        ),
    ) 

    def handle(self, *args, **options):
        print "usage is: python manage.py populate_branch -i <branch_name>  -b <bfr_id as int> -f <flag either 0 or 1>   -- to insert a new branch"
        print "      or: python manage.py populate_branch -u <branch_name>  -b <new_bfr_id as int> -f <new flag as int 0 or 1>  -- to upadate an existing branch"
        print "      or: python manage.py populate_branch -d <branch_name>   -- to dsplay a  branch"
        print "no extensive parameter checking is done   so be careful \n"
        print "\n"
#        print "option %s" %options
#        print "number of args %s "  % len(args)
#        if len(args) == 0:
#            raise CommandError("no arguments provided")
#        print options.keys() 

        if options['ins_branch']:    
            print "reading branch: %s\n" % options['ins_branch']
            branch_name = options['ins_branch']
            if not options['bfr']:
                raise CommandError("missing options in insert bfr is required") 
            else:
                print "reading bfr: %s\n" % options['bfr']
                bfr  = int(options['bfr'])
            if options['flag']:
                print "reading flag: %s\n" % options['flag']
                flag = int(options['flag'])
            else:
                flag = 1
            #insert rec
            try: 
                branch_exists = Branch.objects.get(branch_name=branch_name)
                print "specified branch %s exists it cannot be inserted " %(branch_name)
            except Branch.DoesNotExist:
                print "specified branch %s does not exist it can be inserted  " %(branch_name)
                new_branch = Branch(branch_name=branch_name, bfr_id=bfr, display_flag=flag)
                new_branch.save() 
        elif options['upd_branch']:
            print "reading branch: %s" % options['upd_branch']
            branch_name = options['upd_branch']
            bfr = -1
            if options['bfr']:
                bfr  = int(options['bfr'])
            if options['flag']:
                flag = int(options['flag'])
            #upd rec
            try: 
                branch_exists = Branch.objects.get(branch_name=branch_name)
                branch_exists.display_flag = flag
                print "flag is %d bfr is %d " %(flag, bfr)
                if bfr  is not -1:
                    branch_exists.bfr  = bfr
                print "branch to upd is  %s with bfr %d and display_flag %d"  %(branch_exists.branch_name, branch_exists.bfr_id, branch_exists.display_flag)
                branch_exists.save() 
            except Branch.DoesNotExist:
                print "specified branch %s does not exist cannot be updated " %(branch_name)

        elif options['disp_branch']:
            print "reading branch: %s" % options['disp_branch']
            branch_name = options['disp_branch']
            #display rec
            try: 
                branch_exists = Branch.objects.get(branch_name=branch_name)
                print "branch is  %s with bfr %d and display_flag %d"  %(branch_exists.branch_name, branch_exists.bfr_id, branch_exists.display_flag)
            except Branch.DoesNotExist:
                print "specified branch %s does not exist cannot be displayed " %(branch_name)
        else:     
            print "how did I got here: no options given \n"
            raise CommandError("unknown error or no options given")               
   
