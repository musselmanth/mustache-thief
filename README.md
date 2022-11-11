# About

This python script was created to improve interactivity in an Escape Room. It is set up to run on a raspberry pi to interact with a projector through a serial connection and hdmi. The script allows for user input to the projector through pushing interactive buttons connected to the Raspberry Pi's GPIO board, and control the playback of an interactive video playing through HDMI on the projector.

**The Mustache Thief Rpi/Projector Setup Information**

1. **Code**

   1. The Raspberry Pi is running a python script at boot which creates an instance of omxplayer ([https://github.com/huceke/omxplayer](https://github.com/huceke/omxplayer)) to play the video.
   2. The python script uses an omxplayer wrapper ([https://github.com/willprice/python-omxplayer-wrapper](https://github.com/willprice/python-omxplayer-wrapper)) to create and control the omxplayer instance.
   3. The script uses the pySerial library to control the projector. Information about serial setup and commands can be found in the projector’s manual, on page 50-53. [http://www.vivitek.eu/Files/UserManual/J5P%20Ultra%20VIVITEK%20D516_D517_D518_D519%20UM-20120207.pdf](http://www.vivitek.eu/Files/UserManual/J5P%20Ultra%20VIVITEK%20D516_D517_D518_D519%20UM-20120207.pdf)
   4. The python script is located at “/home/pi/mustachethief.py”. It is well documented so you should be able to figure out what it is doing. A copy of the code is provided at the end of this document.
   5. The video file is located at “/home/pi/MustacheThief.mkv”.
   6. The python script is autorun in the desktop by placing the command “python /home/pi/mustachethief.py” in the file “/home/pi/.config/lxsession/LXDE-pi/autostart”
      1. Note: The pi can’t be controlled with mouse and keyboard while the omxplayer is running. In order to quit to the desktop, a button sequence can be pushed: Yellow, Red, Yellow, Green, Red, Yellow, Yellow, Green

2. **GPIO/Breadboard layout:**

   GPIO pins used:

   <table>
     <tr>
     <td><strong>PIN #</strong>
     </td>
     <td><strong>GPIO PIN</strong>
     </td>
     <td><strong>USE</strong>
     </td>
     </tr>
     <tr>
     <td>Pin #1
     </td>
     <td>
     </td>
     <td>3.3 V +
     </td>
     </tr>
     <tr>
     <td>Pin #6
     </td>
     <td>
     </td>
     <td>Ground -
     </td>
     </tr>
     <tr>
     <td>Pin #11
     </td>
     <td>GPIO17 (in)
     </td>
     <td>Green button
     </td>
     </tr>
     <tr>
     <td>Pin #13
     </td>
     <td>GPIO27 (in)
     </td>
     <td>Red button
     </td>
     </tr>
     <tr>
     <td>Pin #15
     </td>
     <td>GPIO22 (in)
     </td>
     <td>Yellow button
     </td>
     </tr>
     <tr>
     <td>Pin #16
     </td>
     <td>GPIO23 (in)
     </td>
     <td>Blue button
     </td>
     </tr>
     <tr>
     <td>Pin #29
     </td>
     <td>GPIO5 (out)
     </td>
     <td>Green light
     </td>
     </tr>
     <tr>
     <td>Pin #31
     </td>
     <td>GPIO6 (out)
     </td>
     <td>Red light
     </td>
     </tr>
     <tr>
     <td>Pin #13
     </td>
     <td>GPIO13 (out)
     </td>
     <td>Yellow light
     </td>
     </tr>
     <tr>
     <td>Pin #35
     </td>
     <td>GPIO19 (out)
     </td>
     <td>Blue light
     </td>
     </tr>
   </table>

- All cables are labeled with pin number locations, breadboard locations, as well was their use. Everything is hot glued in place on the breadboard as well to prevent wires from falling out.
- The button LED lights have built in resistors. In order to work the resistor must be between the GPIO pin and the light. If the cables ever get unplugged and the LED lights no longer work, try swapping the light cable attachments.

3. **Other tech related notes:**
   1. The USB->Serial cable to the projector must be plugged in the left USB bank in order to work. This is because the python script opens the port on the TTYUSB0 device.
   2. The volume to the projector from the pi over HDMI isn’t very loud. When setting up the omxplayer in the python script, an argument is used to amplify the volume by 6000 millibels: “--amp 6000”
   3. Another omxplayer argument, “-o hdmi” specifies that the audio goes through hdmi. This will need to be changed if the audio device is ever different than the projector.
4. **Operation:** 
   1. Plug in USB to turn on 
   2. Once booted and script has started, blue light turns on. The video player is opened and paused at the beginning. 
   3. Pressing the blue button turns on the projector. The blue button will blink while the projector is warming up. No buttons are operational while the blue light is blinking. 
   4. Once the projector is on and has found HDMI as the source, the blue light stops blinking. The other button lights are now illuminating signifying that they can now be pushed to control the movie. 
   5. Green button plays/pauses the movie. Red button seeks backwards 5 seconds. Yellow button seeks forward 5 seconds. 
   6. Pressing the blue button turns off the projector and resets the movie to the beginning, paused. It also disables the other 3 buttons.To turn off the RPi, press the following sequence: Yellow, Red, Yellow, Green, Red, Yellow, Green, Green
   This will shut off the projector and the raspberry pi. It can also be done if the projector is already off.
