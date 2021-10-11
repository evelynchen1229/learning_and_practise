class Block():
    def __init__(self, array):
        self.array = array
        self._width = array[0]
        self.length = array[1]
        self.height = array[2]
        self.volume = array[0] * array[1] * array[2]
        self.surface_area = (array[0] * array [1] + array[0] * array[2] + array[1] * array[2]) * 2

    def get_array(self):
        return self.array

    def get_width(self):
        '''return the width of the "Block" '''
        return self.width

    def get_length(self):
        '''return the length of the "Block"'''
        return self.length

    def get_height(self):
        '''return the height of the "Block"'''
        return self.height

    def get_volume(self):
        '''return the volume of the "Block"'''
        return self.volume

    def get_surface_area(self):
        '''return the surface area of the "Block"'''
        return self.surface_area

    def set_length(self, l):
        self.length = l
        

    def set_width(self, w):
        self.width = w
        
    
    def set_height(self, h):
        self.height = h
    
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, w):
        self._width = w

    
   
test = Block([2,3,4])
print(test.width)



#test = Block([2.4,4,6])

#print(test.get_width())
#print(test.get_length())
#print(test.get_height())
#print(test.get_volume())
#print(test.get_surface_area())
#test.get_width()

#test.set_width(2)
#print(test.get_width())
#test.width = 2
#print(test.get_width())



