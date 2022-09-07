import RPi.GPIO as GPIO
import os
import serial
from time import sleep
from omxplayer import OMXPlayer
from collections import deque

## Sets pin numbers for button inputs
greenButtPin = 17
redButtPin = 27
yellowButtPin = 22
blueButtPin = 23

## Sets pin numbers for light outputs
greenLightPin = 5
redLightPin = 6
yellowLightPin = 13
blueLightPin = 19

## Setup GPIO pins as input/output
GPIO.setmode(GPIO.BCM)

GPIO.setup(greenButtPin,GPIO.IN)
GPIO.setup(redButtPin,GPIO.IN)
GPIO.setup(yellowButtPin,GPIO.IN)
GPIO.setup(blueButtPin,GPIO.IN)

GPIO.setup(greenLightPin,GPIO.OUT)
GPIO.setup(redLightPin,GPIO.OUT)
GPIO.setup(yellowLightPin,GPIO.OUT)
GPIO.setup(blueLightPin,GPIO.OUT)

## Starts video player instance, plays file @ file_path
## Starts in paused mode. used sleep and then pause instead of pause argument
## because if file pauses at start sometimes it pauses before the player
## actually shows up.
file_path = '/home/pi/MustacheVideo.mkv'
omx = OMXPlayer(file_path, args=['--loop', '-o', 'hdmi'])
sleep(1)
omx.pause()

## Sets up serial port to control projector. First (top left) usb port must
## be used unless "port" is changed.
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)

if ser.isOpen() :
    ser.close()

ser.open()

## button previous state is kept track of so holding down
## the button doesn't cause it to continuously fire
g_prev_state = 0
r_prev_state = 0
y_prev_state = 0
b_prev_state = 0

## initialize arrays to keep track of button sequence,
## in order to use button sequence to shutdown device
## and quit video player. req_sd_array contains the sequence of
## colors that must be pushed to shut down the device
## req_quit_array contains the sequence of colors that must be pushed
## to quit the video player to desktop.
sd_array = deque(["a","a","a","a","a","a","a","a"])
req_sd_array = deque(["y","r","y","g","r","y","g","g"])
req_quit_array = deque(["y","r","y","g","r","y","y","g"])

## function to check the projector state.
## returns true if the projector is on.
def projector_on():
    ser.write('\rV99G0007\r')
    output = ''
    sleep(0.1)
    while ser.inWaiting() > 0:
        output += ser.read(1)
    if output == 'P2\r':
        return 1
    else:
        return 0

## function to check the projector source.
## returns true if source is HDMI
def projector_ready():
    ser.write('\rV99G0220\r')
    output = ''
    sleep(0.1)
    while ser.inWaiting() > 0:
        output += ser.read(1)
    if output == 'P6\r':
        return 1
    else:
        return 0

## function to turn off projector
def set_projector_off():
    ser.write('\rV99S0002\r')
    output = ''
    sleep(0.1)
    while (ser.inWaiting() > 0):
        output += ser.read(1)

## function to turn on projector
def set_projector_on():
    ser.write('\rV99S0001\r')
    output = ''
    sleep(0.1)
    while (ser.inWaiting() > 0):
        output += ser.read(1)

## turn blue light on. This signals the pi is turned on and the script
## has started
GPIO.output(blueLightPin,GPIO.HIGH)


loop = True
while loop:
    ## turns on red, yellow, and green lights if the projector is ready, turns them off if not
    if (projector_ready()):
        GPIO.output(yellowLightPin,GPIO.HIGH)
        GPIO.output(greenLightPin,GPIO.HIGH)
        GPIO.output(redLightPin,GPIO.HIGH)
    else:
        GPIO.output(greenLightPin,GPIO.LOW)
        GPIO.output(yellowLightPin,GPIO.LOW)
        GPIO.output(redLightPin,GPIO.LOW)
    
    ## Reads for button inputs
    g_input = GPIO.input(greenButtPin)
    r_input = GPIO.input(redButtPin)
    y_input = GPIO.input(yellowButtPin)
    b_input = GPIO.input(blueButtPin)
    
    ## If green button is pressed, play or pause the movie,
    ## but only if the projector is ready.
    ## add green to the sequence array
    if ((not g_prev_state) and g_input):
        if (projector_ready()):
            omx.play_pause()
        sd_array.append("g")
        sd_array.popleft()
    
    ## If red button is pressed, rewind 5 seconds
    ## but only if the projector is ready
    ## add red to the sequence array
    if ((not r_prev_state) and r_input):
        if(projector_ready()):
            omx.set_position(omx.position()-5)
        sd_array.append("r")
        sd_array.popleft()
    
    ## If yellow button is pressed, advance 5 seconds
    ## only if projector is ready and current position
    ## plus 5 seconds is not greater than the total duration of
    ## the movie. Add yellow to the sequence array.
    if ((not y_prev_state) and y_input):
        if((omx.position() +5 < omx.duration()) and projector_ready()):
            omx.set_position(omx.position()+5)
        sd_array.append("y")
        sd_array.popleft()
        
    ## If blue button is pressed, and projector is ready, turn off the projector.
    ## Read the serial output to clear the buffer.
    ## If projector is not ready, turn the projector on. and read serial buffer
    ## If projector is warming up, the projector will receive an "on" command
    ## and do nothing.
    ## Add blue to the sequence array
    if((not b_prev_state) and b_input):
        if(projector_on()):
            omx.set_position(0)
            omx.play()
            sleep(0.5)
            omx.pause()
            set_projector_off()
        else:
            omx.set_position(0)
            omx.play()
            sleep(0.5)
            omx.pause()
            set_projector_on()
            while (not projector_ready()):
                sleep(0.5)
                GPIO.output(blueLightPin,GPIO.LOW)
                sleep(0.5)
                GPIO.output(blueLightPin,GPIO.HIGH)
                
    
    ## set the previous states as the current states.
    r_prev_state = r_input
    g_prev_state = g_input
    y_prev_state = y_input
    b_prev_state = b_input
    
    ## checks if either the shutdown or quit sequence has been pushed and
    ## executes accordingly.
    if (sd_array == req_sd_array):
        omx.quit()
        GPIO.output(blueLightPin,GPIO.LOW)
        GPIO.output(greenLightPin,GPIO.LOW)
        GPIO.output(yellowLightPin,GPIO.LOW)
        GPIO.output(redLightPin,GPIO.LOW)
        set_projector_off()
        GPIO.cleanup()
        loop = False
        os.system("sudo shutdown -h now")
    if (sd_array == req_quit_array):
        omx.quit()
        GPIO.output(blueLightPin,GPIO.LOW)
        GPIO.output(greenLightPin,GPIO.LOW)
        GPIO.output(yellowLightPin,GPIO.LOW)
        GPIO.output(redLightPin,GPIO.LOW)
        GPIO.cleanup()
        loop = False
        exit()
    
    ## chills out for like less than a sec
    sleep(0.05)
    
