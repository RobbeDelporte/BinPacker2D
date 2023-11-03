from consts import BIN_WIDTH, BIN_HEIGHT
import numpy as np


class OpenSpaces():

    def __init__(self, n_layers):
        self.width = BIN_WIDTH
        self.height = BIN_HEIGHT

        self.open_spaces = [OpenSpace(0,0,self.width,self.height,i) for i in range(n_layers)]
        self.number_of_layers = n_layers

    def best_corner(self,shape,space_index):
        selected_space = self.open_spaces[space_index]
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        corners_xy = [[selected_space.x,selected_space.y],
                     [selected_space.x+selected_space.w-shape.w,selected_space.y],
                     [selected_space.x,selected_space.y+selected_space.h-shape.h],
                     [selected_space.x+selected_space.w-shape.w,selected_space.y+selected_space.h-shape.h]]
        
        corner_fragmentation = np.zeros(4)

        for i,(x,y) in enumerate(corners_xy):
            fragmentation_rate = 0

            for space_idx, space in enumerate(self.open_spaces):
                if space.layer != selected_space.layer:
                    continue

                x_overlap = max(x,space.x)
                y_overlap = max(y,space.y)
                w_overlap = min(x+shape.w,space.x+space.w) - x_overlap
                h_overlap = min(y+shape.h,space.y+space.h) - y_overlap

                if w_overlap <= 0 or h_overlap <= 0:
                    continue

                fragmentation_rate += (w_overlap*h_overlap)


            corner_fragmentation[i] = fragmentation_rate

        return corner_fragmentation
    

    def best_offset(self,shape,space_index):
        selected_space = self.open_spaces[space_index]
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        offset_fragmentation = np.zeros((selected_space.w-shape.w+1,selected_space.h-shape.h+1))

        for x_offset in range(0,selected_space.w-shape.w+1):
            for y_offset in range(0,selected_space.h-shape.h+1):
                fragmentation_rate = 0
                x = selected_space.x+x_offset
                y = selected_space.y+y_offset

                for space_idx, space in enumerate(self.open_spaces):
                    if space.layer != selected_space.layer:
                        continue

                    x_overlap = max(x,space.x)
                    y_overlap = max(y,space.y)
                    w_overlap = min(x+shape.w,space.x+space.w) - x_overlap
                    h_overlap = min(y+shape.h,space.y+space.h) - y_overlap

                    if w_overlap <= 0 or h_overlap <= 0:
                        continue

                    fragmentation_rate += (w_overlap*h_overlap)

                offset_fragmentation[x_offset,y_offset] = fragmentation_rate

        return offset_fragmentation 


    def split_space(self,shape,space_index,corner=0):
        selected_space = self.open_spaces[space_index]
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        corners_xy = [[selected_space.x,selected_space.y],
                     [selected_space.x+selected_space.w-shape.w,selected_space.y],
                     [selected_space.x,selected_space.y+selected_space.h-shape.h],
                     [selected_space.x+selected_space.w-shape.w,selected_space.y+selected_space.h-shape.h]]
        
        x,y = corners_xy[corner]

        new_spaces = []
        for space_idx, space in enumerate(self.open_spaces):
            if space.layer != selected_space.layer:
                new_spaces.append(space)
                continue

            x_overlap = max(x,space.x)
            y_overlap = max(y,space.y)
            w_overlap = min(x+shape.w,space.x+space.w) - x_overlap
            h_overlap = min(y+shape.h,space.y+space.h) - y_overlap

            if w_overlap <= 0 or h_overlap <= 0:
                new_spaces.append(space)
                continue

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

        return x, y, selected_space.layer
    
    
    def split_space_offset(self,shape,space_index,x_offset=0,y_offset=0):
        selected_space = self.open_spaces[space_index]
        assert selected_space.w >= shape.w and selected_space.h >= shape.h

        x = selected_space.x+x_offset
        y = selected_space.y+y_offset

        new_spaces = []
        for space_idx, space in enumerate(self.open_spaces):
            if space.layer != selected_space.layer:
                new_spaces.append(space)
                continue

            x_overlap = max(x,space.x)
            y_overlap = max(y,space.y)
            w_overlap = min(x+shape.w,space.x+space.w) - x_overlap
            h_overlap = min(y+shape.h,space.y+space.h) - y_overlap

            if w_overlap <= 0 or h_overlap <= 0:
                new_spaces.append(space)
                continue

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

        return x, y, selected_space.layer


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
    

