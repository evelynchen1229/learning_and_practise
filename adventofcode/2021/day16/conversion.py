import math

class NumConvert:
    def __init__(self, num):
        self.num = num

    def hex_to_binary():
        hex_to_binary_dict = { 
                0 : '0000',
                1 : '0001',
                2 : '0010',
                3 : '0011',
                4 : '0100',
                5 : '0101',
                6 : '0110',
                7 : '0111',
                8 : '1000',
                9 : '1001',
                'A' : '1010',
                'B' : '1011',
                'C' : '1100',
                'D' : '1101',
                'E' : '1110',
                'F' : '1111'
                }
        return hex_to_binary_dict[self.num]

    def binary_to_decimal(self):
        digits = int(math.log10(self.num)) + 1
        number = [int(i) for i in str(self.num)]
        i = 0
        decimals = 0
        for n in range(digits - 1, -1, -1):
            decimals += number[i] * 2 ** n
            i += 1

        return decimals

        


