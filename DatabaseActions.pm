#!/usr/bin/perl
#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use DBI;      #DBI module used to connect to database
use CGI;      #CGI Module used to create html tags
##############################################################################################################
#   Package DatabaseActions                                                                               #
##############################################################################################################
#Purpose: Read in template page and populate it with content in proper places
package DatabaseActions;
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

my $Field1;
my $Field2;

my $cgiRequest = new CGI;

my $counter=0;
foreach $a (@_){

$v[$counter] = $_[$counter];
print "$v[$counter]";
$counter++;
}
# Create a new database connection
my $dbh = DBI->connect("DBI:mysql:$v[3]", "$v[4]", "$v[5]",{ RaiseError => 1 });

#prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved request.
# my $script = "SELECT Field1, Field2 FROM test ";

# Fetch the contents of the requests
    my $sth = $dbh->prepare($v[6]);
    $sth->execute();
    $sth->bind_columns(\$Field1, \$Field2);

    # Display the contents

    print $cgiRequest->start_table();
    
    #cycles through each record printing the corresponding fields to an html table
    while($sth->fetch())
    {

	print $cgiRequest->Tr([
          $cgiRequest->td([$cgiRequest->strong("Field 1:"), $Field1]),
	  $cgiRequest->td([$cgiRequest->strong("Field 2:"), $Field2]),
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
 print " $counter $v[$counter]\n";
$counter++;
}

########Parse form for errors or missing data
    #$self->error_checker;

# Create a new database connection
$v[2]  = DBI->connect("DBI:mysql:testdb", "root", "j19a96",{ RaiseError => 1 });

########Submit data to the database via sql
    # Add this entry to the database using placeholders(?'s)
    my $script = "INSERT INTO test ( Field1, Field2) VALUES ( ?, ?)";
    my $sth = $v[2]->prepare($script);

    #Execute script filling in placeholders with variables passed to the execute function
    $sth->execute(( $v[0], $v[1]));
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print "</div>";
    print $cgiRequest->p();
    print "Thank you for your request\.";
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
$v[2]  = DBI->connect("DBI:mysql:testdb", "root", "j19a96",{ RaiseError => 1 });

########Submit data to the database via sql
     my $script = "UPDATE test SET Field1='$v[0]', Field2='$v[1]'";
     my $sth = $v[2]->prepare($script);
    #Execute script
    $sth->execute();
    $sth->finish();

    # Display confirmation that the entry was accepted.
    print '<div id="menu">';
    print "<A class=menuitem href=\"", $cgiRequest->url(), "?action=post\">Post a Request</a>";
    print "</div>";
    print $cgiRequest->p();
    print "Thank you for your request\.";

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
