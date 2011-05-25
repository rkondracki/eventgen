'''
Copyright (C) 2005-2011 Splunk Inc. All Rights Reserved.
'''
from time import gmtime, strftime
import datetime
import hashlib
import random
import string

## sample event
## Mar 05 2010 19:51:21 app=splunkd dest_dns=* dest_port=8089 pid=40257 user=markmorow fd=3u ip_version=4 dvc_id=0x075666e0 transport=TCP

count = 0
iterations = 20
## 1440 represents 24 hour offset
offset = 1440

## array of "port" values
apps = ['sshd','httpd','ntpd','cupsd']
protocols = ['TCP','TCP','TCP','UDP']
ports = ['22','443','123','631']

## get the current date and time
nowTime = datetime.datetime.now()

randDelta = 0

###### Simulate Random Disk Utilization
while count < iterations:

	## create deltaTime
	deltaTime = datetime.timedelta(minutes=randDelta)
	
	## compute time delta
	deltaTime = nowTime - deltaTime
	
	tempPorts = []
	
	for x in range(0,len(ports)):
		tempPort = ''
		event = '@@date app=@@app dest_dns=* dest_port=@@src_port pid=@@pid user=root fd=4u ip_version=4 dvc_id=0x@@dvc_id transport=@@transport'

		event = event.replace('@@date', deltaTime.strftime('%b %d %Y %H:%M:%S'))
		event = event.replace('@@app', apps[x])
		tempPort += apps[x]
		tempPort += '*'
		event = event.replace('@@src_port', ports[x])
		tempPort += ports[x]
		event = event.replace('@@pid', str(random.randint(0,65535)))
		event = event.replace('@@dvc_id', str(random.randint(0,99999999)))
		event = event.replace('@@transport', protocols[x])
		tempPort += protocols[x]
	
		print event
		tempPorts.append(tempPort)
		
	count += 1
	randDelta += offset / iterations
		
	if tempPorts:
		netstat = string.join(tempPorts, '')
		netstat_hash = hashlib.sha1(netstat).hexdigest()
	
		print deltaTime.strftime('%b %d %Y %H:%M:%S') + ' file_hash=' + netstat_hash
