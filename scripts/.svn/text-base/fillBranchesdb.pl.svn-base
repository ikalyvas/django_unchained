#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Text::CSV;
use Cwd;

print "==================================================\n";
print "=============== Fill Branches Table ==============\n";
print "==================================================\n";


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
my $branch;
my @branches=("trunk", "ng20","ng10", "ng10_cd9", "ng10_11b", "ng21_12a", "cat_main", "cat_japan","ng21");

system (`${script_path}cpBranches.sh`);
print "file svn_branches_follower.conf has been copied locally \n";

my $dbargs = {AutoCommit => 0,
              PrintError => 1};
my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
my @data;

my $file="svn_follower_branches";

my $file_csv="rev_dbs\/${file}.csv";
my $file_txt="rev_dbs\/${file}.conf";

system(`cat ${file_txt} | awk 'NR>=65' > ${file_csv}`);
system(`sed -i 's/|/,/g' ${file_csv}`);
system(`sed -i 's/-/ /g' ${file_csv}`);
system(`sed -i 's/+/ /g' ${file_csv}`);
system(`sed -i 's/ //g' ${file_csv}`);
system(`rm ${file_txt}`);
print "file $file_txt has been converted to $file_csv\n";
  

#foreach $branch(@branches) {
  print "Branch is: $branch\n";
  my $csv = Text::CSV->new();
  open (CSV, "<", $file_csv) or die $!;
  while (<CSV>) {
    if ($csv->parse($_)) {
      my @columns = $csv->fields();
      if ($columns[0] !~ /TABLE/ ) {
        print "Incorrect formatted line: $columns[0]\n"; 
      }
      else {
        print "found branch $columns[1]\n\n";
        foreach $branch(@branches) {  
	  if ($columns[1] eq $branch ) {
            print "Branch is: $branch\n";  
            print "Branch: $columns[1] bfr: $columns[2] \n";
            print "=== Insert into db: branch: $columns[1]\tbfr: $columns[2]\n";
            my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
            $dbh->do("insert into 'weblvnapp_branch'(branch_name, bfr_id) values (trim('$columns[1]'), trim('$columns[2]'))");
            $dbh->commit();
            $dbh->disconnect(); 
            last;
          }
        }    
      }
    }   
  }
  close CSV;
#  else {
#       my $err = $csv->error_input;
#       print "Failed to parse line: $err";
#    }
#}	
close CSV;

system(`rm ${script_path}\/rev_dbs\/svn_*.csv`);
#system(`rm ${script_path}\/rev_dbs\/rev_db*.csv`);

