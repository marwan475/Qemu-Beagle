#!/usr/bin/python

'''apport hook for dhclient

(c) 2010 Canonical Ltd.
Author: Chuck Short <chuck.short@canonical.com>

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
the full text of the license.
'''

from apport.hookutils import *
from os import path
import re

def dhcp_leases(pattern):
	''' Extract options from '/var/lib/dhcp/dhclient.leases' which match a regex.
	   pattern should be a "re" object. '''
	lines = ""
	if os.path.exists('/var/lib/dhcp/dhclient.leases'):
		file = '/var/lib/dhcp/dhclient.leases'
	else:
		return lines

	for line in open(file):
		if pattern.search(line):
			lines += line
	return lines
 
def recent_kernlog(pattern):
	'''Extract recent messages from kern.log or message which match a regex.
	   pattern should be a "re" object.  '''
	lines = ''
	if os.path.exists('/var/log/kern.log'):
		file = '/var/log/kern.log'
	elif os.path.exists('/var/log/messages'):
		file = '/var/log/messages'
	else:
		return lines

	for line in open(file):
		if pattern.search(line):
			lines += line
	return lines

def recent_auditlog(pattern):
	'''Extract recent messages from kern.log or message which match a regex.
	   pattern should be a "re" object.  '''
	lines = ''
	if os.path.exists('/var/log/audit/audit.log'):
		file = '/var/log/audit/audit.log'
	else:
		return lines

	for line in open(file):
		if pattern.search(line):
			lines += line
	return lines

def add_info(report, ui):
	response = ui.yesno("The contents of your /etc/dhcp/dhclient.conf file may help developers diagnose your bug more quickly, however, it may contain sensitive information. Do you want to include it in your bug report?")

	if response == None: #user cancelled
		raise StopIteration

	elif response == True:
		attach_file_if_exists(report, '/etc/dhcp/dhclient.conf', 'Dhclient')

		# get apparmor stuff, copied from libvirt-bin.py
		# runs hooks via attach_related packages
		attach_file(report, '/proc/version_signature', 'ProcVersionSignature')
		attach_file(report, '/proc/cmdline', 'ProcCmdLine')

		attach_related_packages(report, ['apparmor', 'libapparmor1',
			'libapparmor-perl', 'apparmor-utils', 'auditd', 'libaudit0'])

		sec_re = re.compile('audit\(|apparmor|selinux|security', re.IGNORECASE)
		report['KernLog'] = recent_kernlog(sec_re)

		attach_file(report, '/etc/apparmor.d/sbin.dhclient')

		if os.path.exists("/var/log/audit"):
			# this needs to be run as root
			report['AuditLog'] = recent_auditlog(sec_re)
		
		leases = re.compile('option|renew|rebind|expire', re.IGNORECASE)
		report['DhclientLeases'] = dhcp_leases(leases)
