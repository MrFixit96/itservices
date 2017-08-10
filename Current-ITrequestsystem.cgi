#!/usr/bin/perl

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
my $dbh  = DBI->connect("DBI:mysql:service_requests", "root", "heatherfdlm",{ RaiseError => 1 });

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
my $user= $request->param("pass");
my $pass= $request->param("pass");
my $loginID= $request->param("loginID");
my $loggedIN = "0";
my $cookie1;
my $cookie2;
#########################################################################################
#	MAIN										#
#########################################################################################
#Purpose: Starts program
# Print the page
if ($loggedIN = "1"){
     #print $request->header(-cookie=>[$cookie1,$cookie2]);
     set_cookie();
}else{
      print $request->header;
}
print $request->start_html(-title=>"$owner\'s Request System", -style=>{'src'=>'../../services/stylesheet1.css'});
#print '<link rel="stylesheet" href="stylesheet1.css">';
print "<div id=logo> IT Services\'s Request System</div>";
print "<br />";

if($action eq "post")	   {post_entry(); }
elsif($action eq "Submit") {submit_entry(); }
elsif($action eq "Admin") {admin_panel(); }
elsif($action eq "Edit")    {login(); }
elsif($action eq "Login")   {authenticate();}
elsif($action eq "Request") {post_task();}
elsif($action eq "Recall")  {recall_entry(); }
elsif($action eq "Change")  {change_entry();}
elsif($action eq "Update")  {update_entry(); }
elsif($action eq "Kbase")   {kbase_display();}
elsif($action eq "View Open"){display_requests();}
elsif($action eq "View Closed"){kbase_display();}
elsif($action eq "View Tasks") {task_display();}
elsif($action eq "Report")  {report_panel();}
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
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=View\">View Service Requests</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=View\">View Service Requests</a>"," <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>";
    print $request->hr;
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
	$request->td(["Time Submitted(In yyyy-mm-dd format): " , $request->textarea(
            -name      => 'timeStart',
            -default   => 'yyyy-mm-dd',
            -rows      => '1',
            -columns   => '20')]),            
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


########Post Data to variables
    print $request->submit(
	-name  => "action",
	-value => "Submit");
    print " ", $request->reset, " ";

    print $request->endform;
}
#########################################################################################
#	error_checker                                                                    									#
#########################################################################################
#Purpose: checks variables for proper data or data existence
sub error_checker
{

if ($name eq ""){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong> You must enter your name to post a service request.</strong>\n";
    exit;}
elsif ($email eq ""){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter an email address to post a service request.</strong>\n";
    exit;}
elsif ($timeStart eq "yyyy-mm-dd"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=35>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "You must enter an Time Submitted to post a service request.\n";
   exit;}
elsif ($assetNumber eq "99999"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter an Asset Number to post a service request.</strong>\n";
    exit;}
elsif ($priorityLevel eq "---SELECT ONE---"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter a Priority Level to post a service request.</strong>\n";
    exit;}
elsif ($errorType eq "---SELECT ONE---"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter an Error Type to post a service request.</strong>\n";
    exit;}
##########Checking for invalid/dangerous characters
elsif ($name=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the name field. Please click Post another request and start over.</strong>\n";
   exit;}
elsif($assetNumber=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the Asset Number field. Please click Post another request and start over.</strong>\n";
   exit;}
elsif ($errorType=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the errorType field. Please click Post another request and start over.</strong>\n";
   exit;}
elsif ($email=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the email field. Please click Post another request and start over.</strong>\n";
   exit;}
elsif ($priorityLevel=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the Priority Level field. Please click Post another request and start over.</strong>\n";
   exit;}
elsif ($description=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the description field. Please click Post another request and start over.</strong>\n";
   exit;}
elsif ($resolution=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the resolution field. Please click Post another request and start over.</strong>\n";
   exit;}
}
#########################################################################################
#	submit_entry									#
#########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements
sub submit_entry
{
    
########Parse form for errors or missing data
    error_checker();
########Submit data to the database via sql
    my $status="Open";
    # Add this entry to the database using placeholders(?'s)
    my $script = "INSERT INTO error_tracking ( Name, Email, AssetTag, Priority, Status, ErrorType, Description, OS) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)";
    my $sth = $dbh->prepare($script);

    #Execute script filling in placeholders with variables passed to the execute function
    $sth->execute(( $name, $email, $assetNumber, $priorityLevel, $status, $errorType, $description, $OS));
    $sth->finish();

    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    # Display confirmation that the entry was accepted.
    print $request->p();
    print "Thank you for your $owner\'s Request\.";
    #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=post\">Post Another Request</a>";
}
#########################################################################################
#	update_entry									#
#########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements
sub update_entry
{
    
########Parse form for errors or missing data
    error_checker();
########Submit data to the database via sql
     my $script = "UPDATE error_tracking SET Name='$name', Email='$email', AssetTag='$assetNumber', Priority='$priorityLevel',`Status`='$status', ErrorType='$errorType', Description='$description', OS='$OS', Assigned='$assigned', TimeStop='$timeStop', Resolution='$resolution' WHERE RegID='$RegID'";
     my $sth = $dbh->prepare($script);
    #Execute script
    $sth->execute();
    $sth->finish();

    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=Recall\">Edit Another Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    # Display confirmation that the entry was accepted.
    print $request->p();
    print "Thank you for your $owner\'s Request\.";
    #print "<a href=../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $request->url(), "?action=View\">Public View</a> "," <a href=\"", $request->url(), "?action=Kbase\">Closed Records</a>"," <a href=\"", $request->url(), "?action=Recall\">Edit another request</a>" ;
}
#########################################################################################
#	display_requests      ********PUBLIC VIEW                                       #
#########################################################################################
#Purpose:Displays only open records for public viewing
sub display_requests
{
#prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved request.
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
                 "  WHERE `Status`!='Resolved (Completed)' AND `Status`!='Closed (Denied)' AND ErrorType!='Internal Task'";
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
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=post\">Post a Request</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>" ;
    print $request->hr;
    print $request->p();
    print "<div id=content>";
    print $request->start_table();
    #cycles through each record printing the corresponding fields to an html table
    while($sth->fetch())
    {
         #print "<strong>Request #:</strong>       ",$RegID, "<br />";
         #print "<strong>Name #:</strong>          ",$name, "<br />";
         #print "<strong>E-Mail:</strong>          ",$email, "<br />";
         #print "<strong>Asset  #:</strong>        ",$assetNumber, "<br />";
         #print "<strong>Status :</strong>         ",$status, "<br />";
         #print "<strong>Priority Level:</strong>  ",$priorityLevel, "<br />";
         #print "<strong>Error Type:</strong>      ",$errorType, "<br />";
         #print "<strong>Description:</strong>     ",$description, "<br />";
         #print "<strong>Windows Version:</strong> ",$OS, "<br />";
         #print "<strong>Assigned To:</strong>     ",$assigned, "<br />";
         #print "<strong>Time Submitted:</strong>  ",$timeStart, "<br />";
         #print "<strong>Resolution:</strong>      ",$resolution, "<br />";
         #print "<strong>Time Completed:</strong>  ",$timeStop, "<br />";
         #print "<br />";
	print $request->Tr([
          $request->td([$request->strong("Request :"), $RegID]),
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
    print "</div>";
    # Stop processing our statement
    $sth->finish();
}
####################################################################################################
#        kbase_display   ***********Knowledge Base VIEW                                             #
####################################################################################################
#purpose: to display only closed or resolved records
sub kbase_display
{
#prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved request.
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
                 "  WHERE `Status`!='In Progress (See Resolution Comments)' AND `Status`!='Open' AND ErrorType!='Internal Task'";
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
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=post\">Post a Request</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>" ;
    print $request->hr;
    print $request->p();
    print $request->start_table();

    #cycles through each record printing the corresponding fields to an html table
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
########################################################################################################################################
#                                  ************ ADMIN VIEW SECTIONS ******************************************                         #
########################################################################################################################################
####################################################################################################
#        login                                                                                     #
####################################################################################################
#purpose: To Login to Admin view
sub login
{
###############Recall cookies if any
    my $recall1=$request->cookie('user_name');
    my $recall2=$request->cookie('password');

#######********Test cookie
if ($recall1 ne ""){
    #print $recall1;
    #print $recall2;
$loginID=$recall1;
$pass=$recall2;
authenticate();
}else{
     # Show the form
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=View\">Public View</a>"," <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>";
    print $request->hr;
    print $request->start_form;
    print $request->strong("Enter Your Information:");
    print $request->p();

    print $request->start_table();
    print $request->Tr([
	$request->td(["User Name: ", $request->textfield(
	    -name      => 'loginID',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["Password: ", $request->password_field(
	    -name      => 'pass',
	    -size      => '50',
	    -maxlength => '255')])]);

    print $request->end_table();
    print $request->p;
#########################################**********************SET COOKIE HERE
$loggedIN = "1"; #***** This changes the header on this page which is set up in the MAIN section to post a cookie header

########Post Data to variables
    print $request->submit(
	-name  => "action",
	-value => "Login");
    print " ", $request->reset, " ";

    print $request->endform;


}
}
####################################################################################################
####************************Setting Cookie
####################################################################################################
sub set_cookie
{
        $cookie1 = $request->cookie(-name=>'user_name',
                                  -expires=>'+1h',
                                  -value=>"$loginID");
        $cookie2 = $request->cookie(-name=>'password',
                                  -value=>"$pass");
        print $request->header(-cookie=>[$cookie1,$cookie2]);
        #print "$ENV{HTTP_COOKIE}\n";
        $loggedIN = "0";
}
####################################################################################################
#        authenticate                                                                              #
####################################################################################################
#purpose: to evaluate user/pass combinations
sub authenticate
{

my $stored_pass;

######################## grab records from database for display
#prepare sql statement to grab contents of error_tracking table
my $script = "SELECT Name, Password FROM security WHERE Name='$loginID'";
######################### Fetch the contents of the requests
my $sth = $dbh->prepare($script);
$sth->execute();
$sth->bind_columns(\$user,
                   \$stored_pass);

while($sth->fetch())
    {

     
if ($user eq $loginID and $pass eq $stored_pass){
        $request->startform;
   admin_panel(); ####Bring up AdminView after Auth.
}else{
      print "Access Denied";
exit;
}

    }
# Stop processing our statement
    $sth->finish();
}
####################################################################################################
#        admin_panel                                                                               #
####################################################################################################
#purpose: A control panel for administrative tasks
sub admin_panel
{
    print $request->start_form;
    print $request->strong("Administrative Task Panel");
    print $request->p();
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=../../services/index.php?Department=25?Department=25\">Back To IT Request System Home</a> ", " <a href=../../services/index.php>Back To Services Home</a> ";
    print $request->hr;
    print $request->p();
############################*****************INSERT COOKIE CALL HERE
########Post Data to variables
   print $request->start_table();
    print $request->Tr([
    $request->td([$request->submit(
	-name  => "action",
	-value => "Recall"), "Edit a previous request"]),  #Edit previous request
    $request->td([$request->submit(
	-name  => "action",
	-value => "Request"), "Post an Intra-Dept Task"]),#Post an Intra-Dept Request
    $request->td([$request->submit(
	-name  => "action",
	-value => "View Open"), "View Open Public Requests"]), #View Open Public Request
    $request->td([$request->submit(
	-name  => "action",
	-value => "View Closed"), "View Closed Public Requests"]), #View Closed Public Requests
    $request->td([$request->submit(
	-name  => "action",
	-value => "View Tasks"), "View Intra-Dept Tasks"]), #View Intra-Dept Requests
    $request->td([$request->submit(
	-name  => "action",
	-value => "Report"), "Run Built-In Reports"])]);  #Built-In Report Generator
#    print $request->submit(  #***** Use this when cookies work right
#	-name  => "action",
#	-value => "Log Out");
    print $request->endform;
}
#########################################################################################
#	post_task       ***** Intra-Dept Task						#
#########################################################################################
#Purpose: Takes info, from html form and stores it to variables For IntraDept. task assignment
sub post_task
{
  # Show the form
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a>"," <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>";
    print $request->hr;
    print $request->start_form;
    print $request->strong("Enter Your Information:");
    print $request->p();

    print $request->start_table();
    print $request->Tr([
	$request->td(["Name: ", $request->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255',
	    -value     =>'IT Services')]),
	$request->td(["E-mail: ", $request->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255')]),
	$request->td(["Asset Number: ", $request->textfield(
	    -name      => 'assetNumber',
	    -size      => '50',
	    -maxlength => '255',
            -value     => 'N/A')]),
 	$request->td(["Error Type: " ,
        $request->popup_menu(
            -name      => 'errorType',
            -default   => 'Internal Task',
            -values    => ["---SELECT ONE---", "Internal Task", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$request->td(["Description: " , $request->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50')]),
	$request->td(["Priority Level: " ,
        $request->popup_menu(
            -name      => 'priorityLevel',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"])]),
 	$request->td(["Assigned To: " ,
        $request->popup_menu(
            -name      => 'assigned',
            -default   => $assigned,
            -values    => ["---SELECT ONE---", "James Anderton", "John MacLean"])]),
        $request->td(["Time Submitted: " , $request->textfield(
            -name      => 'timeStart',
            -rows      => '50',
            -columns   => '50',
            -value     => 'Now( )')]),
       	$request->td(["Time Finished: " , $request->textfield(
            -name      => 'timeStop',
            -rows      => '50',
            -columns   => '50')])]);

    print $request->end_table();
    print $request->p;

$assetNumber="N/A";
$OS="N/A";



########Post Data to variables
    print $request->submit(
	-name  => "action",
	-value => "Submit");
    print " ", $request->reset, " ";

    print $request->endform;

}
####################################################################################################
#        Task_display   ***********Knowledge Base VIEW                                             #
####################################################################################################
#purpose: to display only closed or resolved records
sub task_display
{
#prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved request.
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
                 "  WHERE ErrorType ='Internal Task'";
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
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>" ;
    print $request->hr;
    print $request->p();
    print $request->start_table();

    #cycles through each record printing the corresponding fields to an html table
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
#        report_panel                                                                               #
####################################################################################################
#purpose: A control panel for built-in reports
sub report_panel
{
#######**************ADD BUILTIN REPORTS HERE
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=Admin\">Back to Admin Panel</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a> ";
    print $request->hr;
    print $request->p();
    print "Page Under Construction";
}
####################################################################################################
#        recall_entry                                                                              #
####################################################################################################
#purpose: to choose which record to recall
sub recall_entry
{
######################## grab records from database for display
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
		 "  FROM error_tracking " .
                 "  WHERE `Status`!='Resolved (Completed)' AND `Status`!='Closed (Denied)'";
######################### Fetch the contents of the requests
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
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=Admin\">Back to Admin Panel</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a> ";
    print $request->hr;
    print $request->p();
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
	-value => "Change");
    print " ", $request->reset, " ";

    print $request->endform;
    
##########################Display requests to choose from

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
#        change_entry                                                                              #
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
        print '<div id="menu">';
    print '<A class=menuitem href=\"", $request->url(), "?action=Admin\">Back To Admin Panel</a>';
    print "<A class=menuitem href=\"", $request->url(), "?action=Recall\">Recall a different record</a></div>";
    print "</div>";
    #print "<a href=\"", $request->url(), "?action=Recall\">Recall a different record</a> ", " <a href=\"", $request->url(), "?action=Admin\">Back to Admin Panel</a>" ;
    print $request->hr;
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
            -values    => ["---SELECT ONE---", "Open", "Closed (Denied)", "In Progress (See Resolution Comments)", "Resolved (Completed)"])]),
	$request->td(["Error Type: " ,
        $request->popup_menu(
            -name      => 'errorType',
            -default   => $errorType,
            -values    => ["---SELECT ONE---", "Internal Task", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
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

