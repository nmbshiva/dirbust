#!/bin/env python

# python dirbuster because #javasux! and owasp dirbuster is clunky

import requests
import os
import sys
import time

bannertxt = '\nPython dirbuster by @numbshiva\n' \
			'Takes positional argument for starting url - eg. ' + sys.argv[0] + ' <target url> <wordlist>\n' \
			'Requires dir_list.txt in same directory.\n' \
			'Prints results to stdout, also writes to log file.\n' \
			'\nHappy bug hunting!\n\n'

helptxt = '\nOne or more arguments are missing.\n' \
		  'Usage: {0} <url> <wordlist>\n'.format(sys.argv[0])

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
log = open('log.txt', 'w')

class color:
	red = '\033[91m'
	yellow = '\033[93m'
	green = '\033[94m'
	end = '\033[0m'

try:
	wordlist = open(sys.argv[2],'r')
	print "\n[+] Opened {0} as wordlist.".format(sys.argv[2])
except:
	print color.red + '\n[!] Error! Missing wordlist argument.' + color.end
	print helptxt
	sys.exit(0)

try:
	base_url = sys.argv[1]
	if not base_url.lower().startswith(('http://','https://')):
		base_url = 'https://{0}'.format(sys.argv[1])
		print "[+] URL set to {0}\n".format(base_url)
except:
	print color.red + '\n[!] ERROR! Missing URL argument.' + color.end
	print helptxt
	sys.exit(0)

while True:
	word = wordlist.readline()
	word = word.rstrip()
	if not word:
		print color.green + "\n[!] End of wordlist reached.\n[+] Log file written. Exiting.\n" + color.end
		wordlist.close()
		log.close()
		sys.exit(0)
	
	fetch_url = base_url + '/' + word
	print '[*] Trying: {0}'.format(fetch_url)
	result = requests.get(fetch_url, headers=headers)
	
	# optional sleep so you don't smash a website. useful if they don't like automated crawlers
	# time.sleep(1)
	
	if not result.status_code == 404:
		print color.yellow + '[+] Directory found: {0} with status code {1}'.format(fetch_url, result.status_code) + color.end
		log.write('Directory found: ' + fetch_url + ' status: ' + str(result.status_code) + '\n')


wordlist.close()
log.close()