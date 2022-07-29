import struct
import math
from Crypto.Cipher import AES




def ENC_AES(password: bytearray, text: bytearray):
    iv = b'1234567812345678'
    aes = AES.new(password, AES.MODE_CBC, iv)
    en_text = aes.encrypt(text)


def Final_ni(h1: bytes):
    Lines = [
        bytearray(h1[i * 16:16 + i * 16])
        for i in range(8)
    ]

    ADD(Lines[0], Lines[4])
    XOR(Lines[4], Lines[5])
    XOR(Lines[0], Lines[1])
    ADD(Lines[5], Lines[7])
    ADD(Lines[1], Lines[3])
    ADD(Lines[4], Lines[6])
    ADD(Lines[0], Lines[2])
    XOR(Lines[0], Lines[1])
    ADD(Lines[4], Lines[5])
    ENC_AES(Lines[3], Lines[0])
    XOR(Lines[3], Lines[5])
    ADD(Lines[0], Lines[4])
    XOR(Lines[3], Lines[5])
    ENC_AES(Lines[7], Lines[3])

    return Lines


def MEOW(input_bytes: bytes, h1: bytes):
    Lines1 = Final_ni(h1)

    def meow_mix_reg(i, reads):
        Lines1 = Final_ni(h1)
        XOR(Lines1[0], Lines1[2])
        ADD(Lines1[1], reads[2])
        ENC_AES(Lines1[3], Lines1[0])
        XOR(Lines1[3], reads[0])
        ADD(Lines1[5], reads[0])
        ENC_AES(Lines1[7], Lines1[3])

    get_lane = lambda i: Lines1[i % 8]

    def meow_mix(i, block):
        meow_mix_reg(i, [
            block[offset: offset + 16] for offset in (15, 0, 1, 16)
        ])

    def meow_mix_funky(i, block):
        meow_mix_reg(i, (
            b"\0" + block[:15], block[:16], block[17:] + block[:1], block[16:],
        ))

    original_length = len(input_bytes)
    target_length = ((len(input_bytes) // 32) + 1) * 32
    input_bytes += b"\0" * (target_length - original_length)


    input_bytes, tail_block = input_bytes[:-32], input_bytes[-32:]

    off = 0
    while off + 256 <= len(input_bytes):
        for _ in range(8):
            meow_mix(0, input_bytes[off: off + 32])
            off += 32

    meow_mix_funky(0, tail_block)
    message_length_block = struct.pack("<QQQQ", 0, 0, original_length, 0)
    meow_mix_funky(1, message_length_block)

    while off + 32 <= len(input_bytes):
        meow_mix(2 + off // 32, input_bytes[off: off + 32])
        off += 32

    print(bytes(Lines1[0]).hex(), Lines1[1].hex())
    print(bytes(Lines1[2]).hex(), Lines1[3].hex())
    print(bytes(Lines1[4]).hex(), Lines1[5].hex())
    print(bytes(Lines1[6]).hex(), Lines1[7].hex())


def ADD(a: bytearray, b: bytearray):
    mask64 = 2 ** 64 - 1
    a0, a1 = struct.unpack("<QQ", a)
    b0, b1 = struct.unpack("<QQ", b)
    a[:] = struct.pack("<QQ", (a0 + b0) & mask64, (a1 + b1) & mask64)


def XOR(a: bytearray, b: bytearray):
    for i in range(16):
        a[i] ^= b[i]




origin_m = "201900161096 tianguoxin"
m = bytes(
   origin_m, encoding='utf-8')





h = bytes(("sdu_cst_20220610" "Arbitrary value1.""Arbitrary value2.""Arbitrary value3.""Arbitrary value4.""Arbitrary value5.""Arbitrary value6.""Arbitrary value7."), encoding='utf-8')  
print("目标密文为：sdu_cst_20220610")
print("明文：",origin_m )
print("key：")
MEOW(m, h)
