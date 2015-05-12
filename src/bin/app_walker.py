#!/usr/bin/env python
"""===============================================================================
======================== NSIS 2.45 Application Walker =========================

        The app walker will create output to be used in .nsh includes for 
    the NSIS (Nullsoft Scriptable Install System).  The .nsh files can then be
    included in the install and un-install sections.

    Mode 1:  creates the install lines
    Mode 2:  creates the uninstall lines
    
    Documentation for NSIS can be found at:
        http://NSIS.sourceforge.net/
    
    PyTis.com, This tool was made by Josh Lee, Copyright 2004-2009  
-------------------------------------------------------------------------------
    USAGE Examples: 
        app_walker directory [silent] (mode 0 defaluts, output to screen)
        app_walker -d{directory} -m1 > my_uninstall.nsh

app_walker -dNSIS -m1 > C:\installer\uninstall.nsh (scanned the alpha9 directory)        
    OUTPUT: scanned directory NSIS created file C:\installer\uninstall.nsh
app_walker alpha9 -oalpha9 -F (scanned the alpha9 directory)
    OUTPUT: alpha9_install.nsh, alpha9_uninstall.nsh
app_walker -obeta10 -F (scanned the beta10 directory)
    OUTPUT: beta10_install.nsh, beta10_uninstall.nsh
    
-------------------------------------------------------------------------------
""" 

import datetime
import glob
#import configobj as config
import md5
import optparse 
import os 
import sys 
#CONF = config.load('PyTis_NSIS_tools.ini')

import logging; log=logging.getLogger('foo')
from cStringIO import StringIO

__version__ = 2.0
__author__ = "Josh Lee"    
__created__ = '2009-08-22 06:55:26.958182'

def filesForDir(fdir):
    return [os.path.abspath(os.path.join(fdir,file)) \
        for file in glob.glob(os.path.join(fdir,"*.*")) \
        if '.svn' not in file.lower() and \
        os.path.basename(file) != 'CVS'] 

def dirsForDir(data, fdir, opts):
    for d in os.listdir(fdir):
        d = os.path.abspath(os.path.join(fdir,d))
        if '.svn' not in d.lower() and os.path.basename(d) != 'CVS' and os.path.isdir(d):
            data.append(d)
            if not opts.iterate:
                mfiles = filesForDir(d)
                if mfiles:
                    data.extend(mfiles)
                mdata = dirsForDir([], d, opts)
                if mdata:
                    data.extend(mdata)
    return data

def allFiles(fdir, opts):
    data = []
    for path, dirs, files in os.walk(fdir, topdown=opts.mode is '0' or opts.mode is '2'):
        if '.svn' not in path.lower() and os.path.basename(path) != 'CVS':
            for f in files:
                if opts.iterate and \
                os.path.dirname(os.path.abspath(os.path.join(path,f))) == \
                os.path.abspath(fdir):
                        data.append(os.path.abspath(os.path.join(path,f)))
                elif not opts.iterate:
                    data.append(os.path.abspath(os.path.join(path,f)))
    return data
    
def allDirs(fdir, opts):
    data = []
    for path, dirs, files in os.walk(fdir, topdown=opts.mode is '0' or opts.mode is '2'):
        if '.svn' not in path.lower() and os.path.basename(path) != 'CVS':
            for d in dirs:
                if opts.iterate and \
                os.path.dirname(os.path.abspath(os.path.join(path,d))) == \
                os.path.abspath(fdir):
                    data.append(os.path.abspath(os.path.join(path,d)))
                elif not opts.iterate:
                    data.append(os.path.abspath(os.path.join(path,d)))
    return data

def cleanSlashes(o):
    if "\\\\" in o:
        o = o.replace("\\", "/")
        while '//' in o:
            o = o.replace('//', '/')
        o = o.replace('/','\\')
        cleanSlashes(o)
    o = o.replace('/','\\')
    return o
    
