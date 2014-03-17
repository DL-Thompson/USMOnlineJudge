import os

main_dir = '%s/Desktop/OnlineJudge/' % os.getenv("HOME")
source = main_dir + 'submit/'
dest = main_dir + 'result/'
exCheck = main_dir + 'exCheck/'
permanent = main_dir + 'storage/'


if not os.path.isdir(main_dir):
	os.system('mkdir ' + main_dir)
if not os.path.isdir(source):
	os.system('mkdir ' + source)
if not os.path.isdir(dest):
	os.system('mkdir ' + dest)
if not os.path.isdir(exCheck):
        os.system('mkdir ' + exCheck)
if not os.path.isdir(permanent):
        os.system('mkdir ' + permanent)

os.system('make')
os.system('./compiler_controller -s %s -d %s -e %s -p %s' % (source, dest, exCheck, permanent))