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

wgetVars = {
	'ignore': ["start", "finish", "startHash", "finishHash"],

	"url": varBuilder("url", "thing to wget", True, "", True, None),

	#recursion
	"-r": basicVarBuilder("-r", "recusion flag", False, ""),
	"-l": basicVarBuilder("-l", "levels of depth for recursion", True, " "),
	"-np": basicVarBuilder("-np", "no parent - x.com/y/z -> won't include x.com in recursion ", False, ""),

	#local output
	"-P": basicVarBuilder("-P", "destination directory", True, " "),
	"-o": varBuilder("-o", "output file", True, " ", False, "-a"),
	"-nv": basicVarBuilder("-nv", "nonverbose (light output)", False, ""),

	"-e robots=off": basicVarBuilder("-e robots=off", "ignore robots.txt, cover everything", False, ""),

	#local directory handling
	"-nH": basicVarBuilder("-nH", "no host directory - x.com/y -> y", False, ""),
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
	"-D": basicVarBuilder("-D", "list of allowed domains to span", True, " "),
	"--exclude-domains": basicVarBuilder("--exclude-domains", "list of disallowed domains to span", True, " "),
	"-A": basicVarBuilder("-A", "accept list - only accept these file names or suffix patterns", True, " "),
	"-R": basicVarBuilder("-R", "reject list - reject these file names or suffix patterns", True, " "),
	"--ignoreCase": basicVarBuilder("--ignore-case", "ignore case - affects -R, -A, etc. '.TXT' == '.txt'", True, " "),
	"--accept-regex": basicVarBuilder("--accept-regex", "accept only urls that match this regex", True, " "),
	"--reject-regex": basicVarBuilder("--reject-regex", "reject urls that match this regex", True, " ")
}