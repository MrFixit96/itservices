#!perl

#print "Content-type: text/html\n\n";
#use CGI::Carp('fatalsToBrowser');

#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use CGI;      #CGI module used to make generating dynamic html easier

my $cookie;
my $request =new CGI;


print "Content-Type: text/html\n\n";
print "<html><head><title>Cookie Counter</title></head>\n";
print "<body bgcolor=white>\n";

  
    my $ID = $request->cookie('sessionID');
    print "$ENV{'HTTP_COOKIE'}\n";
    print "$ENV\n";
#    print "$ID\n";
print "</body>\n";
print $request->end_html;
