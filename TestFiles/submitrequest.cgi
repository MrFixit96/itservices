#!perl

$|=1; #stop buffering and caching
#print "Content-type: text/html\n\n"; # forcibly print page header
use CGI::Carp('fatalsToBrowser'); # uses carp module, redirect to browser


#Name: James Anderton
#Date:4-26-04
=Purpose: takes input from user and writes it to a flat file. I will move this to
          a database as time permits.

Use This to make links
print $q->blockquote(
                     "Many years ago on the island of",
                     $q->a({href=>"http://crete.org/";},"Crete"),
                     "there lived a Minotaur named",
                     $q->strong("Fred."),
                    ),
       $q->hr;
=cut


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

make_form();

sub WriteInfo{      # Writes info to a text file.

my $OUTPUT="requests.txt";
chomp(my $date= `date /T`);
chomp(my $time= `time /T`);
my $timestamp= "$date $time\n";
open FILEO, ">> $OUTPUT";
    print FILEO "Time: $timestamp";
    print FILEO "Name: $name\n";
    print FILEO "Email Address: $email\n";
    print FILEO "Asset#: $assetNumber\n";
    print FILEO "Error Type: $errorType\n";
    print FILEO "Description: $description\n";
    print FILEO "Priority Level: $priorityLevel\n";
    print FILEO "\n<br />";
close FILEO;
}

sub ParseInfo{           # Parses info for special chars.
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
sub ErrorPage{        #Writes an error page explaining problem and linking back to form.
print $request->header;
print $request->start_html("Guest Book of Eternal Peril ;-)");
     print "<br />$description<br />";
     print $request->a({href=>"week13labp2.pl"},"Redo Entry"),
       $request->hr;

# Print the page end
print $request->end_html;
}





sub make_form{
# Print the page
print $request->header;
print $request->start_html("Service Request System");

if($submit eq "submit") # first time through initial block is skipped
{

    ParseInfo();#Parses info for special chars and passes to write sub.
}
else
{
    # Show the form - magic starts here
    print $request->start_form;
    print "Name: " ,
        $request->textfield(
            -name      => 'name',
            -default   => 'Your name goes here.',
            -size      => '50',
            -maxlength => '50'),
        $request->br;
    print "Email address: " ,
        $request->textfield(
            -name      => 'email_address',
            -default   => 'me@peoriachristian.org',
            -rows      => '50',
            -columns   => '50'),
        $request->br;
    print "Asset # " ,
        $request->textfield(
            -name      => 'assetNumber',
            -default   => 'Im not sure!',
            -rows      => '50',
            -columns   => '50'),
        $request->br;
    print "(located at the top right of your laptop or right side of your desktop case)<br />";

    print "Description: " ,
        $request->textarea(
            -name      => 'description',
            -rows      => '5',
            -columns   => '50'),
        $request->p;
    print "Error Type: " ,
        $request->popup_menu(
            -name      => 'errorType',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "Network Outage", "Blocked Website", "PC Problem/Question", "Equipment Repair/Replace", "Other"]),
        $request->br;
    print "Priority Level: " ,
        $request->popup_menu(
            -name      => 'priorityLevel',
            -default   => '---SELECT ONE---!',
            -values    => ["---SELECT ONE---", "High (Requires immediate attention)", "Medium (Needs attention soon)", "Normal"]),
        $request->br;
    print $request->submit(
        -name  => "submit",
        -value => "submit");
    print " ", $request->reset, " ";
    print $request->endform;
 }
  print $request->a({href=>"displayrequest.cgi"},"View Open Requests"),
       $request->hr;
# Print the page end
print $request->end_html;
}
