import csv
from tempfile import NamedTemporaryFile
import shutil
import datetime
import sys, os

from cmdBuilder import wget, hashdeep, timestamp, check_dirs
from argReader import getArgs

currentRow = {}
finishedUrls = []

def main(reader, writer, STDERR, COMMANDS):
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
				COMMANDS.write("\nStarting hashes of " + currentRow[' url'] + " at " + timestamp() + "\n")
				hashdeep(currentRow, STDERR, COMMANDS)
				currentRow['finishHash'] = timestamp()
				COMMANDS.write("\nFinished hashes of " + currentRow[' url'] + " at " + timestamp() + "\n")
		else:
			if currentRow['start'] == "":
				currentRow['start'] = timestamp()
				COMMANDS.write("\nStarting download of " + currentRow[' url'] + " at " + timestamp() + "\n")
			else:
				COMMANDS.write("\nResuming download of " + currentRow[' url'] + " at " + timestamp() + "\n")
			wget(row, STDERR, COMMANDS)
			currentRow['finish'] = timestamp()
			currentRow['startHash'] = timestamp()
			COMMANDS.write("\nStarting hashes of " + currentRow[' url'] + " at " + timestamp() + "\n")
			hashdeep(row, STDERR, COMMANDS)
			currentRow['finishHash'] = timestamp()
			COMMANDS.write("\nFinished hashes of " + currentRow[' url'] + " at " + timestamp() + "\n")

		finishedUrls.append(currentRow[' url'])
		writer.writerow(row)	

	shutil.move(tempfile.name, filename)

def handle(reader, writer, STDERR, COMMANDS):
	COMMANDS.write("\nINTERRUPTED AT " + timestamp() + "\n")

	global currentRow
	global finishedUrls

	writer.writerow(currentRow)
	for row in reader:
		if row[' url'] not in finishedUrls and row[' url'] is not currentRow[' url']:
			writer.writerow(row)
	
	shutil.move(tempfile.name, filename)

#this (http://stackoverflow.com/questions/26378988/how-to-correctly-handle-sigint-to-close-files-connections)
#or signal.signal ? (http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python)
if __name__ == "__main__":	

	args = getArgs(sys.argv[1:])
	filename = args['inputFile']
	noext = os.path.basename(os.path.splitext(filename)[0])
	tempfile = NamedTemporaryFile(delete=False)

	check_dirs("output/" + noext)
	STDERR = open("output/" + noext + "/error.log", "a")
	COMMANDS = open("output/" + noext + "/commands.log", "a")

	with open(filename, 'rbU') as csvFile, tempfile:

		reader = csv.DictReader(csvFile)
		writer = csv.DictWriter(tempfile, fieldnames=reader.fieldnames)
		writer.writeheader()

		try:
			main(reader, writer, STDERR, COMMANDS)
		except KeyboardInterrupt:
			handle(reader, writer, STDERR, COMMANDS)