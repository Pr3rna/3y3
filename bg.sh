#!/bin/bash
#cd /lib/security/third_eye/
export XDG_SEAT_PATH="/org/freedesktop/DisplayManager/Seat0"

current_user=$SUDO_USER
echo 'current user is '$current_user
while true
do
    sudo python3 /lib/security/third_eye/detection.py
    line=$(sudo head -1 /lib/security/third_eye/test.txt)
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
            echo -e '[greeter]\nlast-user'$line > /var/lib/lightdm/.cache/unity-greeter/state
            #bash -c 'dm-tool switch-to-greeter;$SHELL'
            dm-tool switch-to-user $line
	    exit 0
        fi
    fi
    sleep 5
done
