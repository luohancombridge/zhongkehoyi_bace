# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#第一个为标题，中间为类名，最后为要输入的数据，列表格式
class  win_exe(object):
    def send(self,z):
        self.z=z
        self.par=win32gui.FindWindow(None,self.z[0])
        for i in self.z[1:-1]:
            self.par=win32gui.FindWindowEx(self.par, None, i, None)
            if self.par==0:
                print(44444)
                print(i)
        win32gui.SendMessage(self.par, win32con.WM_SETTEXT, None,self.z[-1])
    def click(self,u):
        self.z=u
        self.par=win32gui.FindWindow(None,self.z[0])
        for i in self.z[1:]:
            self.par=win32gui.FindWindowEx(self.par, None, i, None)
            if self.par==0:
                print(44444)
                print(i)
        win32gui.SendMessage(self.par, win32con.BM_CLICK, None, None)
if __name__=='__main__':
    s=win_exe()
    s.send(['打开','ComboBoxEx32','ComboBox','Edit','good_data'])
    s.click(['打开','Button'])
