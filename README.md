# CPSC254_RubberDuckyProject
Authors:<br />
Danny Diep - Dannydiep963@csu.fullerton.edu<br />
Ahad Hussain - ahadhussain1999@csu.fullerton.edu<br />
Sean Yu - diginomadik@gmail.com<br />

## Installation - Set up the PICO Board
1. Plug in the Raspberry PICO to the computer via USB port while holding **BOOTSEL** button on the PICO board to put PICO in boot mode
2. Download the **adafruit-circuitpython-raspberry_pi_pico-en_US-7.2.4.uf2** from .UF2_file folder and copy the .uf2 file to the PICO
3. The board will reboot itself
4. Download the **adafruit_hid** and copy the folder to lib folder of the PICO Board
5. Download code.py to the PICO board
6. Download the payload.dd to the PICO board

## Execute
1. After the device installs from the step above
2. Plug in the device via USB port
3. Choose the payload and add to the device. The rename the payload as **payload.dd**
4. Unplug and plug in the device again 
5. Sit back and enjoy!<br />

Note: 
When you plug in the device, the payload with run automatically. In order to prevent the payload to run, there are 2 method
- You have to put the device in boot mode (Step 1 from above). This will reset the board and you have to go through the Installation process again<br/>
- (Recommend) You have to connect board pin GP0 to GND when you plug in the device. This will boot the device in setup mode

## References
[CircuitPython](https://docs.circuitpython.org/en/6.3.x/README.html).<br />
[CircuitPython HID](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse).<br />
