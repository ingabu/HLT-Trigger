#!/usr/bin/env python

import sys,string,math,os
import ConfigParser
import glob

from array import array
from optparse import OptionParser

from PhysicsTools.PythonAnalysis import *
import ROOT
from ROOT import *
gSystem.Load("libFWCoreFWLite.so")
AutoLibraryLoader.enable()


def Book1D(cname,ctitle,nbins,xmin,xmax,doSumw2=True):
    h=TH1F(cname,ctitle,nbins,xmin,xmax)
    if doSumw2: h.Sumw2()
    return h


def BookHistograms():

    ### Book the histograms

    hists={}

    hName="HLT_PFJet400"
    hTitle="Counts"
    hists[hName] = Book1D(hName,hTitle,2,0.,2.)


    outf.cd()
    return hists


if __name__ == "__main__":

    AutoLibraryLoader.enable()

    outfile="test.root"

    outf = TFile(outfile,"RECREATE");
    SetOwnership( outf, False )   # tell python not to take ownership
    print "Output written to: ", outfile


    h=BookHistograms()  # ## book histograms
    #print "CCLA:",h
    
    InputRootFiles = glob.glob ("/pnfs/cms/WAX/11/store/user/lpctrig/ingabu/TMDNtuples/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_50ns/*.root")
    #print InputRootFiles  

    tree = TChain("HltTree")

    for rootfile in InputRootFiles:
        tree.AddFile("dcache:" + rootfile)



    NEntries = tree.GetEntries()
    print "Number of entries on Tree:",NEntries
    nevt=NEntries
    #nevt=100000
    decade=0

    counter0=0
    counter1=0
  

    for jentry in xrange( nevt ):

        tree.GetEntry(jentry) 

        progress = 10.0*jentry/(1.0*nevt);
        k = math.floor(progress); 
        if (k > decade):
            print 10*k," %",jentry
        decade = k  

        counter0 = counter0 + 1

        if tree.HLT_PFJet400_v9 == 1:
            counter1 = counter1 + 1

            h["HLT_PFJet400"].Fill(0.)

        
    print "Initial ", counter0
    print "Passed PFJet400 ", counter1
    

    ###   done with event loop
    outf.cd()
    outf.Write();
    outf.Close();
