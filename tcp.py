# pyuic5 main.ui -o MainWindow.py

import _thread
import socket

import defi
import package


class SEQ:
    def __init__(self):
        self.seq = 1

    def get(self):
        self.seq += 1
        return self.seq


class CLI:
    def __init__(self):
        self.callback = self._callback
        self.seq = SEQ()
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _callback(self, uid, msg):
        print("UUID: %d MSG: %s", uid, msg)

    def heartbeat(self, pk):
        pk.set_request_code(defi.HeartbeatRespond)
        pk.set_ack(pk.get_seq())
        pk.set_seq(self.seq.get())
        pk.set_time()
        pk.set_head_checksum()
        self.cli.send(pk.data)

    # receive message
    def receiver(self):
        while True:
            recv = self.cli.recv(1024)
            if len(recv) < package.Package.LengthHeadPackage:
                continue
            pack = package.convert_to_package(recv)
            if pack.get_request_code() == defi.HeartbeatRequest:
                self.heartbeat(pack)
                continue
            if pack.get_request_code() == defi.TerminateTheConnection:
                print("Server Terminate the connection")
                exit(0)
            uid, msg = package.unwrap_message(pack.get_head_data())
            self.callback(uid, msg)
            # print("UUID: %d [%s]" % (uid, msg))

    def connect(self, ip, port):
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli.connect((ip, port))

    def login(self, user, pwd):
        # Package 1
        pk = package.Package()
        pk.set_request_code(defi.HeartbeatRequest)
        pk.set_seq(self.seq.get())
        pk.set_head_checksum()
        self.cli.send(pk.data)

        recv = self.cli.recv(1024)
        package.convert_to_package(recv)

        pk.set_request_code(defi.Login)
        pk.set_seq(self.seq.get())
        pk.set_ack(0)
        pk.set_head_data(package.wrap_login_data(user, pwd))
        pk.set_head_checksum()
        self.cli.send(pk.data)

        recv = self.cli.recv(1024)
        pk = package.convert_to_package(recv)
        if pk.get_request_code() == defi.LoginSuccessful:
            uid, uname, pwd = package.unwrap_user_info(pk.get_head_data())
            return True, uid, uname, pwd
        else:
            return False, 0, pk.get_head_data().decode("utf-8"), ""

    def send_message(self, uid, message):
        if len(message) == 0:
            return
        pkg = package.Package()
        pkg.set_seq(self.seq.get())
        pkg.set_time()
        pkg.set_request_code(defi.Message)
        pkg.set_head_data(package.wrap_message(uid, message))
        pkg.set_head_checksum()
        self.cli.send(pkg.data)

    def start_receiver(self, callback):
        _thread.start_new_thread(self.receiver, ())


# def test():
#     cli = CLI()
#     cli.connect('121.36.0.122', 7010)
#
#     usr = input("Username: ")
#     pwd = input("Password: ")
#     res, uuid, username, nickname = cli.login(usr, pwd)
#
#     if res:
#         print("Login Successful")
#         cli.start_receiver()
#     else:
#         print("Login Failure:", username)
#         exit(1)
#
#     while True:
#         uuid = input("UUID: ")
#         if len(uuid) == 0:
#             continue
#         mess = input("Message: ")
#         if len(mess) == 0:
#             continue
#         try:
#             cli.send_message(uid=int(uuid), message=mess)
#         finally:
#             continue
