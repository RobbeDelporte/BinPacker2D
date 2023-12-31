import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import colorsys
from spaces import OpenSpaces
from shapes import Shapes
from consts import *

class Packer():

    def __init__(self,order):
        assert np.all(order["Product_ID"].to_numpy() == np.arange(order["Product_ID"].size))
        N = len(order["Product_ID"])

        #index is id, value is quantity
        self.item_quantities = np.array(order["Quantity"])
        self.colors = [colorsys.hsv_to_rgb(x*1.0/N, 1, 1) for x in range(N)]

        self.total_number_of_items = np.sum(self.item_quantities)
        
        self.liquid_filling = np.ceil((order["Quantity"] * order["L"] * order["W"]).sum() / (100*120)).astype(int)

        self.spaces = OpenSpaces(n_layers=1)
        self.packed_items = PackedItems()
        self.shapes = Shapes(order)

    def pack(self):    
        while self.total_number_of_items > 0:

            #fine a space, shape pair with the highest score
            space_idx, shape_idx = self.find_space_shape()

            shape = self.shapes.shapes[shape_idx]

            corner_fragmentation = self.spaces.best_corner(shape,space_idx)
            best_corner = np.argmin(corner_fragmentation)

            x,y,layer = self.spaces.split_space(shape,space_idx,corner=best_corner)

            # add shape to packed items (only used to output result)
            self.packed_items.add_shape(shape,x,y,layer)

            # update item quantities
            self.item_quantities[shape.item_id] -= shape.q
            self.total_number_of_items -= shape.q

            valid_shapes = self.shapes.shapes_array[self.shapes.shapes_array[:,2] <= self.item_quantities[self.shapes.shapes_array[:,3]]]
            if len(valid_shapes) > 0:
                min_width = np.min(valid_shapes[:,0])
                min_height = np.min(valid_shapes[:,1])
                self.spaces.filter_spaces(min_width,min_height)

        
    def find_space_shape(self):
        shapes = self.shapes.shapes_array
        w = shapes[:,0]
        h = shapes[:,1]
        spaces = self.spaces.open_spaces

        # no open spaces, add new layer
        if len(spaces) == 0:
            self.spaces.add_new_layer()
            spaces = self.spaces.open_spaces

        
        # scores for each space, shape pair
        scores = np.zeros((len(spaces),len(shapes)))

        # iterate over all spaces
        for i, space in enumerate(spaces):
            # calculate score for each shape in a vectorized way

            # mask to check if shape fits in space
            fit = np.array((space.w >= w) & (space.h >= h),dtype=bool)
            # mask to check if there are enough items left to make shape
            enough_items = shapes[:,2] <= self.item_quantities[shapes[:,3]]

            # mask to check if there are any shapes that fit and have enough items, if there are none, skip this space
            valid = fit & enough_items
            if not np.any(valid):
                continue

            # get min dimensions of available shapes
            remaining_shapes = shapes[valid]
            min_width = np.min(remaining_shapes[:,0])
            min_height = np.min(remaining_shapes[:,1])

            # cutoff point, point where no shape can fit
            width_cutoff = (space.w - min_width)
            height_cutoff = (space.h - min_height)

            score1_w = (w / space.w) * (w <= width_cutoff)
            score1_h = (h / space.h) * (h <= height_cutoff)

            score2_w = (((w - width_cutoff) / (space.w - width_cutoff))) * (w > width_cutoff)
            score2_h = (((h - height_cutoff) / (space.h - height_cutoff))) * (h > height_cutoff)

            # p = 4
            # score2_w = 1/(min_width**p) * (w - width_cutoff)**p * (w > width_cutoff)
            # score2_h = 1/(min_height**p) * (h - height_cutoff)**p * (h > height_cutoff)

            # a = 0
            # score2_w = ((1 - a*width_cutoff/space.w)/min_width * w + (width_cutoff * (a - 1))/min_width) * (w > width_cutoff)
            # score2_h = ((1 - a*height_cutoff/space.h)/min_height * h + (height_cutoff * (a - 1))/min_height) * (h > height_cutoff)

            width_score = score1_w + score2_w
            height_score = score1_h + score2_h

            # combined score (multiply width and height scores) + mask out invalid shapes
            scores[i] = (width_score * height_score) * valid

        # find max score
        max_score = np.max(scores)

        # no possible fit, add new layer then recursion, carefull here that 0 score actually means that there is no possible fit, and not a possible fit with a bad score
        if max_score == 0:
            self.spaces.add_new_layer()
            return self.find_space_shape()
        
        found_space, found_shape = np.argwhere(scores == max_score)[0]

        # print(max_score, spaces[found_space], shapes[found_shape])
    
        return found_space, found_shape
    

    def visualise(self):
        for layer_index, layer in self.packed_items.layers.items():
            fig = plt.figure()
            ax = fig.add_subplot(111, aspect='equal')
            for x,y,shape in layer:
                plt.axis([0,BIN_WIDTH,0,BIN_HEIGHT])
                width_q = shape.w / shape.item_width
                for i in range(shape.q):
                    ax.add_patch(
                        Rectangle(
                            (x + shape.item_width * (i % width_q), y + shape.item_height * (i // width_q)),  # (x,y)
                            shape.item_width,          # width
                            shape.item_height,          # height
                            facecolor=self.colors[shape.item_id],
                            edgecolor="black",
                            linewidth=1
                        )
                    )
                ax.add_patch(
                    Rectangle(
                        (x, y),  # (x,y)
                        shape.w,          # width
                        shape.h,          # height
                        fill = False,
                        linewidth=3,
                    )
                )
                ax.text(x+shape.w/2, y+shape.h/2, f"{shape.item_id}", ha='center', va='center', fontsize=20)

            for space in self.spaces.open_spaces:
                if space.layer == layer_index:
                    ax.add_patch(
                        Rectangle(
                            (space.x, space.y),  # (x,y)
                            space.w,          # width
                            space.h,          # height
                            facecolor="white",
                            edgecolor="black",
                            fill = False,
                            linewidth=1
                        )
                    )
                    ax.text(space.x+space.w/2, space.y+space.h/2, f"S", ha='center', va='center', fontsize=20)   
        plt.show()



class PackedItems():
    #just stores packed items, no real logic
    def __init__(self):
        self.layers = {}

    def add_shape(self,shape,x,y,layer):
        # print(f"packing {shape} at {x},{y} in layer {layer}")
        if layer not in self.layers:
            self.layers[layer] = []
        self.layers[layer].append([x,y,shape])



