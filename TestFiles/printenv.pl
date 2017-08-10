#!perl
$|=1; #stop buffering and caching
print "Content-type: text/html\n\n"; # forcibly print page header
use CGI::Carp('fatalsToBrowser'); # uses carp module, redirect to browser

#Author: James Anderton
#Purpose: Quiz 3 essay1
use strict;
use warnings;
use CGI;


my $var;
my $val;

# Instantiate a CGI object
my $request = new CGI;

print $request->header;
print $request->start_html("Guest Book of Eternal Peril ;-)");

print "Content-type: text/plain\n\n";
foreach $var (sort(keys(%ENV))) {
    $val = $ENV{$var};
    $val =~ s|\n|\\n|g;
    $val =~ s|"|\\"|g;
    print "<font color= '#00FF00'>${var}</font> ${var}=(<font color='#FF0000'>\'${val}'\</font>)\n";
}
print "$ENV{ REQUEST_URI}";
print $request->end_html;
