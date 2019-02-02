from flask import Flask, render_template
import pigpio
import time
import pigpio
import SDL_Pi_DustSensor
import random
import datetime
import telepot
from telepot.loop import MessageLoop

aqi = 8.5

SENSORPIN = 17

# import testDust
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def cakes():
    

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

      #print("Air Quality Measurements for PM2.5:")
      #print("  " + str(int(c)) + " particles/0.01ft^3")

      # convert to SI units
    concentration_ugm3=dustSensor.pcs_to_ugm3(c)
   # print("  " + str(int(concentration_ugm3)) + " ugm^3")
      
      # convert SI units to US AQI
      # input should be 24 hour average of ugm3, not instantaneous reading
    aqi=dustSensor.ugm3_to_aqi(concentration_ugm3)
      
    print("  Current AQI (not 24 hour avg): " + str(int(aqi)))
      #print("")

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
#          continue

      #print("Air Quality Measurements for PM2.5:")
      #print("  " + str(int(c)) + " particles/0.01ft^3")

      # convert to SI units
	concentration_ugm3=dustSensor.pcs_to_ugm3(c)
   # print("  " + str(int(concentration_ugm3)) + " ugm^3")
      
      # convert SI units to US AQI
      # input should be 24 hour average of ugm3, not instantaneous reading
	aqi=dustSensor.ugm3_to_aqi(concentration_ugm3)
      
	print("  Current AQI (not 24 hour avg): " + str(int(aqi)))
      #print("")

	pi.stop() # Disconnect from Pi.
	bot.sendMessage(chat_id, str(int(aqi)))

bot = telepot.Bot('730151918:AAHf5ZiQnERdK_PussBalnoVltGO3O96zqc')

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

