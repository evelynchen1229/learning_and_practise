import pandas as pd

def integer(i):
    integer_i = []
    for item in i:
        integer_i.append(int(item))
    return integer_i


def decimal(binary):
    decimal = 0
    power = binary_digits - 1
    for i in range (0, binary_digits):
        decimal += binary[i] * 2 ** power
        power -=1
    return decimal

def oxygen(df):
    if len(df) == 1:
        oxygen_rate = df.to_numpy()[0]
        oxygen_rate = integer(oxygen_rate)
        return decimal(oxygen_rate)
    else:
        for i in range(0, binary_digits):
            if len(df) == 1:
                oxygen_rate = df.to_numpy()[0]
                oxygen_rate = integer(oxygen_rate)
                return decimal(oxygen_rate)
            total = df[i].astype('int').sum()
            if total >= 0.5 * len(df):
                df = df[df[i] == '1']
            else:
                df = df[df[i] == '0']
        return oxygen(df)

def co2(df):
    if len(df) == 1:
        co2_rate = df.to_numpy()[0]
        co2_rate = integer(co2_rate)
        return decimal(co2_rate)
    else:
        for i in range(0, binary_digits):
            if len(df) == 1:
                co2_rate = df.to_numpy()[0]
                co2_rate = integer(co2_rate)
                return decimal(co2_rate)
            total = df[i].astype('int').sum()
            if total >= 0.5 * len(df):
                df = df[df[i] == '0']
            else:
                df = df[df[i] == '1']
        return df

binary = []
gamma_rate_list = []
epsilon_rate_list = []
digits = []
gamma_rate = 0 
epsilon_rate = 0

with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        binary.append(line)
f.close()

number_binary_list = len(binary)
binary_digits = len(binary[0])

for i in range(0,number_binary_list):
    digit = list(binary[i])
    digits.append(digit)


df_binary = pd.DataFrame(digits)

# part 1
for i in range (0,binary_digits):
    total = df_binary[i].astype('int').sum()
    if  total > 0.5 * number_binary_list:
        gamma_rate_list.append(1)
        epsilon_rate_list.append(0)
    else:
        gamma_rate_list.append(0)
        epsilon_rate_list.append(1)

gamma_rate = decimal(gamma_rate_list)
epsilon_rate = decimal(epsilon_rate_list)
power_consumption = gamma_rate * epsilon_rate


print(gamma_rate,epsilon_rate,power_consumption)

# part 2
o2 = df_binary.copy()
carbon = df_binary.copy()
oxygen_level = oxygen(o2)
co2_level = co2(carbon)
print(oxygen_level)
print(co2_level)

co2_scrubber = oxygen_level * co2_level
print(co2_scrubber)
