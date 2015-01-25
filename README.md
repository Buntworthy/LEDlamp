LED lamp
======
Code for an LED lamp

Hardware
------
Powered by:

* Raspberry Pi
* Python
* Flask
* Fadecandy
* 60 addressable RGB LEDs (WS2812B)
* Some wire and connectors
* Some aluminium tube
* Something needed to diffuse the LEDs

Aim
------
LED lamp to display colours and change, probably talks
to the internet somehow and controllable over the web.

Progress
------

*Currently:*
Form input into Flask served page sets colour of LED strip

*Next:*
???

*Previously:*
* Displaying single colours (with some noise), fades between
other colours at random intervals.

* One thread responsible for running LED animations (currently displaying a colour with noise, and transitions). Flask webserver runs listening for request for a page which triggers a change to a random colour. 