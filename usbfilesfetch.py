from display import Display

import pyudev
import time
import os

class USBFilesFetch():
    def __init__(self, display : Display):
        self.display = display
        self.usb_storage_location = None

        while self.usb_storage_location == None:
            # display waiting for usb device
            self.usb_storage_location = self.find_usb_location()
            time.sleep(5)

    def find_usb_location(self) -> str:
        monitor = pyudev.Monitor.from_netlink(pyudev.Context)
        monitor.filter_by(subsystem="block", device_type="partition")

        for device in iter(monitor.pool, None):
            if "ID_BUS" in device and device == "usb":
                return device.device_node
        
        return None
    
    def get_instruction_files(self) -> list:
        instruction_files = []

        for file in os.listdir(self.usb_storage_location):
            if file.split(".")[-1] == "txt":
                instruction_files.append(file)
        
        return instruction_files
    
    # def get_instructions_from_file(self, instruction_file_name):
    #     with open(self.usb_storage_location + instruction_file_name, "r") as f:
    #         return f.read()

    def get_path(self) -> str:
        return self.usb_storage_location