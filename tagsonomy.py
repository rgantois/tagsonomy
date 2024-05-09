from classifier import classify
import daemon
from daemon import pidfile
import time
import os
import sys
import lockfile

tagsonomy_pidfile = pidfile.PIDLockFile(os.path.expanduser("~/t/.tagsonomy.pid"))

context = daemon.DaemonContext(
	pidfile=tagsonomy_pidfile,
	detach_process=True,
)

def tagsonomy_loop():
	scan_root = os.path.expanduser("~")
	tagfs_root = scan_root + "/t"
	interval = 360
	while True:
		for dirname in os.listdir(scan_root):
			classify(scan_root + "/" + dirname, tagfs_root)
			time.sleep(interval)

try:
	context.open()
except lockfile.AlreadyLocked as exc:
	print("Could not get tagsonomy lockfile!")
	sys.exit(1)

tagsonomy_loop()

context.close()

