#!/usr/bin/perl

use strict;
use Getopt::Long qw(GetOptions);
use FindBin qw($Bin); 

###
### LSF AND SGE HANDLE QUOTES DEREFERENCING DIFFERENTLY
### SO STICKING IT IN A WRAPPER FOR SIMPLICITY
###

my ($pre, $path, $config, $log, $request, $version, $cov_warn_threshold, $dup_rate_threshold, $cov_fail_threshold, $minor_contam_fail, $major_contam_fail);
GetOptions ('pre=s' => \$pre,
	    'path=s' => \$path,
            'log=s' => \$log,
            'request=s' => \$request,
            'version=s' => \$version,
            'cov_warn_threshold=s' => \$cov_warn_threshold,
            'dup_rate_threshold=s' => \$dup_rate_threshold,
            'cov_fail_threshold=s' => \$cov_fail_threshold,
            'minor_contam_threshold=s' => \$minor_contam_fail,
            'major_contam_threshold=s' => \$major_contam_fail,
	   ) or exit(1);

if(!$pre || !$path  || !$request || !$log || !$version){
    die "MUST PROVIDE PRE, PATH, CONFIG, REQUEST FILE, SVN REVISION NUMBER AND OUTPUT\n";
}
my $R;
if (-d '/opt/common/CentOS_6-dev/bin/current/') {
    $R = '/opt/common/CentOS_6-dev/bin/current/';
}
else {
    $R = '/usr/bin/';
}
my $JAVA = '/usr/bin/';
## generate a PDF file for each plot, a project summary text file and a sample summary text file
print "$R/R CMD BATCH \"--args path='$path' pre='$pre' bin='$Bin' logfile='$log' cov_warn_threshold='$cov_warn_threshold' cov_fail_threshold='$cov_fail_threshold' dup_rate_threshold='$dup_rate_threshold' minor_contam_threshold='$minor_contam_fail' major_contam_threshold='$major_contam_fail' \" $Bin/qc_summary.R\n";
`$R/R CMD BATCH \"--args path='$path' pre='$pre' bin='$Bin' logfile='$log' cov_warn_threshold='$cov_warn_threshold' cov_fail_threshold='$cov_fail_threshold' dup_rate_threshold='$dup_rate_threshold' minor_contam_threshold='$minor_contam_fail' major_contam_threshold='$major_contam_fail'\" $Bin/qc_summary.R`;

my $ec = $? >> 8;

## generate the complete, formal PDF report
print "$JAVA/java -jar $Bin/QCPDF.jar -rf $request -v $version -d $path -o $path -cf $cov_fail_threshold -cw $cov_warn_threshold -pl Variants\n"; 
`$JAVA/java -jar $Bin/QCPDF.jar -rf $request -v $version -d $path -o $path -cf $cov_fail_threshold -cw $cov_warn_threshold -pl Variants`;

my $ec2 = $? >> 8;

if($ec != 0 || $ec2 != 0){ die; }


