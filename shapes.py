import numpy as np
import sympy as sp

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
                    shapes_array.append([i*w, j*h, n, product_id])
                    shapes_array.append([j*h, i*w, n, product_id])


            # #single item shape, both orientations
            # shapes_array.append([w, h, 1, product_id])
            # shapes_array.append([h, w, 1, product_id])

            # #double item shape, both orientations, stacked on both sides
            # shapes_array.append([2*w, h, 2, product_id])
            # shapes_array.append([w, 2*h, 2, product_id])
            # shapes_array.append([h, 2*w, 2, product_id])
            # shapes_array.append([2*h, w, 2, product_id])

            # #quad item shape, both orientations, stacked on all sides
            # shapes_array.append([w, 4*h, 4, product_id])
            # shapes_array.append([2*w, 2*h, 4, product_id])
            # shapes_array.append([4*w, h, 4, product_id])
            # shapes_array.append([h, 4*w, 4, product_id])
            # shapes_array.append([2*h, 2*w, 4, product_id])
            # shapes_array.append([4*h, w, 4, product_id])

            # #six item shape, both orientations, stacked on all sides
            # shapes_array.append([w, 6*h, 6, product_id])
            # shapes_array.append([2*w, 3*h, 6, product_id])
            # shapes_array.append([3*w, 2*h, 6, product_id])
            # shapes_array.append([6*w, h, 6, product_id])
            # shapes_array.append([h, 6*w, 6, product_id])
            # shapes_array.append([2*h, 3*w, 6, product_id])
            # shapes_array.append([3*h, 2*w, 6, product_id])
            # shapes_array.append([6*h, w, 6, product_id])

            # #eight item shape, both orientations, stacked on all sides
            # shapes_array.append([w, 8*h, 8, product_id])
            # shapes_array.append([2*w, 4*h, 8, product_id])
            # shapes_array.append([4*w, 2*h, 8, product_id])
            # shapes_array.append([8*w, h, 8, product_id])
            # shapes_array.append([h, 8*w, 8, product_id])
            # shapes_array.append([2*h, 4*w, 8, product_id])
            # shapes_array.append([4*h, 2*w, 8, product_id])
            # shapes_array.append([8*h, w, 8, product_id])

            # #nine item shape, both orientations, stacked on all sides
            # shapes_array.append([w, 9*h, 9, product_id])
            # shapes_array.append([3*w, 3*h, 9, product_id])
            # shapes_array.append([9*w, h, 9, product_id])
            # shapes_array.append([h, 9*w, 9, product_id])
            # shapes_array.append([3*h, 3*w, 9, product_id])
            # shapes_array.append([9*h, w, 9, product_id])

            # #ten item shape, both orientations, stacked on all sides
            # shapes_array.append([w, 10*h, 10, product_id])
            # shapes_array.append([2*w, 5*h, 10, product_id])
            # shapes_array.append([5*w, 2*h, 10, product_id])
            # shapes_array.append([10*w, h, 10, product_id])
            # shapes_array.append([h, 10*w, 10, product_id])
            # shapes_array.append([2*h, 5*w, 10, product_id])
            # shapes_array.append([5*h, 2*w, 10, product_id])
            # shapes_array.append([10*h, w, 10, product_id])

            # #twelve item shape, both orientations, stacked on all sides
            # shapes_array.append([w, 12*h, 12, product_id])
            # shapes_array.append([2*w, 6*h, 12, product_id])
            # shapes_array.append([3*w, 4*h, 12, product_id])
            # shapes_array.append([4*w, 3*h, 12, product_id])
            # shapes_array.append([6*w, 2*h, 12, product_id])
            # shapes_array.append([12*w, h, 12, product_id])
            # shapes_array.append([h, 12*w, 12, product_id])
            # shapes_array.append([2*h, 6*w, 12, product_id])
            # shapes_array.append([3*h, 4*w, 12, product_id])
            # shapes_array.append([4*h, 3*w, 12, product_id])
            # shapes_array.append([6*h, 2*w, 12, product_id])
            # shapes_array.append([12*h, w, 12, product_id])


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
