# This file uploads PROS projects to the 8 slots on the V5 Microcontroller
# import necessary modules
import subprocess
import time
import argparse

# function to execute command line arguments
def execute(cmd):
	# run command
	popen = subprocess.Popen(cmd, cwd="./114/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	popen.wait()
	
	# check return code
	if popen.returncode:
		raise subprocess.CalledProcessError(popen.returncode, cmd)

parser = argparse.ArgumentParser()
parser.add_argument("auton", help="enter the auton number", type=int, default=-1, nargs="?")
args = parser.parse_args()

# Step 1: Declare Auton Programs
# These set the different upload types
auton_programs = [
	"red_front();",
	"red_front_park();",
	"red_front_elim();",
	"red_back();",
	"blue_front();",
	"blue_front_park();",
	"blue_front_elim();",
	"blue_back();"
]

# Corresponding Names
auton_names = [
	"Red Front",
	"Red Front Park",
	"Red Front Elim",
	"Red Back Park",
	"Blue Front",
	"Blue Front Park",
	"Blue Front Elim",
	"Blue Back Park"
]

# Grab start time
start = time.time()

# if running full script
if(args.auton == -1):
	# Step 2: Create Copies of autonomous.cpp file
	for i, x in enumerate(auton_programs):
		# only run changes after first project uploaded (will always be reset)
		if i != 0:
			# open autonomous file
			s = open("114/src/autonomous.cpp").read()
			
			# replace previous auton call with current one
			s = s.replace(auton_programs[i-1], x)
			
			# write changes
			f = open("114/src/autonomous.cpp", 'w')
			f.write(s)
			f.close()
			
		# change project.pros file to update project name
		with open('114/project.pros') as file:
			# read a list of lines into data
			data = file.readlines()
		
		# update name line
		data[3] = "        \"project_name\": \"%s\",\n" % auton_names[i]
		
		# write changes to file
		with open('114/project.pros', 'w') as file:
			file.writelines(data)
			
		# Build project
		print("[INFO] Building %s" % x)
		execute(["prosv5", "make"])
		time.sleep(1) # delay to ensure it always builds
		
		# Upload project to correct slot
		print("[INFO] Uploading %s to slot %d" % (x, i+1))
		execute(["prosv5", "upload", "--slot", str(i+1)])
		time.sleep(1) # delay to ensure correct upload

		# Step 3: Reset autonomous.cpp file
		s = open("114/src/autonomous.cpp").read()
		s = s.replace(auton_programs[len(auton_programs)-1], auton_programs[0])
		f = open("114/src/autonomous.cpp", 'w')
		f.write(s)
		f.close()

# else if running a single auton build
else:
	# only run changes after first project uploaded (will always be reset)
	if args.auton != 1:
		# open autonomous file
		s = open("114/src/autonomous.cpp").read()
		
		# replace previous auton call with current one
		s = s.replace(auton_programs[0], auton_programs[args.auton-1])
		
		# write changes
		f = open("114/src/autonomous.cpp", 'w')
		f.write(s)
		f.close()
		
	# change project.pros file to update project name
	with open('114/project.pros') as file:
		# read a list of lines into data
		data = file.readlines()
	
	# update name line
	data[3] = "        \"project_name\": \"%s\",\n" % auton_names[args.auton-1]
	
	# write changes to file
	with open('114/project.pros', 'w') as file:
		file.writelines(data)
		
	# Build project
	print("[INFO] Building %s" % auton_programs[args.auton-1])
	execute(["prosv5", "make"])
	time.sleep(1) # delay to ensure it always builds
	
	# Upload project to correct slot
	print("[INFO] Uploading %s to slot %d" % (auton_programs[args.auton-1], args.auton))
	execute(["prosv5", "upload", "--slot", str(args.auton)])
	time.sleep(1) # delay to ensure correct upload

	# Step 3: Reset autonomous.cpp file
	s = open("114/src/autonomous.cpp").read()
	s = s.replace(auton_programs[args.auton - 1], auton_programs[0])
	f = open("114/src/autonomous.cpp", 'w')
	f.write(s)
	f.close()

# Output result
print("[INFO] Upload Successful in %0.2fs" % (time.time()-start))