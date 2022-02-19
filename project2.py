#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 16:52:03 2022

@author: miramota
"""
import numpy as np
from matplotlib import pyplot as plt
from aicsimageio import AICSImage
from pathlib import Path
import czifile
import pandas as pd
from skimage import filters 
import statistics 
# aicsimageio[czi]

folder_path = '/Users/miramota/Desktop/IMGS'
folder_path = Path(folder_path)

def calculate_metrics(path):
    czi_img = AICSImage(path)
    height = czi_img.dims.Y
    width = czi_img.dims.X
    area = height * width 
    czi_array = czi_img.data
    czi_array = czi_array[0,0,:,:,:,]
    maximg = czi_array.max(axis = 0)
    
    thresh = filters.threshold_otsu(maximg)
    binary_mask = maximg >= thresh
    
    #fig, ax = plt.subplots()
    #plt.imshow(binary_mask, cmap='gray')
    #plt.show()
    
    mean_value = maximg[binary_mask].mean()
    count = np.sum(binary_mask)
    percentarea = (count / area) * 100
    keys = 'Mean Value', 'Percent Area'
    values = [mean_value , percentarea]
    # metric = {'': [mean_value], 'Percent Area': []}
    return keys , values

#czi_img = czi_img.get_image_data('ZYX', T=0, C=1)
#c = czi_img.get_image_data('ZYX', T= 0, C=0)


for file in folder_path.iterdir():
    metric = {}
    if file.stem == '.DS_Store':
        continue
    loop = calculate_metrics(file)
    metric.update(loop)

file_df = pd.DataFrame.from_dict({'Filename':[str(file.stem)], 'Filepath':[str(file)]})
df = pd.DataFrame.from_dict(metric, orient = 'columns')

final_df = pd.concat([file_df, df], axis = 1)


def calculate_threshold(path):
    czi_img = AICSImage(path)
    czi_array = czi_img.data
    czi_array = czi_array[0,0,:,:,:,]
    maximg = czi_array.max(axis = 0)
    thresh = filters.threshold_otsu(maximg)
    return thresh 



noinjury = []
injury= []
noinjury_rnai= []
injury_rnai= [] 
nornai = []
rnais = []

for file in folder_path.rglob('*'):
    if file.suffix == '.czi':
        if 'RNAi' not in file.stem:
            nornai.append(file)
        elif 'RNAi' in file.stem:
            rnais.append(file)     
            
for x in nornai: 
    if 'NoInjury' in x.stem:
        noinjury.append(x)
    elif 'NoInjury' not in x.stem:
        injury.append(x)
for y in rnais: 
    if 'NoInjury' in y.stem:
        noinjury_rnai.append(y)
    elif 'NoInjury' not in y.stem: 
        injury_rnai.append(y)

no_injury_thresholds = []
for file in folder_path.iterdir():
    if 'NoInjury' in file.stem:
        print(file)
        file = file.absolute()
        file = file.as_posix()
        threshold = calculate_threshold(file)
        no_injury.append(threshold)
        mean = statistics.mean(no_injury)
    print(mean)
        
        
def calculate_metrics(maximg ,thresh):
   height = maximg.shape[0]
   width = maximg.shape[1]
   area = height * width 
   binary_mask = maximg >= thresh
    #fig, ax = plt.subplots()
    #plt.imshow(binary_mask, cmap='gray')
    #plt.show()
   mean_value = maximg[binary_mask].mean()
   count = np.sum(binary_mask)
   percentarea = (count / area) * 100
   metric = {'Mean Value': [mean_value], 'Percent Area': [percentarea]}
   return metric

z= '/Users/miramota/Desktop/IMGS/01142022_NoInjury9.czi'
czi_img = AICSImage(z)
czi_array = czi_img.data
czi_array = czi_array[0,0,:,:,:,]
maxz = czi_array.max(axis = 0)

calc = calculate_metrics(maxz, 19)


file_df = pd.DataFrame.from_dict({'Filename':[str(file.stem)], 'Filepath':[str(file)]})