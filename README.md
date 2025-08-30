# WRO_2025_UDBTEAM
Proyecto del vehículo autónomo para WRO 2025 - Futuros Ingenieros

<div align="center"><img width="340" height="382" alt="image" src="https://github.com/user-attachments/assets/604953ac-0132-44ae-bd32-a5ebb7cdc35f" />

<img width="360" height="680" alt="image" src="https://github.com/user-attachments/assets/f26c7c01-efc3-4743-9217-228c859b84e3" /></div>

## Content

* `t-photos` contains 2 photos of the team 
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `src` contains code of control software for all components which were programmed to participate in the competition
* `other` contains our training model for cubes based on yolo8

## Introduction
### Steering 
To control the vehicle direction, we adapted the tires form an RC car and implemented a steering mechanism that transforms the rotational motion of the servo motor (model G995) into rotational motion along a different axis as shown in image.  The servo motor provides enough torque to steer the vehicle while allowing precise control of the steering angle.

<div align="center"><img width="531" height="299" alt="image" src="https://github.com/user-attachments/assets/02e7bc8e-c795-4024-b6b2-f040717abaa0" /></div>

### Traction
The traction mechanism was disassembled from the RC car and integrated into the chassis of our vehicle.  The mechanism consists of three large gears that increase the torque of the DC motor, along with a smaller gear that connects the motor shaft to the three larger gears. The DC motor is controlled by an H bridge (L298 Module), which allows rotation in two directions to move the car forward and backward. The module can supply up to 35V and 2A, which is sufficient power for the motor. 

<div align="center"><img width="250" height="350" alt="image" src="https://github.com/user-attachments/assets/4b32bddc-b8b7-4165-8bb6-b13e2d2b7ec5" /></div>

### Power sources 
A power bank  that supplies up to 5V at 3A powers the Raspberry Pi5, which requires a 5V at 5A but can also run on 5V at 3A.  The Raspberry Pi5 supplies power to the Arduino Mega via USB.
Two JYD 18650 batteries connected in series provide up to 8.2V, which is regulated to 6.5V by an LM2596 voltage regulator. This maintains a stable supply for the servo motor and H bridge, even as the batteries discharge.
Two separate power sources are used because a single power source capable of supplying both the Raspberry Pi5 and motors was not available.

<div align="center"><img width="261" height="261" alt="image" src="https://github.com/user-attachments/assets/8144e9d6-18cb-44e5-94ff-79e563eab6b6" />

<img width="162" height="216" alt="image" src="https://github.com/user-attachments/assets/e9e93442-5033-43d7-88a2-f6cbd14001af" /></div>

### Turning the car on and off
A switch connecting GND and the negative terminal of the battery is used to turn the motor and servo motor on and off. The power button on the Raspberry Pi5 is used to turn the Raspberry Pi5 and the Arduino Mega on and off.

### Articial vision
Our car can see its surroundings through a webcam connected via USB to a Raspberry Pi5, which processes the video input using python scripts with Open CV and a YOLO model trained on our dataset of images of red and green cubes.

### Information gathering Open challenge
Raspberry Pi 5 processes the information received from the webcam with three Python scripts. The main one is called xd.py and receives information from detectarcolor.py, which sends data to xd.py when it detects that enough pixels inside the area of interest fall within the blue or orange HSV threshold. xd.py also receives information from detectarpared.py when enough dark pixels are detected inside six different areas of interest: four detect the walls on the sides of the vehicle, one is positioned near the upper edge of the image to detect an incoming wall from the front, and another is located at the bottom center of the screen to detect when the vehicle is too close to a wall.

### Decision making Open challenge
The vehicle moves forward until it detects the blue or orange strips on the floor. A blue detection means the robot must steer to the right and ignore the orange strips. If an orange strip is detected, the robot does the opposite. After this, the vehicle will try to follow the inner walls, having three possible states: too close to the inner wall, close enough, or too far from the inner wall. The vehicle steers as needed to keep itself close enough to the inner wall until it detects a strip of the correct color and repeats the process.