def inis(fdir, opts):
    doc = """/******************************************************************************
    AUTO-GENERATED NSIS include file. 
    
    Genrated %s
    
    List of files to install.
*/
""" 
    outbuf1 = StringIO()
    basename = ""
    data = dirsForDir(filesForDir(fdir), fdir, opts)
    data.reverse()
    outbuf1.write(doc % datetime.datetime.now())
    outbuf1.write("\t;- Root Dir\n")
    
    outbuf2 = StringIO()
    sys.stdout = outbuf2
    
    print '\tSetOutPath "%s"' % opts.instvar
    
    
    while data:
        abs_file = data.pop()

        if os.path.isfile(abs_file):
            if not basename:
                basename = "%s\\" % os.path.abspath(os.path.dirname(abs_file))
            print '\t\tFile "%s"' % os.path.abspath(abs_file)
            if len(data) and not os.path.isfile(data[len(data)-1]):
                print 
        else:
            print "\t;- %s" % abs_file.replace(basename, '')
            print '\tCreateDirectory "%s\%s"' % (opts.instvar, abs_file.replace(basename, ''))
            if len(data) and os.path.isfile(data[len(data)-1]):
                print '\tSetOutPath "%s\%s"' % (opts.instvar, abs_file.replace(basename, ''))
            if len(data) and not os.path.isfile(data[len(data)-1]):
                print
                
    outbuf2 = cleanSlashes(outbuf2.getvalue())
    sys.stdout = sys.__stdout__
    outbuf1.write(outbuf2)
    return outbuf1.getvalue()
                
def uni(fdir, opts):
    doc = """/******************************************************************************
    AUTO-GENERATED NSIS include file. 
    
    Genrated %s
    
    List of files to install.
*/
""" 
    outbuf1 = StringIO()
    outbuf1.write(doc % datetime.datetime.now())
    
    outbuf2 = StringIO()
    sys.stdout = outbuf2
    if opts.force:
        force = " /r"
    else:
        force = ""
    files = allFiles(fdir,opts)
    for f in files:
        print 'Delete "%s\%s"' % (opts.instvar, f.replace(fdir,''))
    dirs = allDirs(fdir,opts)
    for d in dirs:
        print 'RmDir%s "%s\%s"'% (force, opts.instvar, d.replace(fdir,''))

    outbuf2 = cleanSlashes(outbuf2.getvalue())
    sys.stdout = sys.__stdout__
    outbuf1.write(outbuf2)
    return outbuf1.getvalue()


def md5sum(fdir, opts):
    doc = """/******************************************************************************
    AUTO-GENERATED NSIS include file. Genrated %s
    List of directories and files md5sum'ed.
    DO NOT EDIT THIS FILE!
*/
""" 
    longest = 0
    outbuf1 = StringIO()
    outbuf1.write(doc % datetime.datetime.now())
    
    outbuf2 = StringIO()
    sys.stdout = outbuf2
    
    files = allFiles(fdir,opts)
    for f in files:
        abs_file = os.path.abspath(f)
        if len(f.replace(fdir, '')) > longest:
            longest = len(f.replace(fdir, ''))
    longest+=10
    print "; FILES "
    for f in files:
        abs_file = os.path.abspath(f)
        padding = longest - len(abs_file.replace(fdir, ''))
        print abs_file.replace(fdir, '')[1:], " "*padding, md5.new(file(abs_file, 'rb').read()).hexdigest()

    print ';', '-'*79
    print "; DIRECTORIES"
    for d in allDirs(fdir,opts):
        print d.replace(fdir, '')[1:]     

    outbuf2 = cleanSlashes(outbuf2.getvalue())
    sys.stdout = sys.__stdout__
    outbuf1.write(outbuf2)
    return outbuf1.getvalue()

def mode(opts):

    # Run for mode
    if opts.mode is '0' or opts.all:
        f1 = inis(opts.directory, opts)
        
        if opts.outfile or opts.handle:
            if opts.handle:
                handle = opts.handle
            else:
                handle = file("%s_install.nsh" % opts.outfile,'w')
            handle.write(f1)
            handle.close()
        else:
            print f1
    if opts.mode is '1' or opts.all: 
        f2 = uni(opts.directory, opts)
        if opts.outfile or opts.handle:
            if opts.handle:
                handle = opts.handle
            else:
                handle = file("%s_uninstall.nsh" % opts.outfile,'w')
            handle.write(f2)
            handle.close()
        else:
            print f2

    
    if opts.mode is '2' or opts.all: 
        f3 = md5sum(opts.directory, opts)
        if opts.outfile or opts.handle:
            if opts.handle:
                handle = opts.handle
            else:
                handle = file("%s_md5sum.txt" % opts.outfile,'w')
            handle.write(f3)
            handle.close()
        else:
            print f3

