#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Cwd;
use Text::CSV;

use Time::localtime;
my $counter=0;
my $rev='';
my @data;
my @builddata;
my @revdata;

print "\n";

my $noofargs=@ARGV;
#print "number of args: $noofargs\n";

my $usr;
if ($noofargs != 0) {
   print "Usage : ./buildinfo_all.pl \n";
   exit 1;
}

my $arr_ref;

my $builds_cre_file;
my $builds_file;
my $last_count;

my $svn_export_file;
my $str;

my $SCRIPT_DIR="~/lvnproject/Weblvn/scripts";
# read conf file
my @build_data = <DATA>;

print "here \n";
print "get Current date\n";
my $tm = localtime;
my ($day, $month, $year) = ($tm->mday, $tm->mon, $tm->year);
$month += 1;
$year += 1900;
print "today is $day - $month - $year\n";

foreach my $line (@build_data) {
    my $relname;
	my $buildpath;
	my $branch='';
	my $build='';
	my $pos;
	my $len;
	my $delivery;
	my $latest_rev;
	$line =~ s/#.*$//;
	print "$line\n";
	next if $line =~ /^\s*$/;
	$line =~ s/\s+//g;
	if ($line =~ /\|.*\|.*\|/) {
	    ($buildpath, $relname, $build) = split( /\|/, $line);
        print "$buildpath, $relname, $build\n";
		if ($build eq "None") {
			print "running for $relname\n";
            $latest_rev = select_latest_entry_from_db($relname);
			print "found latest rev $latest_rev for $relname\n";
            system(`./builds_trunk.sh $buildpath $relname`);
	        $builds_cre_file = "build_cre_dt_".$relname.".txt";
            print "builds file: $builds_cre_file \n";
		    ($arr_ref, $last_count) = process_trunk_file($builds_cre_file, $latest_rev);
		    @builddata = @{$arr_ref};	
	        print "\n";
	        foreach my $row(@builddata) {
                foreach my $val(@$row) {
                    print "$val ";
	            }
	        print "\n";
	        }

	       for ($counter=0;$counter<$last_count;$counter++) {
		        $revdata[$counter]=$builddata[$counter][2];
		        print "rev : $revdata[$counter]\n";
           }
        }	
        else {
		     print "running for $relname\n";
             system(`./builds.sh $buildpath $relname`);
	         $builds_cre_file = "build_cre_dt_".$relname.".txt";
		     $builds_file     = "build_dir_dt_".$relname.".txt";
             print "-------builds file: $builds_cre_file \n";
             $latest_rev = select_latest_entry_from_db($relname);
			 print "found latest rev $latest_rev for $relname\n";
			 ($arr_ref, $last_count) = process_cat_file($relname, $builds_file, $builds_cre_file, $latest_rev);
	         unlink $builds_file;
		     @builddata = @{$arr_ref};	
	         print "\n";
	         foreach my $row(@builddata) {
                 foreach my $val(@$row) {
                    print "$val ";
	             }
	         print "\n";
	         }

	         for ($counter=0;$counter<$last_count;$counter++) {
		        $revdata[$counter]=$builddata[$counter][2];
		        print "rev : $revdata[$counter]\n";
             }
	     }
		 if ($last_count > 1) {
	        print "svn export for  $relname\n";
	        prepare_svnexport_script($relname, @revdata); 
	        system("chmod 755 build_export.sh") ;
	        system("./build_export.sh");
	        for ($counter=0; $counter < $last_count; $counter++) {
	           $svn_export_file = "./svnexpdir/mf".$builddata[$counter][2].".txt";
	           open (SVNFILE, "<", $svn_export_file) or print "file $svn_export_file not found or could not be opened\n";
               while (<SVNFILE>) {
                 chomp;
                 $str  = $_;
	             if ($str =~ /^DELIVERY:/) {
	                 $pos = index($str, ":");
	                 $len  = length($str); 
                     $delivery = substr($str, $pos+1, $len-1);
	                 print "delivery $delivery\n";
                     $builddata[$counter][3] = $delivery;
	             } 
	           }       
               close SVNFILE;   
             }  
	         print "cleaning \n";
		     system("rm ./svnexpdir/mf*.txt");
		     system("rm build_export.sh");
		 }	 
	     unlink $builds_cre_file;
	     my $csvfile = "csv_$relname.txt";
         open (CSVFILE, ">", $csvfile) or die $!;

	     for ($counter=0; $counter < $last_count; $counter++) {
            print CSVFILE "$builddata[$counter][0], $builddata[$counter][1], $builddata[$counter][2], $builddata[$counter][3], $builddata[$counter][4]\n";
	     }	
         close CSVFILE;
	     filldb($relname, $csvfile);
		 unlink $csvfile;
    }
}

