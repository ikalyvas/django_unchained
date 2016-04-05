#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Text::CSV;
use Cwd;

#my $path_dir="\/home\/siatos\/lvnproject\/Weblvn\/";

print "===================================================\n"; 
print "================   running fill db ================\n";
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



my @rev_db_file=("rev_db_cache_trunk","rev_db_cache_ng20", "rev_db_cache_ng20s","rev_db_cache_ng10", "rev_db_cache_ng10_cd9","rev_db_cache_ng10_cd8", "rev_db_cache_ng10_cd6", "rev_db_cache_ng10_cd6_pt5", "rev_db_cache_ng10_11b");

my $file_csv;
my $file_txt;
my $file;

system (`${script_path}cpfiles.sh`);
print "files have been copied locally \n";
my $dbargs = {AutoCommit => 0,
              PrintError => 1};

my @data;

foreach $file(@rev_db_file) {
  $file_csv="rev_dbs\/${file}.csv";
  $file_txt="rev_dbs\/${file}.txt";
  system(`cat ${file_txt} | awk 'NR>=14' > ${file_csv}`);
  system(`sed -i 's/|/,/g' ${file_csv}`);
  system(`rm ${file_txt}`);
  print "file $file_txt has been converted to $file_csv\n";
  
  my $csv = Text::CSV->new();
  my $branch = substr $file, 13;
  print "Branch is: $branch\n";  

  open (CSV, "<", $file_csv) or die $!;

  while (<CSV>) {
    if ($csv->parse($_)) {
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
           print "=== Insert into db: lvn: $columns[7]\tbranch: $columns[0]\trev: $columns[1]\n";
           my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
           $dbh->do("insert into 'weblvnapp_lvn_entry'(lvn, branch_name_id, rev_id, src_dir_change, h_file_change, inc_file_change, layout_check, layout_done, layout_status, md5sum_str, commit_date, author, layout_rev) values (trim('$columns[7]'), trim('$columns[0]'), trim('$columns[1]'), trim('$columns[2]'), trim('$columns[3]'), trim('$columns[4]'), trim('$columns[5]'), trim('$columns[8]'), trim('$columns[9]'), trim('$columns[10]'), trim('$columns[12]'), trim('$columns[13]'), trim('$columns[14]'))");
           $dbh->commit();
#           if ($dbh->err()) { 
#              die "$DBI::errstr\n"; 
#           }
           $dbh->disconnect(); 
         }   
       } 
    }   
    else {
       my $err = $csv->error_input;
       print "Failed to parse line: $err";
    }
  }	
  close CSV;
}
close CSV;
system(`rm ${script_path}\/rev_dbs\/rev_db*.txt`);
system(`rm ${script_path}\/rev_dbs\/rev_db*.csv`);

