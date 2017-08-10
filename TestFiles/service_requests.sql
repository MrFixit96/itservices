# phpMyAdmin SQL Dump
# version 2.5.7-pl1
# http://www.phpmyadmin.net
#
# Host: localhost
# Generation Time: Aug 10, 2004 at 04:54 PM
# Server version: 4.0.20
# PHP Version: 4.3.8
# 
# Database : `service_requests`
# 

# --------------------------------------------------------

#
# Table structure for table `error_tracking`
#

CREATE TABLE `error_tracking` (
  `RegID` int(6) NOT NULL auto_increment,
  `Name` varchar(50) NOT NULL default '',
  `Email` varchar(50) NOT NULL default '',
  `AssetTag` varchar(10) NOT NULL default '',
  `Priority` varchar(50) NOT NULL default '',
  `Status` varchar(50) default NULL,
  `ErrorType` varchar(50) NOT NULL default '',
  `Description` varchar(255) default NULL,
  `OS` varchar(50) default NULL,
  `Assigned` varchar(50) default NULL,
  `TimeStart` timestamp(14) NOT NULL,
  `TimeStop` date default '0000-00-00',
  `Resolution` varchar(255) default NULL,
  PRIMARY KEY  (`RegID`,`RegID`),
  KEY `Name` (`Name`,`Email`,`AssetTag`,`Priority`,`Status`)
) TYPE=MyISAM AUTO_INCREMENT=16 ;

#
# Dumping data for table `error_tracking`
#

INSERT INTO `error_tracking` VALUES (1, 'James Anderton', 'janderton@peoriachristian.org', '31309', 'High (Requires immediate attention)', 'In Progress (See Resolution Comments)', 'PC Problem/Question', 'My Laptop Crashed with error Operating System Not Found!', 'Windows XP', 'James Anderton', 20040809092330, '0000-00-00', 'Needs New Hard Drive Purchased.');
INSERT INTO `error_tracking` VALUES (2, 'James Anderton', 'janderton@peoriachristian.org', '31309', 'Normal (Fix as Schedule Permits)', 'Resolved (Completed)', 'Other', 'Updated Status System', 'Windows XP', 'James Anderton', 20040806145605, '0000-00-00', 'Works Great.');
INSERT INTO `error_tracking` VALUES (3, 'James Anderton', 'janderton@peoriachristian.org', '31309', 'High (Requires immediate attention)', 'Closed (Denied)', 'Other', 'Testing SQL Filtering', 'Windows XP', 'James Anderton', 20040806163911, '0000-00-00', 'Try the OR function');
INSERT INTO `error_tracking` VALUES (4, 'James Anderton', 'janderton@peoriachristian.org', '31309', 'High (Requires immediate attention)', 'Open', 'Other', 'Finish Built-In Reporting\r\nSolve TimeStamp Issue\r\nFinish Error Trapping\r\nAdd Auto-notification module\r\nAdd Login to AdminView', 'Windows XP', 'James Anderton', 20040810152136, '0000-00-00', 'Finished Error Trapping\r\nFinished Login for AdminView');

# --------------------------------------------------------

#
# Table structure for table `security`
#

CREATE TABLE `security` (
  `Name` varchar(50) NOT NULL default '',
  `Password` varchar(25) NOT NULL default ''
) TYPE=MyISAM;

#
# Dumping data for table `security`
#

INSERT INTO `security` VALUES ('jcaa', 'j19a96');
INSERT INTO `security` VALUES ('jm', 'neadd');
INSERT INTO `security` VALUES ('shutton', '9waye');
