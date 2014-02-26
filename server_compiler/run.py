import os

#main_dir = '/home/lucas/Desktop/OnlineJudge/'
main_dir = '%s/Desktop/OnlineJudge/' % os.getenv("HOME")
source = main_dir + 'submit/'
dest = main_dir + 'result/'

if not os.path.isdir(main_dir):
	os.system('mkdir ' + main_dir)
if not os.path.isdir(source):
	os.system('mkdir ' + source)
if not os.path.isdir(dest):
	os.system('mkdir ' + dest)

os.system('make')
os.system('./compiler_controller -s %s -d %s' % (source, dest))