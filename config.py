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

        self.recovery = {
            '0x00 0x00': '0x01 0x01 0x0B 0x14 0x1C 0x00 0x00 0xC3',
            '0x08 0x00': '0x01 0x0A',
            '0x57 0x00': '0xF5',
            '0x58 0x00': '0x01 0x09 0x17 0xCC',
            '0x68 0x00': '0xCB',
            '0x74 0x00': '0xE0',
            '0x95 0x00': '0xC8',
            '0x9E 0x00': '0xC1',
            '0xA0 0x00': '0x01 0x08 0x00',
            '0xA6 0x00': '0xCC',
            '0xB3 0x00': '0xD0',
            '0xC4 0x00': '0xCA',
            '0xCF 0x00': '0xCC',
            '0xDC 0x00': '0xC0 0xC1 0x00',
            '0xE0 0x00': '0x01 0x24 0x00 0xCC',
            '0xF0 0x00': '0xE0',
            '0x11 0x01': '0xD8',
            '0x2A 0x01': '0xC6',
            '0x31 0x01': '0xD8',
            '0x4A 0x01': '0xE0',
            '0x6B 0x01': '0xC0 0xC1',
            # product extra
            '0x6B 0x01': '0xC0 0xD8',
            '0x85 0x01': '0xC1',
        }

        # fru write/read command for arbok
        self.fru_write_command = 'raw 0x0a 0x12 0x00 '
        self.fru_read_command = 'raw 0x06 0x52 0x07 0xa6 '

        strtime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        self.logFileName = "logs\\fru_edit_%s.log" % strtime
        logging.basicConfig(filename=self.logFileName, level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(module)s | %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S')
        logging.info("Logger initialized with file %s" % self.logFileName)
        self.logger = logging.getLogger()


if __name__ == '__main__':
    Setting()