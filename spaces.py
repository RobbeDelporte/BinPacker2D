from consts import BIN_WIDTH, BIN_HEIGHT
import numpy as np

class Spaces():
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


    def add_new_layer(self):
        new_space = OpenSpace(0,0,self.width,self.height,self.number_of_layers)
        self.number_of_layers += 1

        self.open_spaces.append(new_space)
        return len(self.open_spaces)
    

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
    


class OpenSpaces():
    def __init__(self, n_layers):

        self.width = BIN_WIDTH
        self.height = BIN_HEIGHT

        self.open_spaces = [OpenSpace(0,0,self.width,self.height,i) for i in range(n_layers)]
        self.number_of_layers = n_layers

    def split_space(self,shape,space_index):
        selected_space = self.open_spaces.pop(space_index)
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        new_spaces = []

        new_spaces.append(OpenSpace(selected_space.x+shape.w, selected_space.y, selected_space.w-shape.w,selected_space.h,selected_space.layer))
        new_spaces.append(OpenSpace(selected_space.x, selected_space.y+shape.h,selected_space.w,selected_space.h-shape.h,selected_space.layer))


        for space in self.open_spaces:
            if space.layer != selected_space.layer:
                continue

            x_overlap = max(selected_space.x,space.x)
            y_overlap = max(selected_space.y,space.y)
            w_overlap = min(selected_space.x+shape.w,space.x+space.w) - x_overlap
            h_overlap = min(selected_space.y+shape.h,space.y+space.h) - y_overlap



            if w_overlap <= 0 or h_overlap <= 0:
                continue

            print(selected_space.x,selected_space.y,shape,space,x_overlap,y_overlap,w_overlap,h_overlap)

            


        for new_space in new_spaces:
            self.add_space(new_space)

        return selected_space.x, selected_space.y, selected_space.layer

    def add_new_layer(self):
        new_space = OpenSpace(0,0,self.width,self.height,self.number_of_layers)
        self.number_of_layers += 1

        self.open_spaces.append(new_space)
        return len(self.open_spaces)

    def add_space(self,new_space):
        if not new_space.is_valid():
            return False
        
        self.open_spaces.append(new_space)
        return True

    
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
    

