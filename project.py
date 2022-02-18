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
from skimage import filters, color
from matplotlib import pyplot as plt
from statistics import mean

pathin = ('/Users/miramota/Desktop/IMGS/01142022_Injury5.czi')
pathnoi = ('/Users/miramota/Desktop/IMGS/01142022_NoInjury9.czi')

with czifile.CziFile(path) as czi:
    xml_metadata = czi.metadata()

#find timestamps (this is relevant only if you have a time series, but you don’t have one because the fourth axis in your .czi file is empty)
#for attachment in czi.attachments():
#if attachment.attachment_entry.name == ‘TimeStamps’:
#timestamps = attachment.data()
#break

#This gets the resolution of the image in microns.
root = ET.fromstring(xml_metadata)
for neighbor in root.iter('ScalingX'):
    pixel_size_in_meters = neighbor.text
    pixel_size_in_microns = float(pixel_size_in_meters)*1000000
    resolution_x = 1/pixel_size_in_microns

    
img = czifile.imread(path)
img = img[0,0,0,:,:,:,0]
maximg = img.max(axis = 0)
thresh = filters.threshold_otsu(maximg)

binary_mask = maximg >= thresh
fig, ax = plt.subplots()
plt.imshow(binary_mask, cmap='gray')
plt.show()

#%%

fig, ax = plt.subplots(figsize =(10, 7))
N=30
ax.hist(maximg.flatten(), bins = N+1, range=(0,N))
plt.show()



#%%
import numpy as np
from matplotlib import pyplot as plt
import czifile 

im= czifile.imread('/Users/miramota/Downloads/Injury/01142022_Injury9.czi')
im= czifile.imread('/Users/miramota/Desktop/IMGS/01142022_NoInjury9.czi')

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

#endswith .czi 
for dir, subdir, files in os.walk(folder_path):
    # print(files)
    for x in files:
            if 'No Injury' in x:
                noinjury_filepath.append(os.path.join(dir,x))
                no_injury.append(x)
            else:
                injury_filepath.append(os.path.join(dir,x))
                injury.append(x)
            if '.DS_Store' in x:
                continue

imgs_df = pd.DataFrame(list(zip(injury_filepath, injury)),
                       columns = ['Filepath', 'Filename'])   
        
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
    
        
    

for z in injury_filepath[1:]:
    num = czifile.imread(z)
    num = num[0,0,0,:,:,:,0]
    injury_values.append(num)
    i_max = np.max(num, axis = 0)
    injury_max.append(i_max)
    
imgs_df['No Injury Values'], imgs_df['No Injury Max Proj'], imgs_df['Injury Values'], imgs_df['Injury Max Proj'] = [noinjury_values, noinjury_max, injury_values, injury_max]


'''
img_values = []
max_values = []
for image in dfname['Filepath']:
        reader = AICSImage(image)
        img_array = reader.get_image_data('ZYX', T =0, C=0)
        img_values.append(img_array)
        maxprojection = img_array.max(axis = 0)
        max_values.append(maxprojection)'''
#%%

fig, ax = plt.subplots(figsize =(10, 7))
ax.hist(maximg.flatten(), bins = 256, range=(0,30))
plt.show()


#%%

from aicsimageio import AICSImage
# aicsimageio[czi]

path = ('~/Desktop/IMGS/01142022_NoInjury9.czi')
czi_img = AICSImage(path)

c = czi_img.get_image_data('ZYX', T= 0, C=0)

blur = skimage.filters.gaussian(czi_array, sigma = 1.0)

meanvalue = i[binaryi].mean()

#%%
#THIS ONE 
# dfcopy = imgs_df.copy()

def add_values_to_df(dfname, mode, titles , list_to_add):
    '''
    Trying to make a function to add lists created while going through a current dataframe \
        into new rows or columns depending on what is defined in mode. 
        
    Parameters
    ----------
    dfname : dataframe
        Dataframe to add to.
    mode: row or column
    [titles] : list
        list of the titles want to add to the dataframe in string.
    [list_of_dfs] : list
        list of the lists that were created to add to the dataframe. Order has to match with the titles \
            that were in the list of titles. 
            

    Returns
    -------
    DataFrame

    '''
    if mode == 'column':    
        i = 0
        for x in (titles): 
            dfname[x] = list_of_dfs[i]
            i+=1
    if mode == 'row':
        df = pd.DataFrame()
        for x in list_to_add:
            df = pd.DataFrame(list(zip(list_to_add)),columns = [titles])
            dfname = dfname.concat([dfname, df], sort =False).fillna(0)
            #dfname.append(df, ignore_index=True).fillna(0)
            
    return dfname
      
dfcopy = add_values_to_df(dfcopy, mode = 'row' , titles = titles, list_to_add= [row10,row11])
#adding rows to dataframe 
#d = pd.DataFrame(list(zip(injury_filepath, injury)),columns = ['Filepath', 'Filename'])


duplicated = pd.concat([dfcopy, dfcopy.loc[:,['Filename', 'Filepath']]], axis=0, join='outer')
print(duplicated)

new_files_path = Path('/Users/miramota/Desktop/new')
print(list(new_files_path.iterdir()))

def calc_metric(file):
    
    img = czifile.imread(file)
    img = img[0,1,:,:,:,0]
    maximg = img.max(axis = 0)
    # norm
    thresh = filters.threshold_otsu(maximg)
    
    binary_mask = maximg >= thresh
    
    grand_mean = maximg[binary_mask].mean()
    
    return grand_mean

for file in new_files_path.iterdir():
    if file.stem == '.DS_Store':
        continue
    
    metric = calc_metric(file)
    
    res_dict = {'Filename':str(file.stem), 'Filepath':str(file), 'metric':metric}

for file in new_files_path.iterdir():
    if file.stem == '.DS_Store':
        continue
    

    
    metric = calc_metric(file)
    
    res_dict = {'Filename':str(file.stem), 'Filepath':str(file), 'metric':metric}
    
    
    dfcopy= dfcopy.append(res_dict, ignore_index=True)


#adds rows to dataframe  but have to make a dataframe first 
#dfappend = dfcopy.append(d, ignore_index = True) 