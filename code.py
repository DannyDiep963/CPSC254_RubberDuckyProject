# License : GPLv2.0
#https://docs.circuitpython.org/projects/hid/en/latest/


import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode

import supervisor

'''CircuitPython Essentials HID KEYBOARD library'''
import time
import digitalio
from board import *
led = digitalio.DigitalInOut(LED)
led.direction = digitalio.Direction.OUTPUT

'''Dictionary for the keyboard layout'''
duckyCommands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'BACKSPACE': Keycode.BACKSPACE,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,
}

'''
Function: convertLine()
Description: Translating the keyboard input (payload) script
Param: line - each line from the payload script
Return: a new translated line
'''
def convertLine(line):
    newline = []
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            newline.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    return newline

'''
Function: runScriptLine()
Description: Control the press and release all pressed keys
Param: line - single script line
Return: NONE
'''
def runScriptLine(line):
    for k in line:
        kbd.press(k)
    kbd.release_all()

'''
Function: sendString()
Description: Typing the string out
Param: line - single script line
Return: None
'''
def sendString(line):
    layout.write(line)

'''
Function: parseLine()
Description: Translate the command meaning of the payload
Param: line - each line from the payload script
Call the function runScriptLine() to press and release the keyboard input
'''
def parseLine(line):
    global defaultDelay
    if(line[0:3] == "REM"):                 # Comment 
        # ignore ducky script comments
        pass
    elif(line[0:5] == "DELAY"):             # DELAY 
        time.sleep(float(line[6:])/1000)
    elif(line[0:6] == "STRING"):            # STRING
        sendString(line[7:])
    elif(line[0:5] == "PRINT"):             # PRINT
        print("[SCRIPT]: " + line[6:])
    elif(line[0:6] == "IMPORT"):            # IMPORT
        runScript(line[7:])
    elif(line[0:13] == "DEFAULT_DELAY"):    # DEFAULT DELAY
        defaultDelay = int(line[14:]) * 10
    elif(line[0:12] == "DEFAULTDELAY"):     # DEFAULT DELAY
        defaultDelay = int(line[13:]) * 10
    elif(line[0:3] == "LED"):               # LED
        if(led.value == True):
            led.value = False
        else:
            led.value = True
    else:
        newScriptLine = convertLine(line)
        runScriptLine(newScriptLine)
'''
Function: getProgramminStatus()
Description: Check if the device is in booting mode
Param: NONE
Return: the status of the device
'''
def getBootingStatus():
    # check GP0 for setup mode
    # see setup mode for instructions
    deviceStatusPin = digitalio.DigitalInOut(GP0)
    deviceStatusPin.switch_to_input(pull=digitalio.Pull.UP)
    deviceStatus = not deviceStatusPin.value
    return(deviceStatus)

'''
Function: runScript()
Description: Open and read the payload, then separate each line for translation and performing
Param: file - payload script
Return: NONE
'''
def runScript(file):
    global defaultDelay
    duckyScriptPath = file
    f = open(duckyScriptPath,"r",encoding='utf-8')
    previousLine = ""
    for line in f:
        line = line.rstrip()
        if(line[0:6] == "REPEAT"):
            for i in range(int(line[7:])):
                #repeat the last command
                parseLine(previousLine)
                time.sleep(float(defaultDelay)/1000)
        else:
            parseLine(line)
            previousLine = line
        time.sleep(float(defaultDelay)/1000)


'''main method'''
# Setup the PICO as Keyboard Devices
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

# Turn off automatically reloading when files are written to the pico
supervisor.disable_autoreload()

# Allow the device a quick initial time to be recognized by the host computer
time.sleep(.5)
led.value = True
defaultDelay = 0

#Getting the status of the board
deviceStatus = False                # Set defaul status
deviceStatus = getBootingStatus()

if(deviceStatus == False):          # If the device is not in setup mode, inject the payload
    payload = 'payload.dd'
    runScript(payload)
    led.value = True                # LED stay on indicate that the script has successfully injected.

else:
    # Led blinking indicate that the script has not run and the device is in the setup mode
    while True:
        time.sleep(1.0)
        led.value = False
        time.sleep(1.0)
        led.value = True

    