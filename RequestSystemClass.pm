#!/usr/bin/perl
#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use DBI;      #DBI module used to connect to database
use CGI;      #CGI Module used to create html tags
##############################################################################################################
#   Package RequestSystemClass                                                                               #
##############################################################################################################
#Purpose: Read in template page and populate it with content in proper places
package RequestSystemClass;
my @v;
##############################################################################
#     Method "new"                                                           #
##############################################################################
#Purpose: Gives the ability to create new objects from the AssemblePage Class
    sub new {
        my $self = {};
        $self->{SubmitRequest};
        $self->{UpdateRequest};
        $self->{Kbase};
        $self->{DisplayRequest};
        $self->{error_checker};
        bless $self;
        return $self;

    }
##############################################################################
#Method "DisplayRequest" ***NEEDS A HEADER PRINTED BEFORE THIS METHOD IS CALLED#
##############################################################################
#Purpose: Reads in data from a HTML template file
sub DisplayRequest{

my $cgiRequest = new CGI;

# Create a new database connection
$v[13]  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

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
    my $sth = $v[13]->prepare($script);
    $sth->execute();
    $sth->bind_columns(\$v[0],
                       \$v[1],
		       \$v[2],
		       \$v[3],
		       \$v[4],
		       \$v[5],
                       \$v[6],
                       \$v[7],
                       \$v[8],
                       \$v[9],
                       \$v[10],
                       \$v[11],
                       \$v[12]);

    # Display the requests
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>" ;
    print $cgiRequest->hr;
    print $cgiRequest->p();
    print $cgiRequest->start_table();
    
    #cycles through each record printing the corresponding fields to an html table
    while($sth->fetch())
    {

	print $cgiRequest->Tr([
          $cgiRequest->td([$cgiRequest->strong("Request #:"), $v[0]]),
	  $cgiRequest->td([$cgiRequest->strong("Name:"), $v[1]]),
	  $cgiRequest->td([$cgiRequest->strong("E-mail:"),
	      "<a href=\"mailto:$v[2]\">$v[2]</a>"]),
  	  $cgiRequest->td([$cgiRequest->strong("Asset Number:"), $v[3]]),
	  $cgiRequest->td([$cgiRequest->strong("Status:"),$v[4]]),
	  $cgiRequest->td([$cgiRequest->strong("Priority:"), $v[5]]),
	  $cgiRequest->td([$cgiRequest->strong("Error Type:"), $v[6]]),
	  $cgiRequest->td([$cgiRequest->strong("Description:"), $v[7]]),
	  $cgiRequest->td([$cgiRequest->strong("Windows Version:"), $v[8]]),
          $cgiRequest->td([$cgiRequest->strong("Assigned To:"), $v[9]]),
	  $cgiRequest->td([$cgiRequest->strong("Time Submitted:"), $v[11]]),
	  $cgiRequest->td([$cgiRequest->strong("Resolution:"), $v[10]]),
       	  $cgiRequest->td([$cgiRequest->strong("Time Completed:"), $v[12]]),
	  $cgiRequest->td([$cgiRequest->br(), $cgiRequest->br()]),
	]);
    }

    print $cgiRequest->end_table();

    # Stop processing our statement
    $sth->finish();
        }
########################################################################################
#     Submit Request                                                                   #
########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements
sub SubmitRequest{
my $self= shift;
my $cgiRequest = new CGI;

######Pulling in parameters passed in function call from @_ to actual variables so we can modify them
my $counter=0;
foreach $a (@_){

 $v[$counter] = $_[$counter];
 print $v[$counter];
$counter++;
}

########Parse form for errors or missing data
    #$self->error_checker;

# Create a new database connection
$v[13]  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

########Submit data to the database via sql
    $v[4]="Open";
    # Add this entry to the database using placeholders(?'s)
    my $script = "INSERT INTO error_tracking ( Name, Email, AssetTag, Priority, Status, ErrorType, Description, OS) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)";
    my $sth = $v[13]->prepare($script);

    #Execute script filling in placeholders with variables passed to the execute function
    $sth->execute(( $v[1], $v[2], $v[3], $v[4], $v[5], $v[6], $v[7], $v[8]));
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    print $cgiRequest->p();
    print "$v[14]'s\n";
    print "Thank you for your $v[14]\'s Request\.";
    }
