from tkinter import *
from tkinter.messagebox import *
import ipaddress, os, subprocess
from mainpage import MainPage


class LoginPage(object):
    def __init__(self, master=None, config=None):
        self.root = master  # 定义内部变量root
        self.root.resizable(0, 0)
        self.cfg = config
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.ipaddr = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.tool = self.cfg.tool
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='IP   :').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.ipaddr).grid(row=1, column=1, stick=E)
        Label(self.page, text='账户: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=3, column=1, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=4, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=4, column=1, stick=E)


    def chk_ip(self, ipaddr):
        try:
            ipaddress.ip_address(ipaddr)
        except ValueError as e:
            self.cfg.logger.warning(str(e))
            showinfo(title="Error", message=str(e))
            return False
        self.cfg.logger.info("Running ping -n 1 %s" % ipaddr)
        if not subprocess.call("ping -n 1 %s" % ipaddr):
            return True
        else:
            self.cfg.logger.warning("Ping %s fail, Please check it!" % ipaddr)
            showinfo(title="Warning", message="Ping %s fail, Please check it!" % ipaddr)
            return False

    def loginCheck(self):
        ipaddr = self.ipaddr.get()
        name = self.username.get()
        secret = self.password.get()
        ipflag = self.chk_ip(ipaddr)
        if ipflag:
            if not name or not secret:
                self.cfg.logger.warning("用户名或密码为空")
                showinfo(title="Warning", message="用户名或密码为空")
            elif not subprocess.call(self.tool+" -H %s -U %s -P %s raw 6 1" % (ipaddr, name, secret)):
                self.ipmi = self.tool+" -H %s -U %s -P %s " % (ipaddr, name, secret)
                self.cfg.logger.info(self.ipmi)
                # try:
                cmd = self.ipmi + "fru list 0"
                self.cfg.logger.info(cmd)
                try:
                    subpro = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = subpro.communicate()
                    if not subpro.returncode:
                        self.cfg.logger.info(stdout)
                        self.page.destroy()
                        if re.search("Product Extra", stdout.decode('utf-8')):
                            self.extraflag = True
                        else:
                            self.extraflag = False
                    else:
                        self.cfg.logger.error(stderr)
                        self.cfg.logger.error("Get fru fail")
                        showwarning(message="Get fru fail!!")
                except Exception as e:
                    showinfo(message=str(e))
                else:
                    print(self.extraflag)
                    MainPage(self.root, self.cfg, self.ipmi, self.extraflag)
            else:
                showinfo(title="Warning", message="BMC over lan fail, Please check it!")


if __name__ == '__main__':
    root = Tk()
    root.title("Fru Edit")
    LoginPage(root)
    root.mainloop()