# PAM interface in python, launches compare.py

# Import required modules
import subprocess
import sys
import os
import glob

# pam-python is running python 2, so we use the old module here
import ConfigParser

# Read config from disk
config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/config.ini")


def doAuth(pamh):
	"""Starts authentication in a seperate process"""
	print('called third eye')
	# Abort if third_eye is disabled
	if config.getboolean("core", "disabled"):
		sys.exit(0)


	pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, "Attemptinga face detection"))

	# Run compare as python3 subprocess to circumvent python version and import issues
	status = subprocess.call(["/usr/bin/python3", os.path.dirname(os.path.abspath(__file__)) + "/new_compare.py", pamh.get_user()])

	# Status 12 means we aborted
	if status == 12:
		return pamh.PAM_AUTH_ERR
	# Status 0 is a successful exit
	elif status == 0:
		# Show the success message if it isn't suppressed
		pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, "Identified face as " + pamh.get_user()))
		return pamh.PAM_SUCCESS
	#unknown err
	return pamh.PAM_SYSTEM_ERR


def pam_sm_authenticate(pamh, flags, args):
	#main function called by pam
	return doAuth(pamh)


def pam_sm_open_session(pamh, flags, args):
	#for su
	return doAuth(pamh)


def pam_sm_close_session(pamh, flags, argv):
	return pamh.PAM_SUCCESS


def pam_sm_setcred(pamh, flags, argv):
	return pamh.PAM_SUCCESS
