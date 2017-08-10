#!perl

#$|=1;
#print "Content-type: text/html\n\n";
#use CGI::Carp('fatalsToBrowser');

#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use CGI;      #CGI module used to make generating dynamic html easier

my %answers;
my $cookie1;
my $cookie2;
my $query =new CGI;
        $cookie1 = $query->cookie(-name=>'riddle_name',
                                  -expires=>'+1h',
                                  -value=>"The Sphynx's Question");
        $cookie2 = $query->cookie(-name=>'answers',
                                  -value=>\%answers);
        print $query->header(-cookie=>[$cookie1,$cookie2]);
    print "<br />";
    my $ID = $query->cookie('riddle_name');
 #   print "$ENV{'HTTP_COOKIE'}\n";
    print "$ID\n";
