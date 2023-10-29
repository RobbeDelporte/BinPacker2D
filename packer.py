import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import colorsys
from spaces import Spaces
from shapes import *
from consts import BIN_WIDTH, BIN_HEIGHT

class Packer():

    def __init__(self,order):
        assert np.all(order["Product_ID"].to_numpy() == np.arange(order["Product_ID"].size))
        N = len(order["Product_ID"])

        #index is id, value is quantity
        self.item_quantities = np.array(order["Quantity"])
        self.colors = [colorsys.hsv_to_rgb(x*1.0/N, 1, 1) for x in range(N)]


        self.total_number_of_items = np.sum(self.item_quantities)
        
        liquid_filling = np.ceil((order["Quantity"] * order["L"] * order["W"]).sum() / (100*120)).astype(int)

        # we will at least need liquid_filling layers, initialize a free space for all of them for more packing possibilities
        self.open_spaces = Spaces(n_layers=liquid_filling)
        self.packed_items = PackedItems()
        self.shapes = Shapes(order)


    def pack(self):
    
        while self.total_number_of_items > 0:

            #fine a space, shape pair with the highest score
            space_idx, shape_idx = self.find_space_shape()

            #pack the shape into the space
            self.pack_shape(shape_idx,space_idx)


    def find_space_shape(self):
        shapes = self.shapes.shapes_array
        w = shapes[:,0]
        h = shapes[:,1]
        spaces = self.open_spaces.open_spaces
        
        # scores for each space, shape pair
        scores = np.zeros((len(spaces),len(shapes)))

        # iterate over all spaces
        for i, space in enumerate(spaces):
            # calculate score for each shape in a vectorized way

            # mask to check if shape fits in space
            fit = np.array((space.w >= w) & (space.h >= h),dtype=bool)

            # mask to check if there are enough items left to make shape
            enough_items = shapes[:,2] <= self.item_quantities[shapes[:,3]]

            # get min dimensions of available shapes
            remaining_shapes = shapes[enough_items]
            min_width = np.min(remaining_shapes[:,0])
            min_height = np.min(remaining_shapes[:,1])

            # cutoff point, point where no shape can fit
            width_cutoff = (space.w - min_width)
            height_cutoff = (space.h - min_height)

            width_cutoff = width_cutoff * (w > width_cutoff)
            height_cutoff = height_cutoff * (h > height_cutoff)

            # score
            width_score = (((w - width_cutoff) / (space.w - width_cutoff)))
            height_score = (((h - height_cutoff) / (space.h - height_cutoff)))

            # combined score (multiply width and height scores) + mask out invalid shapes
            scores[i] = (width_score * height_score) * fit * enough_items

        # find max score
        max_score = np.max(scores)

        # no possible fit, add new layer then recursion
        if max_score == 0:
            self.open_spaces.add_new_layer()
            return self.find_space_shape()
        
        found_space, found_shape = np.argwhere(scores == max_score)[-1]

        # print(max_score, spaces[found_space], shapes[found_shape])
    
        return found_space, found_shape
    

    def pack_shape(self,shape_idx,space_idx):
        shape = self.shapes.shapes[shape_idx]
        x,y,layer = self.open_spaces.split_space(shape,space_idx)
        self.packed_items.add_shape(shape,x,y,layer)
        self.item_quantities[shape.id] -= shape.q
        self.total_number_of_items -= shape.q


    def visualise(self):
        for layer_index, layer in self.packed_items.layers.items():
            fig = plt.figure()
            ax = fig.add_subplot(111, aspect='equal')
            for x,y,w,h,q,id in layer:
                plt.axis([0,BIN_WIDTH,0,BIN_HEIGHT])
                ax.add_patch(
                    Rectangle(
                        (x, y),  # (x,y)
                        w,          # width
                        h,          # height
                        facecolor=self.colors[id],
                        edgecolor="black",
                        linewidth=3
                    )
                )
                ax.text(x+w/2, y+h/2, f"{id}: {q}", ha='center', va='center', fontsize=20)

            for space in self.open_spaces.open_spaces:
                if space.layer == layer_index:
                    ax.add_patch(
                        Rectangle(
                            (space.x, space.y),  # (x,y)
                            space.w,          # width
                            space.h,          # height
                            facecolor="white",
                            edgecolor="black",
                            linewidth=3
                        )
                    )
                    ax.text(space.x+space.w/2, space.y+space.h/2, f"S", ha='center', va='center', fontsize=20)   
        plt.show()



class PackedItems():
    #just stores packed items, no real logic
    def __init__(self):
        self.layers = {}

    def add_shape(self,shape,x,y,layer):
        print(f"packing {shape} at {x},{y} in layer {layer}")
        if layer not in self.layers:
            self.layers[layer] = []
        self.layers[layer].append([x,y,shape.w,shape.h,shape.q,shape.id])



