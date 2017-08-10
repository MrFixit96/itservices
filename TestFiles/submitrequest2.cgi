#!perl

#$|=1; #stop buffering and caching
#print "Content-type: text/html\n\n"; # forcibly print page header
#use CGI::Carp('fatalsToBrowser'); # uses carp module, redirect to browser


#Name: James Anderton
#Date:8-3-04
#Purpose: Takes in User Service Requests and stores them to a mysql backend so that IT Services
#		has a realtime queue for keeping track of jobs and letting the user know its status.         


use strict;
use warnings;
use CGI;

#########################################################################################
#	Variables									#
#########################################################################################

# Instantiate a CGI object
my $request = new CGI;

# Get the list of parameters passed
my $name = $request->param("name");
my $assetNumber = $request->param("assetNumber");
my $errorType = $request->param("errorType");
my $email = $request->param("email_address");
my $description = $request->param("description");
my $priorityLevel = $request->param("priorityLevel");
my $submit = $request->param("submit");
my $view = $request->param("view");

#########################################################################################
#	MAIN										#
#########################################################################################
#Purpose: Starts program
make_form();

#########################################################################################
#	WriteInfo									#
#########################################################################################
#Purpose: Takes info, formats and prints it to a textfile.

sub WriteInfo{      
my $OUTPUT="requests.txt";
chomp(my $date= `date /T`);
chomp(my $time= `time /T`);
my $timestamp= "$date $time\n";
open FILEO, ">> $OUTPUT";
    print FILEO "Time: $timestamp";
    print FILEO "Priority Level: $priorityLevel\n";
    print FILEO "Status: OPEN\n";
    print FILEO "Name: $name\n";
    print FILEO "Email Address: $email\n";
    print FILEO "Asset#: $assetNumber\n";
    print FILEO "Error Type: $errorType\n";
    print FILEO "Description: $description\n";
    print FILEO "Assigned To:                 \n";
    print FILEO "Resolution:                  \n";
    print FILEO "Date Solved:                  \n";
    print FILEO "<br />";
close FILEO;
#Call ReadInfo
ReadInfo();
}

#########################################################################################
#	ReadInfo									#
#########################################################################################
#Purpose: Reads info in from textfile and prints it line for line in html

sub ReadInfo{
print $request->start_html("Service Request System");
     print $request->a({href=>"submitrequest2.cgi"},"Submit New Request."),
       $request->hr;
my $file="requests.txt";
open FILE, $file or die "Can't open $file: $!";
while(<FILE>){
        chomp;
        print "$_\n<br />";
}
close FILE;

# Print the page end
print $request->end_html;
}
#########################################################################################
#	ParseInfo									#
#########################################################################################
#Purpose: Parses info for special chars and bails to an error page if found

sub ParseInfo{ 
   if ($name=~ /;|&|>|</){
        $description= "Special Characters are not allowed.<br /> Please click Redo Entry and start over.\n";
        ErrorPage();
    }else{
        if ($assetNumber=~ /;|&|>|</){
        $description= "Special Characters are not allowed.<br /> Please click Redo Entry and start over.\n";
        ErrorPage();
    }else{
        if ($errorType=~ /;|&|>|</){
        $description= "Special Characters are not allowed.<br /> Please click Redo Entry and start over.\n";
        ErrorPage();
    }else{
        if ($email=~ /;|&|>|</){
        $description= "Special Characters are not allowed.<br /> Please click Redo Entry and start over.\n";
        ErrorPage();
    }else{
        if ($priorityLevel=~ /;|&|>|</){
        $description= "Special Characters are not allowed.<br /> Please click Redo Entry and start over.\n";
        ErrorPage();
    }else{
        if ($description=~ /;|&|>|</){
        $description= "Special Characters are not allowed.<br /> Please click Redo Entry and start over.\n";
        ErrorPage();
    }else{
          WriteInfo();
          #exit
         }
        }
       }
     }
    }
  }
}

#########################################################################################
#	ErrorPage									#
#########################################################################################
#Purpose:Writes an error page explaining problem and linking back to form.

sub ErrorPage{        
print $request->header;
print $request->start_html("IT Services");
     print "<br />$description<br />";
     print $request->a({href=>"week13labp2.pl"},"Redo Entry"),
       $request->hr;

# Print the page end
print $request->end_html;
}




#########################################################################################
#	Make_Form									#
#########################################################################################
#Purpose:Creates the request submission form

sub make_form{
# Print the page
print $request->header;
print $request->start_html("Service Request System");

if($submit eq "submit") # first time through initial block is skipped otherwise submits data
{

    ParseInfo();#Parses info for special chars and passes to write sub.
}
elsif($view eq "View Requests"){  #Skips to the ReadInfo sub
       ReadInfo();
}
else
{

        # Show the form
    #print "<a href=\"", $request->url(), "?action=View\">View Requests</a>";
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
	$request->td(["Description: " , $request->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50')]),
	$request->td(["Error Type: " ,
        $request->popup_menu(
            -name      => 'errorType',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"])]),
	$request->td(["Priority Level: " ,
        $request->popup_menu(
            -name      => 'priorityLevel',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal (Fix as Schedule Permits)"]),
            ])]);

    print $request->end_table();
    print $request->p;
    print $request->submit(
	-name  => "submit",
	-value => "submit");
    print " ", $request->reset, " ";
    print $request->submit(
	-name  => "view",
	-value => "View Requests");
    print $request->endform;
 }
# Print the page end
print $request->end_html;
}
