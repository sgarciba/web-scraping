#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import math
import functools
import numpy as np


# In[3]:


ecars = pd.read_csv('eCars.csv', index_col=0)
ecars


# In[4]:


# Because the variables have different scales, we should normalize the table before measuring distance
ecars_norm = ecars.copy()
ecars_norm.iloc[:,2:] = ecars_norm.iloc[:,2:].apply(lambda x: (x-x.mean())/ x.std(), axis=0)
ecars_norm.head()


# In[5]:


def n_dimensional_euclidean_distance(a, b):
   """
   Returns the euclidean distance for n>=2 dimensions
   :param a: tuple with integers
   :param b: tuple with integers
   :return: the euclidean distance as an integer
   """
   dimension = len(a) # notice, this will definitely throw a IndexError if len(a) != len(b)
   return round(math.sqrt(functools.reduce(lambda i,j: i + ((a[j] - b[j]) ** 2), range(dimension), 0)),2)


# In[6]:


# TEST: Compare e-Tron Audi with Model XP100D Tesla
eTron = list(ecars_norm.iloc[0,2:])
Xp100dTesla = list(ecars_norm.iloc[29,2:]) 
print('e-tron Audi:', list(ecars.iloc[0,2:]))
print('Model X100PD Tesla:', list(ecars.iloc[29,2:]))

dist = n_dimensional_euclidean_distance(eTron, Xp100dTesla)
print('\n')
print('Euclidean Distance:', dist)


# In[7]:


edist = np.zeros([len(ecars), len(ecars)])

for i in range(len(ecars)):
    edist[i,:] = list(n_dimensional_euclidean_distance(ecars_norm.iloc[i,2:],ecars_norm.iloc[j,2:]) for j in range(len(ecars)))


# In[8]:


ecars_dist = pd.DataFrame(edist)
ecars_dist


# In[9]:


# Create a function that given a new vector, finds the closest eCar

def your_ecar(vector, table, table_norm):
    """
    Create a function that given a new vector, finds the closest eCar
    """
    norm_fun = lambda x,y: (x-y.mean())/ y.std()
    vnorm = list(norm_fun(vector,table.iloc[:,2:]))

    neighbours = np.array(list(n_dimensional_euclidean_distance(vnorm,table_norm.iloc[i,2:]) for i in range(len(table))))
    idx = neighbours.argmin()
    
    return table.iloc[idx,:]


# In[10]:


your_ecar(list(ecars.iloc[3,2:]), ecars, ecars_norm)


# In[23]:


test_vector = [435.7, 70.27000000000001, 1, 0, 4.728470588235293, 1.9089999999999996, 1.6605000000000003, 1746.625, 84.41666666666667, 13.041250000000002, 227.0, 600.0, 100000.0]


# In[24]:


your_ecar(test_vector, ecars, ecars_norm)


# In[ ]:




