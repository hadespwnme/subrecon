try:
	import platform
	import subprocess
	import os
	import distro
	import time
except ImportError as error:
	print("\n\t   [!] Error on import", error)

dist = distro.id()

#warna
red = "\x1B[31m"
green = "\x1B[32m"
cyan = "\e[36m"
bold = "\33[1m"
nc="\033[1;37m"
yellow="\033[1;33m"

#cek tool
def cek(i):
	if os.path.exists("/usr/bin/" + i) == True:
		print(green + bold + "[*] " + i +  " exist")
		time.sleep(0.2)

	elif os.path.exists("/usr/bin/" + i) == False:
		print(red + '[!] Please Install '+ green + i + red + " first"+ nc)
		print(red + bold + "[+] Your Distro is: "+ nc + dist)
		print('''
			1) Arch Based
			2) Debian Based
			3) Red Hat Based (RHEL)
		''')
		pil = input(green + '[+]Input your distro based: '+ nc)
		if pil == "1":
			os.system("sudo pacman -Syu " + i)
		elif pil == "2":
			os.system("sudo apt install -y "+ i)
		elif pil == "3":
			os.system("sudo dnf install "+ i)
		else:
			print(red + "[!] Choose your distro based please...")
			cek(i)

list = ['wafw00f','subfinder', 'httprobe']
for i in list:
    cek(i)
    pass

#input target
target = input(red + '\n[+]Enter your target: '+ nc)
os.system('clear')

#cek web aplication firewall
def waf():

	#convert domain pake httprobe
	get_host   = subprocess.check_output(("echo %s | httprobe -prefer-https" % target), shell=True, text=True)
	detect_waf = subprocess.check_output(("wafw00f %s > /dev/null" % get_host), shell=True, text=True)

	if ("is behind" in detect_waf):
		##cek beberapa WAF
		processed_string = detect_waf[detect_waf.find("is behind"):]
		pre_parser  = processed_string.find("\x1b[1;96m") #cuma ambil hasil
		post_parser = processed_string.find("\x1b[0m")
		which_waf   = processed_string[pre_parser:post_parser] #jngan kasih code warna

		print(green + "\n\t->[INF] WAF: DETECTED [ %s ]" % which_waf + nc)

	elif ("No WAF detected" in detect_waf):
		print(red + "\n ->[WRN] WAF: NOT DETECTED"+ nc)
	else:
		print(red + "\n\t ->[!] FAIL TO DETECT WAF" + nc)

#scan subdomain
def scan_subdo():
	#scan
	os.system('subfinder -d ' + target + ' -o .subdo.txt -silent > /dev/null')

	#baca file
	with open('.subdo.txt', encoding="utf-8") as file:
		daftar_subdo = file.read().splitlines()

	print(green+ "\t->[INF] Success: %s" % len(daftar_subdo) + nc)

	#tampilkan
	for f in daftar_subdo:
		print('\t |-> ' + f)
	
	os.system('rm -rf .subdo.txt')

def menu():
	sistem = platform.uname()
	LOGO = (f'''
	                {red}.YYY555PPPPGGGG?
	                .BBB####&&&&&@@?
	                .GBBB:.....P&&@?
	         .~     .GBBG      5@&@?
	        ^BJ     .GBBG      5@&@?
	       ?B#J     .GBBG      5@&@?   {yellow}| {nc}System    : {green}{sistem.system}{red}
	      !BBBJ     .PGGG      5@&@?   {yellow}| {nc}Node Name : {green}{sistem.node}{red}
	      !BB#J                5@&@?   {yellow}| {nc}Machine   : {green}{sistem.machine}{red}
	      !BB#J     {green}HADES{red}      5@&@?   {yellow}| {nc}Distro    : {green}{dist}
	     {nc} !BB#J        ..      5@&@?
	      !BB#J      #&&&.     5@&@?
	      !BB#J      &&@@.     5@@5
	      !BB#J      &&@&.     P&~
	      !BB#J      &&@&.     !.
	      !BBBY.....:&&@&.
	      !BBB###&&&&&@@@.
	      !YYYY555PPPGGGG.{nc}

	              [{red}+{nc}]{green}SubRecon{nc}[{red}+{nc}]
	''')
	print(LOGO)
	print('''
		  1) Scan WAF Tech
		  2) Scan Subdomain
		  3) All Scan
	''')
	print(yellow + 'Your target is: '+ red + target + nc)
	pil = int(input('hades> '))
	if pil == 1:
		waf()
	elif pil == 2:
		scan_subdo()
	elif pil == 3:
		waf()
		print('\n\n')
		scan_subdo()
	else:
		menu()


menu()