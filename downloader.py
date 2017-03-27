import csv
from tempfile import NamedTemporaryFile
import shutil
import datetime
#import signal
import sys, getopt

from cmdBuilder import wget, hashdeep

def timestamp():
	return str(datetime.datetime.now())

#export to its own file?
def getArgs():
	helpMessage = 'downloader.py -i <input csv>'
	clargs = {}

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:",[])
	except getopt.GetoptError:
		print helpMessage
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			print helpMessage
			sys.exit()
		elif opt == '-i':
			clargs['inputFile'] = arg

	if 'inputFile' not in clargs:
		print helpMessage
		sys.exit(1)

	return clargs

#http://stackoverflow.com/questions/16020858/inline-csv-file-editing-with-python
#filename = 'input/test1.csv' #get from cmd line
args = getArgs()
filename = args['inputFile']
tempfile = NamedTemporaryFile(delete=False)

currentRow = {}
finishedUrls = []

#scope: http://stackoverflow.com/questions/291978/short-description-of-python-scoping-rules
def main(reader, writer):
	global currentRow
	global finishedUrls

	for row in reader:
		currentRow = row
		if currentRow["finish"] != "":
			print "already downloaded %s" % (currentRow[' url'])
			if currentRow["finishHash"] != "":
				print "already created hashes for %s" % (currentRow[' url'])
			else:
				currentRow['startHash'] = timestamp()
				hashdeep(currentRow)
				currentRow['finishHash'] = timestamp()
		else:
			if currentRow['start'] == "":
				currentRow['start'] = timestamp()
			wget(row)
			currentRow['finish'] = timestamp()
			currentRow['startHash'] = timestamp()
			hashdeep(row)
			currentRow['finishHash'] = timestamp()

		finishedUrls.append(currentRow[' url'])
		writer.writerow(row)	

	shutil.move(tempfile.name, filename)

def handle(reader, writer):
	global currentRow
	global finishedUrls

	writer.writerow(currentRow)
	for row in reader:
		print row
		if row[' url'] not in finishedUrls and row[' url'] is not currentRow[' url']:
			writer.writerow(row)
	
	shutil.move(tempfile.name, filename)

#this (http://stackoverflow.com/questions/26378988/how-to-correctly-handle-sigint-to-close-files-connections)
#or signal.signal ? (http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python)
if __name__ == "__main__":	
	with open(filename, 'rbU') as csvFile, tempfile:

		reader = csv.DictReader(csvFile)
		writer = csv.DictWriter(tempfile, fieldnames=reader.fieldnames)
		writer.writeheader()

		try:
			main(reader, writer)
		except KeyboardInterrupt:
			handle(reader, writer)









# with open('test.csv', 'rU') as csvfile:
# 	reader = csv.DictReader(csvfile)
# 	for row in reader:
# 		if(row["finish"] != ""):
# 			print "already downloaded %s" % (row[' url'])
# 			if(row["finishHash"] != ""):
# 				print "already created hashes for %s" % (row[' url'])
# 			else:
# 				hashdeep(row)
# 		else:
# 			wget(row)