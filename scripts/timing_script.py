import timeit

_test_ = 'mean_avg'
number = 1000000

if _test_ == 'mean_avg':
    from statistics import mean
    def lib_mean(L):
        return mean(L)

    def naive_mean(L):
        return sum(L) / len(L)

    import numpy as np
    def np_mean(L):
        return np.average(np.array(L))

    def for_append(L):
        l = []
        for i in L:
            l.append(i)
        return sum(l) / len(l)

    def for_add(L):
        c = 0
        s = 0
        for i in L:
            c += 1
            s += i
        return s / c

    L = list(range(4000))
    stmt = '_mean(L)'

    setups = [
        'from __main__ import L; from __main__ import naive_mean as _mean',
        'from __main__ import L; from __main__ import for_append as _mean',
        'from __main__ import L; from __main__ import for_add as _mean',
    ]
    number = 1000

elif _test_ == 'for_range':
    def range_for(l: list):
        last_d = None
        diffs = []
        for d in l:
            try:
                diffs.append(d - last_d)
            except Exception:
                pass
            last_d = d
        return diffs

    def enum_for(l: list):
        diffs = []
        for i, d in enumerate(l):
            try:
                diffs.append(d-l[i-1])
            except Exception:
                pass
        return diffs

    def idx_for(l: list):
        diffs = []
        for i in range(len(l)):
            try:
                diffs.append(l[i]-l[i-1])
            except Exception:
                pass
        return diffs

    rl = list(range(2000))

    stmt = "floop(rl)"

    setups = [
        "from __main__ import rl; from __main__ import range_for as floop",
        "from __main__ import rl; from __main__ import enum_for as floop",
        "from __main__ import rl; from __main__ import idx_for as floop",
    ]
    number = 1000


elif _test_ == 'bytes':
    import operator
    def bxor(b1, b2):
        result = b""
        for b1, b2 in zip(b1, b2):
            result += bytes([b1 ^ b2])
        return result

    def bxor_join(b1, b2):
        parts = []
        for b1, b2 in zip(b1, b2):
            parts.append(bytes([b1 ^ b2]))
        return b''.join(parts)

    def bxor_ba(b1, b2):
        result = bytearray()
        for b1, b2 in zip(b1, b2):
            result.append(b1 ^ b2)
        return result

    def bxor_map(b1, b2):
        return bytes(map(operator.xor, b1, b2))

    b1 = b'abcdefg' * 1000
    b2 = b'1234567' * 1000
    number = 100

    stmt = 'it(b1,b2)'

    setups = [
        #"from __main__ import b1,b2; from __main__ import bxor as it",
        # "from __main__ import b1,b2; from __main__ import bxor_join as it",
        "from __main__ import b1,b2; from __main__ import bxor_ba as it",
        "from __main__ import b1,b2; from __main__ import bxor_map as it",
    ]

elif _test_ == 'unpack_int':
    from struct import unpack
    # ------------------------------------------------------------------------------
    def up(data):
        return unpack('>l', data)[0]

    # ------------------------------------------------------------------------------
    def ifb(data):
        return int.from_bytes(data, byteorder='big', signed=False)

    data = b'\x00\x11\x22\x33'
    stmt = 'ui(data)'
    setups = [
        'from struct import unpack;from __main__ import data; from __main__ import up as ui',
        'from __main__ import data; from __main__ import ifb as ui',
    ]
    number = 1000
    # timeit.timeit("unpack('>l', data)[0]", 'from __main__ import data; from struct import unpack')
    # 0.1647498442748656
    # timeit.timeit("int.from_bytes(data, byteorder=\'big\', signed=False)", 'from __main__ import data')
    # 0.6380259364794938
elif _test_ == 'escape':
    def send_escape(data):
        yield data[0]
        for b in data[1:-1]:
            if b in (ord(')'), ord('('), 0x3d):
                yield 0x3d
                yield b^0x3d
            else:
                yield b
        yield data[-1]

    def send_escape_2(data):
        yield data[0]
        for b in data[1:-1]:
            if b not in (ord(')'), ord('('), 0x3d):
                yield b
            else:
                yield 0x3d
                yield b^0x3d
        yield data[-1]

    data = b'(DP6\x00\x90a \x84\x004\x01\x01?"\x05\x17\t2)C\x17wQ\x00\x15#@s\x12\x98\t\x0f\x00\x00\x04\xec\x00\x10\x01\x00;\x84\x1e\x9c\x16\xb0I\x90N\x00\x00\x00\x8a\x00\x00\xff\x00\x008\x00\xff\xfc\x1e)'
    stmt = 'escape(data)'

    setups = [
        'from __main__ import data; from __main__ import send_escape as escape',
        'from __main__ import data; from __main__ import send_escape_2 as escape',
    ]

