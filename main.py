import csv
import pandas as pd
import numpy as np
from packer import Packer




df = pd.read_csv('dataset.csv', sep=',')

if __name__ == "__main__":

    for order_id, order in df.groupby("Order_ID"):
        packer = Packer(order)

        packer.pack()

        packer.visualise()
        break

