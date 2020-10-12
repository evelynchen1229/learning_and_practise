class Block():
    def __init__(self, array):
        self.array = array

    def get_array(self):
        return self.array

    def get_width(self):
        '''return the width of the "Block" '''
        array = self.get_array()
        return array[0]

    def get_length(self):
        '''return the length of the "Block"'''
        array = self.get_array()
        return array[1]

    def get_height(self):
        '''return the height of the "Block"'''
        array = self.get_array()
        return array[2]

    def get_volume(self):
        '''return the volume of the "Block"'''
        array = self.get_array()
        return array[0] * array[1] * array[2]

    def get_surface_area(self):
        '''return the surface area of the "Block"'''
        array = self.get_array()
        return (array[0] * array [1] + array[0] * array[2] + array[1] * array[2]) * 2


test = Block([2,4,6])

print(test.get_width())
print(test.get_length())
print(test.get_height())
print(test.get_volume())
print(test.get_surface_area())




