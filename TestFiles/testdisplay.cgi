#!perl

# Uncomment these for more debugging info:
$|=1;
print "Content-type: text/html\n\n";
use CGI::Carp('fatalsToBrowser');

use strict;
use warnings;
use CGI;
#use DBI;

# Instantiate a CGI object
my $request = new CGI;


# Get the list of parameters passed
my $action = $request->param("action");
my $name = $request->param("name");
my $email = $request->param("email");
my $url = $request->param("url");
my $gender = $request->param("gender");
my $comments = $request->param("comments");

# Other values
my $owner = "Mark";

# Print the page
print $request->header;
print $request->start_html("$owner\'s Guestbook");
print $request->h3("$owner\'s Guestbook");


{
    # Show the form
    print "<a href=\"", $request->url(), "?action=View\">View Guestbook</a>";
    print $request->start_form;
    print $request->strong("Enter Your Information:");
    print $request->p();

    print $request->start_table();
    print $request->Tr([
	$request->td(["Name ", $request->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["Gender ", $request->popup_menu(
	    -name      => 'gender',
	    -default   => '',
	    -values    => ["", "Male", "Female"])]),
	$request->td(["E-mail ", $request->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["URL ", $request->textfield(
	    -name      => 'url',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["Comments ", $request->textarea(
	    -name      => 'comments',
	    -rows      => '5',
	    -columns   => '50')]),
	]);

    print $request->end_table();
    print $request->p;
    print $request->submit(
	-name  => "action",
	-value => "Submit");
    print " ", $request->reset, " ";

    print $request->endform;
}


