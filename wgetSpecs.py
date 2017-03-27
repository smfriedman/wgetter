def varBuilder(name, description, hasArgs, separator, ignoreName, continueAlt):
	return {
		"name": name,
		"description": description,
		"hasArgs": hasArgs,
		"separator": separator,
		"ignoreName": ignoreName,
		"continueAlt": continueAlt
	}

def basicVarBuilder(name, description, hasArgs, separator):
	return varBuilder(name, description, hasArgs, separator, False, None)

# add?
#	nd
#	regex
#	accept (file exts)
wgetVars = {
	'ignore': ["start", "finish", "startHash", "finishHash"],

	"url": varBuilder("url", "thing to wget", True, "", True, None),

	#recursion
	"-r": basicVarBuilder("-r", "recusion flag", False, ""),
	"-l": basicVarBuilder("-l", "levels of depth for recursion", True, " "),

	#local output
	"-P": basicVarBuilder("-P", "destination directory", True, " "),
	"-o": varBuilder("-o", "output file", True, " ", False, "-a"),
	"-nv": basicVarBuilder("-nv", "nonverbose (light output)", False, ""),

	"-e robots=off": basicVarBuilder("-e robots=off", "ignore robots.txt, cover everything", False, ""),

	#local directory handling
	"-nH": basicVarBuilder("-nH", "no host directory - google.com/xyz -> xyz", False, ""),
	"-nd": basicVarBuilder("-nd", "no directories - all files saved to same in same dir without clobbering", False, ""),
	"-x": basicVarBuilder("-x", "force directories (flat dir structure)", False, ""),

	#style
	"-p": basicVarBuilder("-p", "preserve style resources", False, ""),
	"-E": basicVarBuilder("-E", "convert extions to html - make viewing easier", False, ""),
	"-k": basicVarBuilder("-k", "convert links to local - make viewing easier", False, ""),
	"-K": basicVarBuilder("-K", "back up originals modified by -k", False, ""),

	#host spanning
	"-H": basicVarBuilder("-H", "span hosts", False, ""),
	"--follow-ftp": basicVarBuilder("--follow-ftp", "get links to FTP not just HTTP/HTTPS", False, ""),
	"-D": basicVarBuilder("-D", "allowed domains", True, "")
}