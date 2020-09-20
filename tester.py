#!/usr/bin/python3
# #######################
#
# This file runs tests for this coding assignment.
# Read the file but do not modify.
#
# #######################
#
# Autograde test.py runner
# Some code taken from test.py from submit
#

import os, sys, subprocess, json, argparse
from subprocess import Popen, PIPE, STDOUT

#####################
# Start Test Utilities
#####################

def preparefile(file):
	# Chown bin so autograde user can execute it
	runcmd('chown autograde:autograde ' + file)

	# Set executable bit
	runcmd('chmod +x ' + file)

def runcmdsafe(binfile):
	# Test as autograde user
	#b_stdout, b_stderr, b_exitcode = runcmd('sudo', '-u', 'autograde' + binfile)
	b_stdout, b_stderr, b_exitcode = runcmd(binfile)
	
	return b_stdout, b_stderr, b_exitcode

def runcmd(cmd):
	executed = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	stdout, stderr = executed.communicate()
	return stdout, stderr, executed.returncode

def assertequals(expected, actual):
	if expected == actual:
		passtest('')
	else:
		failtest(f'Expected {expected} got {actual}')

def failtest(message):
	testmsg('failed', message)
	
def passtest(message):
	testmsg('passed', message)
	
def testmsg(status, message):
	x = {
	  "status": status,
	  "message": message
	}
	print(json.dumps(x))
	sys.exit()
	
#####################
# End Test Utilities
#####################

verbose = False

def runtest(name):
	global verbose
	
	print('---------------------')
	print(f'\nRunning test: {name}')
	try:
		python_bin = sys.executable
		output = subprocess.check_output(f'{python_bin} driver.py', cwd=f'test/{name}', shell=True, timeout=15)
		y = json.loads(output)
		status = y["status"]
		message = y["message"]
		stdout = output
		
		if verbose and len(message) > 0:
			print("\n\nSTDOUT: ")
			print(message)
		
		if status == "timeout":
			print(' 	TIMED OUT')
			return False
		if status == "failed":
			print('		FAILED')
			return False
		if status == "passed":
			print(' 	PASSED')
			return True
		
	except:
		print(' 	TIMED OUT')
		return False


def runtests():
	tests = listtests()
	num_passed = 0

	for test in tests:
		if runtest(test):
			num_passed += 1
	
	print('\n===========================')
	print(f'Summary: {num_passed} / {len(tests)} tests passed')
	print('===========================')
		
def listtests():
	tests = [test for test in os.listdir("test/")]
	tests.sort()
	return tests

def main():
	global verbose
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--list', '-l', help='List available tests', action='store_true')
	parser.add_argument("--all", "-a", help='Perform all tests', action='store_true')
	parser.add_argument('--verbose', '-v', help='View test stdout, verbose output', action='store_true')
	parser.add_argument('--test', '-t', help='Perform a specific testname (case sensitive)')
	args = parser.parse_args()

	if args.verbose:
		verbose = True

	if args.all:
		runtests()
		return
		
	if args.test:
		if not os.path.exists(f'test/{args.test}'):
			print(f'Test "{args.test}" not found')
			return

		runtest(args.test)
		return
		
	if args.list:
		print("Available tests: ")
		print(*listtests(), sep='\n')
		return
		
	parser.print_help()

if __name__ == "__main__": main()
