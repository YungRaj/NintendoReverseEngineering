import sys, os, subprocess

path = sys.argv[1]
outpath = sys.argv[2]
dumppath = sys.argv[3]

if not os.path.exists(outpath):
	os.makedirs(outpath)

if not os.path.exists(dumppath):
	os.makedirs(dumppath)

for dirpath, dirnames, filenames in os.walk(path):

	for filename in filenames:

		p = subprocess.Popen('./hactool -k ./prod.keys %s --plaintext=%s' %(dirpath + '/' + filename, outpath + '/' + filename), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		stdout, stderr = p.communicate()

		rc = p.returncode

		print(stdout);

		to_match = ['0100000000000819', '010000000000081A', '010000000000081B', '010000000000081C']

		if(any(x in stdout for x in to_match)):
			
			if rc == 0:
				print(stdout)
			else:
				print(stderr);

			print('\n')

		found = False

		title_id = ''
		partition_type = ''

		for line in stdout.split('\n'):

			to_find = 'Title ID:'

			if to_find in line:
				title_id = line.strip().split(to_find)[1].strip()

			to_find = 'Partition Type:'

			if to_find in line:
				partition_type = line.strip().split(to_find)[1].strip().lower()

			if title_id and partition_type:

				dump = dumppath + '/' + title_id

				if not os.path.exists(dump):
					os.makedirs(dump)

				p = subprocess.Popen('./hactool -x %s --%sdir=%s' %(outpath + '/' + filename, partition_type, dump), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

				dump_stdout, dump_stderr = p.communicate()

				print(dump_stdout)

				dump_rc = p.returncode

				found = True

				break

		if not found:
			print('Error!\n')
			print('Could not find title id and partition type \n')
			print('hactool output =\n')

			if rc == 0:
				print(stdout)
			else:
				print(stderr);

			print('\n')
				


for dirpath, dirnames, filenames in os.walk(outpath):

	for filename in filenames:

		p = subprocess.Popen('./hactool -i %s' %(dirpath + '/' + filename), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		stdout, stderr = p.communicate()

		print(stdout)

		rc = p.returncode