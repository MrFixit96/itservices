#!perl
# Uncomment these 3 lines for more debugging info:
$|=1;
print "Content-type: text/html\n\n";
use CGI::Carp('fatalsToBrowser');

#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use CGI;      #CGI module used to make generating dynamic html easier
use DBI;      #DBI module used to connect to database

#########################################################################################
#	Variables									#
#########################################################################################

#my $request = new CGI; # Instantiate a CGI object
my $page = new AssemblePage;
my $html;
# Create a new database connection
my $dbh  = DBI->connect("DBI:mysql:service_requests", "root", "j19a96",{ RaiseError => 1 });

##############################################################################################################
#   Package Assemble Page                                                                                    #
##############################################################################################################
#Purpose: Read in template page and populate it with content in proper places
package AssemblePage;

##############################################################################
#     Method "new"                                                           #
##############################################################################
#Purpose: Gives the ability to create new objects from the AssemblePage Class
    sub new {
        my $self = {};
        $self->{CreateContent}       =undef
        $self->{AreaLevelNav}        =undef
        $self->{CurrentLevelNav}     =undef
        $self->{Template}            =undef
        bless $self;
        return $self;

    }
##############################################################################
#     Method "ReadTemplate"                                                  #
##############################################################################
#Purpose: Reads in data from a HTML template file
    sub Template{

        my $template;
        my $file="C:\\WEBDSN\\HTML\\jpmPageTemplate2.htm";

        open FILE, $file or die "Can't open $file: $!";

        while(<FILE>){
                $template=$template . $_;
                }
        close FILE;
        print "$template";
        
        my $self = shift;
        if (@_) { @{ $self->{Template} } = @_ }
        return @{ $self->{Template} };
    }
    ##############################################
    ## methods to access per-object data        ##
    ##                                          ##
    ## With args, they set the value.  Without  ##
    ## any, they only retrieve it/them.         ##
    ##############################################    
    sub CreateContent {
        my $self = shift;
        if (@_) { $self->{CreateContent} = shift }
        return $self->{CreateContent};
    }
    sub AreaLevelNav {
        my $self = shift;
        if (@_) { $self->{AreaLevelNav} = shift }
        return $self->{AreaLevelNav};
    }
    sub CurrentLevelNav {
        my $self = shift;
        if (@_) { @{ $self->{AreaLevelNav} } = @_ }
        return @{ $self->{AreaLevelNav} };
    }    1;  # so the require or use succeeds


##########################################################################################################
# ENDING PACKAGE ASSEMBLEPAGE                                                                            #
##########################################################################################################

# Print Template to HTML
$html = $page->ReadTemplate;





# Wait for the user to press a key

&press_enter_to_continue();

# Get out of here!
#exit;

# Wait for the user to press a key

sub press_enter_to_continue

{
 <>;
 return;
}

