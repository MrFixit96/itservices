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
use RequestSystemClass; #Calls RequestSystemClass.pm module
#########################################################################################
#	Variables									#
#########################################################################################
# Instantiate new objects
my $cgiRequest = new CGI; #Makes cgiRequest an instance of the CGI Object
my $serviceRequest = new RequestSystemClass; #Makes serviceRequest an instance of the RequestSystemClass Object

# Create a new database connection
my $dbh  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

# Get the list of parameters passed by html form
my $action = $cgiRequest->param("action");
my $name = $cgiRequest->param("name");
my $assetNumber = $cgiRequest->param("assetNumber");
my $errorType = $cgiRequest->param("errorType");
my $email = $cgiRequest->param("email");
my $description = $cgiRequest->param("description");
my $priorityLevel = $cgiRequest->param("priorityLevel");
my $OS = $cgiRequest->param("OS");
my $record = $cgiRequest->param("record");
my $status= $cgiRequest->param("status");
my $RegID= $cgiRequest->param("RegID");
my $assigned= $cgiRequest->param("assigned");
my $timeStart= $cgiRequest->param("timeStart");
my $timeStop= $cgiRequest->param("timeStop");
my $resolution= $cgiRequest->param("resolution");
my $owner = "IT Services";
my $user= $cgiRequest->param("pass");
my $pass= $cgiRequest->param("pass");
my $loginID= $cgiRequest->param("loginID");
my $loggedIN = "0";
my $cookie1;
my $cookie2;
my @args=($RegID,$name,$email,$assetNumber,$priorityLevel,$status,$errorType,$description,$OS,$assigned,$timeStart,$timeStop,$resolution,$dbh,$owner);

#########################################################################################
#	MAIN										#
#########################################################################################
#Purpose: Starts program
# Print the page
if ($loggedIN = "1"){
     #print $cgiRequest->header(-cookie=>[$cookie1,$cookie2]);
     set_cookie();
}else{
      print $cgiRequest->header;
}
print $cgiRequest->start_html(-title=>"$owner\'s Request System", -style=>{'src'=>'../../stylesheet1.css'});
#print '<link rel="stylesheet" href="stylesheet1.css">';
print "<div id=logo> IT Services\'s Request System</div>";
print "<br />";

if($action eq "post")	   {post_entry(); }
elsif($action eq "Submit") {$serviceRequest->SubmitRequest(@args); }
elsif($action eq "Admin") {admin_panel(); }
elsif($action eq "Edit")    {login(); }
elsif($action eq "Login")   {authenticate();}
elsif($action eq "Request") {post_task();}
elsif($action eq "Recall")  {recall_entry(); }
elsif($action eq "Change")  {change_entry();}
elsif($action eq "Update")  {$serviceRequest->UpdateRequest(@args); }
elsif($action eq "Kbase")   {$serviceRequest->Kbase(@args);}
elsif($action eq "View Open"){$serviceRequest->DisplayRequest(@args);}
elsif($action eq "View Closed"){$serviceRequest->Kbase(@args);}
elsif($action eq "View Tasks") {task_display();}
elsif($action eq "Report")  {report_panel();}
else			   { $serviceRequest->DisplayRequest(@args); }

