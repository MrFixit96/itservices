#!perl

#print "Content-type: text/html\n\n";
#use CGI::Carp('fatalsToBrowser');

#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use CGI;      #CGI module used to make generating dynamic html easier

my $cookie;
my $request =new CGI;

print "Set-Cookie: session_id=12345\n; expires=Monday, 27-Aug-2004 00:00:00 GMT\n";
print "Set-Cookie: name=jcaa\n; expires=Monday, 27-08-2004 00:00:00 GMT\n";
print "Content-Type: text/html\n\n";
print "<html><head><title>Cookie Counter</title></head>\n";
print "<body bgcolor=white>\n";



    print "<br />";
    my $ID = $request->cookie('sessionID');
    print "$ENV{'HTTP_COOKIE'}\n";
    print @ENV;
#    print "$ID\n";
print "</body></html>\n";
#print $request->end_html;
