#!/usr/bin/env python
# coding: utf-8

# ## 1. DATA EXPLORATORY ANALYSIS

# In[1]:


# Import packages
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


# Load data file
ecars = pd.read_csv('eCars.csv', index_col=0)
print("Data Shape =", ecars.shape)
ecars.head()


# In[12]:


ecars['Precio desde €'].max()


# In[4]:


ecars.loc[ecars["Capacidad batería (kWh)"] == ecars["Capacidad batería (kWh)"].min()]


# In[5]:


ecars.info()


# In[6]:


ecars.plot.scatter(x='Potencia máxima (CV)', y='Capacidad batería (kWh)')


# In[23]:


import seaborn as sns
import numpy as np
f, ax = plt.subplots(figsize=(10, 8))
corr = ecars.corr()
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax, annot=True)


# In[24]:


# Distribution of the variables

var = ecars.columns[2:]
fig, ax = plt.subplots(5,3, figsize=(15,20))
count = 0
fig.suptitle('Variables Distribution')
for row in range(0,5):
    for col in range(0,3):
        if count == 13:
            break
        else:
            ecars[var[count]].hist(ax=ax[row,col], alpha=0.9)
            ax[row,col].set_xlabel(var[count])
            ax[row,col].set_axisbelow(True)
            count += 1

fig.delaxes(ax[4,1])
fig.delaxes(ax[4,2])


# In[25]:


ecars[ecars.isnull().any(axis=1)]


# In[26]:


# Replace null values by the average brand
ecars.iloc[4,11] = ecars.loc[ecars.Brand == 'Citroën', '0 a 100 km/h (seg.)'].mean()

ecars.iloc[10,14] = ecars.loc[ecars.Brand == 'Kia', 'Precio desde €'].mean()
ecars.iloc[11,14] = ecars.loc[ecars.Brand == 'Kia', 'Precio desde €'].mean()

ecars.iloc[22,3] = ecars.loc[ecars.Brand == 'Tesla', 'Par máximo (mkg)'].mean()
ecars.iloc[23,3] = ecars.loc[ecars.Brand == 'Tesla', 'Par máximo (mkg)'].mean()

ecars.to_csv('eCars.csv')


# In[27]:


# Perform PCA
from sklearn.decomposition import PCA
X = np.array(ecars[var])

pca = PCA(n_components=2)
principal_comp = pca.fit_transform(X)


# In[28]:


plt.plot(principal_comp[:,0], principal_comp[:,1], 'ro', alpha=0)
for i in range(principal_comp.shape[0]):
    plt.text(principal_comp[i,0], principal_comp[i,1], str(i), color='red')

plt.show()


# In[ ]:





# In[ ]:




