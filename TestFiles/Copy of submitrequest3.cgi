#!perl

# Uncomment these for more debugging info:
$|=1;
#print "Content-type: text/html\n\n";
use CGI::Carp('fatalsToBrowser');

use strict;
use warnings;
use CGI;
use DBI;

# Instantiate a CGI object
my $request = new CGI;

# Create a new database connection
my $dbh  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

# Get the list of parameters passed
my $action = $request->param("action");
my $status="OPEN";
my $RegID;
my $name = $request->param("name");
my $assetNumber = $request->param("assetNumber");
my $errorType = $request->param("errorType");
my $email = $request->param("email");
my $description = $request->param("description");
my $priorityLevel = $request->param("priorityLevel");
my $OS = $request->param("OS");
my $assigned;
my $timeStart;
my $timeStop;
my $resolution;

# Other values
my $owner = "IT Services";

# Print the page
print $request->header;
print $request->start_html("$owner\'s Request System");
print $request->h3("$owner\'s Request System");

if($action eq "post")	   { post_entry(); }
elsif($action eq "Submit") { submit_entry(); }
else			   { display_guestbook(); }

# Disconnect from the database
$dbh->disconnect();

# Print the page end
print $request->end_html;
exit;

##
## Post an entry to the Request System
##
sub post_entry
{
    # Show the form
    print "<a href=\"", $request->url(), "?action=View\">View Service Requests</a>";
    print $request->start_form;
    print $request->strong("Enter Your Information:");
    print $request->p();

    print $request->start_table();
    print $request->Tr([
	$request->td(["Name: ", $request->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["E-mail: ", $request->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["Asset # " , $request->textfield(
            -name      => 'assetNumber',
            -default   => '99999',
            -rows      => '50',
            -columns   => '50')]),
 	$request->td(["Windows Version: " ,
        $request->popup_menu(
            -name      => 'OS',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "Windows XP", "Windows 2000", "Windows 98"])]),
	$request->td(["Error Type: " ,
        $request->popup_menu(
            -name      => 'errorType',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$request->td(["Description: " , $request->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50')]),
	$request->td(["Priority Level: " ,
        $request->popup_menu(
            -name      => 'priorityLevel',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"]),
            ])]);

    print $request->end_table();
    print $request->p;
    print $request->submit(
	-name  => "action",
	-value => "Submit");
    print " ", $request->reset, " ";

    print $request->endform;
}

##
## Sanitize the data and write it to our file.
##
sub submit_entry
{
    # Add this entry to the database using placeholders(?'s)
    my $script = "INSERT INTO error_tracking ( Name, Email, AssetTag, Priority, Status, ErrorType, Description, OS) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)";
    my $sth = $dbh->prepare($script);

    #Execute script filling in placeholders with variables passed to the execute function
    $sth->execute(( $name, $email, $assetNumber, $priorityLevel, $status, $errorType, $description, $OS));
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print "script:$script\n";
    print ($name, $email, $assetNumber, $priorityLevel, $status, $errorType, $description, $OS);
    print "Thank you for your $owner\'s Request\.";
    print $request->p();
    print "<a href=\"", $request->url(), "?action=View\">View Requests</a>";
}

##
## Display the guestbook
##
sub display_guestbook
{
    #my ($guest, $email, $url, $gender, $comments);

    # Fetch the contents of the guestbook
    my $script = "SELECT RegID,         " .
                 "  Name,	        " .
		 "  Email,		" .
		 "  AssetTag,		" .
		 "  Priority,		" .
		 "  Status,		" .
		 "  ErrorType,		" .
		 "  Description,	" .
		 "  OS,             	" .
                 "  Assigned,           " .
                 "  TimeStart,          " .
                 "  TimeStop,           " .
                 "  Resolution            " .
		 "  FROM error_tracking ";

    my $sth = $dbh->prepare($script);
    $sth->execute();
    $sth->bind_columns(\$RegID,
                       \$name,
		       \$email,
		       \$assetNumber,
		       \$priorityLevel,
		       \$status,
                       \$errorType,
                       \$description,
                       \$OS,
                       \$assigned,
                       \$timeStart,
                       \$timeStop,
                       \$resolution);

    # Display the guestbook
    print "<a href=\"", $request->url(), "?action=post\">Post a Request</a>";
    print $request->p();
    print $request->start_table();

    while($sth->fetch())
    {

	print $request->Tr([
          $request->td([$request->strong("Request #:"), $RegID]),
	  $request->td([$request->strong("Name:"), $name]),
	  $request->td([$request->strong("E-mail:"),
	      "<a href=\"mailto:$email\">$email</a>"]),
  	  $request->td([$request->strong("Asset Number:"), $assetNumber]),
	  $request->td([$request->strong("Status:"),$status]),
	  $request->td([$request->strong("Priority:"), $priorityLevel]),
	  $request->td([$request->strong("Error Type:"), $errorType]),
	  $request->td([$request->strong("Description:"), $description]),
	  $request->td([$request->strong("Windows Version:"), $OS]),
          $request->td([$request->strong("Assigned To:"), $assigned]),
	  $request->td([$request->strong("Time Submitted:"), $timeStart]),
	  $request->td([$request->strong("Resolution:"), $resolution]),
       	  $request->td([$request->strong("Time Completed:"), $timeStop]),
	  $request->td([$request->br(), $request->br()]),
	]);
    }

    print $request->end_table();

    # Stop processing our statement
    $sth->finish();
}

