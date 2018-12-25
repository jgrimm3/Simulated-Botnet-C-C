import array
import sys
import subprocess

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

READ_SIZE = 100

if len(sys.argv) != 4:
	print "Usage: python ttlmod.py <filename> <char1> <char2>"
	exit()

else:
	# Get file from args
	file = str(sys.argv[1])
	print file

	# Calculate ttl from given characters
	if (len(sys.argv[2]) != 1) or (len(sys.argv[3]) != 1):
		print "Program only accepts one character at a time! Aborting"
		exit()

	char1 = sys.argv[2]
	char2 = sys.argv[3]

	num1 = ord(char1)
	num2 = ord(char2)

	ttl = ((num1 * 256) + num2) * 2
	print(ttl)

	fo = open(file, "r+")
	str = fo.read(READ_SIZE)
	searchstr = "$TTL"

	if(str.find(searchstr)):
		#create new ttl string with cmd line args
		newTTL = '$TTL\t%d\n' % ttl
		replace_line(file, 3, newTTL)
		print 'Successfully updated TTL'
		# Restart bind9 service
		command = 'service bind9 restart'
		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

	else:
		print "Could not find TTL field, aborting"
		exit()

