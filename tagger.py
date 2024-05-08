import os

transaction = ""

def update_tags(filepath, tags):
	global transaction

	if filepath == "":
		return

	transaction += f"tmsu untag '{filepath}' $(tmsu tags) > /dev/null 2>&1 \n"

	tags = list(tags)
	if tags != []:
		transaction += f"tmsu tag --tags {' '.join(tags)} '{filepath}' \n"

	return

def commit():
	global transaction

	print(transaction)
	os.system(transaction)

