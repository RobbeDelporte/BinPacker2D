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
        
        self.spaces = Spaces()
        self.layers = Layers()
        self.shapes = Shapes(order)
        self.packed_items = []


    def pack(self):
    
        while self.number_of_items > 0:

            space_idx, shape_idx = self.find_space_shape()

            # shape_idx = self.next_shape()
            # shape = self.shapes.shapes[shape_idx]
            # space_idx = self.find_space(shape)
            self.pack_shape(shape_idx,space_idx)
            
    
    def pack_shape(self,shape_idx,space_idx):
        shape = self.shapes.shapes[shape_idx]
        x,y,layer = self.spaces.split_space(shape.w,shape.h,space_idx)
        self.layers.add_shape(shape,x,y,layer)
        self.item_quantities[shape.id] -= shape.q
        self.number_of_items -= shape.q


    def find_space(self,shape):
        for idx, space in enumerate(self.spaces.free_spaces):
            if space.w >= shape.w and space.h >= shape.h:
                return idx
            
        #no fits
        self.spaces.add_new_layer()

        return self.find_space(shape)
    

    def next_shape(self):
        s = self.shapes.shapes_array
        area = s[:,0] * s[:,1]
        available = s[:,2] <= self.item_quantities[s[:,3]]
        prio = area * (available)

        next_shape_idx = np.argmax(prio)
        return next_shape_idx
    
    def find_space_shape(self):
        shapes = self.shapes.shapes_array
        w = shapes[:,0]
        h = shapes[:,1]
        spaces = self.spaces.free_spaces
        scores = np.zeros((len(spaces),len(shapes)))
        for i, space in enumerate(spaces):
            fit = np.array((space.w >= w) & (space.h >= h),dtype=bool)
            enough_items = shapes[:,2] <= self.item_quantities[shapes[:,3]]
            wasted_space = np.abs(space.w * space.h - w * h)
            scores[i] = (1 / (wasted_space+1e-6)) * fit * enough_items

        max_score = np.max(scores)

        #recursion, yes i know but it works here rather well so whatever
        if max_score == 0:
            self.spaces.add_new_layer()
            return self.find_space_shape()
        
        found_space, found_shape = np.argwhere(scores == np.max(scores))[-1]
    
        return found_space, found_shape


    def visualise(self):
        for index, layer in enumerate(self.layers.layers):
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
                if space.layer == index:
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
            
        fig.show()



class Layers():

    def __init__(self):
        self.layers = []

    def add_shape(self,shape,x,y,layer):

        if len(self.layers) <= layer:
            self.layers.append([])
        
        self.layers[layer].append([x,y,shape.w,shape.h,shape.q,shape.id])