# Disconnect from the database
$dbh->disconnect();

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
	$cgiRequest->td(["Name: ", $cgiRequest->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255')]),
	$cgiRequest->td(["E-mail: ", $cgiRequest->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255')]),
	$cgiRequest->td(["Asset # " , $cgiRequest->textfield(
            -name      => 'assetNumber',
            -default   => '99999',
            -rows      => '50',
            -columns   => '50')]),
	$cgiRequest->td(["Time Submitted(In yyyy-mm-dd format): " , $cgiRequest->textarea(
            -name      => 'timeStart',
            -default   => 'yyyy-mm-dd',
            -rows      => '1',
            -columns   => '20')]),
 	$cgiRequest->td(["Windows Version: " ,
        $cgiRequest->popup_menu(
            -name      => 'OS',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "Windows XP", "Windows 2000", "Windows 98"])]),
	$cgiRequest->td(["Error Type: " ,
        $cgiRequest->popup_menu(
            -name      => 'errorType',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$cgiRequest->td(["Description: " , $cgiRequest->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50')]),
	$cgiRequest->td(["Priority Level: " ,
        $cgiRequest->popup_menu(
            -name      => 'priorityLevel',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"]),
            ])]);

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
#	error_checker                                                                    									#
#########################################################################################
#Purpose: checks variables for proper data or data existence
sub error_checker
{

#########Checking for missing data
if ($name eq ""){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong> You must enter your name to post a service cgiRequest.</strong>\n";
    exit;}
elsif ($email eq ""){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter an email address to post a service cgiRequest.</strong>\n";
    exit;}
elsif ($timeStart eq "yyyy-mm-dd"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=35>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "You must enter an Time Submitted to post a service cgiRequest.\n";
   exit;}
elsif ($assetNumber eq "99999"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter an Asset Number to post a service cgiRequest.</strong>\n";
    exit;}
elsif ($priorityLevel eq "---SELECT ONE---"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter a Priority Level to post a service cgiRequest.</strong>\n";
    exit;}
elsif ($errorType eq "---SELECT ONE---"){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>You must enter an Error Type to post a service cgiRequest.</strong>\n";
    exit;}
    

##########Checking for invalid/dangerous characters
elsif ($name=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the name field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
elsif($assetNumber=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the Asset Number field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
elsif ($errorType=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the errorType field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
elsif ($email=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the email field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
elsif ($priorityLevel=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the Priority Level field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
elsif ($description=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the description field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
elsif ($resolution=~ /;|&|>|<|\?|\!|\'|\`/){
   print '<div id="menu">';
   print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   print "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   print "<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in the resolution field. Please click Post another cgiRequest and start over.</strong>\n";
   exit;}
}
#########################################################################################
#	submit_entry									#
#########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements

#**********POINTS TO RequestSystemClass.pm NOW

#########################################################################################
#	update_entry									#
#########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements

#**********POINTS TO RequestSystemClass.pm NOW

#########################################################################################
#	display_requests      ********PUBLIC VIEW                                       #
#########################################################################################
#Purpose:Displays only open records for public viewing

#**********POINTS TO RequestSystemClass.pm NOW

####################################################################################################
#        kbase_display   ***********Knowledge Base VIEW                                             #
####################################################################################################
#purpose: to display only closed or resolved records

#**********POINTS TO RequestSystemClass.pm NOW

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
    my $recall1=$cgiRequest->cookie('user_name');
    my $recall2=$cgiRequest->cookie('password');

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
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=View\">Public View</a>"," <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>";
    print $cgiRequest->hr;
    print $cgiRequest->start_form;
    print $cgiRequest->strong("Enter Your Information:");
    print $cgiRequest->p();

    print $cgiRequest->start_table();
    print $cgiRequest->Tr([
	$cgiRequest->td(["User Name: ", $cgiRequest->textfield(
	    -name      => 'loginID',
	    -size      => '50',
	    -maxlength => '255')]),
	$cgiRequest->td(["Password: ", $cgiRequest->password_field(
	    -name      => 'pass',
	    -size      => '50',
	    -maxlength => '255')])]);

    print $cgiRequest->end_table();
    print $cgiRequest->p;
#########################################**********************SET COOKIE HERE
$loggedIN = "1"; #***** This changes the header on this page which is set up in the MAIN section to post a cookie header

########Post Data to variables
    print $cgiRequest->submit(
	-name  => "action",
	-value => "Login");
    print " ", $cgiRequest->reset, " ";

    print $cgiRequest->endform;


}
}
####################################################################################################
####************************Setting Cookie
####################################################################################################
sub set_cookie
{
        $cookie1 = $cgiRequest->cookie(-name=>'user_name',
                                  -expires=>'+1h',
                                  -value=>"$loginID");
        $cookie2 = $cgiRequest->cookie(-name=>'password',
                                  -value=>"$pass");
        print $cgiRequest->header(-cookie=>[$cookie1,$cookie2]);
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
        $cgiRequest->startform;
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
    print $cgiRequest->start_form;
    print $cgiRequest->strong("Administrative Task Panel");
    print $cgiRequest->p();
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=../../services/index.php?Department=25?Department=25\">Back To IT Request System Home</a> ", " <a href=../../services/index.php>Back To Services Home</a> ";
    print $cgiRequest->hr;
    print $cgiRequest->p();
############################*****************INSERT COOKIE CALL HERE
########Post Data to variables
   print $cgiRequest->start_table();
    print $cgiRequest->Tr([
    $cgiRequest->td([$cgiRequest->submit(
	-name  => "action",
	-value => "Recall"), "Edit a previous cgiRequest"]),  #Edit previous cgiRequest
    $cgiRequest->td([$cgiRequest->submit(
	-name  => "action",
	-value => "Request"), "Post an Intra-Dept Task"]),#Post an Intra-Dept Request
    $cgiRequest->td([$cgiRequest->submit(
	-name  => "action",
	-value => "View Open"), "View Open Public Requests"]), #View Open Public Request
    $cgiRequest->td([$cgiRequest->submit(
	-name  => "action",
	-value => "View Closed"), "View Closed Public Requests"]), #View Closed Public Requests
    $cgiRequest->td([$cgiRequest->submit(
	-name  => "action",
	-value => "View Tasks"), "View Intra-Dept Tasks"]), #View Intra-Dept Requests
    $cgiRequest->td([$cgiRequest->submit(
	-name  => "action",
	-value => "Report"), "Run Built-In Reports"])]);  #Built-In Report Generator
#    print $cgiRequest->submit(  #***** Use this when cookies work right
#	-name  => "action",
#	-value => "Log Out");
    print $cgiRequest->endform;
}
#########################################################################################
#	post_task       ***** Intra-Dept Task						#
#########################################################################################
#Purpose: Takes info, from html form and stores it to variables For IntraDept. task assignment
sub post_task
{
  # Show the form
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a>"," <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>";
    print $cgiRequest->hr;
    print $cgiRequest->start_form;
    print $cgiRequest->strong("Enter Your Information:");
    print $cgiRequest->p();

    print $cgiRequest->start_table();
    print $cgiRequest->Tr([
	$cgiRequest->td(["Name: ", $cgiRequest->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255',
	    -value     =>'IT Services')]),
	$cgiRequest->td(["E-mail: ", $cgiRequest->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255')]),
	$cgiRequest->td(["Asset Number: ", $cgiRequest->textfield(
	    -name      => 'assetNumber',
	    -size      => '50',
	    -maxlength => '255',
            -value     => 'N/A')]),
 	$cgiRequest->td(["Error Type: " ,
        $cgiRequest->popup_menu(
            -name      => 'errorType',
            -default   => 'Internal Task',
            -values    => ["---SELECT ONE---", "Internal Task", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$cgiRequest->td(["Description: " , $cgiRequest->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50')]),
	$cgiRequest->td(["Priority Level: " ,
        $cgiRequest->popup_menu(
            -name      => 'priorityLevel',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"])]),
 	$cgiRequest->td(["Assigned To: " ,
        $cgiRequest->popup_menu(
            -name      => 'assigned',
            -default   => $assigned,
            -values    => ["---SELECT ONE---", "James Anderton", "John MacLean"])]),
        $cgiRequest->td(["Time Submitted: " , $cgiRequest->textfield(
            -name      => 'timeStart',
            -rows      => '50',
            -columns   => '50',
            -value     => 'Now( )')]),
       	$cgiRequest->td(["Time Finished: " , $cgiRequest->textfield(
            -name      => 'timeStop',
            -rows      => '50',
            -columns   => '50')])]);

    print $cgiRequest->end_table();
    print $cgiRequest->p;

$assetNumber="N/A";
$OS="N/A";



########Post Data to variables
    print $cgiRequest->submit(
	-name  => "action",
	-value => "Submit");
    print " ", $cgiRequest->reset, " ";

    print $cgiRequest->endform;

}
####################################################################################################
#        Task_display   ***********Knowledge Base VIEW                                             #
####################################################################################################
#purpose: to display only closed or resolved records
sub task_display
{
#prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved cgiRequest.
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
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>" ;
    print $cgiRequest->hr;
    print $cgiRequest->p();
    print $cgiRequest->start_table();

    #cycles through each record printing the corresponding fields to an html table
    while($sth->fetch())
    {

	print $cgiRequest->Tr([
          $cgiRequest->td([$cgiRequest->strong("Request #:"), $RegID]),
	  $cgiRequest->td([$cgiRequest->strong("Name:"), $name]),
	  $cgiRequest->td([$cgiRequest->strong("E-mail:"),
	      "<a href=\"mailto:$email\">$email</a>"]),
  	  $cgiRequest->td([$cgiRequest->strong("Asset Number:"), $assetNumber]),
	  $cgiRequest->td([$cgiRequest->strong("Status:"),$status]),
	  $cgiRequest->td([$cgiRequest->strong("Priority:"), $priorityLevel]),
	  $cgiRequest->td([$cgiRequest->strong("Error Type:"), $errorType]),
	  $cgiRequest->td([$cgiRequest->strong("Description:"), $description]),
	  $cgiRequest->td([$cgiRequest->strong("Windows Version:"), $OS]),
          $cgiRequest->td([$cgiRequest->strong("Assigned To:"), $assigned]),
	  $cgiRequest->td([$cgiRequest->strong("Time Submitted:"), $timeStart]),
	  $cgiRequest->td([$cgiRequest->strong("Resolution:"), $resolution]),
       	  $cgiRequest->td([$cgiRequest->strong("Time Completed:"), $timeStop]),
	  $cgiRequest->td([$cgiRequest->br(), $cgiRequest->br()]),
	]);
    }

    print $cgiRequest->end_table();

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
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=Admin\">Back to Admin Panel</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a> ";
    print $cgiRequest->hr;
    print $cgiRequest->p();
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
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=Admin\">Back to Admin Panel</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a> ";
    print $cgiRequest->hr;
    print $cgiRequest->p();
########################REQUEST A RECORD
    print $cgiRequest->start_form;
    print $cgiRequest->p();
    print $cgiRequest->start_table();
    print $cgiRequest->Tr([
	$cgiRequest->td(["Which record Do you want to recall? ", $cgiRequest->textfield(
	    -name      => 'record',
	    -size      => '50',
	    -maxlength => '255')])]);
    print $cgiRequest->end_table();
    print $cgiRequest->p;
    print $cgiRequest->submit(
	-name  => "action",
	-value => "Change");
    print " ", $cgiRequest->reset, " ";

    print $cgiRequest->endform;
    
##########################Display requests to choose from

    print $cgiRequest->start_table();

    while($sth->fetch())
    {

	print $cgiRequest->Tr([
          $cgiRequest->td([$cgiRequest->strong("Request #:"), $RegID]),
	  $cgiRequest->td([$cgiRequest->strong("Name:"), $name]),
	  $cgiRequest->td([$cgiRequest->strong("E-mail:"),
	      "<a href=\"mailto:$email\">$email</a>"]),
  	  $cgiRequest->td([$cgiRequest->strong("Asset Number:"), $assetNumber]),
	  $cgiRequest->td([$cgiRequest->strong("Status:"),$status]),
	  $cgiRequest->td([$cgiRequest->strong("Priority:"), $priorityLevel]),
	  $cgiRequest->td([$cgiRequest->strong("Error Type:"), $errorType]),
	  $cgiRequest->td([$cgiRequest->strong("Description:"), $description]),
	  $cgiRequest->td([$cgiRequest->strong("Windows Version:"), $OS]),
          $cgiRequest->td([$cgiRequest->strong("Assigned To:"), $assigned]),
	  $cgiRequest->td([$cgiRequest->strong("Time Submitted:"), $timeStart]),
	  $cgiRequest->td([$cgiRequest->strong("Resolution:"), $resolution]),
       	  $cgiRequest->td([$cgiRequest->strong("Time Completed:"), $timeStop]),
	  $cgiRequest->td([$cgiRequest->br(), $cgiRequest->br()]),
	]);
    }

    print $cgiRequest->end_table();

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
    print '<A class=menuitem href=\"", $cgiRequest->url(), "?action=Admin\">Back To Admin Panel</a>';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=Recall\">Recall a different record</a></div>";
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=Recall\">Recall a different record</a> ", " <a href=\"", $cgiRequest->url(), "?action=Admin\">Back to Admin Panel</a>" ;
    print $cgiRequest->hr;
    print $cgiRequest->p();
    print $cgiRequest->start_table();

    while($sth->fetch())
    {




 #######################################################
    #Prints a form with all the original values of requested record from variables.
    print $cgiRequest->start_form;
    print $cgiRequest->strong("Edit Request Information:");
    print $cgiRequest->p();
    print $cgiRequest->start_table();
    print $cgiRequest->Tr([
    	$cgiRequest->td(["RegID: ", $cgiRequest->textfield(
	    -name      => 'RegID',
	    -size      => '50',
	    -maxlength => '255',
            -value     => $RegID)]),
	$cgiRequest->td(["Name: ", $cgiRequest->textfield(
	    -name      => 'name',
	    -size      => '50',
	    -maxlength => '255',
            -value     => $name)]),
	$cgiRequest->td(["E-mail: ", $cgiRequest->textfield(
	    -name      => 'email',
	    -size      => '50',
	    -maxlength => '255',
            -value     => $email)]),
	$cgiRequest->td(["Asset # " , $cgiRequest->textfield(
            -name      => 'assetNumber',
            -default   => '99999',
            -rows      => '50',
            -columns   => '50',
            -value     => $assetNumber)]),
        $cgiRequest->td(["Priority Level: " ,
        $cgiRequest->popup_menu(
            -name      => 'priorityLevel',
            -default   => $priorityLevel,
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"])]),
        $cgiRequest->td(["Status: " ,
        $cgiRequest->popup_menu(
            -name      => 'status',
            -default   => $status,
            -values    => ["---SELECT ONE---", "Open", "Closed (Denied)", "In Progress (See Resolution Comments)", "Resolved (Completed)"])]),
	$cgiRequest->td(["Error Type: " ,
        $cgiRequest->popup_menu(
            -name      => 'errorType',
            -default   => $errorType,
            -values    => ["---SELECT ONE---", "Internal Task", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$cgiRequest->td(["Description: " , $cgiRequest->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50',
            -value     => $description)]),
 	$cgiRequest->td(["Windows Version: " ,
        $cgiRequest->popup_menu(
            -name      => 'OS',
            -default   => $OS,
            -values    => ["---SELECT ONE---", "Windows XP", "Windows 2000", "Windows 98"])]),
 	$cgiRequest->td(["Assigned To: " ,
        $cgiRequest->popup_menu(
            -name      => 'assigned',
            -default   => $assigned,
            -values    => ["---SELECT ONE---", "James Anderton", "John MacLean"])]),
        $cgiRequest->td(["Time Submitted: " , $cgiRequest->textfield(
            -name      => 'timeStart',
            -rows      => '50',
            -columns   => '50',
            -value     => $timeStart)]),
       	$cgiRequest->td(["Time Finished: " , $cgiRequest->textfield(
            -name      => 'timeStop',
            -rows      => '50',
            -columns   => '50',
            -value     => $timeStop)]),
	$cgiRequest->td(["Resolution Comments: " , $cgiRequest->textarea(
            -name      => 'resolution',
            -rows      => '5',
            -columns   => '50',
            -value     => $resolution)]),
            ]);

    print $cgiRequest->end_table();
    print $cgiRequest->p;
    print $cgiRequest->submit(
	-name  => "action",
	-value => "Update");
    print " ", $cgiRequest->reset, " ";

    print $cgiRequest->endform;
    
    ############
    }
    # Stop processing our statement
    $sth->finish();
    $record=$RegID;
 }

