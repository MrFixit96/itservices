#!perl
#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors

#########################################################################################
#	Variables									#
#########################################################################################


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
        $self->{CreateContent};
        $self->{AreaLevelNav};
        $self->{CurrentLevelNav};
        $self->{ReadTemplate};
        bless $self;
        return $self;

    }
##############################################################################
#Method "ReadTemplate" ***NEEDS A HEADER PRINTED BEFORE THIS METHOD IS CALLED#
##############################################################################
#Purpose: Reads in data from a HTML template file
    sub ReadTemplate{
        my $self = shift;
        if (@_) { $self->{ReadTemplate} }
        my $template;
        my $file="C:\\WEBDSN\\HTML\\jpmPageTemplate2.htm";

        open FILE, $file or die "Can't open $file: $!";

        while(<FILE>){
                $template=$template . $_;
                }
        close FILE;
        print "$template";
        return  $self->{ReadTemplate} };
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
        if (@_) { $self->{CurrentLevelNav} }
        return $self->{CurrentLevelNav} };
    1;  # so the require or use succeeds


##########################################################################################################
# ENDING PACKAGE ASSEMBLEPAGE                                                                            #
##########################################################################################################
