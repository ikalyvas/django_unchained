#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Text::CSV;
use POSIX qw(strftime);
use DBI qw(:sql_types);
use Cwd;
use Switch;

print "|==================================================================|\n"; 
print "|==============   running printWiki_rev1_2_rev2 ===================|\n";
print "|                                                                  |\n";
print "|A perl script that produces a .txt output of the                  |\n";
print "|wiki entries                                                      |\n";
print "|usage is: ./printWiki_rev1_2_rev2 rev1 rev2 [<branch1> <branch2>] |\n"; 
print "|where rev1 = rev of branch 1 (src)                                |\n";
print "|      rev2 = rev of branch 2 (trg). Script still                  |\n";
print "|needs further work to be improved.                                |\n";
print "|==================================================================|\n"; 
print "|==================================================================|\n"; 
print "|                                                                  |\n";
print "|           branch 1                 branch2                       |\n";
print "|              |                       |                           |\n";
print "|              |<-rev 1                |<-rev 2                    |\n";
print "|              |                       |                           |\n";
print "|bfr id = 1----x-----------------------x-------------trunk         |\n";
print "|              ^                       ^                           |\n";
print "|              | bfr_id 1              | bfr id 2                  |\n";
print "|                                                                  |\n";
print "|                                                                  |\n";
print "|==================================================================|\n"; 
print "\n";
print "\n";

my $path_dir=cwd();
$path_dir="${path_dir}\/..\/";
#print "working in path: $path_dir\n";

#print "\n";
#print "\n";

my $sql_fpath="${path_dir}WeblvnApp.db";
#print "sql file path located at: $sql_fpath\n";
#print "\n";
#print "\n";

my $script_path="${path_dir}scripts\/";
#print "script path is: $script_path\n";
#print "\n";
#print "\n";


my $file_txt;
my $file;

my $dbargs = {AutoCommit => 0,
              PrintError => 1};


my $latest_rev;
my @data;


my $noofargs=@ARGV;
#print "args1: $noofargs\n";

if (!$noofargs or ($noofargs != 2 and $noofargs != 4)) {
   print "usage is: printWiki.pl <rev1> <rev2> [<bra1> <bra2>] where rev1=start rev2=end (rev1 rev2 are required)\n";
   print "and bra1=branch for rev1 bra2=branch for rev2 (bra1 and bra2 are optional)\n";
   print "Either give no branches just rev numbers or both branches and revs. \n";
   print "For bra1 it will try to find max(rev) that belongs to the given branch and is less then rev1. The same for bra2. \n";
   exit 1; 
} 

my $bra1='';
my $bra2='';
my $rev1='';
my $rev2='';
my $rev1_1='';
my $rev2_1='';

$rev1=$ARGV[0];
$rev2=$ARGV[1];
if ($noofargs == 4) {
   $bra1=$ARGV[2];
   $bra2=$ARGV[3];
}

my $branch_id1;
my $branch_id2;
my $bfr_id1;
my $bfr_id2;
my $path_val=0b0;





#print "-------------------------------\n";
#print "from $rev1 to $rev2\n";
#print "-------------------------------\n";

my $rows;

if (($bra1 eq '') xor ($bra2 eq '')) {
   print "Either give no branches just rev numbers or both branches and revs. \n";
   exit 1;
}
else {
   print "Args: $noofargs $rev1 $rev2 $bra1 $bra2\n";
}

   
$branch_id1='';
$branch_id2='';