sub process_cat_file
{
	my $builds_file;
	my $builds_cre_file;
    my @builddata;
	my @builddata_row;
	my $branch;
	my $latest_rev;
	($branch, $builds_file, $builds_cre_file, $latest_rev)=@_;
	print "builds: $builds_file builds: $builds_cre_file\n";
	my $counter = 0;
    open (BSFILE, "<", $builds_file) or die $!;
    my $bldline;
	my $len2;
	my $build;
	my $buildname;
	my $buildrev;
	my $build_found=0;
#	my $iso_found=0;
	my $pos1;
    my $pos;
	my $len;
	my $delivery;
    my $bldlinecre;
	my $build_dt;
	my $line_count;
	$line_count  = 0;
    while (<BSFILE>) {
		$line_count ++;
    }
    print "found $line_count lines in $builds_file\n";
    close BSFILE;
    open (BSFILE, "<", $builds_file) or die $!;	
	while (<BSFILE>) {
        chomp;
        $bldline  = $_;
		$len2 = length($bldline);
		if ($bldline =~ /^build_\d{1,4}/) {
			 $pos1 = index($bldline, ":");
			 $build = substr($bldline, 0, $pos1);
			 $build_found = 1;
			 print "found build: $build\n";
			 $builddata_row[0] = $build;
             open (BSCREFILE, "<", $builds_cre_file) or die $!;
             $build_dt= "";
			 while (<BSCREFILE>) {
                     chomp;
                     $bldlinecre  = $_;
		             if ($bldlinecre =~ /$build/) {
			            $build_dt = substr($bldlinecre, 0, 19);
				        $builddata_row[4]= $build_dt;
			            print "found build date: $build_dt\n";
						$build_dt = "";
                        last; 
					 }
		    }	 
            close BSCREFILE;
		} 
		elsif (($bldline =~ /R_FSPR5CAT[a-zA-Z0-9_\.]*iso/) and ($bldline !~ /md5sum/)){
			 if ($build_found == 1) {
				$build_found = 0;
                $pos1 = index($bldline, "R_FSPR5CAT");
			    $len2 = length($bldline);
			    $buildname = substr($bldline, $pos1, $len2-1);
				print "buildname is $bldline";
                if ($branch eq "cat_main") {
				       if ($buildname =~ /(?<=r)\d{6}(?=_debug\.iso)/g) {
						   print "build name 2 : $buildname\n";
				           $buildrev = substr($buildname, $-[0], 6);
						   print "and buildrev is $-[0]  $buildrev \n";
			           }
			     }
                 else {
				       if ($buildname =~ /(?<=r)\d{6}(?=\.iso)/g) {
				            $buildrev = substr($buildname, $-[0], 6);
			           }   
				 }	   
                 print "$build, $buildname, $buildrev, $build_dt\n";
				 $builddata_row[1]= $buildname;
				 $builddata_row[2]= $buildrev;
				 $builddata_row[3]= "-";
		         if ($buildrev > $latest_rev) {
				    push(@builddata, [@builddata_row]);
				 #print("at $builddata[$counter]\n");
                    $counter++;
			     }
				 else {
	                 print "rev found $buildrev but latest is $latest_rev it will not be pushed\n";		
				 }	 
		    }
        } 
    }   
    close BSFILE;
	print "\n";
	foreach my $row(@builddata) {
       foreach my $val(@$row) {
          print "$val ";
	   }
	   print "\n";
	}
    return (\@builddata, $counter)
}


