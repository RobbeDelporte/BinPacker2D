from consts import BIN_WIDTH, BIN_HEIGHT
import numpy as np


    
    
class SimpleSpaces():

    def __init__(self, n_layers):
        self.width = BIN_WIDTH
        self.height = BIN_HEIGHT

        self.open_spaces = [OpenSpace(0,0,self.width,self.height,i) for i in range(n_layers)]
        self.number_of_layers = n_layers

    def split_space(self,shape,space_index):
        selected_space = self.open_spaces.pop(space_index)
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        space1 = OpenSpace(selected_space.x+shape.w, selected_space.y, selected_space.w-shape.w,selected_space.h,selected_space.layer)
        space2 = OpenSpace(selected_space.x, selected_space.y+shape.h,shape.w,selected_space.h-shape.h,selected_space.layer)

        self.add_space(space1)
        self.add_space(space2)

        return selected_space.x, selected_space.y, selected_space.layer

    def add_space(self,new_space):
        if not new_space.is_valid():
            return False
        
        for idx, space in enumerate(self.open_spaces):
            if space.layer != new_space.layer:
                continue
            
            #can merge vertically
            if space.x == new_space.x and space.w == new_space.w and (space.y + space.h == new_space.y or new_space.y + new_space.h == space.y):
                space = self.open_spaces.pop(idx)
                x = space.x
                y = min(space.y,new_space.y)
                w = space.w
                h = space.h + new_space.h
                merged_space = OpenSpace(x,y,w,h,space.layer)
                self.add_space(merged_space)
                return True

            #can merge horizontally
            if space.y == new_space.y and space.h == new_space.h and (space.x + space.w == new_space.x or new_space.x + new_space.w == space.x):
                space = self.open_spaces.pop(idx)
                x = min(space.x,new_space.x)
                y = space.y
                w = space.w + new_space.w
                h = space.h
                merged_space = OpenSpace(x,y,w,h,space.layer)
                self.add_space(merged_space)
                return True
        
        # no adjacent spaces found
        self.open_spaces.append(new_space)
        return True
    
    def add_new_layer(self):
        new_space = OpenSpace(0,0,self.width,self.height,self.number_of_layers)
        self.number_of_layers += 1

        self.add_space(new_space)
        return len(self.open_spaces)

    def __str__(self):
        return self.open_spaces.__str__()

    
class OpenSpaces():

    def __init__(self, n_layers):
        self.width = BIN_WIDTH
        self.height = BIN_HEIGHT

        self.open_spaces = [OpenSpace(0,0,self.width,self.height,i) for i in range(n_layers)]
        self.number_of_layers = n_layers
    
    def split_space(self,shape,space_index):
        selected_space = self.open_spaces.pop(space_index)
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        fragmentation_rate = 0
        new_spaces = []

        new_spaces.append(OpenSpace(selected_space.x+shape.w, selected_space.y, selected_space.w-shape.w,selected_space.h,selected_space.layer))
        new_spaces.append(OpenSpace(selected_space.x, selected_space.y+shape.h,selected_space.w,selected_space.h-shape.h,selected_space.layer))

        for space_idx, space in enumerate(self.open_spaces):
            if space.layer != selected_space.layer:
                new_spaces.append(space)
                continue

            x_overlap = max(selected_space.x,space.x)
            y_overlap = max(selected_space.y,space.y)
            w_overlap = min(selected_space.x+shape.w,space.x+space.w) - x_overlap
            h_overlap = min(selected_space.y+shape.h,space.y+space.h) - y_overlap

            if w_overlap <= 0 or h_overlap <= 0:
                new_spaces.append(space)
                continue

            fragmentation_rate += (w_overlap*h_overlap)/(space.w*space.h)

            # space has overlap with shape, needs to be split
            space1 = OpenSpace(space.x,space.y,x_overlap-space.x,space.h,space.layer)
            space2 = OpenSpace(space.x,space.y,space.w,y_overlap-space.y,space.layer)
            space3 = OpenSpace(space.x,y_overlap+h_overlap,space.w,(space.y+space.h)-(y_overlap+h_overlap),space.layer)
            space4 = OpenSpace(x_overlap+w_overlap,space.y,(space.x+space.w)-(x_overlap+w_overlap),space.h,space.layer)

            new_spaces.append(space1)
            new_spaces.append(space2)
            new_spaces.append(space3)
            new_spaces.append(space4)

        self.open_spaces = []
        for new_space in new_spaces:
            self.add_space(new_space)

        return selected_space.x, selected_space.y, selected_space.layer , fragmentation_rate

    def add_space(self,new_space):
        if not new_space.is_valid():
            return False
        
        for idx, space in enumerate(self.open_spaces):
            if space.layer != new_space.layer:
                continue
            
            x_overlap = max(new_space.x,space.x)
            y_overlap = max(new_space.y,space.y)
            w_overlap = min(new_space.x+new_space.w,space.x+space.w) - x_overlap
            h_overlap = min(new_space.y+new_space.h,space.y+space.h) - y_overlap

            if w_overlap <= 0 or h_overlap <= 0:
                continue

            # if space is contained in new space, we can remove it
            if w_overlap == space.w and h_overlap == space.h:
                self.open_spaces.pop(idx)
                continue

            # if new space is contained in another space, we can safely return
            if w_overlap == new_space.w and h_overlap == new_space.h:
                return False
                
        self.open_spaces.append(new_space)
        return True
    
    def filter_spaces(self,min_width,min_height):
        self.open_spaces = [space for space in self.open_spaces if space.w >= min_width and space.h >= min_height]
    
    def add_new_layer(self):
        new_space = OpenSpace(0,0,self.width,self.height,self.number_of_layers)
        self.number_of_layers += 1

        self.add_space(new_space)
        return len(self.open_spaces)

    def __str__(self):
        return self.open_spaces.__str__()
    

    
class OpenSpace():
    __slots__ = ['x','y','w','h','layer','corners']

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
    

