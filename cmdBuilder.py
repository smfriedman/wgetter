import subprocess
from wgetSpecs import wgetVars
import datetime
import os


def timestamp():
	return str(datetime.datetime.now())

# caution: race condition
# http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
# TODO handle OSError, or update python to 3.2+ to allow for exist_ok
def check_dirs(path):
	if not os.path.exists(path):
		os.makedirs(path)#, exist_ok=True)

STDOUT = open("output/output.log", "a")
STDERR = open("output/error.log", "a")
COMMANDS = open("output/commands.log", "a")

def execute(cmd):
	COMMANDS.write("\n" + timestamp() + "\t" + cmd + "\n")
	#STDOUT.write("\n" + timestamp() + "\t" + cmd + "\n")
	STDERR.write("\n" + timestamp() + "\t" + cmd + "\n")
	subprocess.call(cmd, shell=True, stderr=STDERR) #stdin=subprocess.PIPE, stdout=STDOUT,
	#subprocess.check_call(cmd, shell=True, stderr=STDERR) #stdin=subprocess.PIPE, stdout=STDOUT,
	#subprocess.Popen(cmd, shell=True, stderr=STDERR) #stdin=subprocess.PIPE, stdout=STDOUT,

def wgetCmd(row):
	check_dirs(row[" -P"])
	check_dirs(os.path.dirname(row[" -o"]))

	cmd = "wget "
	cont = (row["start"] != "")
	for key in row:
		if(key not in wgetVars['ignore'] and row[key] != ""):
			# need to add space in csv for excel to interpret opening hyphens properly
			varKey = key[1:len(key)]
			wgetVar = wgetVars[varKey]
			cmd += ("" if wgetVar['ignoreName'] else (wgetVar['continueAlt']  if (cont and wgetVar['continueAlt'] is not None) else wgetVar['name']))
			cmd	+=  (wgetVar['separator'] + row[key] if wgetVar['hasArgs'] else "")
			cmd +=  " "
	if(cont):
		cmd += "-c"
	return cmd

#TODO 
#	handle indiv files better
#	hash files extension
def singleHashCmd(row, hashFunc):
	src = os.path.normpath(row[" -P"] if row[" -P"] is not None else row[" url"])
	dest_dir = src + "_meta/"
	check_dirs(dest_dir)
	src_base = os.path.basename(src)
	dest = dest_dir + src_base + hashFunc + "." + hashFunc
	cmd = "hashdeep -rl -c " + hashFunc + " " + src + " > " + dest
	return cmd

def hashCmd(row):
	return singleHashCmd(row, "md5") + " & " + singleHashCmd(row, "sha256")

def wget(row):
	print "starting download of %s" % (row[' url'])
	cmd = wgetCmd(row)
	execute(cmd)
	return

def hashdeep(row):
	print "starting hashes of %s" % (row[' url'])
	cmd = hashCmd(row)
	execute(cmd)	
	return