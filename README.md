![Logo](https://github.com/djcopley/Tiltometer/blob/master/Assets/banner.png)

This program uses input data from an IMU to calculate the pitch and roll of your vehicle and then display it visually 

# Introduction
I came to develop this program just mostly out of summer boredom. I drive a Jeep and I thought I could do some cool
projects by affixing a screen and a raspberry-pi in it. Just like that the Jeep Tiltometer was born :P (yes I am aware 
it is actually called an inclinomter). I plan on installing a rear view camera and using libraries such as OpenCV and
TensorFlow to create some sort of obstacle detection and notification, so stay tuned for that. Feel free to fork this and 
make changes or improvements as you see fit. One thing that could definitely use improvement is the method of rotation I used. 
Pixbuf and Gdk don't support image rotation or very good scaling so I kind of had to hack it and just sort of animate it.
A more efficient solution would be using Cairo or something to rotate the image (I will update this at some point hopefully).
Anyway thanks for visiting and enjoy!

# Installation
1. Clone repository:  `git clone https://github.com/djcopley/Tiltometer.git`
2. Install dependencies: `sudo apt install ` `pip install `
3. 

# Resources
LSM9DS0 [Data Sheet](http://ozzmaker.com/wp-content/uploads/2014/12/LSM9DS0.pdf)

Finding [Pitch and Roll](http://samselectronicsprojects.blogspot.com/2014/07/getting-roll-pitch-and-yaw-from-mpu-6050.html)



# Licensing
**This project falls under the purview of the [MIT License](https://github.com/djcopley/Tiltometer/blob/master/LICENSE).**
