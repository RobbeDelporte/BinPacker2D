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

            # bool vector: true if shape fits in space

            fit = np.array((space.w >= w) & (space.h >= h),dtype=bool)

            # bool vector: true if enough items are left to make shape
            enough_items = shapes[:,2] <= self.item_quantities[shapes[:,3]]

            # [0,1] vector: fill rate of space by shape
            fill_rate = np.array((w * h) / (space.w * space.h),dtype=np.float16)

            # Calculating wasted space, space that can never be filled (unless maybe with a good space merge)
            # resulting w,h of spaces after space split
            space1_w = space.w - w; space1_h = space.h; space2_w = w; space2_h = space.h - h
            # bool vector: true if no shape exists that fits in space
            space1_wasted = self.shapes.min_fits[np.clip(space1_w,0,BIN_WIDTH-1)] > space1_h
            space2_wasted = self.shapes.min_fits[np.clip(space2_w,0,BIN_WIDTH-1)] > space2_h  
            # int vector: wasted space area
            wasted_area = np.array(space1_wasted * (space1_w * space1_h) + space2_wasted * (space2_w * space2_h),dtype=int)
            fill_rate = (w * h) / (space.w * space.h)

            scores[i] = fill_rate * fit * enough_items

        max_score = np.max(scores)

        # no possible fit, add new layer then recursion
        if max_score == 0:
            self.spaces.add_new_layer()
            return self.find_space_shape()
        
        found_space, found_shape = np.argwhere(scores == np.max(scores))[-1]

        print(max_score, spaces[found_space], shapes[found_shape])
    
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



