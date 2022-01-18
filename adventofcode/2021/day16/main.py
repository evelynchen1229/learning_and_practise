from construction import constructor
from conversion import NumConvert

example = 'example.txt'
example_transmission = constructor(example)
print(example_transmission)

a = 110
a = NumConvert(a)
print(a.binary_to_decimal())
