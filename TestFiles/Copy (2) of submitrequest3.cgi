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

#########################################################################################
#	Variables									#
#########################################################################################
# Instantiate a CGI object
my $request = new CGI;

# Create a new database connection
my $dbh  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

# Get the list of parameters passed by html form
my $action = $request->param("action");
my $name = $request->param("name");
my $assetNumber = $request->param("assetNumber");
my $errorType = $request->param("errorType");
my $email = $request->param("email");
my $description = $request->param("description");
my $priorityLevel = $request->param("priorityLevel");
my $OS = $request->param("OS");
my $record = $request->param("record");
my $status= $request->param("status");
my $RegID= $request->param("RegID");
my $assigned= $request->param("assigned");
my $timeStart= $request->param("timeStart");
my $timeStop= $request->param("timeStop");
my $resolution= $request->param("resolution");
my $owner = "IT Services";

#########################################################################################
#	MAIN										#
#########################################################################################
#Purpose: Starts program
# Print the page
print $request->header;
print $request->start_html("$owner\'s Request System");
print $request->h3("$owner\'s Request System");

if($action eq "post")	   { post_entry(); }
elsif($action eq "Submit") { submit_entry(); }
elsif($action eq "Edit")    { recall_entry(); }
elsif($action eq "Recall")    { change_entry(); }
elsif($action eq "Update")    {update_entry(); }
else			   { display_requests(); }

# Disconnect from the database
$dbh->disconnect();

# Print the page end
print $request->end_html;
exit;

#########################################################################################
#	post_entry									#
#########################################################################################
#Purpose: Takes info, from html form and stores it to variables
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

#########################################################################################
#	submit_entry									#
#########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements
sub submit_entry
{
    # Add this entry to the database using placeholders(?'s)
    my $script = "INSERT INTO error_tracking ( Name, Email, AssetTag, Priority, Status, ErrorType, Description, OS) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)";
    my $sth = $dbh->prepare($script);

    #Execute script filling in placeholders with variables passed to the execute function
    $sth->execute(( $name, $email, $assetNumber, $priorityLevel, $status, $errorType, $description, $OS));
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print "Thank you for your $owner\'s Request\.";
    print $request->p();
    print "<a href= ../../index.html>Back To Services Home</a>";
}
#########################################################################################
#	update_entry									#
#########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements
sub update_entry
{

     my $script = "UPDATE error_tracking SET Name='$name', Email='$email', AssetTag='$assetNumber', Priority='$priorityLevel',`Status`='$status', ErrorType='$errorType', Description='$description', OS='$OS', Assigned='$assigned', TimeStop='$timeStop', Resolution='$resolution' WHERE RegID='$RegID'";
     my $sth = $dbh->prepare($script);
        print "$RegID IS IT HERE\n<br />";
       print "$script\n<br />";
    #Execute script
    $sth->execute();
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print "Thank you for your $owner\'s Request\.";
    print $request->p();
    print "<a href= ../../index.html>Back To Services Home</a> "," <a href=\"", $request->url(), "?action=Edit\">Admin View</a>" ;


}
#########################################################################################
#	display_requests								#
#########################################################################################
#Purpose: Takes info, formats and prints it to a textfile.
sub display_requests
{
#prepare sql statement to grab contents of error_tracking table
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
# Fetch the contents of the requests
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

    # Display the requests
    print "<a href=\"", $request->url(), "?action=post\">Post a Request</a> "," <a href=\"", $request->url(), "?action=Edit\">Admin View</a>" ;
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
####################################################################################################
#        recall_entry                                                                                #
####################################################################################################
#purpose: to choose which record to recall
sub recall_entry
{
############### Display Records
      #prepare sql statement to grab contents of error_tracking table
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
# Fetch the contents of the requests
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

    # Display the requests
    print "<a href=\"", $request->url(), "?action=post\">Post a Request</a> "," <a href=\"", $request->url(), "?action=Edit\">Admin View</a>" ;
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
     
########################REQUEST A RECORD
    print $request->start_form;
    print $request->p();
    print $request->start_table();
    print $request->Tr([
	$request->td(["Which record Do you want to recall? ", $request->textfield(
	    -name      => 'record',
	    -size      => '50',
	    -maxlength => '255')])]);
    print $request->end_table();
    print $request->p;
    print $request->submit(
	-name  => "action",
	-value => "Recall");
    print " ", $request->reset, " ";

    print $request->endform;
      
}


####################################################################################################
#        change_entry                                                                                #
####################################################################################################
#purpose: to allow administrative editing of records
sub change_entry
 {

#########################PULL UP RECORD VALUES TO VARIABLES
 	#prepare sql statement to grab contents of error_tracking table
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
                 "  Resolution          " .
		 "  FROM error_tracking " .
                 "  WHERE RegID = $record";
# Fetch the contents of the requests
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

    # Display the requests
    print "<a href=\"", $request->url(), "?action=Edit\">Recall a different record</a>" ;
    print $request->p();
    print $request->start_table();

    while($sth->fetch())
    {




 #######################################################
    #Prints a form with all the original values of requested record from variables.
    print $request->start_form;
    print $request->strong("Edit Request Information:");
    print $request->p();
    print $request->start_table();
    print $request->Tr([
    	$request->td(["RegID: ", $request->textfield(
	    -name      => 'RegID',
	    -size      => '50',
	    -maxlength => '255',
            -value     => $RegID)]),
	$request->td(["Name: ", $request->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255',
            -value     => $name)]),
	$request->td(["E-mail: ", $request->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255',
            -value     => $email)]),
	$request->td(["Asset # " , $request->textfield(
            -name      => 'assetNumber',
            -default   => '99999',
            -rows      => '50',
            -columns   => '50',
            -value     => $assetNumber)]),
        $request->td(["Priority Level: " ,
        $request->popup_menu(
            -name      => 'priorityLevel',
            -default   => $priorityLevel,
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"])]),
        $request->td(["Status: " ,
        $request->popup_menu(
            -name      => 'status',
            -default   => $status,
            -values    => ["---SELECT ONE---", "OPEN", "Closed (Denied)", "In Progress (See Resolution Comments)", "Resolved (Completed)"])]),
	$request->td(["Error Type: " ,
        $request->popup_menu(
            -name      => 'errorType',
            -default   => $errorType,
            -values    => ["---SELECT ONE---", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$request->td(["Description: " , $request->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50',
            -value     => $description)]),
 	$request->td(["Windows Version: " ,
        $request->popup_menu(
            -name      => 'OS',
            -default   => $OS,
            -values    => ["---SELECT ONE---", "Windows XP", "Windows 2000", "Windows 98"])]),
 	$request->td(["Assigned To: " ,
        $request->popup_menu(
            -name      => 'assigned',
            -default   => $assigned,
            -values    => ["---SELECT ONE---", "James Anderton", "John MacLean"])]),
        $request->td(["Time Submitted: " , $request->textfield(
            -name      => 'timeStart',
            -rows      => '50',
            -columns   => '50',
            -value     => $timeStart)]),
       	$request->td(["Time Finished: " , $request->textfield(
            -name      => 'timeStop',
            -rows      => '50',
            -columns   => '50',
            -value     => $timeStop)]),
	$request->td(["Resolution Comments: " , $request->textarea(
            -name      => 'resolution',
            -rows      => '5',
            -columns   => '50',
            -value     => $resolution)]),
            ]);

    print $request->end_table();
    print $request->p;
    print $request->submit(
	-name  => "action",
	-value => "Update");
    print " ", $request->reset, " ";

    print $request->endform;
    
    ############
    }
    # Stop processing our statement
    $sth->finish();
    $record=$RegID;
 }

