from consts import BIN_WIDTH, BIN_HEIGHT


class Spaces():
    def __init__(self):

        self.width = BIN_WIDTH
        self.height = BIN_HEIGHT

        self.free_spaces = [FreeSpace(0,0,self.width,self.height,0)]

        self.number_of_layers = 0


    def split_space(self,w,h,space_index):
        space = self.free_spaces.pop(space_index)
        layer = space.layer
        assert space.w >= w and space.h >= h

        space1 = FreeSpace(space.x+w, space.y, space.w-w,space.h,layer)
        space2 = FreeSpace(space.x, space.y+h,w,space.h-h,layer)

        if space1.is_valid():
            self.free_spaces.append(space1)
        if space2.is_valid():
            self.free_spaces.append(space2)

        return space.x, space.y, space.layer
    
    def get_space_split(self,w,h,space_index):
        space = self.free_spaces[space_index]
        layer = space.layer
        space1 = FreeSpace(space.x+w, space.y, space.w-w,space.h,layer)
        space2 = FreeSpace(space.x, space.y+h,w,space.h-h,layer)

        if not space1.is_valid():
            space1 = None
        if not space2.is_valid():
            space2 = None
        return space1, space2


    def add_new_layer(self):
        self.number_of_layers += 1
        new_space = FreeSpace(0,0,self.width,self.height,self.number_of_layers)
        self.free_spaces.append(new_space)
        return len(self.free_spaces)
    

    def merge_spaces(self):
        #TODO
        pass

    
class FreeSpace():
    def __init__(self, x, y, w, h, layer):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.layer = layer

    def __repr__(self):
        return "({}, {}, {}, {}, layer: {})".format(self.x,self.y,self.w,self.h,self.layer)
    
    def is_valid(self):
        return self.w > 0 and self.h > 0
