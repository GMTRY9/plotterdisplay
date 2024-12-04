from usbfilesfetch import USBFilesFetch
from display import Display
import time
import RPi.GPIO as GPIO

class Controller():
    def __init__(self):
        # SET PINS FOR INCREMENT AND START BUTTON PIN NUMBERS
        INCREMENT_BUTTON_PIN_NUMBER = 1
        START_BUTTON_PIN_NUMBER = 2

        # initialise singleton classes (my homies hate inheritance)
        self.display = Display()

        # program should wait here for a USB storage device to be plugged in
        self.usbfilesfetch = USBFilesFetch(self.display)
        # instruction filenames in array ["file1.txt", "file2.txt", ...]
        self.instruction_files = self.usbfilesfetch.get_instruction_files()
        self.current_file_index = 0

        # GPIO shenanigans for PTM switches to execute relevant function
        # executes on rising edge only, so hopefully switch bouncing wont be a problem
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(INCREMENT_BUTTON_PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # due to "low level multithreading", GPIO events should execute parallel to mainloop
        GPIO.add_event_detect(INCREMENT_BUTTON_PIN_NUMBER, GPIO.RISING, callback=self.increment_button_callback)

        GPIO.setup(START_BUTTON_PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(START_BUTTON_PIN_NUMBER, GPIO.RISING, callback=self.start_button_callback)

        self.context = "display"

        while True: # sorry i have no idea how we are handling power off
            self.main_controller()

    # CONTEXTS: "display", "increment", "startplot"
    def main_controller(self):
        while self.context == "display":
            instruction_file_name = self.instruction_files[self.current_file_index]
            # display text with scroll index
            time.sleep(0.2)

        if self.context == "increment":
            if self.current_file_index == len(self.instruction_files)-1:
                self.current_file_index = 0
            else:
                self.current_file_index += 1

        if self.context == "startplotting":
            filepath = self.usbfilesfetch.get_path() + self.instruction_files[self.current_file_index]
            self.context = "NO" # NO USER INPUTS ACCEPTED acc maybe we want the start button to stop the plotting acc

            # pass filepath to IE and WAIIT!!!!!!

            # reset to defaults once finished
            self.context = "display"
            self.current_file_index = 0
        
    def increment_button_callback(self):
        if self.context == "NO":
            return
        
        self.context = "increment"

    def start_button_callback(self):
        if self.context == "NO":
            return
        
        self.context = "startplotting"
