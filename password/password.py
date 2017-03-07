#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
from PyQt4 import uic, QtGui, QtCore
from PyQt4.QtGui import QPixmap, QApplication, QIcon
from PyQt4.QtCore import QTextCodec, QRegExp
import locale
import re


code = QTextCodec.codecForName("utf-8")
QTextCodec.setCodecForTr(code)
    
QTextCodec.setCodecForLocale(QTextCodec.codecForLocale())
QTextCodec.setCodecForCStrings(QTextCodec.codecForLocale())

class PageKde(QtGui.QWidget):
    def __init__(self):
        super(PageKde, self).__init__()
        self.initUi();

    def initUi(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Test')
        self.setWindowIcon(QIcon('test.png'))
        self.cdir = os.getcwd() + '/mainwindow.ui'
        self.page = uic.loadUi(self.cdir)

        warningIcon = QPixmap("/usr/share/icons/Windows7-iSoft/status/22/dialog-warning.png")
        
        self.page.comboBox.addItem("中文")
        self.page.comboBox.addItem(self.tr("英文"))

        self.page.username.setPlaceholderText(self.tr("输入用户名"))
        self.page.fullname.setPlaceholderText(self.tr("输入别名"))
        
        self.page.pwd.setText(self.tr("密码"))
        self.page.password.setPlaceholderText(self.tr("请输入密码"))
        self.page.password.setEnabled(True)
        self.page.pwd_err.setPixmap(warningIcon)
        self.page.password.setToolTip(self.tr("新密码格式：\n1.密码不包含中文;\n2.密码长度8-20;"\
                "\n3.密码应包含小写字符;\n4.密码应包含大写字符;\n5.密码应包含数字."))
        
        self.page.vfdpwd.setText(self.tr("确认密码"))
        self.page.verified_password.setPlaceholderText(self.tr("请输入确认密码"))
        self.page.verified_password.setEnabled(False)
        self.page.vfdpwd_err.setPixmap(warningIcon)


        self.page.password.textChanged[str].connect(self.on_password_changed)
        self.page.verified_password.textChanged[str].connect(self.on_verified_password_changed)

        self.clear_errors()
        self.page.show()

    def on_password_changed(self):
        username = self.get_username()
        realname = self.get_fullname()
        new_password = self.get_password()
        confirm_password = self.get_verified_password()
        if new_password != confirm_password:
            self.vfdpwd_error(self.tr("确认密码与密码不相同"))
        else:
            self.page.vfdpwd_err.hide()
            self.page.vfdpwd_err_msg.hide()
        if self.password_check_contain_zh_cn(new_password) == True:
            self.page.password.setText("")
            self.password_error(self.tr("密码不能有中文!"))
            self.page.verified_password.setEnabled(False)
        
        elif self.password_len(new_password) != True:
            self.password_error(self.tr("密码长度8-20"))
            self.page.verified_password.setEnabled(False)
        
        elif self.password_check_username(username, new_password) == True:
            self.password_error(self.tr("密码不能和用户名相同"))
            self.page.verified_password.setEnabled(False)
        
        elif self.password_check_realname(realname, new_password) == True: 
            self.password_error(self.tr("密码不能和用户别名相同"))
            self.page.verified_password.setEnabled(False)
        
        elif self.password_check_contain_lower(new_password) != True:
            self.password_error(self.tr("密码应包含小写字符"))
            self.page.verified_password.setEnabled(False)
        
        elif self.password_check_contain_upper(new_password) != True:
            self.password_error(self.tr("密码应包含大写字符"))
            self.page.verified_password.setEnabled(False)
        
        elif self.password_check_contain_num(new_password) != True:
            self.password_error(self.tr("密码应包含数字"))
            self.page.verified_password.setEnabled(False)
            
        else:
            self.page.pwd_err.hide()
            self.page.pwd_err_msg.setText(self.tr("密码可用"))
            self.page.verified_password.setEnabled(True)
            if new_password != confirm_password:
                self.vfdpwd_error(self.tr("确认密码与密码不相同"))
            else:
                self.page.vfdpwd_err.hide()
                self.page.vfdpwd_err_msg.setText(self.tr("密码可用"))
                self.page.vfdpwd_err_msg.show()

    def on_verified_password_changed(self):
        new_password = self.get_password()
        confirm_password = self.get_verified_password()
        if new_password != confirm_password:
            self.vfdpwd_error(self.tr("确认密码与密码不相同"))
        else:
            self.page.vfdpwd_err.hide()
            self.page.vfdpwd_err_msg.setText(self.tr("密码可用"))
            self.page.vfdpwd_err_msg.show()
        

    def clear_errors(self):
        self.page.pwd_err.hide()
        self.page.vfdpwd_err.hide()
        self.page.pwd_err_msg.hide()
        self.page.vfdpwd_err_msg.hide()

    def password_error(self, msg):
        self.page.pwd_err_msg.setText(msg)
        self.page.pwd_err.show()
        self.page.pwd_err_msg.show()

    def vfdpwd_error(self, msg):
        self.page.vfdpwd_err_msg.setText(msg)
        self.page.vfdpwd_err.show()
        self.page.vfdpwd_err_msg.show()
   
    def password_len(self, password):
        return 8 <= len(password) <= 20

    def password_check_contain_upper(self, password):
        pattern = re.compile('[A-Z]+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False

    def password_check_contain_num(self,password):
        pattern = re.compile('[0-9]+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False
    def password_check_contain_zh_cn(self,password):
        if password.contains(QRegExp("[\\x4e00-\\x9fa5]+")):
            return True
        else:
            return False

    def password_check_contain_lower(self, password):
        pattern = re.compile('[a-z]+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False

    def password_check_symbol(self, password):
        pattern = re.compile('([^a-z0-9A-Z])+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False

    def password_check_username(self, username, password):
        if(username == password):
            return True
        else:
            return False
    def password_check_realname(self,realname, password):
        if(realname == password):
            return True
        else:
            return False

    def get_password(self):
        return self.page.password.text()
    
    def get_verified_password(self):
        return self.page.verified_password.text()

    def get_username(self):
        return self.page.username.text()

    def get_fullname(self):
        return self.page.fullname.text()


def main():

    app = QApplication(sys.argv)
    ex = PageKde()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()    
