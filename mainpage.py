from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from subpage import *
import subprocess
from threading import Thread
import os, json

class MainPage:
    def __init__(self, master, config, ipmi, extraflag=False):
        self.root = master
        self.root.resizable(0, 0)
        self.cfg = config
        self.root.geometry("%dx%d" % (400, 540))
        self.ipmi = ipmi
        self.extraflag = extraflag
        self.labellist = self.cfg.labellist
        self.result = dict()
        self.__entrylist = list()
        self.creatpage()
        self.get_items()

    def creatpage(self):
        self.mpage = Frame(self.root)
        self.mpage.pack(expand=YES, fill=BOTH)
        self.mainmenu = Menu(self.root)
        self.binmenu = Menu(self.mainmenu)
        self.remenu = Menu(self.mainmenu)
        self.binmenu.add_command(label="Read Bin", command=self.readbin)
        self.binmenu.add_command(label="Write Bin", command=self.writebin)
        self.remenu.add_command(label="Recovery")
        self.remenu.add_command(label="Write Template")
        self.mainmenu.add_cascade(label="Bin", menu=self.binmenu)
        self.mainmenu.add_cascade(label="Recovery", menu=self.remenu)
        self.root['menu'] = self.mainmenu
        if not self.extraflag:
            self.labellist.pop()
        for row, name, field, index, length, state in self.labellist:
            Label(self.mpage, borderwidth=5, text=name + " :").grid(row=row, stick=E)
            self.__entrylist.append(StringVar())
            Entry(self.mpage, borderwidth=2, textvariable=self.__entrylist[row], state=state, width=25).grid(row=row,
                                                                                                        column=1)
            if state != DISABLED:
                a = Button(self.mpage, borderwidth=2, text="Modify",
                           command=lambda name=name, row=row, field=field, index=index, length=length: self.setitem(row,
                                                                                                                    name,
                                                                                                                    field,
                                                                                                                    index,
                                                                                                                    length)).grid(row=row, column=2)

        Button(self.mpage, text="Refresh", bd=5, command=self.get_items).grid(row=(len(self.labellist)+1), column=0, pady=20)
        Button(self.mpage, text="SetAll", bd=5, command=self.setall).grid(row=(len(self.labellist)+1), column=2)

    def setitem(self, row, name, field, index, length, flag=True):
        value = self.__entrylist[row].get()
        self.cfg.logger.info("Begin set %s : %s ........." % (name, value))
        if len(value) > length and row != 1:
            self.cfg.logger.warning("Warning", "Your Input is too long ( %s Characters )!\n The max length is %s Characters" % (
                len(value), length))
            showwarning("Warning", "Your Input is too long ( %s Characters )!\n The max length is %s Characters" % (
                len(value), length))
            return
        else:
            text = value + (length - len(value)) * " "
            cmd = "%s fru edit 0 field %s %s '%s'" % (self.ipmi, field, index, text)
            self.cfg.logger.info("Running " + cmd)
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            stdout, stderr = res.communicate()
            if flag:
                if stderr:
                    self.cfg.logger.error(stderr)
                    self.cfg.logger.error("%s flash fail ..." % name)
                    showinfo(title="Error", message="%s flash fail ..." % name)
                else:
                    self.cfg.logger.info(stdout)
                    showinfo(title="info", message="%s flash pass ..." % name)
            else:
                if stderr:
                    self.cfg.logger.error(stderr)
                    self.cfg.logger.error("%s flash fail ..." % name)
                    self.result[name] = 'fail'
                else:
                    self.cfg.logger.info(stdout)
                    self.result[name] = 'pass'

    def setall(self):
        self.result.clear()
        threadlist = []
        for row, name, field, index, length, state in self.labellist:
            if state != DISABLED:
                t = Thread(self.setitem(row, name, field, index, length, False))
                t.start()
                threadlist.append(t)
        for t in threadlist:
            t.join()
        self.cfg.logger.info("Flash all items Result.................")
        self.cfg.logger.info(json.dumps(self.result, indent=4))
        with open("logs\\result.log", 'w') as fp:
            json.dump(self.result, fp,  indent=4)
        if "fail" in self.result.values():
            self.cfg.logger.error("Flash .......... [ Fail ]")
            showinfo(title="Fail", message="Flash fail, Check detail result from logs/result.log")
        else:
            self.cfg.logger.info("Flash  .......... [ Pass ]")
            showinfo(title="Pass", message="Flash successful, Check detail result from logs/result.log")

    def getfru(self):
        cmd = self.ipmi+"fru list 0"
        self.cfg.logger.info(cmd)
        subpro = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        stdout, stderr = subpro.communicate()
        if not subpro.returncode:
            self.cfg.logger.info(stdout)
            fru = stdout.decode('utf-8')
            return fru
        else:
            self.cfg.logger.error(stderr)
            raise RuntimeError("Get Fru fail !!")

    def get_items(self):
        try:
            fruinfo = self.getfru()
            # print(fruinfo)
            row = 1
            for line in fruinfo.split('\n'):
                # print("line: "+line)
                if line:
                    value = line.split(':', 1)[1].strip()
                    self.__entrylist[row].set(value)
                    row += 1
        except RuntimeError as e:
            showerror(message=str(e))

    def readbin(self):
        file = asksaveasfilename()
        if file:
            cmd = self.ipmi + "fru read 0 %s" % file
            self.cfg.logger.info("Running : " + cmd)
            subpro = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            stdout, stderr = subpro.communicate()
            if subpro.returncode:
                self.cfg.logger.error(stderr)
                showerror(message="Read fru bin fail")

    def writebin(self):
        file = askopenfilename()
        if file:
            cmd = self.ipmi + "fru write 0 %s" % file
            self.cfg.logger.info("Running : " + cmd)
            subpro = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            stdout, stderr = subpro.communicate()
            if subpro.returncode:
                self.cfg.logger.error(stderr)
                showerror(message="Write fru bin fail")

    def recovery(self):
        self.cfg.logger.info("Begin recovery fru ......")
        self.recovery = self.cfg.recovery.copy()
        if not self.extraflag:
            self.recovery.pop()
            self.recovery.pop()
        for addr, value in self.recovery.items():
            cmd = "%s %s %s %s" % (self.ipmi, self.cfg.fru_write_command, addr, value)
            self.cfg.logger.info("Running command: %s " % cmd)
            try:
                subpro = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
                stdout, stderr = subpro.communicate()
                if not subpro.returncode:
                    self.cfg.logger.info(stdout)
                else:
                    self.cfg.logger.error(stderr)
                    raise RuntimeError("Excute command %s ----- [ Fail ]" % cmd)
            except Exception as e:
                self.cfg.logger.error(str(e))
                showwarning("Recovery fru fail!!!")

if __name__ == '__main__':
    from config import Setting
    root = Tk()
    root.title("Fru edit")
    config = Setting()
    MainPage(root, config, 'E:\\python_pycharm\\fru_edit_v2\\tools\\win64\\ipmitool-1.8.18-lan\\ipmitool.exe')
    root.mainloop()