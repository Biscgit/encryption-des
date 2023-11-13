#!/usr/bin/python3
# by David Horvát, 2022
# example values by https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

import typing
from random import getrandbits

# text and key
text: int = 0b_0000_0001_0010_0011_0100_0101_0110_0111_1000_1001_1010_1011_1100_1101_1110_1111 or getrandbits(64)
key: int = 0b_00010011_00110100_01010111_01111001_10011011_10111100_11011111_11110001 or getrandbits(64)

# predefined values
pc_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]
pc_2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]
p_init = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]
p_reverse = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]
expand_48 = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]
s_boxes = [
    [
        14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
    ],
    [
        15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
    ],
    [
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
    ],
    [
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
    ],
    [
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
    ],
    [
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
    ],
    [
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
    ],
    [
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
    ]
]
s_permutation = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# shift keys by x: [rounds]
key_shift: dict[int: list[int]] = {
    1: [1, 2, 9, 16],
    2: [3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]
}


if __name__ == '__main__':
    print('DES Encryption v1.0 only using mathematical operations.\n')
    print(f'Initial Text: \t\t{text :064b}')
    print(f'Encryption Key: \t{key :064b}')

    # 1.
    # Initial permutation - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # ToDo: rewrite this without the need of "length"
    def shift_bits_to(binary: int, length: int, positions: list[int]) -> int:
        # shifts all bits from a number to a new position (left to right!)
        def execute() -> typing.Generator[int, None, None]:
            for i, position in enumerate(positions[::-1]):
                yield ((binary >> (length - position)) & True) << i

        return sum(execute())

    permuted_text = shift_bits_to(text, 64, p_init)

    # splitting the permuted text in the middle
    text_l, text_r = permuted_text >> 32, permuted_text % 2 ** 32

    # 2.
    # Generating 16 keys - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def generate_keys(base_key: int) -> typing.Generator[int, None, None]:
        shifting = [_ for _ in range(16)]
        for num, indexes in key_shift.items():
            for x in indexes:
                shifting[x - 1] = num

        # shifts bits by x to the left for the next key
        for x in shifting:
            base_key = shift_bits_to(base_key, 28, [y for y in range(x + 1, 29)] + [y for y in range(1, x + 1)])
            yield base_key

    # parity drop
    cipher_key = shift_bits_to(key, 64, pc_1)

    # generating C and D keys
    c_keys = [x for x in generate_keys(cipher_key >> 28)]
    d_keys = [x for x in generate_keys(cipher_key % 2 ** 28)]

    # compression p-box
    round_keys = [shift_bits_to((x << 28) + y, 56, pc_2) for x, y in zip(c_keys, d_keys)]

    # 3.
    # Encryption rounds - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def apply_s_box(binaries: list[int]) -> typing.Generator[int, None, None]:
        # looping over split bits and s-boxes backwards (from lowest to highest)
        for binary, box in zip(binaries[::-1], s_boxes[::-1]):
            inner_bits = (binary >> 1) % 2 ** 4
            outer_bits = (binary >> 5) * 2 + (binary & True)
            yield box[inner_bits + 16 * outer_bits]

    for round_key in round_keys:

        # a) Expansion - and -  b) Apply XOR to R and Key
        func = shift_bits_to(text_r, 32, expand_48) ^ round_key

        # c) s-boxes (splitting bits into 8 pairs and substituting them)
        split_bits = [(func >> (6 * x)) % 2 ** 6 for x in range(7, -1, -1)]
        func = sum([x << (4 * i) for i, x in enumerate(apply_s_box(split_bits))])

        # final post s-box permutation
        func = shift_bits_to(func, 32, s_permutation)

        # d) Apply XOR to R and L Data
        text_r, text_l = text_l ^ func, text_r

    # 4.
    # Inverse init permutation - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    encrypted_text = (text_r << 32) + text_l
    encrypted_text = shift_bits_to(encrypted_text, 64, p_reverse)

    print(f'\nEncrypted Text: \t{encrypted_text :064b}')
