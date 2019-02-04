from flask import Flask, render_template
import pigpio
import time
import pigpio
#local import change if renamed file
import SDL_Pi_DustSensor
#
import random
import datetime
import telepot
from telepot.loop import MessageLoop
#this is an error value
aqi = 70773
#this sets the pin for the sensor as pin 17
SENSORPIN = 17

# import testDust
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    

    pi = pigpio.pi() # Connect to Pi.
   
    dustSensor = SDL_Pi_DustSensor.SDL_Pi_DustSensor(pi, SENSORPIN) # set the GPIO pin number

      # Use 30s for a properly calibrated reading.
    time.sleep(30) 
      
      # get the gpio, ratio and concentration in particles / 0.01 ft3
    g, r, c = dustSensor.read()

      # concentration above 1,080,000 considered error
    if (c>=1080000.00):
        print("Concentration Error\n")
#          continue

   

      # convert to SI units
    concentration_ugm3=dustSensor.pcs_to_ugm3(c)
   # print("  " + str(int(concentration_ugm3)) + " ugm^3")
      
      # convert SI units to US AQI
      # input should be 24 hour average of ugm3, not instantaneous reading
    aqi=dustSensor.ugm3_to_aqi(concentration_ugm3)
      
    print("  Current AQI (not 24 hour avg): " + str(int(aqi)))

    pi.stop() # Disconnect from Pi.
    templateData = {
    'aqi' : str(int(aqi)),
    'aqiindex' : 'gg'
      }
    return render_template('mains.html', **templateData)
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/joke':
	bot.sendMessage(chat_id,str('Knock Knock'))
	if command == 'Who is there':
	    bot.sendMessage(chat_id,str('canoe'))
	    if command == 'canoe who':
		bot.sendMessage(chat_id,str('canoe help me with my homework'))
    elif command == '/usage':
	bot.sendMessage(chat_id,str('ZeroAQI was meant to be portable, but that does not mean you can take me everywhere.  My electronics hate getting wet, because when they do they stop working.  So, please do not stick me in a lake or put me in the rain as it will not end well.  To take accurate readings I need still air so I will not function well on a windy day unless you shield me.  To take the best readings I also need to be upright, an easy way to check is if the wire connecter is closest to the ground.  Since again my electronics hate getting wet it is advised that I stay indoors when it is humid outside, sorry no waterslides for me.'))
    elif command == '/about':
	bot.sendMessage(chat_id,str('ZeroAQI is an affordable, portable air quality sensor for everybody.  All the code is on github with an open source license so anyone can make one.  Since there are no designated parts lists you can find the best prices for your components.  You are welcome to play around with the code and when you create somethimg amazing please commit it to ZeroAQIs github so ZeroAQI can get even better. Please enjoy ZeroAQI'))
    elif command == '/How to improve my AQI':
	bot.sendMessage(chat_id,str('You can purchase an air filter such as a HEPA air filter.  You could also consider vacumming to reduce dust and improving your ventilation.  If this is an outdoor AQI detector and the AQI is unhealthy you should consider moving indoors'))
    elif command == '/aqi':
	pi = pigpio.pi() # Connect to Pi.

	dustSensor = SDL_Pi_DustSensor.SDL_Pi_DustSensor(pi, SENSORPIN) # set the GPIO pin number

# Use 30s for a properly calibrated reading.
	time.sleep(30) 
      
# get the gpio, ratio and concentration in particles / 0.01 ft3
	g, r, c = dustSensor.read()

      # concentration above 1,080,000 considered error
	if (c>=1080000.00):
		print("Concentration Error\n")

      # convert to SI units
	concentration_ugm3=dustSensor.pcs_to_ugm3(c)
      
      # convert SI units (EU) to US AQI {optional you can comment this out}
      #NOTE: input should be 24 hour average of ugm3, not instantaneous reading
	aqi=dustSensor.ugm3_to_aqi(concentration_ugm3)
      
	print("  Current AQI (not 24 hour avg): " + str(int(aqi)))
      #print("")

	pi.stop() # Disconnect from Pi.
	bot.sendMessage(chat_id, str(int(aqi)))
#make sure to put your api key here
bot = telepot.Bot('YOURAPIKEY')

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

