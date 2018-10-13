# ImageRecognition
Image recognition project built in python using OpenCV.

------------------------------------------------------------------------
**Environment install instructions**

*Install Rasbian*

*Update*
```
sudo apt-get update
```
*Install video module*

*Check video module*
```
	sudo raspi-config
		Interfacing Options => P1 Camera => Enable
		Advanced Options => Memory Split => 144mb
	raspistill -o cam.jpg
```
*Install dlib*
```
instruction based on : 
https://www.pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/
if there is ever an issue might be worth checking :
https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/
	Update swap file size
		sudo nano /etc/dphys-swapfile
		CONF_SWAPSIZE=1024
		sudo /etc/init.d/dphys-swapfile stop
		sudo /etc/init.d/dphys-swapfile start
		free -m
	Update boot options and memory split
		sudo raspi-config
			Boot Options => Desktop / CLI => Console Autologin
			Advanced Options => Memory Split => 16mb
	Reboot to console
	Install dlib prerequisites
		sudo apt-get update
		sudo apt-get install build-essential cmake
		sudo apt-get install libgtk-3-dev
		sudo apt-get install libboost-all-dev
		verify pip is installed (pip)
		#if pip returns error regarding main use python -m pip
		python -m pip install numpy
		python -m pip install scipy
		python -m pip install scikit-image
	Install dlib
		python -m pip install dlib
	Reconfigure swap , boot and memory
		sudo nano /etc/dphys-swapfile
		CONF_SWAPSIZE=100
		sudo /etc/init.d/dphys-swapfile stop
		sudo /etc/init.d/dphys-swapfile start
		free -m
		sudo raspi-config
			Boot Options => Desktop / CLI => Desktop Autologin
			Advanced Options => Memory Split => 144mb #144 for camera to work 64 default
	Reboot to console
```	
*Audio*
```
	sudo apt-get update
	sudo pip install gTTS
	sudo apt-get install mpg321
```
*Video*
```
	sudo apt-get update
	sudo apt-get install build-essential
	sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
	sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev python-opencv python-matplotlib
	python -m pip install imutils
	python -m pip install face_recognition
```