elif _test_ == 'decode_bcd':
    import binascii
    from binascii import hexlify
    from functools import reduce

    # ------------------------------------------------------------------------------
    def bcdDecode(chars):
        for char in chars:
            for val in (char >> 4, char & 0xF):
                if val >= 0xA:
                    return
                yield val


    # ------------------------------------------------------------------------------
    def asmDigits(digits, base=10):
        return reduce(lambda x, y: x*base+y, digits)

    # ------------------------------------------------------------------------------
    def hexify(data):
        return binascii.hexlify(data).decode('ascii').strip('0')
    
    # ------------------------------------------------------------------------------
    def ihex(data):
        return data.hex().strip('0')
    

    def hex_f_parse_loc(data):
        parsedData = {}

        lat_d = int(hexlify(data[6:7]))
        lat_m = int(hexlify(data[7:10]))
        parsedData['lat'] = lat_d + round(lat_m/600000, 6) #convert to degree

        lng_d = int(hexlify(data[10:12])) * 0.1
        lng_m = int(hexlify(data[12:14])) + lng_d % 1 * 100000
        parsedData['lng'] = (lng_d + round(lng_m/60000, 5))  #convert to degree

        parsedData['spd'] = int(hexlify(data[14:16])) * 0.1
        parsedData['crs'] = int(hexlify(data[16:18]))
        parsedData['alt'] = int(hexlify(data[18:20]))

        return parsedData


    def hex_parse_loc(data):
        parsedData = {}

        lat_d = int(hexlify(data[6:7]))
        lat_m = int(hexlify(data[7:10]))
        parsedData['lat'] = lat_d + round(lat_m/600000, 6) #convert to degree

        lng_d = int(hexlify(data[10:12])) * 0.1
        lng_m = int(hexlify(data[12:14])) + lng_d % 1 * 100000
        parsedData['lng'] = (lng_d // 1 + round(lng_m/60000, 5)) #convert to degree

        parsedData['spd'] = int(hexlify(data[14:16])) * 0.1
        parsedData['crs'] = int(hexlify(data[16:18]))
        parsedData['alt'] = int(hexlify(data[18:20]))

        return parsedData


    def mix_parse_loc(data):
        parsedData = {}

        lat_d = int(hexlify(data[6:7]))
        lat_m = int(hexlify(data[7:10]))
        parsedData['lat'] = lat_d + round(lat_m/600000, 6) #convert to degree

        digit_list = list(bcdDecode(data[10:14]))
        lng_d = asmDigits(digit_list[:3])
        lng_m = asmDigits(digit_list[3:8])
        parsedData['lng'] = lng_d + round(lng_m/60000, 5) #convert to degree

        parsedData['spd'] = int(hexlify(data[14:16])) * 0.1
        parsedData['crs'] = int(hexlify(data[16:18]))
        parsedData['alt'] = int(hexlify(data[18:20]))

        return parsedData


    def parse_gps_loc(data):
        parsedData = {}
        # BCD part
        digit_list = list(bcdDecode(data[:20]))

        lat_d = asmDigits(digit_list[12:14])
        lat_m = asmDigits(digit_list[14:20])
        parsedData['lat'] = lat_d + round(lat_m/600000, 6) #convert to degree

        lng_d = asmDigits(digit_list[20:23])
        lng_m = asmDigits(digit_list[23:28])
        parsedData['lng'] = lng_d + round(lng_m/60000, 5) #convert to degree

        parsedData['spd'] = asmDigits(digit_list[28:32]) * 0.1
        parsedData['crs'] = asmDigits(digit_list[32:36])
        parsedData['alt'] = asmDigits(digit_list[36:40])

        return parsedData



    # ------------------------------------------------------------------------------
    def mil_asm(data):
        return asmDigits(data[21:24], base=0x100) * 0.1

    # ------------------------------------------------------------------------------
    def mil_asm_d(data):
        return asmDigits(data[21:24], base=0x100) / 10

    # data = b'\x00\x00\x08b\x15\x102\x037\x95'
    data = b'\x17\x05\x18\x154Q"5$\x06\x115\x15\x02\x00\x00\x00\x00\x00\x00\xfc\x00\x00\x00\x00\x00t\x1a\x00\x00\x00\x00'

    # stmt = 'decode_bcd(data)'
    stmt = 'parse_loc(data)'

    setups = [
        'from __main__ import data; import binascii; from __main__ import hex_parse_loc as parse_loc;',
        'from __main__ import data; import binascii; from __main__ import mix_parse_loc as parse_loc;',
        'from __main__ import data; from functools import reduce; from __main__ import bcdDecode, asmDigits; from __main__ import parse_gps_loc as parse_loc;',
    ]
    stmt = 'mil(data)'
    setups = [
        'from __main__ import data; from functools import reduce; from __main__ import asmDigits; from __main__ import mil_asm as mil;',
        'from __main__ import data; from functools import reduce; from __main__ import asmDigits; from __main__ import mil_asm_d as mil;',
    ]

    number = 100000
    pass

elif _test_ == 'crc':
    from functools import reduce
    from operator import xor
    import operator
    import random

    def crc_for_naive(data: bytes)-> int:
        crc = 0
        for d in data:
            crc = crc ^ d
        return crc

    def crc_for(data: bytes)-> int:
        crc = 0
        for d in data:
            crc ^= d
        return crc

    def crc_reduce_lambda(data: bytes)-> int:
        return reduce(lambda x, y: x ^ y, data)

    def crc_reduce_op(data: bytes)-> int:
        return reduce(xor, data)

    def crc_reduce_opg(data: bytes)-> int:
        return reduce(operator.xor, data)


    data = bytes(random.randint(0, 255) for i in range(529))

    stmt = 'crc(data)'
    setups = [
        'from __main__ import data; from __main__ import crc_for_naive as crc',
        'from __main__ import data; from __main__ import crc_for as crc',
        'from __main__ import data; from functools import reduce; from __main__ import crc_reduce_lambda as crc',
        'from __main__ import data; from functools import reduce; from operator import xor; from __main__ import crc_reduce_op as crc',
        'from __main__ import data; from functools import reduce; import operator; from __main__ import crc_reduce_op as crc',
    ]
    number = 20000
    pass

elif _test_ == 'struct':
    from struct import unpack
    import struct

    def gup(data: bytes)-> int:
        return unpack('>h',data[0:2])[0]

    def dup(data: bytes)-> int:
        return struct.unpack('>h',data[0:2])[0]

    def bop(data: bytes)-> int:
        return (data[0]<<8|data[1])

    def bopa(data: bytes)-> int:
        return (data[0]<<8+data[1])

    def taop(data: bytes)-> int:
        return (data[0]*256+data[1])

    data = b'\xff\xff'
    stmt = 'upack(data)'

    setups = [
        'from __main__ import data; from struct import unpack; from __main__ import gup as upack',
        'from __main__ import data; import struct; from __main__ import dup as upack',
        'from __main__ import data; from __main__ import bop as upack',
        'from __main__ import data; from __main__ import bopa as upack',
        'from __main__ import data; from __main__ import taop as upack',
    ]
    pass

elif _test_ == 'str_cat':
    import string
    import random
    def randomstring(size=20, chars=string.ascii_uppercase + string.digits):
        return ''.join((random.choice(chars) for _ in range(size)))

    from functools import reduce
    from operator import add

    # ------------------------------------------------------------------------------
    def str_add(strings: list) -> str:
        return reduce(add, strings)

    # ------------------------------------------------------------------------------
    def str_join(strings: list) -> str:
        return ''.join(strings)

    # ------------------------------------------------------------------------------
    def str_mod_format(strings: list) -> str:
        return '%s' * len(strings) % tuple(strings)

    # ------------------------------------------------------------------------------
    def str_format(strings: list) -> str:
        return ('{}' * len(strings)).format(*strings)

    strings = [randomstring(random.randint(12, 20)) for _ in range(100)]
    number = 100000

    stmt = 'cat_str(strings)'
    setups = [
        'from __main__ import strings; from functools import reduce; from operator import add; from __main__ import str_add as cat_str',
        'from __main__ import strings; from __main__ import str_join as cat_str',
        'from __main__ import strings; from __main__ import str_mod_format as cat_str',
        'from __main__ import strings; from __main__ import str_format as cat_str',
        # 'from __main__ import strings; from __main__ import __ as cat_str',
    ]
    pass

for setup in setups:
    print(timeit.timeit(stmt, setup, number=number))
