#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:05:06 2022

@author: miramota
"""
#%%

import tkinter as tk
from tkinter import filedialog
import os 

root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()
#filename = 'tester.xlsx'
#file_path = os.path.join(folder_path + '/' + filename)

#%%
import czifile 
import numpy as np
from skimage import filters
from matplotlib import pyplot as plt
from statistics import mean

path = ('/Users/miramota/Desktop/IMGS/01142022_Injury5.czi')
img = czifile.imread(path)
img = img[0,0,0,:,:,:,0]
maximg = img.max(axis = 0)
thresh = filters.threshold_otsu(maximg)

binary_mask = maximg >= thresh
fig, ax = plt.subplots()
plt.imshow(binary_mask, cmap='gray')
plt.show()







#%%
import numpy as np
from matplotlib import pyplot as plt
import czifile 

im= czifile.imread('/Users/miramota/Downloads/Injury/01142022_Injury9.czi')
max = im.max(axis =0)

plt.imshow(max, interpolation='nearest')
plt.show()

 #%%
 
#import os.path
#import os.path, time
from pathlib import Path
import czifile
import pandas as pd

 
injury = []
no_injury = []
noinjury_filepath = []
injury_filepath = []


for dir, subdir, files in os.walk(folder_path):
    # print(files)
    for x in files:
            if 'NoInjury' in x:
                noinjury_filepath.append(os.path.join(dir,x))
                no_injury.append(x)
            else:
                injury_filepath.append(os.path.join(dir,x))
                injury.append(x)
            if '.DS_Store' in x:
                continue

imgs_df = pd.DataFrame(list(zip(noinjury_filepath, no_injury)),
                       columns = ['No Injury Filepath', 'Filename'])   
        
noinjury_values= []
noinjury_max= []
injury_values= []
injury_max = []
noinjury_otsu = []

for i in noinjury_filepath:
    value = czifile.imread(i)
    value = value[0,0,0,:,:,:,0]
    noinjury_values.append(value)
    noi_max = np.max(value, axis = 0)
    noinjury_max.append(noi_max)
    for noi in noinjury_max:
        threshold = filters.threshold_otsu(noi)
        noinjury_otsu.append(threshold)
        avgmax = mean(noinjury_otsu)
        return avgmax
        
    

for z in injury_filepath[1:]:
    num = czifile.imread(z)
    num = num[0,0,0,:,:,:,0]
    injury_values.append(num)
    i_max = np.max(num, axis = 0)
    injury_max.append(i_max)
    
imgs_df['No Injury Values'], imgs_df['No Injury Max Proj'], imgs_df['Injury Values'], imgs_df['Injury Max Proj'] = [noinjury_values, noinjury_max, injury_values, injury_max]


  