if ($bra1 ne '') {
   my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
   my $sth2 = $dbh->prepare("select trim(branch_name_id) from 'weblvnapp_lvn_entry' where rev_id = '$rev1' and trim(branch_name_id)='$bra1'");
   $sth2->execute();
   while (@data = $sth2->fetchrow_array()) {
#    $rows = int($data[0]);
       $branch_id1=$data[0];
   }
   $dbh->disconnect();
   if ($branch_id1 eq '') {
      print "$rev1 not found in given branch. Try to find closest to $rev1 belonging to $bra1.\n";
      $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
      $sth2 = $dbh->prepare("select trim(branch_name_id), max(rev_id) from 'weblvnapp_lvn_entry' where rev_id <='$rev1' and trim(branch_name_id)='$bra1'");
      $sth2->execute();
      while (@data = $sth2->fetchrow_array()) {
         $branch_id1=$data[0];
         $rev1 = $data[1];
      }
      $dbh->disconnect();
   }
   $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
   $sth2 = $dbh->prepare("select trim(branch_name_id) from 'weblvnapp_lvn_entry' where rev_id = '$rev2' and trim(branch_name_id)='$bra2'");
   $sth2->execute();
   while (@data = $sth2->fetchrow_array()) {
#    $rows = int($data[0]);
       $branch_id2=$data[0];
   }
   $dbh->disconnect();

   if ($branch_id2 eq '') {
      print "$rev2 not found in given branch. Try to find closest to $rev2 belonging to $bra2.\n";
      $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
      $sth2 = $dbh->prepare("select trim(branch_name_id), max(rev_id) from 'weblvnapp_lvn_entry' where rev_id <= '$rev2' and trim(branch_name_id)='$bra2'");
      $sth2->execute();
      while (@data = $sth2->fetchrow_array()) {
         $branch_id2=$data[0];
         $rev2 = $data[1];
      }
      $dbh->disconnect();
   }
}
else {
   my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
   my $sth2 = $dbh->prepare("select trim(branch_name_id), max(rev_id) from 'weblvnapp_lvn_entry' where rev_id <='$rev1'");
   $sth2->execute();
   while (@data = $sth2->fetchrow_array()) {
       $branch_id1=$data[0];
       $rev1 = $data[1];
   }
   $dbh->disconnect();
 
   $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
   $sth2 = $dbh->prepare("select trim(branch_name_id), max(rev_id) from 'weblvnapp_lvn_entry' where rev_id <='$rev2'");
   $sth2->execute();
   while (@data = $sth2->fetchrow_array()) {
       $branch_id2=$data[0];
       $rev2 = $data[1];
   }
   $dbh->disconnect();
 
}

my $inbranch;
print "-------------------------------------------------\n";
print "from $branch_id1 at $rev1 to $branch_id2 at $rev2\n"; 
print "-------------------------------------------------\n";
if ($branch_id1 eq $branch_id2) {
   print "in branch \n";
   $inbranch = 1;
   $path_val=0b010;
}
else {
   print "not in branch\n";
   $inbranch = 0;
}

print "-------------------------------------------------\n";
print "find bfrs\n";
print "-------------------------------------------------\n";
$bfr_id1=$bfr_id2=0;
my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
my $sth2 = $dbh->prepare("select trim(bfr_id) from 'weblvnapp_branch' where branch_name='$branch_id1'");
$sth2->execute();
while (@data = $sth2->fetchrow_array()) {
#    $rows = int($data[0]);
    $bfr_id1=$data[0];
}
if ($inbranch == 1) {
   $bfr_id2 = $bfr_id1;
}
else {
   $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
   $sth2 = $dbh->prepare("select trim(bfr_id) from 'weblvnapp_branch' where branch_name='$branch_id2'");
   $sth2->execute();
   while (@data = $sth2->fetchrow_array()) {
#    $rows = int($data[0]);
      $bfr_id2=$data[0];
   }
   $dbh->disconnect();
}


print "---------------------------------------------------------------------------------\n";
print "from $branch_id1 at $rev1 (with $bfr_id1) to $branch_id2 at $rev2 (with $bfr_id2)\n"; 
print "---------------------------------------------------------------------------------\n";
if ($bfr_id1 == 1) {
   print "start point is trunk "; 
   if ($bfr_id2 == 1) {
       print "and end point is trunk\n"; 
       $rev1_1 = $bfr_id1;
	   $rev2_1 = $bfr_id1;
	   $path_val=0b010;
   }	
   else {
        print "and end point is $branch_id2\n";
		if ($bfr_id2 > $rev1) {
           print "start point in trunk cannot be greater than bfr from end point branch. We dont go back \n";
		   exit 1;
		}	
		else {
             $rev1_1 = $bfr_id2;
			 $rev2_1 = $bfr_id2;
	         $path_val=0b011;
	    }		
   }
}	
else {
   print "start point is $branch_id1 ";
   if ($bfr_id2 == 1) {
       print "and end point is trunk\n"; 
		if ($bfr_id1 > $rev2) {
           print "end point in trunk cannot be less than bfr from start branch. We dont go back \n";
		   exit 1;
		}	
		else {
             $rev1_1 = $bfr_id1;
			 $rev2_1 = $bfr_id1;
	         $path_val=0b110;
	    }		
   }	
   else {
        print "and end point is $branch_id2\n";
        $rev1_1 = $bfr_id1;
		$rev2_1 = $bfr_id2;
	    $path_val=0b111;
   }
}	

