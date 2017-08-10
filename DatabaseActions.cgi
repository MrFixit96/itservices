#!perl

# Uncomment these 3 lines for more debugging info:
$|=1;
#print "Content-type: text/html\n\n";
use CGI::Carp('fatalsToBrowser');

#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use CGI;      #CGI module used to make generating dynamic html easier
use DBI;      #DBI used for managing sql based data stores.
use DatabaseActions; #Calls RequestSystemClass.pm module
#########################################################################################
#	Variables									#
#########################################################################################
# Instantiate new objects
my $cgiRequest = new CGI; #Makes cgiRequest an instance of the CGI Object
my $serviceRequest = new DatabaseActions; #Makes serviceRequest an instance of the RequestSystemClass Object

# store database info
my $database="testdb";
my $databaseuser="root";
my $databasepass="j19a96";
my $script;
# Get the list of parameters passed by html form
my $action = $cgiRequest->param("action");
my $field1 = $cgiRequest->param("field1");
my $field2 = $cgiRequest->param("field2");
my @args=($field1, $field2, $database, $databaseuser, $databasepass);

#########################################################################################
#	MAIN										#
#########################################################################################
#Purpose: Starts program
# Print the page

print $cgiRequest->header;
print $cgiRequest->start_html(-title=>"Service Request System", -style=>{'src'=>'../../stylesheet1.css'});
print "<div id=logo> IT Services\'s Request System</div>";
print "<br />";

if($action eq "post")	   {post_entry(); }
elsif($action eq "Submit") {submit(); }
elsif($action eq "Update")  {$serviceRequest->UpdateRequest(@args); }
elsif($action eq "View"){$serviceRequest->DisplayRequest(@args);}
else			   { $serviceRequest->DisplayRequest(@args); }

# Disconnect from the database
#$dbh->disconnect();

# Print the page end
print $cgiRequest->end_html;
exit;

#########################################################################################
#	post_entry									#
#########################################################################################
#Purpose: Takes info, from html form and stores it to variables
sub post_entry
{
    # Show the form
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=View\">View Service Requests</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=View\">View Service Requests</a>"," <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>";
    print $cgiRequest->hr;
    print $cgiRequest->start_form;
    print $cgiRequest->strong("Enter Your Information:");
    print $cgiRequest->p();

    print $cgiRequest->start_table();
    print $cgiRequest->Tr([
	$cgiRequest->td(["Field1: ", $cgiRequest->textfield(
	    -name      => 'field1',
	    -size      => '50',
	    -maxlength => '255')]),
	$cgiRequest->td(["field2: ", $cgiRequest->textfield(
	    -name      => 'field2',
	    -size      => '50',
	    -maxlength => '255')]),
            ]);

    print $cgiRequest->end_table();
    print $cgiRequest->p;


########Post Data to variables
    print $cgiRequest->submit(
	-name  => "action",
	-value => "Submit");
    print " ", $cgiRequest->reset, " ";

    print $cgiRequest->endform;
}
#########################################################################################
#	submit                                                                           								#
#########################################################################################
#Purpose: submits info to database
sub submit
{
     $script = "SELECT Field1, Field2 FROM test";
  my @args2=($field1, $field2, $database, $databaseuser, $databasepass, $script);
     $serviceRequest->SubmitRequest(@args2);
}