def main(args=''):
    args = args.split()
    errors = []
    fdir=None
    parser = optparse.OptionParser(description=__doc__)
    parser.set_usage(main.__doc__)
    parser.formatter.format_description = lambda s:s

    parser.add_option("-D", "--debug", action="store_true",
        default=False, help="Enable debugging")
    parser.add_option("-A", "--all", action="store_true",
        default=False, help="Run all modes, over-rides -m, outputs to a file and will auto-select name if not provided.")

    parser.add_option("-d", "--directory", action="store",
        default=None, help="The folder to walk")    
    parser.add_option("-f", "--force", action="store_true",
        default=False, help="Force Remove (for Uninstall mode)")
    parser.add_option("-i", "--iterate", action="store_true",
        default=False, help="Only itterate, non-recursive")
    parser.add_option("-m", "--mode", action="store",
        default='0', help="0=Install (default), 1=Uninstall")
    parser.add_option("-o", "--outfile", action="store",
        default='', help="Output filename only specify a file name a suffix and extension are automatically added.")
    parser.add_option("-s", "--silent", action="store_true",
        default=False, help="Do not print anything, even errors.")
    parser.add_option("-V", "--instvar", action="store",
        default='$INSTVAR', help="Install variable (default $INSTDIR\)")
    if not args:
        (opts, cmd) = parser.parse_args(sys.argv[1:])
    else:
        (opts, cmd) = parser.parse_args(args)
    
    opts.handle = None
    # Error checking

    if len(cmd) > 1:
        errors.append("INVALID INPUT (try --debug)")
        
    if opts.mode not in ['0','1']:
        errors.append("INVALID RUNTYPE: usage: 0 or 1 -- You typed: %s" % opts.mode)
    
    if opts.directory:
        opts.directory = os.path.abspath(opts.directory)
    elif len(cmd):
        opts.directory = os.path.abspath(cmd[0])
    else:
        errors.append("Please specify a directory to scan")
        
    if opts.outfile:
        if not os.path.isdir(os.path.abspath(os.path.dirname(os.path.abspath(opts.outfile)))):
            errors.append("Outfile directory does not exist: %s" % os.path.abspath(os.path.dirname(os.path.abspath(opts.outfile))))
    if opts.directory and not os.path.isdir(opts.directory):
        errors.append("Directory not found: %s" % opts.directory)
        
    # Display errors if any
    if errors and opts.silent:
        return
    if errors or (len(sys.argv) < 2 and not cmd):
        parser.print_help()
        for error in errors:
            print "ERROR:",error
           
        if len(sys.argv) < 2:
            
            options = raw_input("Enter options (q to quit):")
            if 'q' == options.lower():
                print 'Have a nice day :) !'
                os.system("pause")
            else:
                return main(options)
                os.system("%s %s" % (__file__,options))
        return 

    # Set OutFile
    if opts.all and not opts.outfile:
        opts.outfile = os.path.basename(opts.directory)
        
    # Logging Configuration
    log.setLevel(0)
    formatter = '%(levelname)-8s %(message)s'

    if opts.debug:
        if opts.mode is '0': pmode = 'INSTALL'
        if opts.mode is '1': pmode = 'UNINSTALL'

        print ';', '='*78
        print ';', '='*30, 'DEBUGING', '='*30
        print ';Directory passed with argument:  ', opts.directory
        print ';Directory passed in sys args:    ', len(cmd) > 0
        print ';Install Variable:                ', opts.instvar
        print ';Directory:                       ', opts.directory
        print ';Recursive:                       ', not opts.iterate
        print ';Silent:                          ', False
        print ';Mode:                            ', pmode
        print ';OutFile:                         ', opts.outfile
        print ';', '='*78
        logging.basicConfig(level=logging.DEBUG, format=formatter)
    else:
        logging.basicConfig(level=logging.INFO, format=formatter)
    
    mode(opts)
    if not opts.outfile:
        os.system("pause")

if __name__ == '__main__':
    main()