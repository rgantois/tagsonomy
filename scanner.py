import os

def stasis_score(filepath: str):
	return 100

def reachability_score(filepath: str):
	if "/." in filepath:
		return 0
		
	return 100

def scan_files(scan_root, tagfs_root):
	for (dirpath, dirnames, filenames) in os.walk(scan_root):

		if os.path.commonprefix([dirpath, tagfs_root]) == tagfs_root:
			continue

		for filename in filenames:
			filepath = os.path.join(dirpath, filename)

			if stasis_score(filepath) < 0.5:
				continue
			
			if reachability_score(filepath) < 0.5:
				continue

			if "@" in filename:
				continue

			yield filepath

