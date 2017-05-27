#! /usr/bin/env python

'''
Script to check the server accesses, and warn if an abnormal number of occurrence of 404 errors

Creation date: 24/02/2017
Date last updated: 18/04/2017

* 
* License: GPL
* Copyright (c) 2017 DI-FCUL
* 
* Description:
* 
* This file contains the check_apache404 plugin
* 
* Use the nrpe program to check request on remote server.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
from optparse import OptionParser
from time import strftime
import time
import datetime

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def checklogs(opts):
    critical = [i for i in opts.critical.split(",")]
    warning = [i for i in opts.warning.split(",")]
    try:
        critical_total = int(critical[0])
        critical_ip = int(critical[1])
    except:
        print('Review value of critical options, these must be a intiger separated by ":"')
        sys.exit(ExitUnknown)
    try:
        warning_total = int(warning[0])
        warning_ip = int(warning[1])
    except:
        print('Review value of warning options, these must be a intiger separated by ":"')
        sys.exit(ExitUnknown)
    if opts.number:
        totalerror = int(os.popen("tail -n %s %s | grep 404 | wc -l"%(opts.number,opts.path)).read())
        qtdd = str(os.popen("tail -n %s %s | grep 404 | awk '{print $1}' | sort | uniq -c | sort $1 |awk '{print $1}' | sort -nr | awk '{print $1}'"%(opts.number, opts.path)).read())
        ips = str(os.popen("tail -n %s %s | grep 404 | awk '{print $1}' | sort | uniq -c | sort -nr $1 | sort -nr | awk '{print $2}'"%(opts.number,opts.path)).read())
        os.popen("tail -n %s %s | grep 404 > %s"%(opts.number,opts.path,opts.output)).read()
        
    else:
        totalerror = int(os.popen("cat %s | grep 404 | wc -l"%opts.path).read())
        qtdd = str(os.popen("cat %s | grep 404 | awk '{print $1}' | sort | uniq -c | sort $1 |awk '{print $1}' | sort -nr | awk '{print $1}'"%opts.path).read())
        ips = str(os.popen("cat %s | grep 404 | awk '{print $1}' | sort | uniq -c | sort -nr $1 | sort -nr | awk '{print $2}'"%opts.path).read())
        os.popen("cat %s %s | grep 404 > %s"%(opts.number,opts.path,opts.output)).read()
    num_ip = []
    IPs = []
    
    if totalerror != 0:
        newitemip = [i for i in ips.split("\n")]
        IPs.extend([i for i in newitemip])
        IPs.pop(-1)
        newitemnum = [i for i in qtdd.split("\n")]
        num_ip.extend([i for i in newitemnum])
        num_ip.pop(-1)
        num = 0
        for numero in num_ip:
            if int(numero) >= critical_ip or totalerror >= critical_total:
                print("Critical - Were found %s errors 404, the IP Address %s, did %s acess attempts, see %s"%(totalerror, IPs[num],numero,opts.output))            
                sys.exit(ExitCritical)
            elif int(numero) >= warning_ip or totalerror >= warning_total:
                print("Warning - Were found %s errors 404, the IP Address %s, did %s acess attempts, see %s"%(totalerror, IPs[num],numero,opts.output))
                sys.exit(ExitWarning)
            elif int(numero) < warning_ip or totalerror < warning_total:
                print("Ok - Were found only %s errors 404, the IP Address %s, did %s acess attempts, see %s"%(totalerror, IPs[num],numero,opts.output))
                sys.exit(ExitOK) 
            else:
                num = num +1            
    else:
        print('No 404 error were found in file log "%s"'%opts.path)
        sys.exit(ExitOK)
                
def main():
    parser = OptionParser("usage: %prog [options] ARG1 ARG2 FOR EXAMPLE: -c 300,100 -w 200,70 -p /var/log/apache2/access.log -n 2000")
    parser.add_option("-p","--path", dest="path",
                      help="Enter the full path to the apache logs file, i.e. -p /var/log/apache2/access.log")
    parser.add_option("-o","--output", dest="output", default="/tmp/apache.txt",
                      help="Enter the full path to save txt file contined all find line, i.e. -p /var/log/apache2/apache.txt"+
                      "default is /tmp, but this folder is not secure to save this file")
    parser.add_option("-c","--critical", dest="critical", default=False, type=str,
                      help="Enter the number of all attemps you considered critical and number of attemps of a single IP are considered critical, separated by ':'")
    parser.add_option("-w","--warning", dest="warning", default=False, type=str,
                      help="Enter the number of all attemps you considered warning and number of attemps of a single IP are considered warning, separated by ':'")
    parser.add_option("-n","--number", dest="number", default=False, type=int,
                      help="Enter the number of records that you want to check")
    parser.add_option("-V","--version", action="store_true", dest="version", help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author", help="This option show author information and exit")
    (opts, args) = parser.parse_args()
    
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_apache404.py %s"%__version__)
        sys.exit()
    if not opts.critical:
        parser.error('Please, this program requires critical values arguments, these must be a intiger separated by ","')
    elif not opts.warning:
        parser.error('Please, this program requires warning values arguments, these must be a intiger separated by ","')
    if opts.path:
        if not os.path.exists(opts.path):
            parser.error("Please, this program requires to specify a valid path file.")
        else:
            checklogs(opts)
    else:
        parser.error("Please, this program requires to specify a valid path file.")

if __name__ == '__main__':
    main()
