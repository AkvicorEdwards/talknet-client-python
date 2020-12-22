
def uint16_to_bytes(val):
    b = bytearray(2)
    for i in range(0, 2):
        b[1 - i] = (val >> (i * 8)) & 0xff
    return b


def bytes_to_int(bt):
    val = 0
    for i in range(len(bt)):
        val = val << 8
        val += bt[i]
    return val


def int32_to_bytes(val):
    b = bytearray(4)
    for i in range(0, 4):
        b[3 - i] = (val >> (i * 8) & 0xff)
    return b


def int64_to_bytes(val):
    b = bytearray(8)
    for i in range(0, 8):
        b[7 - i] = (val >> (i * 8) & 0xff)
    return b
