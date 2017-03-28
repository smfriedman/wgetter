import sys, getopt
import os

def getArgs(argv):
	helpMessage = 'downloader.py -i <input csv>'
	clargs = {}

	try:
		opts, args = getopt.getopt(argv,"hi:",[])
	except getopt.GetoptError:
		print helpMessage
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			print helpMessage
			sys.exit()
		elif opt == '-i':
			if os.path.splitext(arg)[1] != ".csv":
				print helpMessage
				sys.exit(1)
			else:
				clargs['inputFile'] = arg

	if 'inputFile' not in clargs:
		print helpMessage
		sys.exit(1)

	return clargs