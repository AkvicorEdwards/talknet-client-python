import zlib, time
import defi
import util


def wrap_login_data(username, password):
    data = bytearray(182)
    usr = bytes(username, encoding="utf8")
    pas = bytes(password, encoding="utf8")

    data[defi.LoginDataOffsetUsernameLength] = len(usr)
    data[defi.LoginDataOffsetPasswordLength] = len(pas)

    for i in range(len(usr)):
        data[defi.LoginDataOffsetUsername + i] = usr[i]

    for i in range(len(pas)):
        data[defi.LoginDataOffsetPassword + i] = pas[i]

    return data


def unwrap_user_info(data):
    return util.bytes_to_int(data[defi.UserInfoOffsetUUID:defi.UserInfoOffsetUUID + defi.UserInfoLengthUUID]), data[
            defi.UserInfoOffsetUsername:defi.UserInfoOffsetUsername + data[defi.UserInfoOffsetUsernameLength]].decode(
                "utf-8"), data[
            defi.UserInfoOffsetNickname:defi.UserInfoOffsetNickname + data[defi.UserInfoOffsetNicknameLength]].decode(
                "utf-8")


def wrap_message(uuid, message):
    data = bytearray(Package.LengthHeadData)
    user = util.int32_to_bytes(uuid)
    mess = bytes(message, encoding="utf8")
    data[defi.MessageOffsetMessageLength] = len(mess)
    for i in range(len(user)):
        data[defi.MessageOffsetUUID + i] = user[i]
    for i in range(len(mess)):
        data[defi.MessageOffsetMessage + i] = mess[i]
    return data


def unwrap_message(data):
    return (util.bytes_to_int(data[defi.MessageOffsetUUID:defi.MessageOffsetUUID + defi.MessageLengthUUID]),
            data[defi.MessageOffsetMessage:defi.MessageOffsetMessage + data[defi.MessageOffsetMessageLength]].decode(
                "utf-8"))


def convert_to_package(data):
    p = Package()
    if len(data) < Package.LengthHeadPackage:
        print("Error: convert_to_package")
        return p
    for i in range(Package.LengthHeadPackage):
        p.data[i] = data[i]
    return p


class Package:
    LengthHeadPackage = 210
    OffsetRequestCode = 0
    LengthRequestCode = 2
    OffsetSEQ = 2
    LengthSEQ = 4
    OffsetACK = 6
    LengthACK = 4
    OffsetTime = 10
    LengthTime = 8
    OffsetExtendedDataFlag = 18
    LengthExtendedDataFlag = 1
    OffsetHeadDataLength = 19
    LengthHeadDataLength = 1
    OffsetHeadData = 20
    LengthHeadData = 182
    OffsetExtendedDataHash = 202
    LengthExtendedDataHash = 4
    OffsetHash = 206
    LengthHash = 4

    def __init__(self):
        self.data = bytearray(210)

    def set_seq(self, seq):
        conv = util.int32_to_bytes(seq)
        for i in range(len(conv)):
            self.data[self.OffsetSEQ + i] = conv[i]

    def get_seq(self):
        return util.bytes_to_int(self.data[self.OffsetSEQ:self.OffsetSEQ + self.LengthSEQ])

    def set_ack(self, ack):
        conv = util.int32_to_bytes(ack)
        for i in range(len(conv)):
            self.data[self.OffsetACK + i] = conv[i]

    def get_ack(self):
        return util.bytes_to_int(self.data[self.OffsetACK:self.OffsetACK + self.LengthACK])

    def set_time(self):
        a = int(time.time_ns())
        conv = util.int64_to_bytes(a)
        for i in range(len(conv)):
            self.data[self.OffsetTime + i] = conv[i]

    def set_request_code(self, val):
        co = util.uint16_to_bytes(val)
        for i in range(0, 2):
            self.data[self.OffsetRequestCode + i] = co[i]

    def get_request_code(self):
        return util.bytes_to_int(self.data[self.OffsetRequestCode:self.OffsetRequestCode + self.LengthRequestCode])

    def set_head_checksum(self):
        ha = 0
        ha = zlib.crc32(self.data[:206], ha)
        conv = util.int32_to_bytes(ha)

        for i in range(0, 4):
            self.data[self.OffsetHash + i] = conv[i]

    def set_head_data(self, data):
        self.data[self.OffsetHeadDataLength] = len(data)

        for i in range(len(data)):
            self.data[self.OffsetHeadData + i] = data[i]

    def get_head_data(self):
        return self.data[self.OffsetHeadData:self.OffsetHeadData + self.LengthHeadData]

    def get_data(self):
        return self.data
