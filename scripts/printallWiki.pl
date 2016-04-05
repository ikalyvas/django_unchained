#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Text::CSV;
use POSIX qw(strftime);
use DBI qw(:sql_types);
use Cwd;

print "===================================================\n"; 
print "==============   running printallWiki =============\n";
print "                                                   \n";
print "A perl script that produces a .txt output of all   \n";
print "wiki entries ifor a branch                         \n";
print "usage is: ./printallwiki branch                    \n"; 
print "                                                   \n";
print "===================================================\n"; 
print "\n";
print "\n";

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


my $file_txt;
my $file;

my $dbargs = {AutoCommit => 0,
              PrintError => 1};


my $latest_rev;
my @data;


my $noofargs=@ARGV;
print "args1: $noofargs\n";

if (!$noofargs or $noofargs != 1)  {
   print "empty\n";
   print "usage is: printWiki.pl <branch>  where <branch>=branch \n";
   exit 1; 
} 

my $branch=$ARGV[0];
print "branch is $branch\n";

my $rows;

my @line;
my @fields;
my $item;



my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";

my $Q ="select count(*) from 'weblvnapp_wiki_entry' where branch_name_id = '$branch'";
print "Q = $Q\n"; 

my $sth2 = $dbh->prepare($Q);
$sth2->execute();
@data=$sth2->fetchrow_array();
my $found = int($data[0]);
if ($found >= 0) {
   open (OUTFILE, ">", "LVN_$branch.html") or die $!;
   print "found: $found entries from $branch\n";
   $Q ="select trim(rev_id), trim(bfr_lvn), trim(author), trim(adaptation) from 'weblvnapp_wiki_entry' where branch_name_id= '$branch' order by rev_id desc";
   print "Q = $Q\n"; 
   $sth2 = $dbh->prepare($Q);
   $sth2->execute();
   my $i;
   for ($i=1; $i<=$found; $i++) {
       @data = $sth2->fetch();
       foreach $item(@data) {
          print OUTFILE "@$item[0]\t - @$item[1]\t - @$item[2]\t - @$item[3]\n"; 
       } 
   }
}
else {
   print "found nothing /n";
}
close OUTFILE; 
