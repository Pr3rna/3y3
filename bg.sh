#!/bin/bash

current_user=$SUDO_USER
echo $current_user
while true
do
    sudo python3 detection.py
    line=$(sudo head -1 ./test.txt)
    echo $line
    if [ $line = $current_user ]
    then
	# enables the keyboard and the mouse if the correct user is present
	xinput set-int-prop 16 "Device Enabled" 8 1
	xinput set-int-prop 3 "Device Enabled" 8 1
    fi
    if [ $line = "unknown" ]
    then
        xinput set-int-prop 16 "Device Enabled" 8 0 #this disables the touchpad
        #xinput set-int-prop 3 "Device Enabled" 8 0  #disable the keyboard if you are daring enough !
    else
        if [ $line != $current_user ]
        then
            dm-tool switch-to-user $detected_user
            exit 0
        fi
    fi
    sleep 5
done
