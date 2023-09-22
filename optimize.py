import os
import sys
import pandas as pd
import numpy as np
from pulp import *
import openpyxl




print(sys.argv)

file_path = 'slate_excel/'
file_name = 'week1_main_slate.csv'
file = file_path+file_name
print(file)

slate_file = pd.read_csv(file)
print(type(slate_file))


