import os
import glob

tagfs_linkmap = {}
occupancy_map = {}

class Tagger():
	def __init__(self, root):
		linkmap = {}

		links = glob.glob(root + "/*/*")

		for link in links:
			(tag_dir, link_name) = os.path.split(link)
			tag = os.path.basename(tag_dir)
			if tag[0] == ".":
				continue

			realpath = os.path.realpath(link)

			if "@" in link_name:
				(filename, sep, link_index)  = link_name.partition("@")
				link_index = int(link_index)
			else:
				filename = link_name
				link_index = 1

			if (filename, tag) in occupancy_map:
				occupancy_map[(filename, tag)] = max(link_index, occupancy_map[(filename, tag)])
			else:
				occupancy_map[(filename, tag)] = link_index

			if realpath not in linkmap:
				linkmap[realpath] = [(tag, realpath)]
			else:
				linkmap[realpath].append((tag, realpath))

		self.linkmap = linkmap
		self.occupancy_map = occupancy_map
		self.root = root

	def update_tags(self, filepath, tags):
		# No need to update tagfs_linkmap, each filepath will only be processed once

		if filepath == "":
			return

		filename = os.path.basename(filepath)

		links = self.linkmap.get(filepath, [])

		old_tags = set([])
		new_links = set([])
		for (tag, realpath) in links:
			if tag not in tags:
				os.remove(link)
				continue
			else:
				old_tags.add(tag)

		for tag in tags - old_tags:
			tag_dir = self.root + "/" + tag
			if not os.path.exists(tag_dir):
				os.mkdir(tag_dir)

			if (filename, tag) in occupancy_map:
				os.symlink(filepath, tag_dir + "/" + filename + "@" + str(self.occupancy_map[(filename, tag)])) 
				self.occupancy_map[(filename, tag)] += 1
			else:
				os.symlink(filepath, tag_dir + "/" + filename)
				self.occupancy_map[(filename, tag)] = 1

		# Just a small precautionary measure
		tagfs_linkmap[filepath] = None


