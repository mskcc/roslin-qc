#!/usr/bin/perl

use strict;
use Getopt::Long qw(GetOptions);
use FindBin qw($Bin); 

###
### LSF AND SGE HANDLE QUOTES DEREFERENCING DIFFERENTLY
### SO STICKING IT IN A WRAPPER FOR SIMPLICITY
###

my ($pre, $path, $config, $log, $request, $version);
GetOptions ('pre=s' => \$pre,
	    'path=s' => \$path,
            'log=s' => \$log,
            'request=s' => \$request,
            'version=s' => \$version
	   ) or exit(1);

if(!$pre || !$path  || !$request || !$log || !$version){
    die "MUST PROVIDE PRE, PATH, CONFIG, REQUEST FILE, SVN REVISION NUMBER AND OUTPUT\n";
}

my $R = '/usr/bin/';
my $JAVA = '/usr/bin/';
## generate a PDF file for each plot, a project summary text file and a sample summary text file
print "$R/R CMD BATCH \"--args path='$path' pre='$pre' bin='$Bin' logfile='$log'\" $Bin/qc_summary.R\n";
`$R/R CMD BATCH \"--args path='$path' pre='$pre' bin='$Bin' logfile='$log'\" $Bin/qc_summary.R`;

my $ec = $? >> 8;

## generate the complete, formal PDF report
print "$JAVA/java -jar $Bin/QCPDF.jar -rf $request -v $version -d $path -o $path -pl Variants\n"; 
`$JAVA/java -jar $Bin/QCPDF.jar -rf $request -v $version -d $path -o $path -pl Variants`;

my $ec2 = $? >> 8;

if($ec != 0 || $ec2 != 0){ die; }


