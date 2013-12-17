##############################################################
#
# simple python script for hadding root files from Fermi dCache 
#
###############################################################

MYEXEC = 'hadd -f'

CopyCommand="dc_dccp" # dccp (dCache) or cp
# CopyCommand="cp" # dccp (dCache) or cp

SearchString=".root"
import sys,string,math,os, commands,tempfile

def usage():
    """ Usage: python haddFromdCache.py <inputDir> <outputFile>
    Add all root files in <inputDir> and put the output in <outputFile>
    """
    pass


if __name__ == '__main__':

    narg=len(sys.argv)
    # print sys.argv[0]

    if narg < 3 :
        print usage.__doc__
        sys.exit(1)

    inDir=sys.argv[1]
    outFile=sys.argv[2]
    currDir=os.getcwd()

    if not os.path.isabs(outFile):
        outFile=os.path.join(currDir,outFile)
    print "Writing output to: ",outFile

    xx=commands.getstatusoutput("which " + MYEXEC)
    returnVal= xx[0]
    if (returnVal!=0):
        print MYEXEC, " command not found"
        print "Please check that root and/or CMSSW are setup"
        sys.exit(0)


    if not os.path.exists(inDir):
        print "Input directory:", inDir," does not exist -- check name"
        sys.exit(1)

    mytempdir=tempfile.mkdtemp()
    # print mytempdir

    fileList=os.listdir(inDir)
    # print fileList

    nfile=0
    print "\nCopying files"

    for ifile in fileList:

        indx=ifile.find(SearchString)
        if indx>-1:

            sourcefile=os.path.join(inDir,ifile)
            # print sourcefile

            nfile+=1
            myargs=string.join([CopyCommand,sourcefile,mytempdir])
            print myargs
            os.system(myargs)
            
    if nfile > 0:
        print "\nDone copying"
        myargs=string.join([MYEXEC,outFile,"*"])
        os.chdir(mytempdir)
        # print os.listdir(mytempdir)
        print "Now executing: ",myargs
        os.system(myargs)
    else:
        print "No files copied"

    # cleanup
    tmpList=os.listdir(mytempdir)
    for ifile in tmpList:
        os.remove(ifile)
    os.chdir(currDir)
    os.rmdir(mytempdir)

    print "\n"
    sys.exit(0)

