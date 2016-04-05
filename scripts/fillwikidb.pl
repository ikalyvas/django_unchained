#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Text::CSV;
use Cwd;

#my $path_dir="\/home\/django\/lvnproject\/Weblvn\/";

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




my $file_csv;
my $file_txt;
my $file;
my $linecounter;

my $dbargs = {AutoCommit => 0,
              PrintError => 1};

my @data;

$file_csv="LVN.csv";
  
my $csv = Text::CSV->new();

my $bfr;
my $branch;
my $lvn;
my $pos;
my $ibfr;
my $ilvn;

#system(`sed -i 's/\<a\ href=\"//g' ${file_csv}`);
#system(`sed -i 's/\"\ class=\"twikiLink\"*\/a\>//g' ${file_csv}`);

print "delete all in wiki start\n";
my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
my $rowsdel = $dbh->do("delete from 'weblvnapp_wiki_entry'");
$dbh->commit();
$dbh->disconnect(); 
print "delete all in wiki end\n";
my $adaptation=""; 
open (CSV, "<", $file_csv) or die $!;
$linecounter=0;
while (<CSV>) {
  $linecounter++;
  if ($csv->parse($_)) {
     my @columns = $csv->fields();
     $ibfr = 0;
     $ilvn = 0;
     $columns[1] =~ s/^\s+//;
     $columns[1] =~ s/\s$//; 
     if ($columns[1]) {
       $pos= int(index($columns[1], "_"));
       print "pos at: $pos\n"; 
       $bfr = substr $columns[1], 0, $pos;
       $pos = $pos + 1;
       $lvn = substr $columns[1], $pos;
       print "found: $bfr $lvn -----\n";
       if ($bfr) {
         $ibfr= int($bfr);
       }
       if ($lvn) {
         $ilvn = int($lvn);
       }
       print "found: $bfr $lvn -----\n";
       if (($ibfr == 0)  ||  ($ilvn == 0)) {  
         print "---problem with following line: $columns[0] $columns[1] $columns[2] at line: $linecounter\n";
         next;
       } 
       else {
         print "found bfr in csv: $bfr \n";
       }
     }
     else {
       print "field seems to be empty at $linecounter\n";
       next;
     }
     print "before select \n";
     $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
     my $sth1 = $dbh->prepare('select branch_name from weblvnapp_branch where bfr_id = ?'); 
     $sth1->execute($bfr);
     while (@data = $sth1->fetchrow_array()) {
       $branch = $data[0];
       print "found branch: $branch bfr: $bfr \n";
     }
     $dbh->disconnect(); 
     print "=========Insert into db  bfr and lvn:  $bfr, $lvn \n\n";
     $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
     $adaptation=$columns[3].'- Adaptation: '.$columns[4];
       $dbh->do("insert into 'weblvnapp_wiki_entry'(bfr_lvn, branch_name_id, rev_id, author, adaptation, other) values (trim('$columns[1]'), trim('$branch'), trim('$columns[0]'), trim('$columns[2]'), trim('$adaptation'), trim('$columns[5]'))"); 
     $dbh->commit();
     $dbh->disconnect(); 
  } 
  else {
       my $err = $csv->error_input;
       print "----- Failed to parse line: $err line is: $linecounter";
  }
}	
close CSV;
