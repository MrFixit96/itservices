#!perl

#Name: James Anderton
#Date:4-26-04
#Purpose:Dispays text from service request file.

use strict;
use warnings;
use CGI;

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

#call ReadInfo
ReadInfo();
#call ReadInfo to read the guestbook from a file.

sub ReadInfo{
print $request->header;
print $request->start_html("Service Request System");
     print $request->a({href=>"submitrequest.cgi"},"Submit New Request."),
       $request->hr;
#***************SPLIT INTO TWO FILES**** ONE CALLING THE OTHER.
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

