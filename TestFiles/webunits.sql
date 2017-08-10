# phpMyAdmin SQL Dump
# version 2.5.7-pl1
# http://www.phpmyadmin.net
#
# Host: localhost
# Generation Time: Sep 10, 2004 at 03:40 PM
# Server version: 4.0.20
# PHP Version: 4.3.8
# 
# Database : `content`
# 

# --------------------------------------------------------

#
# Table structure for table `webunits`
#

CREATE TABLE `webunits` (
  `Key` int(11) NOT NULL auto_increment,
  `AreaID` int(11) NOT NULL default '0',
  `Department` int(11) NOT NULL default '0',
  `SubDepartment` int(11) NOT NULL default '0',
  `AreaDisplayName` varchar(40) NOT NULL default '',
  `LinkText` varchar(40) NOT NULL default '',
  `DirectoryName` varchar(30) NOT NULL default '',
  `OwnerGID` varchar(30) NOT NULL default '',
  `Approver` varchar(30) NOT NULL default '',
  `AreaSort` int(11) NOT NULL default '0',
  `DeptSort` int(11) NOT NULL default '0',
  `SubDeptSort` int(11) NOT NULL default '0',
  `Status` tinyint(1) NOT NULL default '0',
  PRIMARY KEY  (`Key`)
) TYPE=MyISAM AUTO_INCREMENT=170 ;
