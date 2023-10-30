import numpy as np
from consts import *

class Shapes():

    def __init__(self,order):
        self.shapes_array = []
        self.shapes = []

        self.generate_shapes(order)

    def generate_shapes(self,order):

        shapes_array = []
        for _, product in order.iterrows():
            _, product_id, quantity, w, h = product

            for n in range(1,quantity+1):
                for i in range(1,n+1):
                    if n%i != 0:
                        continue
                    j = n//i

                    if i*w <= BIN_WIDTH and j*h <= BIN_HEIGHT:
                        shapes_array.append([i*w, j*h, n, product_id])
                        self.shapes.append(Shape(i*w, j*h, n, product_id, w, h))
                    if i*h <= BIN_WIDTH and j*w <= BIN_HEIGHT:
                        shapes_array.append([i*h, j*w, n, product_id])
                        self.shapes.append(Shape(i*h, j*w, n, product_id, h, w))

        self.shapes_array = np.array(shapes_array)



class Shape():
    __slots__ = ['w', 'h', 'q', 'item_id', 'item_width', 'item_height']

    def __init__(self,w,h,q,item_id,item_width,item_height):
        self.w = w
        self.h = h
        self.q = q
        self.item_id = item_id
        self.item_width = item_width
        self.item_height = item_height

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.w,self.h,self.q,self.item_id)
