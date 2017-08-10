#!/usr/bin/perl
#Modules used
use strict;   #requires "dim'ing of variables through the (my) statement
use warnings; #prints out non-fatal errors
use DBI;      #DBI module used to connect to database

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
        $self->{CreatePage};
        $self->{DepartmentLevelNav};
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
        my $template;
        my $self = shift;

        my $file="C:\\WEBDSN\\HTML\\jpmPageTemplate2.htm";
        open FILE, $file or die "Can't open $file: $!";
        while(<FILE>){
                $template=$template . $_;
                }
        close FILE;

        return $template;
        }
sub CreatePage {
        my $self = shift;
        my $x;
        my $page;
        my $searchC = '%content%';
        my $replaceC='hacker';
        my $searchD = '%DepartLevelNav%';
        my $replaceD=$self->DepartmentLevelNav;
        my $searchL = '%CurrentArea%';
        my $replaceL=$self->CurrentLevelNav ;

        $page = $self->ReadTemplate;
        $page =~ s/($searchC)/$replaceC/;   # $page contains the HTML TEMPLATE READ BY $self->ReadTemplate
        $page =~ s/($searchD)/$replaceD/;
        $page =~ s/($searchL)/$replaceL/;
        print $page;
    }
sub DepartmentLevelNav {
        my $self = shift;
        my $dbh  = DBI->connect("DBI:mysql:content", "root", "j19a96",{ RaiseError => 1 });
        my $script;
        my $Department;
        my $SubDepartment;
        my $Status;
        my $AreaID;
        my $AreaDisplayName;
        my $DirectoryName;
        my $OwnerGID;
        my $Approver;
        my $AreaSort;
        my $DeptSort;
        my $SubDeptSort;
        my $LinkText;
        my $NavCount="0";
        my $link1;
        my $link2;
        #prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved request.
   $script = " SELECT* FROM webunits ".
                 " WHERE AreaID=11 AND Status = 2      ".
		 " ORDER BY 'AreaSort'   ";

# Fetch the contents of the requests
    my $sth = $dbh->prepare($script);
    $sth->execute();
    $sth->bind_columns(\ my $Key, 
         \$AreaID,
         \$Department,
         \$SubDepartment,
         \$AreaDisplayName,
         \$LinkText,
         \$DirectoryName,
         \$OwnerGID,
         \$Approver,
         \$AreaSort,
         \$DeptSort,
         \$SubDeptSort,
         \$Status);
         
while($sth->fetch())
    {           #IF THE Record is the Current Area then bold the link...Check this through using ENV variables
        #if ($ENV{ REQUEST_URI} eq $LinkText){   #USE THIS WHEN FILENAMES ARE CORRECT.
        if ($Department eq "0"){
            $link1 .= "<a href = ../../index.php?Department=$Department><b>$LinkText</b></a>";
        }else{
            $link2 .= "<a href = ../../index.php?Department=$Department>$LinkText</a><br />";
        }
    }
    return my $NavBar=$link1."<br />".$link2;
}
sub CurrentLevelNav {
        my $self = shift;
        my $dbh  = DBI->connect("DBI:mysql:content", "root", "j19a96",{ RaiseError => 1 });
        my $script;
        my $Department;
        my $SubDepartment;
        my $Status;
        my $AreaID;
        my $AreaDisplayName;
        my $DirectoryName;
        my $OwnerGID;
        my $Approver;
        my $AreaSort;
        my $DeptSort;
        my $SubDeptSort;
        my $LinkText;
        my $NavCount="0";
        my $link1;
        my $link2;
        #prepare sql statement to grab contents of error_tracking table thats not either a closed or resolved request.
   $script = " SELECT* FROM webunits ".
                 " WHERE AreaID=11 AND Status = 2      ".
		 " ORDER BY 'AreaSort'   ";

# Fetch the contents of the requests
    my $sth = $dbh->prepare($script);
    $sth->execute();
    $sth->bind_columns(\ my $Key, 
         \$AreaID,
         \$Department,
         \$SubDepartment,
         \$AreaDisplayName,
         \$LinkText,
         \$DirectoryName,
         \$OwnerGID,
         \$Approver,
         \$AreaSort,
         \$DeptSort,
         \$SubDeptSort,
         \$Status);
         
while($sth->fetch())
    {           #IF THE Record is the Current Area then bold the link...Check this through using ENV variables
        if ($ENV{ REQUEST_URI} eq "index.php?Department=$Department"){   #USE THIS WHEN FILENAMES ARE CORRECT.
            #$link1 .= "<a href = ../../index.php?Department=$Department><b>$LinkText</b></a>";
            $link1="<a href=../../$ENV{ REQUEST_URI}><b>$LinkText</b></a>";
        }
    }
    return my $NavBar=$link1;
    #return "<a href=../../$ENV{ REQUEST_URI}><b>$LinkText</b></a>";

    }
    1;  # so the require or use succeeds


##########################################################################################################
# ENDING PACKAGE ASSEMBLEPAGE                                                                            #
##########################################################################################################
