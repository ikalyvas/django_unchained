#!/usr/bin/perl
use strict; 
use DBI;
use warnings;
use Cwd;
use Text::CSV;

my $branch='';
my $prefix='';
my $counter=0;
my $rev='';
my @data;
my @builddata;
my @revdata;
my @builddatadesc;
my $BFR="133406";

my $count2=0;
print "\n";
my $last_count;

#my @branches=("trunk", "ng20","ng10", "ng10_cd9", "ng10_11b", "ng21_12a", "cat_main", "cat_japan","ng21");
my @branches=("cat_japan", "cat_main", "ng21", "ng21_12a");
#my @branches=("ng21", "ng21_12a");
#my @branches=("ng21_12a");
#my @branches=("cat_japan");


#my $dbh = DBI->connect( "dbi:SQLite:${sql_fpath}", "", "", $dbargs ) || die "Cannot connect: $DBI::errstr";

my $noofargs=@ARGV;
print "number of args: $noofargs\n";

my $usr;
if ($noofargs != 1) {
   print "Usage : ./buildinfo.pl <usrname> \n";
   print "<usrname> : user that will be used to connect to hyperion in order to run svn export\n";
   print "future mods: use django user to directly connect to svn. Then there is no need to supply username or connect to hyperion.\n";
   print "also branches can be derived from table branches in db and svn could run from a build that does not exist in db and above.\n";
   exit 1;
}

print "Args: $ARGV[0]\n";
$usr=$ARGV[0];

