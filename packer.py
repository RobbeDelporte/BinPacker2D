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
        self.number_of_items = np.sum(self.item_quantities)

        self.item_shapes = np.array([order["L"], order["W"]]).T
        self.item_areas = self.item_shapes[:,0] * self.item_shapes[:,1]
        
        liquid_filling = np.ceil((order["Quantity"] * order["L"] * order["W"]).sum() / (100*120)).astype(int)

        self.spaces = Spaces(n_layers=liquid_filling)
        self.packed_items = PackedItems()
        self.shapes = Shapes(order)


    def pack(self):
    
        while self.number_of_items > 0:

            space_idx, shape_idx = self.find_space_shape()

            # shape_idx = self.next_shape()
            # shape = self.shapes.shapes[shape_idx]
            # space_idx = self.find_space(shape)
            self.pack_shape(shape_idx,space_idx)


    def find_space_shape(self):
        shapes = self.shapes.shapes_array
        w = shapes[:,0]
        h = shapes[:,1]
        spaces = self.spaces.free_spaces
        
        # scores for each space, shape pair
        scores = np.zeros((len(spaces),len(shapes)))

        # iterate over all spaces
        for i, space in enumerate(spaces):
            # calculate score for each shape in a vectorized manner

            fit = np.array((space.w >= w) & (space.h >= h),dtype=bool)

            enough_items = shapes[:,2] <= self.item_quantities[shapes[:,3]]

            # space1_w = shape_width - x; space1_h = shape_height; space2_w = x; space2_h = shape_height - y

            # get min dimensions of available shapes
            remaining_shapes = shapes[enough_items]
            min_width = np.min(remaining_shapes[:,0])
            min_height = np.min(remaining_shapes[:,1])

            # cutoff point, point where no shape can fit
            width_cutoff = space.w - min_width
            height_cutoff = space.h - min_height

            # pre-cutoff score (fill rate)
            score1_w = (w / space.w) * (w <= width_cutoff)
            score1_h = (h / space.h) * (h <= height_cutoff)

            # post-cutoff score (linear)
            score2_w = (((w - width_cutoff) / (space.w - width_cutoff))) * (w > width_cutoff)
            score2_h = (((h - height_cutoff) / (space.h - height_cutoff))) * (h > height_cutoff)

            # add score functions (only one of score1_w and score2_w will be non-zero)
            width_score = score1_w + score2_w
            height_score = score1_h + score2_h

            # combined score (multiply width and height scores) + mask out invalid shapes
            scores[i] = (width_score * height_score) * fit * enough_items

        # find max score
        max_score = np.max(scores)

        # no possible fit, add new layer then recursion
        if max_score == 0:
            self.spaces.add_new_layer()
            return self.find_space_shape()
        
        found_space, found_shape = np.argwhere(scores == max_score)[-1]

        # print(max_score, spaces[found_space], shapes[found_shape])
    
        return found_space, found_shape
    

    def pack_shape(self,shape_idx,space_idx):
        shape = self.shapes.shapes[shape_idx]
        x,y,layer = self.spaces.split_space(shape.w,shape.h,space_idx)
        self.packed_items.add_shape(shape,x,y,layer)
        self.item_quantities[shape.id] -= shape.q
        self.number_of_items -= shape.q


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

            for space in self.spaces.free_spaces:
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
        if layer not in self.layers:
            self.layers[layer] = []
        self.layers[layer].append([x,y,shape.w,shape.h,shape.q,shape.id])



