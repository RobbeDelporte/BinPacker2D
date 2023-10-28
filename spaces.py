from consts import BIN_WIDTH, BIN_HEIGHT
import numpy as np

class Spaces():
    def __init__(self, n_layers):

        self.width = BIN_WIDTH
        self.height = BIN_HEIGHT

        self.free_spaces = [FreeSpace(0,0,self.width,self.height,i) for i in range(n_layers)]
        self.number_of_layers = n_layers


    def split_space(self,w,h,space_index):
        space = self.free_spaces.pop(space_index)
        layer = space.layer
        assert space.w >= w and space.h >= h

        space1 = FreeSpace(space.x+w, space.y, space.w-w,space.h,layer)
        space2 = FreeSpace(space.x, space.y+h,w,space.h-h,layer)

        self.add_space(space1)
        self.add_space(space2)

        return space.x, space.y, space.layer
    

    def add_space(self,new_space):
        if not space.is_valid():
            return False
        
        #check for merge possibilities
        for space_idx, space in enumerate(self.free_spaces):
            if np.intersect1d(space.corners, new_space.corners).size == 2:
                free_space.w = max(free_space.w, space.w)
                free_space.h = max(free_space.h, space.h)
                return True

    
    def get_space_split(self,w,h,space_index):
        #to be used in speculative execution
        space = self.free_spaces[space_index]
        layer = space.layer
        assert space.w >= w and space.h >= h
        space1 = FreeSpace(space.x+w, space.y, space.w-w,space.h,layer)
        space2 = FreeSpace(space.x, space.y+h,w,space.h-h,layer)

        # no valid check, area can be 0
        return space1, space2


    def add_new_layer(self):
        new_space = FreeSpace(0,0,self.width,self.height,self.number_of_layers)
        self.number_of_layers += 1

        self.free_spaces.append(new_space)
        return len(self.free_spaces)
    

    def add_space(self,new_space):
        if not new_space.is_valid():
            return False
        
        for idx, space in enumerate(self.free_spaces):
            if space.layer != new_space.layer:
                continue
            
            #can merge vertically
            if space.x == new_space.x and space.w == new_space.w and (space.y + space.h == new_space.y or new_space.y + new_space.h == space.y):
                space = self.free_spaces.pop(idx)
                x = space.x
                y = min(space.y,new_space.y)
                w = space.w
                h = space.h + new_space.h
                merged_space = FreeSpace(x,y,w,h,space.layer)
                self.add_space(merged_space)
                return True

            #can merge horizontally
            if space.y == new_space.y and space.h == new_space.h and (space.x + space.w == new_space.x or new_space.x + new_space.w == space.x):
                space = self.free_spaces.pop(idx)
                x = min(space.x,new_space.x)
                y = space.y
                w = space.w + new_space.w
                h = space.h
                merged_space = FreeSpace(x,y,w,h,space.layer)
                self.add_space(merged_space)
                return True
        
        # no adjacent spaces found
        self.free_spaces.append(new_space)
        return True


    
class FreeSpace():
    def __init__(self, x, y, w, h, layer):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.layer = layer
        self.corners = [(x,y),(x+w,y),(x,y+h),(x+w,y+h)]

    def __repr__(self):
        return "({}, {}, {}, {}, layer: {})".format(self.x,self.y,self.w,self.h,self.layer)
    
    def is_valid(self):
        return self.w > 0 and self.h > 0
    

