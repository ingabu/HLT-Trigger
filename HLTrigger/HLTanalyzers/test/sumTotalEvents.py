### place and run in each Pt directory ###

import glob, os

currDir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

totalEventList = []
fList = glob.glob('*.stdout')

if fList != []:
	for f in fList:
		fileObj = open(f,'r')
		for line in fileObj:
			if line.count('Events total') != 0:		# find line containing
													# 	'Events total'
				totalEventList.append(int(line.split()[4]))	# add total to list

print ' total events' 
print '--------------------'	
print ' ' + currDir.split('_')[1], sum(totalEventList)
print '--------------------'	
