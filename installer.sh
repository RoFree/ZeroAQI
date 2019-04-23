echo "Ready to install ZeroAQI"
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install pigpio
sudo pip3 install flask
sudo pip install telepot
sudo apt-get install python
sed s/"exit 0"/"sudo pigpiod"\n"python /home/pi/ZeroAQI/index.py &"\n"exit 0"
echo "All right we are done!"
echo "To finish installation you need to do a few things"
echo "Set up a telegram bot (for information see the github site)"
echo "Put the bot api key in the python code"
