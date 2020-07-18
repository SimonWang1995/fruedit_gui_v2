from tkinter import *
import os, time, logging, platform

class Setting:
    """A class to store all settings for config"""
    def __init__(self):
        base_cwd = os.getcwd()
        template_cwd = os.path.join(base_cwd, 'template')
        tool_cwd = os.path.join(base_cwd, 'tools')

        self.extra_template = os.path.join(template_cwd, '512_V05_1_productextra.bin')
        self.no_extra_template = os.path.join(template_cwd, '512_V05_1_productextra.bin')
        if platform.system() == "Windows":
            self.tool = os.path.join(tool_cwd,"win64\\ipmitool-1.8.18-lan\\ipmitool.exe")
        elif platform.system() == "Linux":
            self.tool = os.path.join(tool_cwd, "linux\\ipmitool-1.8.18-lan\\ipmitool")
        else:
            print("No support" + platform.system())
            exit(1)

        self.labellist = [(0, 'FRU Device Description', 'NULL', 'NULL', 0, DISABLED),
                          (1, 'Chassis Type', 'NULL', 'NULL', 0, DISABLED),
                          (2, 'Chassis Part Number', 'c', '0', 12, NORMAL),
                          (3, 'Chassis Serial', 'c', '1', 11, NORMAL),
                          (4, 'Chassis Extra', 'c', '2', 32, NORMAL),
                          (5, 'Board Mfg Date', 'NULL', 'NULL', 0, DISABLED),
                          (6, 'Board Mfg', 'b', '0', 12, DISABLED),
                          (7, 'Board Product', 'b', '1', 16, NORMAL),
                          (8, 'Board Serial', 'b', '2', 10, NORMAL),
                          (9, 'Board Part Number', 'b', '3', 12, NORMAL),
                          (10, 'Product Manufacturer', 'p', '0', 12, DISABLED),
                          (11, 'Product Name', 'p', '1', 32, NORMAL),
                          (12, 'Product Part Number', 'p', '2', 24, NORMAL),
                          (13, 'Product Version', 'p', '3', 6, NORMAL),
                          (14, 'Product Serial', 'p', '4', 24, NORMAL),
                          (15, 'Product Asset Tag', 'p', '5', 32, NORMAL),
                          (16, 'Product Extra', 'p', '7', 24, NORMAL )]

        strtime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        self.logFileName = "logs\\fru_edit_%s.log" % strtime
        logging.basicConfig(filename=self.logFileName, level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(module)s | %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S')
        logging.info("Logger initialized with file %s" % self.logFileName)
        self.logger = logging.getLogger()


if __name__ == '__main__':
    Setting()