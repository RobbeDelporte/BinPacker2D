import numpy as np
from consts import *

class Shapes():

    def __init__(self,order):
        self.shapes_array = []
        self.shapes = []

        self.generate_shapes(order)

        self.min_fits = np.zeros(BIN_WIDTH)
        self.min_fits.fill(BIN_HEIGHT+1)
        for i in range(BIN_WIDTH):
            idx = np.where(self.shapes_array[:,0] <= i)[0]
            if len(idx) == 0:
                continue
            self.min_fits[i] = np.min(self.shapes_array[idx,1])
    

    def generate_shapes(self,order):

        shapes_array = []
        for _, product in order.iterrows():
            _, product_id, quantity, w, h = product

            for n in range(1,quantity+1):
                for i in range(1,n+1):
                    if n%i != 0:
                        continue
                    j = n//i

                    if i*w <= BIN_WIDTH or j*h <= BIN_HEIGHT:
                        shapes_array.append([i*w, j*h, n, product_id])
                    if i*h <= BIN_WIDTH or j*w <= BIN_HEIGHT:
                        shapes_array.append([j*h, i*w, n, product_id])

        self.shapes_array = np.array(shapes_array)

        for shape in self.shapes_array:
            self.shapes.append(Shape(*shape))




class Shape():
    def __init__(self,w,h,q,id):
        self.w = w
        self.h = h
        self.q = q
        self.id = id

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.w,self.h,self.q,self.id)