sub process_trunk_file
{
	my $builds_file;
    my @builddata;
	my @builddata_row;
	my $latest_rev;
	($builds_file, $latest_rev)=@_;
	my $counter = 0;
    open (BSFILE, "<", $builds_file) or die $!;
    my $bldline;
	my $len2;
	my $build="NA";
	my $buildname;
	my $buildrev;
	my $build_found=0;
#	my $iso_found=0;
	my $pos1;
    my $pos;
	my $len;
	my $delivery;
    my $bldlinecre;
	my $build_dt;
	my $line_count;
#	$line_count  = 0;
#    while (<BSFILE>) {
#		$line_count ++;
#    }
#    print "found $line_count lines in $builds_file\n";
#    close BSFILE;
#    open (BSFILE, "<", $builds_file) or die $!;
	while (<BSFILE>) {
        chomp;
        $bldline  = $_;
		$len2 = length($bldline);
	    $build_dt = substr($bldline, 0, 19);
		$builddata_row[4]= $build_dt;
		$buildname = substr($bldline, 36, $len2-1); 
	    if ($buildname =~ /r\d{6}/g) {
			$buildrev = substr($buildname, $-[0], 7);
			$buildrev = substr($buildrev, 1, 6);
		}
		$builddata_row[0]= "-";
		$builddata_row[1]= $buildname.".iso";
		$builddata_row[2]= $buildrev;
		$builddata_row[3]= "-";
		if ($buildrev > $latest_rev) {
           print "$counter: $builddata_row[0], $builddata_row[1], $builddata_row[2], $builddata_row[3], $builddata_row[4]\n";
		   push(@builddata, [@builddata_row]);
           #or use: $builddata[$counter]=[@builddata_row];
		   #$builddata[$counter]=[@builddata_row];
           $counter++;
	    }
		else  {
	       print "rev found $buildrev but latest is $latest_rev it will not be pushed\n";		
		}	

    } 
    close BSFILE;
    return (\@builddata, $counter)
}

sub prepare_svnexport_script 
{
	my $inbranch;
	my @indata;
	($inbranch, @indata)=@_;
    print "received branch $inbranch\n"; 
    my $line = ""; 
	#my $svnfile = "svnExp.sh";
	my $svnfileexp = "build_export.sh";
	#my $svnfileexpcl= "clean_build_export.sh";
    my $svnline = "svn+ssh://ngman\@svne1.access.nokiasiemensnetworks.com/isource/svnroot/flexi_bng/";
	if ($inbranch eq "trunk")  {
       $svnline = $svnline . "$inbranch"."/src/scripts/nginfo/MANIFEST";
	   print "$svnline\n";
	}
    else {
       $svnline = $svnline . "branches/delivery/$inbranch"."/src/scripts/nginfo/MANIFEST";
	   print "$svnline\n";
	}	
#    open (SVNFILE, ">", $svnfile) or die $!;
    open (SVNFILEEXP, ">", $svnfileexp) or die $!;
    $line = "cd $SCRIPT_DIR/svnexpdir/";
    print SVNFILEEXP "$line\n";
    foreach $b(@indata) {
        $line = "svn export -r$b $svnline mf$b.txt";
        print SVNFILEEXP "$line\n";
    }
    close SVNFILEEXP;
}

sub filldb {
	my $branch;
	my $csvfile;
	($branch, $csvfile)=@_;
    print "received branch $branch and csv file $csvfile\n"; 
    print "===================================================\n"; 
    print "==============   running fill build  ==============\n";
    print "===================================================\n"; 
    print "\n";
    print "\n";

    my $path_dir=cwd();
    #$path_dir="${path_dir}\/..\/";
    print "working in path: $path_dir\n";

    print "\n";
    print "\n";


    my $sql_fpath="\/home\/django\/lvnproject\/Weblvn\/WeblvnApp.db";
    print "sql file path located at: $sql_fpath\n";
    print "\n";

    my $linecounter=0;

    my $count = 0;
    my $dbargs = {AutoCommit => 0,
                  PrintError => 1};

    my @data;
	my @columns;
    my $csv = Text::CSV->new();
    my $pos;
    my $build;
	my $rev;
    my $stmt;
    my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
	my $sth1;
    open (CSV, "<", $csvfile) or die $!;
    while (<CSV>) {
        $linecounter++;
        if ($csv->parse($_)) {
            @columns = $csv->fields();

            print "before select build $columns[0]  $columns[1] in $branch\n";
			#$count = $dbh->selectrow_array("select count(*) from weblvnapp_build_entry where branch_name_id = '$branch' and build_name = '$columns[1]'");  

            #my $sth1 = $dbh->prepare('select count(*) from weblvnapp_build_entry where branch_name_id like ? and build_name like ?');
			$branch =~ s/^\s+|\s+$//g;
			$columns[0] =~ s/^\s+|\s+$//g;	
			$columns[1] =~ s/^\s+|\s+$//g;

			if ($columns[0] =~ /^build/) {
			     $sth1 = $dbh->prepare("select build, rev, dt from weblvnapp_build_entry where branch_name_id = ? and build = ?");
			     $sth1->execute($branch,$columns[0]);
			}
		    else {
			     $sth1 = $dbh->prepare("select build, rev, dt from weblvnapp_build_entry where branch_name_id = ? and build_name = ?");
			     $sth1->execute($branch,$columns[1]);
			}	
			$count = 0;
            while (@data = $sth1->fetchrow_array()) {
				 $count ++;
            }
			if ($count > 0) {
                print "selected buildname $columns[1] was found in db $count times     not entered \n";
			}	
			else {
                print "insert build $columns[0] $columns[1] $columns[2] $columns[3] in db\n";
                $dbh->do("insert into 'weblvnapp_build_entry'(build, branch_name_id, build_name, rev, rel, dt) values (trim('$columns[0]'), trim('$branch'), trim('$columns[1]'),
					trim('$columns[2]'), trim('$columns[3]'), trim('$columns[4]'))");  
                $dbh->commit();
			}	
        } 
        else {
             my $err = $csv->error_input;
             print "----- Failed to parse line: $err line is: $linecounter";
        }
    }	
    $dbh->disconnect(); 
    close CSV;
}

