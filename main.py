# 这里进行导入
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

import winlogin
import winmain
import tcp


# Receive message callback function
def p_message(uid, msg):
    # print("UUID:[%d] MSG:[%s]" % (uid, msg))
    child.chat.textBrowser.append("[RECV] <- UUID:[%d] MSG:[%s]" % (uid, msg))


# Send Message
def send():
    try:
        send_id = child.chat.lineEdit.text()
        mess = child.chat.textEdit.toPlainText()
        child.chat.textBrowser.append("[SEND] -> UUID:[%s] MSG:[%s]" % (send_id, mess))
        # print(send_id, mess)
        cli.send_message(int(send_id), mess)
    finally:
        return


# Login Request
def login(usr, pwd):
    res = False
    uuid = 0
    username = "ERROR"

    try:
        cli.connect('121.36.0.122', 7010)
        res, uuid, username, nickname = cli.login(usr, pwd)
    finally:
        if res:
            print("Login Successful")
            child.chat.textBrowser.append("UUID:[%d] Username:[%s]" % (uuid, username))
            cli.callback = p_message
            cli.start_receiver(p_message)
            return True
        else:
            print("Login Failure:", username)
            return False


# Get input username and password
# Call login
def log_in():
    login_user = window.main_ui.name.text()
    login_password = window.main_ui.password.text()
    # print(login_user, login_password)

    if login(login_user, login_password):
        window.hide()
        child.show()
    else:
        window.main_ui.waring.setVisible(1)


# Login Window
class ParentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.main_ui = Ui_MainWindow()
        self.main_ui = winlogin.Ui_loginWindow()
        self.main_ui.setupUi(self)


# Main Window
class ChildWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.chat = winmain.Ui_chatWindow()
        self.chat.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParentWindow()
    child = ChildWindow()
    cli = tcp.CLI()

    window.main_ui.waring.setVisible(0)
    window.main_ui.denglu.clicked.connect(log_in)
    child.chat.pushButton.clicked.connect(send)

    # 显示
    window.show()
    sys.exit(app.exec_())
