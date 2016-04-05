#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Text::CSV;
use POSIX qw(strftime);
use DBI qw(:sql_types);
use Cwd;

print "===================================================\n"; 
print "==============   running update db ================\n";
print "===================================================\n"; 
print "\n";
print "\n";

#my $path_dir="\/home\/siatos\/lvnproject\/Weblvn\/";
my $path_dir=cwd();
$path_dir="${path_dir}\/..\/";
print "working in path: $path_dir\n";

print "\n";
print "\n";

my $sql_fpath="${path_dir}WeblvnApp.db";
print "sql file path located at: $sql_fpath\n";
print "\n";
print "\n";

my $script_path="${path_dir}scripts\/";
print "script path is: $script_path\n";
print "\n";
print "\n";


my @rev_db_file=("rev_db_cache_trunk", "rev_db_cache_15a_isu_pretest", "rev_db_cache_15b_isu_pretest", "rev_db_cache_ng15", "rev_db_cache_ng15_15a", "rev_db_cache_ng165_global_isu_pretest", "rev_db_cache_ng16_atca", "rev_db_cache_ng16_15b", "rev_db_cache_pretest_cISUG", "rev_db_cache_ng16_cloud", "rev_db_cache_16a_isu_pretest");
#my @rev_db_file=("rev_db_cache_trunk");


my $file_csv;
my $file_txt;
my $file;

system (`${script_path}cpfiles.sh`);
print "files have been copied locally \n";
my $dbargs = {AutoCommit => 0,
              PrintError => 1};

my $latest_rev;
my @data;

foreach $file(@rev_db_file) {
  $file_csv="rev_dbs\/${file}.csv";
  $file_txt="rev_dbs\/${file}.txt";
  print "txt: $file_txt  csv: $file_csv\n\n";
  system(`cat ${file_txt} | awk 'NR>=14' > ${file_csv}`);
  system(`sed -i 's/|/,/g' ${file_csv}`);
  system(`rm ${file_txt}`);
  print "file $file_txt has been converted to $file_csv\n";
  
  my $csv = Text::CSV->new();
  my $branch = substr $file, 13;
  print "Branch is: $branch\n";  
  my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
  my $sth1 = $dbh->prepare('select max(rev_id) from weblvnapp_lvn_entry where trim(branch_name_id)=?');
  $sth1->execute($branch);
 
  while (@data = $sth1->fetchrow_array()) {
    $latest_rev = int($data[0]);
    print "latest rev is: $latest_rev for Branch: $branch\n";
  }
  $dbh->disconnect(); 
  open (CSV, "<", $file_csv) or die $!;
  my $i=0;
  while (<CSV>) {
#      next if ($. == 1);
      if ($csv->parse($_)) {
        print "parsing line $i\n";  
        my @columns = $csv->fields();
        print "branch: $columns[0] rev: $columns[1] lvn: $columns[7]\n";
        if ($columns[0] =~ /#/ or $columns[0] =~ /-/ ) {
          print "Incorrect formatted line: $columns[0]\n"; 
        }
        else {  
          my $tmp = 0;
          $tmp =  int($columns[1]);
          if ($columns[7] == -1) {
             print "Found for rev $columns[1] --> lvn = $columns[7] : -1\n";      
          }
          else {          
            if ($tmp > $latest_rev) {   
              print "=== Insert into db: lvn: $columns[7]\tbranch: $columns[0]\trev: $columns[1]\n";
              my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
              $dbh->do("insert into 'weblvnapp_lvn_entry'(lvn, branch_name_id, rev_id, src_dir_change, h_file_change, inc_file_change, layout_check, layout_done, layout_status, md5sum_str, commit_date, author, layout_rev) values (trim('$columns[7]'), trim('$columns[0]'), trim('$columns[1]'), trim('$columns[2]'), trim('$columns[3]'), trim('$columns[4]'), trim('$columns[5]'), trim('$columns[8]'), trim('$columns[9]'), trim('$columns[10]'), trim('$columns[12]'), trim('$columns[13]'), trim('$columns[14]'))");
              $dbh->commit();
              if ($dbh->err()) { 
                die "$DBI::errstr\n"; 
              }
              $dbh->disconnect(); 
            }   
          } 
        }
      }
      else {
        my $err = $csv->error_input;
        print "Failed to parse line: $err";
      }
      $i=$i+1;
    }
  close CSV;
}
close CSV;

print "update last update time\n\n";
my $tstr = localtime;
print "time is: $tstr\n\n";

#my @data;
my $rows;
my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
my $sth2 = $dbh->prepare("select count(*) from 'weblvnapp_dbupdate'");
$sth2->execute();
while (@data = $sth2->fetchrow_array()) {
    $rows = int($data[0]);
}
$dbh->disconnect(); 
print "found $rows in last db update\n";
if ($rows > 0 ) {
  my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
  my $rowsdel = $dbh->do("delete from 'weblvnapp_dbupdate'");
  $dbh->commit();
  if ($rowsdel == 1) {
    my $now = strftime("%Y-%m-%d %H:%M:%S\n", localtime(time));
    print "now is:   $now\n";
    $dbh->do("insert into 'weblvnapp_dbupdate' (lastUpdDate) values ( trim('$now') )");
    $dbh->commit();
  }  
  else {
    print "error deleting last upd entry rows del = $rowsdel\n";
  }
  $dbh->disconnect(); 

}
else {
    print "this way when nothing in last db upd \n";
    my $now = strftime("%Y-%m-%d %H:%M:%S\n", localtime(time));
    print "now is:   $now\n";
    my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
    $dbh->do("insert into 'weblvnapp_dbupdate' (lastUpdDate) values ( trim('$now') )");
    $dbh->commit();
    $dbh->disconnect(); 

}

system(`rm ${script_path}\/rev_dbs\/rev_db*.txt`);
system(`rm ${script_path}\/rev_dbs\/rev_db*.csv`);
system(`cd /home/django/ && /bin/bash /home/django/poll.sh`);
system(`cd /home/django/ && /usr/bin/python /home/django/fix_svnlog.py`);
exit;