my $Q;
open (OUTFILE, ">", "report.txt") or die $!;
   switch ($path_val) {
      case 0b010 {
          print_head_foot($rev1, $rev2, $branch_id1, 1);
          run_the_path($rev1, $rev2, $branch_id1); 
          print_head_foot($rev1, $rev2, $branch_id1, 0);
	  }	   
      case 0b110 {
          print_head_foot($rev1, $bfr_id1, $branch_id1, 1);
          run_the_path($rev1, $bfr_id1, $branch_id1); 
          print_head_foot($rev1, $bfr_id1, $branch_id1, 0);

		  print_head_foot($rev2_1, $rev2, "trunk", 1);
          run_the_path($rev2_1, $rev2, "trunk"); 
          print_head_foot($rev2_1, $rev2, "trunk", 0);
	  }	   
      case 0b011 {
          print_head_foot($rev1, $bfr_id2, "trunk", 1);
          run_the_path($rev1, $bfr_id2, "trunk"); 
          print_head_foot($rev1, $bfr_id2, "trunk", 0);

          print_head_foot($bfr_id2, $rev2, $branch_id2, 1);
		  run_the_path($bfr_id2, $rev2, $branch_id2); 
          print_head_foot($bfr_id2, $rev2, $branch_id2, 0);
	  }	   
      case 0b111 {
          print_head_foot($rev1, $bfr_id1, $branch_id1, 1);
          run_the_path($rev1, $bfr_id1, $branch_id1); 
          print_head_foot($rev1, $bfr_id1, $branch_id1, 0);

          print_head_foot($rev1_1, $rev2_1, "trunk", 1);
          run_the_path($rev1_1, $rev2_1, "trunk"); 
          print_head_foot($rev1_1, $rev2_1, "trunk", 0);

          print_head_foot($bfr_id2, $rev2, $branch_id2, 1);
          run_the_path($bfr_id2, $rev2, $branch_id2); 
          print_head_foot($bfr_id2, $rev2, $branch_id2, 0);
	  }	   
      else {
          print "should not reach this point\n"; 
      }		  

   }	   


  close OUTFILE; 

  
  
sub run_the_path
{
	my $r1;
	my $r2;
	my $branch;
	($r1, $r2, $branch)=@_;
	print "rev1 is $r1\n";
	print "rev2 is $r2\n";
	print "branch is $branch\n";

	my @line;
    my @fields;
    my $item;
    if ($r1 > $r2) {
       ($r1, $r2) = ($r2, $r1);
    }
 
	$dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
	$Q="select count(*) from 'weblvnapp_wiki_entry' where (rev_id between '$r1' and '$r2') and (branch_name_id= '$branch')";
    print "$Q\n";
    $sth2 = $dbh->prepare($Q); 
	#$sth2 = $dbh->prepare("select count(*) from 'weblvnapp_wiki_entry' where (rev_id between '$r1' and '$2') and (branch_name_id= '$branch')");
    $sth2->execute();
    @data=$sth2->fetchrow_array();
    my $found=$data[0];
    print("found : $found\n");
      my $i;
      if ($found > 0) {
         $Q="select trim(rev_id), trim(author), trim(bfr_lvn), trim(adaptation) from 'weblvnapp_wiki_entry' where (rev_id between '$r1' and '$r2')  and (branch_name_id= '$branch') order by rev_id asc";
         print "$Q\n";
         $sth2 = $dbh->prepare($Q); 
		 #$sth2 = $dbh->prepare("select trim(rev_id), trim(author), trim(bfr_lvn) from 'weblvnapp_wiki_entry' where (rev_id between '$r1' and '$r2')  and (branch_name_id= '$branch')");
         $sth2->execute();
	     for ($i=1; $i<=$found; $i++) {
            @data = $sth2->fetch();
	        foreach $item(@data) {
                             #012345678901234567890123456789012345678901234567890123456789012345678901234567890   
                             #          1         2         3         4         5         6         7         8 
	           print OUTFILE "|@$item[0]\t  |  @$item[1]\t   | @$item[2]  |                                    |\n"; 
	        }		 
         }
      }
      $dbh->disconnect();
}

sub print_head_foot 
{
	my $r1;
	my $r2;
	my $branch;
	my $head;
	($r1, $r2, $branch, $head)=@_;
    if ($head == 1) { 
			          #012345678901234567890123456789012345678901234567890123456789012345678901234567890   
				      #          1         2         3         4         5         6         7         8 
     	print OUTFILE "|------------------------  $branch start from $r1 to $r2 -----------------------|\n";
		print OUTFILE "|-- Rev ---|---- Author ----|-- bfr_lvn -|--------------------------------------|\n";
		print OUTFILE "\n";
    }
	else  {
			          #012345678901234567890123456789012345678901234567890123456789012345678901234567890   
				      #          1         2         3         4         5         6         7         8 
     	print OUTFILE "------------------------  $branch end from $r1 to $r2 ---------------------------\n";
		print OUTFILE "---------------------------------------------------------------------------------\n";
		print OUTFILE "\n";
	}	
}	