########################################################################################
#    Update Request                                                                   #
########################################################################################
#Purpose: Takes data from variables and formats it for entry to mySQL database via sql statements
sub UpdateRequest {

my $cgiRequest = new CGI;

######Pulling in parameters passed in function call from @_ to actual variables so we can modify them
my $counter=0;
foreach $a (@_){

 $v[$counter]=$_[$counter];
$counter++;
}

# Create a new database connection
$v[13]  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

########Parse form for errors or missing data
    error_checker();
########Submit data to the database via sql
     my $script = "UPDATE error_tracking SET Name='$v[1]', Email='$v[2]', AssetTag='$v[3]', Priority='$v[4]',`Status`='$v[5]', ErrorType='$v[6]', Description='$v[7]', OS='$v[8]', Assigned='$v[9]', TimeStop='$v[10]', Resolution='$v[11]' WHERE RegID='$v[0]'";
     my $sth = $v[13]->prepare($script);
    #Execute script
    $sth->execute();
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    print $cgiRequest->p();
    print "Thank you for your $v[14]\'s Request\.";

}
########################################################################################
#    kbase Display                                                                     #
########################################################################################
 #purpose: to display only closed or resolved records
sub Kbase {

my $cgiRequest = new CGI;

# Create a new database connection
$v[13]  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

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
    my $sth = $v[13]->prepare($script);
    $sth->execute();
    $sth->bind_columns(\$v[0],
                       \$v[1],
		       \$v[2],
		       \$v[3],
		       \$v[4],
		       \$v[5],
                       \$v[6],
                       \$v[7],
                       \$v[8],
                       \$v[9],
                       \$v[10],
                       \$v[11],
                       \$v[12]);
    # Display the requests
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
    print "</div>";
    #print "<a href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a> ", " <a href=../../services/index.php?Department=25>Back To IT Request System Home</a>" ;
    print $cgiRequest->hr;
    print $cgiRequest->p();
    print $cgiRequest->start_table();

    #cycles through each record printing the corresponding fields to an html table
    while($sth->fetch())
    {

	print $cgiRequest->Tr([
          $cgiRequest->td([$cgiRequest->strong("Request #:"), $v[0]]),
	  $cgiRequest->td([$cgiRequest->strong("Name:"), $v[1]]),
	  $cgiRequest->td([$cgiRequest->strong("E-mail:"),
	      "<a href=\"mailto:$v[2]\">$v[2]</a>"]),
  	  $cgiRequest->td([$cgiRequest->strong("Asset Number:"), $v[3]]),
	  $cgiRequest->td([$cgiRequest->strong("Status:"),$v[4]]),
	  $cgiRequest->td([$cgiRequest->strong("Priority:"), $v[5]]),
	  $cgiRequest->td([$cgiRequest->strong("Error Type:"), $v[6]]),
	  $cgiRequest->td([$cgiRequest->strong("Description:"), $v[7]]),
	  $cgiRequest->td([$cgiRequest->strong("Windows Version:"), $v[8]]),
          $cgiRequest->td([$cgiRequest->strong("Assigned To:"), $v[9]]),
	  $cgiRequest->td([$cgiRequest->strong("Time Submitted:"), $v[11]]),
	  $cgiRequest->td([$cgiRequest->strong("Resolution:"), $v[10]]),
       	  $cgiRequest->td([$cgiRequest->strong("Time Completed:"), $v[12]]),
	  $cgiRequest->td([$cgiRequest->br(), $cgiRequest->br()]),
	]);
    }

    print $cgiRequest->end_table();

    # Stop processing our statement
    $sth->finish();
}
#########################################################################################
#	error_checker                                                                    									#
#########################################################################################
#Purpose: checks variables for proper data or data existence
sub error_checker{

my $self=shift;
my $cgiRequest = new CGI;
my $error;
my $html;

my $counter=0;
foreach $b (@v){
if ($v[$counter]=~ /(;|&|>|<|\?|\!|\'|\`)/ or $v[$counter]= ""){
   $html.= '<div id="menu">';
   $html.= "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>";
   $html.= '<A class=menuitem href="../../services/index.php?Department=25">Back To IT Request System Home</a></div>';
   $html.= "</div><br />";
   #print "<a href= ../../services/index.php?Department=25>Back To IT Request System Home</a> "," <a href=\"", $cgiRequest->url(), "?action=post\">Post Another Request</a>", "<br />" ;
   $html.="<strong>Special Characters such as ; & > < ? ! ' ` are not allowed in text fields such as here $v[$counter]. Please click Post another Request and start over.</strong>\n";
   print "$html\n";
   exit;}
   $counter++;
}
}
##########################################################################################################
# ENDING PACKAGE RequestSystemClass                                                                           #
##########################################################################################################
1;
