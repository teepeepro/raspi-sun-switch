# raspi-sun-switch
Python script for Raspberry Pi that uses web Sunrise and Sunset times to turn on/off a relay controlled light or any other GPIO device, making a nifty sun-driven IoT device.

Using this script, you can change the settings on the GPIO pins of a raspberry pi (on or off), based on the times of the sunset or sunrise anywhere in the world.

Before you get started, make sure you have the following installed on your Raspberry Pi or in the case of a weather API, set up an account. All instructions are written more or less for Raspian, or Debian based OSes. 

<ul><li>Python 3 for overall code (Note- should be installed on Rasbian OS, but use <code>sudo apt-get install python3</code> to check or instal)</li>
<li>A free weather API - in this case, OpenWeatherMap.com</li>
  <p><a href="http://openweathermap.org/appid">Easy instructions on how to obtain OpenWeatherMap.com API code.</a>
<li>and the Rpi.GPIO python library (Note- It is installed by default on Rasbian OS) to install, simple run the following on the command line <br>
<code>sudo apt-get install python-dev python-rpi.gpio</code></li>

<h2>Manipulating Script for your needs</h2>
<p>This section describes how to change parts of the script to modify for your needs</p>
<ul>
  <li>First, take a look at the Get_Sun_Times function, and change the city code (look up city code here) and place your API key in the apikey variable.
  <code>def get_sun_times():
    city = "3451190" #Default is Rio de Janeiro, BR
    apikey = "000000"</code>
    </li>
    <li>Next, make sure your GPIO pins are correctly assigned. Since this is set up as an array, you can put multiple pins here, for multiple relays and lights that you wish to control
    <code># init list with pin numbers, add for more relays
pinList = [22]
    </code>
    </li>
    <li>Finally, you can adjust how long after sunset or sunrise the lamp or relay turns on and off, respectively. The value is in seconds, so adjust accordingly, or leave the defaults as is.
      <code>#Define your times to wait after and before Sunset and Sunrise
  waitTimeAfterSunset = 1800  
  waitTimeBeforeSunrise = 19800</code>
    </li>
  <li>The rest of the code is free to manipulate based on your needs and should be pretty readable with basic python or programming knowledge. Have fun!</li>


