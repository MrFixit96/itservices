#!perl
# Uncomment these 3 lines for more debugging info:
$|=1;
#print "Content-type: text/html\n\n";
use CGI::Carp('fatalsToBrowser');

#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use CGI;      #CGI module used to make generating dynamic html easier
use DBI;      #DBI module used to connect to database
use AssemblePage; #Page Assembly Class Module
#########################################################################################
#	Variables									#
#########################################################################################
# Instantiate a CGI object
my $request = new CGI;       #Makes $request an instance of CGI class
my $page = new AssemblePage; #Makes $page an instance of AssemblePage class


#**********Printing HTML Header for template page
print $request->header;

#####***** Calling CreateContent Method of AssemblePage Class
my $html = $page->CreatePage;





# Wait for the user to press a key

&press_enter_to_continue();

# Get out of here!
#exit;

# Wait for the user to press a key

sub press_enter_to_continue

{
 <>;
 return;
}

