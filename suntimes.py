#!/usr/bin/python
import RPi.GPIO as GPIO
from datetime import datetime, date, timedelta, time
import time as mtime
import requests

# Connecting to the OpenWeatherMap api
def get_suntimes():
	city = "3451190"
	apikey = "0a26e4405f88c8088a6ae5175cb84999"
	url = str("http://api.openweathermap.org/data/2.5/weather?id="+city+"&appid="+apikey)
	weather_request = requests.get(url)
	weather_json = weather_request.json()
    # Parsing JSON for sun times
	set = weather_json['sys']['sunset']
	rise = weather_json['sys']['sunrise']
	return set, rise
	
def GPIO_Initialization(): #setting up raspberrypi GPIO pins
	GPIO.setmode(GPIO.BCM)
	# init list with pin numbers, add for more relays
	pinList = [22]
	for i in pinList: 
		GPIO.setup(i, GPIO.OUT) 
	return pinList

def show_times(timeRightNow,sunset,sunrise):#Showing time information from initial json GET request and any day adjustments needed
	print("\nThe time right now is... ", timeRightNow,"\n")
	print("Next sunset time is -", datetime.fromtimestamp(sunset),"\n")
	print("Next sunrise time is -", datetime.fromtimestamp(sunrise),"\n")
	

def time_dayadjustment(sunrise,sunset):
	dayAdjustment = timedelta(days=1).total_seconds()
	if mtime.time() > sunrise and mtime.time() < sunset:
		sunrise = sunrise + dayAdjustment
		#print("\nSunrise time was adjusted, \nit is now", datetime.fromtimestamp(sunrise))
		return sunrise, sunset
	elif mtime.time() > sunrise and mtime.time() > sunset:
		sunrise = sunrise + dayAdjustment
		sunset = sunset + dayAdjustment
		print("\nSunrise and Sunset time was adjusted", datetime.fromtimestamp(sunset))
		return sunrise,sunset
	else:
		print("nothing changed")

def time_update():
	print("Updating sunrise and sunset times from the Internet")
	suntimes = get_suntimes()
	print("Done.\n")
	sunset = suntimes[0]
	sunrise = suntimes[1]
	timeRightNow = datetime.fromtimestamp(mtime.time())
	print("Adjusting dates")
	adjtimes = time_dayadjustment(sunrise,sunset)
	print("Done.\n")
	sunrise = adjtimes[0]
	sunset = adjtimes[1]
	show_times(timeRightNow,sunset,sunrise)
	return sunrise,sunset

def lamp_delaytimes(sunrise,sunset):
	waitTimeAfterSunset = 1800
	waitTimeBeforeSunrise = 19800
	lampONTime = sunset + waitTimeAfterSunset
	lampOFFTime = sunrise - waitTimeBeforeSunrise
	return lampONTime,lampOFFTime

#Define your times to wait after and before Sunset and Sunrise, respectively
def main():
	print("Welcome to SunSwitch for Raspberry Pi\n")
	print("Initializing Raspberry Pi GPIO pins\n")
	pinList = GPIO_Initialization()
	x = time_update()
	sunrise = x[0]
	sunset = x[1]
	lampdelay = lamp_delaytimes(sunrise,sunset)
	lampONTime = lampdelay[0]
	lampOFFTime = lampdelay[1]
	#Loop that turns on and off your GPIO pin/lamp between your sunrise and sunset times, should only need to edit your gpio pin number here
	while True:
		if mtime.time() > lampONTime and mtime.time() < lampOFFTime:
			GPIO.output(pinList, GPIO.LOW)
			lampOFFDT = datetime.fromtimestamp(lampOFFTime)
			print("The Lamp is ON until", lampOFFDT)
			mtime.sleep(120);
		else:
			GPIO.output(pinList, GPIO.HIGH)
			lampONDT = datetime.fromtimestamp(lampONTime)
			print("The Lamp is OFF until ", lampONDT)
			new = time_update()
			sunrise = new[0]
			sunset = new[1]
			print("Program will now sleep until 30 minutes after sunset")
			safetybuffer = 10
			#timeDT = datetime.fromtimestamp(mtime.time())
			slumber = (lampONTime + safetybuffer) - mtime.time()
			#print(slumber)
			slumberClean = datetime.fromtimestamp(mtime.time() + slumber)
			#print("Just",slumberClean.strftime("%H hours, %M minutes and %S seconds to go."))
			print("zzzzZZZzzz...for", slumber,"seconds...zzzzZZZZzzz")
			mtime.sleep(slumber)
			print("OK, program woke up @ ", datetime.fromtimestamp(mtime.time()), "! \nRunning back through the program!")
			
try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nOK, bye!")