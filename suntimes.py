#!/usr/bin/python
import RPi.GPIO as GPIO
import time, datetime
import requests

# Connecting to the OpenWeatherMap api
def get_sun_times():
    city = "3451190"
    apikey = "0a26e4405f88c8088a6ae5175cb84999"
    url = str("http://api.openweathermap.org/data/2.5/weather?id="+city+"&appid="+apikey)
    weather_request = requests.get(url)
    weather_json = weather_request.json()
    return weather_json
      

# Parsing JSON for sun times
suntimes = get_sun_times()
sunset = suntimes['sys']['sunset']
sunrise = suntimes['sys']['sunrise']

#setting up raspberrypi GPIO pins

GPIO.setmode(GPIO.BCM)

# init list with pin numbers, add for more relays
pinList = [22]

for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 

#Showing Time information from initial json GET request

timeRightNow = time.time()

def show_times():
    print("The time right now is... ", datetime.datetime.fromtimestamp(timeRightNow))
    print("Next sunset time is -", datetime.datetime.fromtimestamp(sunset))
    print("Next sunrise time is -", datetime.datetime.fromtimestamp(sunrise))
    return

show_times()

#Define your times to wait after and before Sunset and Sunrise, respectively

waitTimeAfterSunset = 1800
waitTimeBeforeSunrise = 19800

lampONTime = sunset + waitTimeAfterSunset
lampOFFTime = sunrise - waitTimeBeforeSunrise

#Loop that turns on and off your GPIO pin/lamp between your sunrise and sunset times, should only need to edit your gpio pin number here

while True:
    if timeRightNow > lampONTime and timeRightNow < lampOFFTime:
      GPIO.output(22, GPIO.LOW)
      lampOFFDT = datetime.datetime.fromtimestamp(lampOFFTime)
      print("The Lamp is ON until", lampOFFDT)
      time.sleep(120);
    else:
      GPIO.output(22, GPIO.HIGH)
      lampONDT = datetime.datetime.fromtimestamp(lampONTime)
      print("The Lamp is OFF until ", lampONDT)
      get_sun_times()
      print("New suntimes times have been loaded. \nProgram will now sleep until 30 minutes after sunset")
      safetybuffer = datetime.timedelta(seconds=10)
      timeDT = datetime.datetime.fromtimestamp(time.time())
      slumber = ((lampONDT + safetybuffer) - timeDT).total_seconds()
      print("Just ",str(datetime.timedelta(seconds=slumber))," to go.")
      time.sleep(slumber)
      print("OK, program woke up @ ", timeDT, "! \nRunning back through the program!")
      show_times()
