# 3y3
Third eye, a dynamic facial recognition app used to switch/ lock/ autologin users based on real time face recognition.

Instructions to install: 

- Clone the repository into /lib/security folder as a root
- copy the pam-config/third_eye file into /usr/share/pam-config folder
- include third eye as a mode for authentication for common auth in /etc/pam.d/common-auth by adding the line
  auth   [success=2 default=ignore]        pam_python.so /lib/security/third_eye/pam.py
- To add new users use the python script 'new_user.py [name of the account]'

Notes:
- More updates to come in the future.
- Inspired by the howdy project by boltgolt.
