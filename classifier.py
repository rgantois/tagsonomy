from scanner import scan_files
from tagger import update_tags, commit
import fnmatch
import os
import string
import time

def validate_tag(tag: str):
	return tag == "".join([c for c in tag if c in string.ascii_letters + "-_"])

def validate_match(match):
	return match == "".join([c for c in match if c in string.ascii_letters + "-_/ " + "*"])

def parse_rules(rule_file):
	for line in rule_file:
		if ":" not in line:
			continue

		(tag,colon,match) = line.strip("\n").partition(":")

		if not validate_tag(tag):
			print("Invalid tag {tag}!!")
			continue

		yield (tag, match)

def load_rules(root: str):
	rules = []

	with open(f"{root}/.tag_rules", "r") as rule_file:
		for rule in parse_rules(rule_file):
			rules.append(rule)

	return rules

def check_match(filepath, match):
	return fnmatch.filter([filepath], match) != []
	
def check_rule(filepath: dict, match: str):
	if not validate_match(match):
		print(f"Invalid match {match}!")
		return False

	return check_match(filepath, match)

def classify_file(filepath: str, rules: list) -> set:

	tags = set([])

	for (tag, match) in rules:
		if not check_rule(filepath, match):
			continue

		tags.add(tag)

	return tags
			
	
def classify(root: str):
	t0 = time.time()
	nb_files = 0

	rules = load_rules(root)

	for filepath in scan_files(root):
		tags = classify_file(filepath, rules)
		update_tags(filepath, tags)
		nb_files += 1

	commit()

	print(f"Classified {nb_files} files in {time.time() - t0} seconds!")

