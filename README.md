![LOGO](https://github.com/djcopley/Tiltometer/blob/master/assets/banner.png)

### Table of Contents
**[Introduction](#introduction)**<br>
**[Requirements](#requirements)**<br>
**[Installation](#installation)**<br>
**[Resources](#resources)**<br>
**[Contributing](#contributing)**<br>
**[Licensing](#licensing)**<br>

## Introduction
I came to develop this program mostly out of summer boredom. I drive a Jeep and thought it would be cool to install
a touch screen coupled with a raspberry pi inside. I plan on affixing a rear view camera to my tailgate, and using some  
open source libraries like OpenCV to achieve some obstacle recognition in the future. Feel free to submit a pull request and make changes or improvements 
as you see fit. I will review and merge valuable changes. Please see the section on **[contributing](#contributing)** for more details and guidelines. 
Anyways, thanks for visiting and enjoy!

## Requirements
This is the list of parts I used and how to configure them:
* Raspberry Pi Model 3
* LSM9DS0 [IMU](http://amzn.to/2tsNNs8)
* 7" Raspberry Pi [Touch Screen](http://amzn.to/2tDvX83)
* A soldering iron
* 5V power supply for the Raspberry Pi

## Installation
1. Clone repository:  `git clone https://github.com/djcopley/Tiltometer.git`
2. Enable i2c - in terminal type `sudo raspi-config` then navigate to Interfacing Options > I2C > Yes
3. Install dependencies: `sudo apt install i2c-tools libi2c-dev python-smbus python3.4` `pip3 install PyGObject`
4. Make start_tiltometer executable `chmod +x start_tiltometer.sh`

You will most likely need to solder the headers to your LSM9DS0 IMU module so start by doing that. Next we can start wiring the IMU to our Raspberry Pi.

![Raspi-Pinout](http://www.elektronik-kompendium.de/sites/raspberry-pi/fotos/raspberry-pi-15.jpg)

For our purposes we need to find the I2C headers. It's the same for both models of the Raspberry Pi so if you have a different model, no need to worry.
Pin 3 and 5 are our I2C headers(GPIO  2 and 3). Connect power to 3.3v, SDA to GPIO 2, SCL to GPIO 3 and GND to... well ground of course.


After all this, you're ready to go! Just go to your Tiltometer directory and type `./start_tiltometer.sh`.

## Resources
LSM9DS0 [Data Sheet](http://ozzmaker.com/wp-content/uploads/2014/12/LSM9DS0.pdf)

Finding [Pitch and Roll](http://samselectronicsprojects.blogspot.com/2014/07/getting-roll-pitch-and-yaw-from-mpu-6050.html)

Gtk Python [Documentation](https://python-gtk-3-tutorial.readthedocs.io/en/latest/)

## Contributing
I would like to keep this as simple as possible so all I will say here is be courteous and use common sense and there won't be any issues. 
In case there is any discrepancy or you would like more information, please check out the full set of guidelines [here](https://github.com/djcopley/Tiltometer/blob/master/CONTRIBUTING.md).
Any contribution is much appreciated!

Thank you! 😁

## Licensing
**This project falls under the purview of the [MIT License](https://github.com/djcopley/Tiltometer/blob/master/LICENSE).**
