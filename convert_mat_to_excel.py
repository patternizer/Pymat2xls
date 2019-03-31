#!/usr/bin/env python

# ipdb> import os; os._exit(1)   

# call as: python convert_mat_to_excel.py 

# =======================================
# Version 0.1
# 30 March, 2019
# michael.taylor AT reading DOT ac DOT uk
# =======================================

import os
import os.path
import glob
import optparse
from  optparse import OptionParser
import sys
import numpy as np
from scipy.io import loadmat
import xarray
import pandas as pd
from pandas import Series, DataFrame, Panel
import datetime as dt
from sklearn.preprocessing import StandardScaler
import seaborn as sns; sns.set(style="darkgrid")
import matplotlib.pyplot as plt; plt.close("all")
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import urllib

def create_dataframe(file_in):

    #
    # LOAD MATLAB ARRAY
    #

    mat_dict = loadmat(file_in, squeeze_me=True)
    mat_keys = sorted( mat_dict.keys() )
    py_dict = { k: mat_dict[k] for k in mat_keys}

    # ---------------------------
    # INPUTS p_sim2 (1685790, 10)
    # ---------------------------
    #  (1) single1: irradiance @ 305 nm [Ir1]
    #  (2) single2: irradiance @ 312 nm [Ir2]
    #  (3) single3: irradiance @ 320 nm [Ir3]
    #  (4) single4: irradiance @ 340 nm [Ir4]
    #  (5) single5: irradiance @ 380 nm [Ir5]
    #  (6) solar zenith angle [SZA]
    #  (7) day of the year [DOY
    #  (8) [Cos(DOY)]
    #  (9) [Sin(DOY)]
    # (10) day of the week (DOW)
    # ---------------------------
    # TIME t_sim2 (1685790, 1)
    # ---------------------------
    # OUTPUTS y_sim2 (1685790, 6) 
    # ---------------------------
    # (1) Ir1: vitamin D with action spectrum 1 [VitD(AS1)]
    # (2) Ir2: vitamin D with action spectrum 2 [VitD(AS2)]
    # (3) vitamin D with action spectrum from Ilias [VitD(AS3)]
    # (4) DNA damage effective dose (DNAD)
    # (5) CIE erythemal dose (CIE)
    # (6) Plant Growth (PG)
    # ---------------------------

    # EXTRACT INPUTS:
    x = py_dict['p_sim2'].T

    # EXTRACT OUTPUTS:
    y = py_dict['y_sim2'].T

    # CONVERT MATLAB DATETIME TO PANDAS DATETIME: 
    # NB: 719529 is the Matlab datenum value of the Unix epoch start (1970-01-01)
    t = pd.to_datetime(py_dict['t_sim2'] - 719529, unit='D')

    # SELECT SAMPLE:
    x = x[0:10000,:]
    y = y[0:10000,:]
    t = t[0:10000]

    # PANDAS COLUMN HEADINGS:
    x_cols = ['Ir_305','Ir_312','Ir_320','Ir_340','Ir_380','SZA','DOY','CosDOY','SinDOY','DOW']
    y_cols = ['VitaminD_AS1','VitaminD_AS2','VitaminD_AS3','DNA_Damage','CIE','Plant_Growth']
    cols = np.append(x_cols,y_cols)

    # MERGE INPUTS & OUTPUTS INTO PANDAS DATAFRAME:
    df1 = pd.DataFrame(x, columns=x_cols, index=t)
    df2 = pd.DataFrame(y, columns=y_cols, index=t)
    df = pd.concat([df1,df2], axis=1)

    return df

if __name__ == "__main__":

#    parser = OptionParser("usage: %prog file_in")
#    (options, args) = parser.parse_args()
#    file_in = args[0]
    file_in = 'RUN_06_04_2016.mat'
    df = create_dataframe(file_in)
    df.to_excel('mike.xlsx', sheet_name='Sheet1')
 
    df[{'Ir_305','VitaminD_AS3'}].plot()
    plt.savefig('mike.png')



