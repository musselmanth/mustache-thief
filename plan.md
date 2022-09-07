**Mustache Thief DVD Player Replacement**

**Materials Needed:**

- Raspberry Pi
- Breadboard
- 4 push buttons (like the ones in timescape)
- 10K resistor
- Jumper Wires
- 6 ft HDMI cable
- 6 ft USB to Serial RS-232 adapter ([https://www.amazon.com/dp/B017CZ3FZ2/ref=cm_sw_r_cp_dp_T2_eKxFzbHGY1571](https://www.amazon.com/dp/B017CZ3FZ2/ref=cm_sw_r_cp_dp_T2_eKxFzbHGY1571))
- Wall mounted box to house the buttons and pi (we can build this)
- Some sort of lockable enclosure to cover the buttons (thermostat cover?)

**The Setup**

- Four buttons are connected to the raspberry pi’s GPIO pins and have the following functions:
  - Play/Pause
  - Rewind (will actually function by skipping backward 5 seconds)
  - Fast Foward (skip forward 5 seconds)
  - Projector On/Off
- The raspberry pi will be connected via USB to the projector’s RS-232 serial port so it can read the projector’s on/off state and send commands to turn it on/off.
- A simple python script will load at boot and loop the mustache thief video full screen, starting in a paused state. The play/pause, rewind, and fast forward button will only accept input if the projector is turned on. Once the video is over, it will start again from the beginning and continue playing until play/pause is pushed.