sub select_latest_entry_from_db {
	my $branch;
	($branch)=@_;

	my @data_rev;
    $data_rev[0] = -1; 

    my $path_dir=cwd();
    #$path_dir="${path_dir}\/..\/";
    print "working in path: $path_dir\n";


    my $sql_fpath="\/home\/django\/lvnproject\/Weblvn\/WeblvnApp.db";
    print "sql file path located at: $sql_fpath to select latest for $branch\n";
    print "\n";

    my $dbargs = {AutoCommit => 0,
                  PrintError => 1};

    my $stmt;
    my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";
	my $sth1;
    $sth1 = $dbh->prepare("select max(rev) from weblvnapp_build_entry where branch_name_id = ?");
    $sth1->execute($branch);
    @data_rev = $sth1->fetchrow_array();
    if ($data_rev[0] > -1) {
         print "found max rev $data_rev[0] for $branch\n";
    }
	else {
         print "incorrect value \n";
	}	
    $dbh->disconnect(); 
    return ($data_rev[0]);
    
}
__DATA__
#======================================================================|
#     path                          |  release      | build dir exists | 
#======================================================================|
##NG3.0/ng30_13a_delivery_AB2/ATCA   |  ng30_13a     | None            |
NG3.0/ng30_13a_delivery_AB4/ATCA     |  ng30_13a     | None            | 
NG3.1/trunk_debug_AB2/ATCA           |  trunk        | None            |
##NG3.1/trunk_debug_AB4/ATCA         |  trunk        | None            |
##NG3.1/trunk_delivery_AB2/ATCA      |  trunk        | None            |
NG3.1/trunk_delivery_AB4/ATCA        |  trunk        | None            |
#NG3.1/ng31_pt4_delivery_AB4/ATCA    |  ng31_pt4     | None            |
#NG3.1/ng31_pt7_delivery_AB4/ATCA    |  ng31_pt7     | None            |
NG3.1/ng31_pt9_delivery_AB4/ATCA     |  ng31_pt9     | None            |
NG3.1/ng31_delivery_AB4/ATCA         |  ng31         | None            |
NG3.1/ng3120_14a_delivery_AB4/ATCA   |ng3120_14a     | None            |
#cat_japan/ATCA                      |  cat_japan    | build           |
#cat_main/ATCA                        |  cat_main     | build           |
#ng211/ATCA                           |  ng211        | build           |
#ng212/ATCA                           |  ng212        | build           |
##ng21_12a/ATCA                      |  ng21_12a     | build           |
#======================================================================|

# Some necessary notes:
# First column path is the actual path after home where builds reside
# two different configurations are used for the build location:
# one is used for cat_main, cat_japan (cat pf) where builds are located
# under ATCA dir in builds dirs. In each build_nnn dir the actual iso file together
# with md etc files are located the other
# the other is used for trunk, ng30_13a (cougar pf) where builds are located in dirs under ATCA 
# that have the same name as the iso file.
# The third column in the DATA is used for this purpose
# The second column is the actual release