foreach $branch (@branches) {
    print "running for $branch \n";
	print "\n"; 
	system(`./builds.sh $branch`);

    my $builds_file;
    my $builds_cre_file;
	$builds_file = "build_dir_det.txt";
	$builds_cre_file = "build_cre_dt.txt";
    print "builds file: $builds_file \n";
    
	$counter = 0;
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
	while (<BSFILE>) {
        chomp;
        $bldline  = $_;
		$len2 = length($bldline);
		if ($bldline =~ /^build_\d{1,4}/) {
			 $pos1 = index($bldline, ":");
			 $build = substr($bldline, 0, $pos1);
			 $build_found = 1;
			 print "found build: $build\n";
			 $builddata[$counter][0]= $build;
             open (BSCREFILE, "<", $builds_cre_file) or die $!;
             $build_dt= "";
			 while (<BSCREFILE>) {
                     chomp;
                     $bldlinecre  = $_;
		             if ($bldlinecre =~ /$build/) {
			            $build_dt = substr($bldlinecre, 0, 19);
				        $builddata[$counter][4]= $build_dt;
			            print "found build date: $build_dt\n";
						$build_dt = "";
                        last; 
					 }
		    }	 
            close BSCREFILE;		} 
		elsif (($bldline =~ /R_FSPR5CAT[a-zA-Z0-9_\.]*iso/) and ($bldline !~ /md5sum/)){
			 if ($build_found == 1) {
				$build_found = 0;
                $pos1 = index($bldline, "R_FSPR5CAT");
			    $len2 = length($bldline);
			    $buildname = substr($bldline, $pos1, $len2-1);
                if ($branch eq "cat_main") {
				       if ($buildname =~ /(?<=r)\d{6}(?=_debug\.iso)/g) {
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
				   $builddata[$counter][1]= $buildname;
				   $builddata[$counter][2]= $buildrev;
				   $builddata[$counter][3]= "-";
                   print("at $builddata[$counter][0], $builddata[$counter][1], $builddata[$counter][2], $builddata[$counter][3], $builddata[$counter][4]\n");
                   $counter++;
		    }
        } 
    }   
    close BSFILE;

	$last_count = $counter;
	my $svn_export_file;
	my $str;

	for ($counter=0; $counter < $last_count; $counter++) {
        $revdata[$counter]=$builddata[$counter][2];
	}	
	prepare_svnexport_script($branch, @revdata); 
    system("./svnExp.sh");


	for ($counter=0; $counter < $last_count; $counter++) {
	   $svn_export_file = "mf".$builddata[$counter][2].".txt";
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
    system("rm mf*.txt");
    system("rm svnExp.sh build_export.sh clean_build_export.sh");
    system("rm build_dir_det.txt");
    system("rm build_cre_dt.txt");
	my $csvfile = "csv_$branch.txt";
    open (CSVFILE, ">", $csvfile) or die $!;

	for ($counter=0; $counter < $last_count; $counter++) {
        print CSVFILE "$builddata[$counter][0], $builddata[$counter][1], $builddata[$counter][2], $builddata[$counter][3], $builddata[$counter][4]\n";
	}	
    close CSVFILE;
    filldb($branch, $csvfile); 
}
system("rm csv_*.txt");
exit 0;


sub prepare_svnexport_script 
{
	my $inbranch;
	my @indata;
	($inbranch, @indata)=@_;
    print "received branch $inbranch\n"; 
    my $line = ""; 
	my $svnfile = "svnExp.sh";
	my $svnfileexp = "build_export.sh";
	my $svnfileexpcl= "clean_build_export.sh";
    my $user = getlogin();
#    open (SVNFILE, ">", $svnfile) or die $!;
    open (SVNFILEEXP, ">", $svnfileexp) or die $!;
    $line = "cd ../$inbranch/src/scripts/nginfo/";
    print SVNFILEEXP "$line\n";
    foreach $b(@indata) {
        $line = "svn export -r$b MANIFEST mf$b.txt";
        print SVNFILEEXP "$line\n";
    }
    close SVNFILEEXP;
    open (SVNFILEEXPCLN, ">", $svnfileexpcl) or die $!;
    $line = "cd ../$inbranch/src/scripts/nginfo/";
    print SVNFILEEXPCLN "$line\n";
    $line = "rm mf*.txt";
    print SVNFILEEXPCLN "$line\n";
    close SVNFILEEXPCLN;


    open (SVNFILE, ">", $svnfile) or die $!;
    $line = "ssh $usr\@hyperion \'bash -s\' < build_export.sh";
    print SVNFILE "$line\n";
    $line = "scp $usr\@hyperion:../$inbranch/src/scripts/nginfo/mf*.txt .";
    print SVNFILE "$line\n";
    $line = "ssh $usr\@hyperion \'bash -s\' < clean_build_export.sh";
    print SVNFILE "$line\n";
    close SVNFILE;
	system("chmod 777 svnExp.sh build_export.sh clean_build_export.sh");
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
    open (CSV, "<", $csvfile) or die $!;
    while (<CSV>) {
        $linecounter++;
        if ($csv->parse($_)) {
            @columns = $csv->fields();

            print "before select build $columns[0]\n";
            my $sth1 = $dbh->prepare('select build, rev, dt from weblvnapp_build_entry where branch_name_id = ? and build = ?'); 
            $sth1->execute($branch, $columns[0]);
			$count = 0;
            while (@data = $sth1->fetchrow_array()) {
				 $count ++; 
                 $build = $data[0];
				 $rev   = $data[1];
            }
			if ($count > 0) {
                print "selected build $columns[0] was found in db $count times (rev found: $rev)\n";
				if ($rev == 0) {
					print "update rev $rev in build $build\n";
				    $stmt = "update 'weblvnapp_build_entry' set rev = trim('$columns[2]') where branch_name_id = '$branch' and build = '$columns[0]'";
                    $dbh->do($stmt);
                    $dbh->commit();
#      	            $sth1 = $dbh->prepare($stmt);
#    				$sth1->execute();
#				$sth1->finish();
				}
#				print "update dt in build $build\n";
#				$stmt = "update 'weblvnapp_build_entry' set dt = trim('$columns[4]') where branch_name_id = '$branch' and build = '$columns[0]'";
#               $dbh->do($stmt);
#               $dbh->commit();
			}	
			else {
                print "insert build $columns[0] in db\n";
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
