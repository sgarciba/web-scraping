#!/usr/bin/env python
# coding: utf-8

# ## 1. LOAD DATA

# In[1]:


# Import packages
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


# In[2]:


r = requests.get('https://www.cea-online.es/blog/496-coches-electricos-disponibles-en-espana')

# Convert to a beautiful soup object
soup = bs(r.content)
# Print out the HTML
contents = soup.prettify()
print(contents)


# In[3]:


# Get the information of the tables
info_article = soup.find(class_='tm-article-content')
info_article = info_article.find_all('table')
tables = [row for row in info_article]
print('Number of Tables:', len(tables))


# In[4]:


# Create a dictionary with all the info of the cars
def get_content(table):
    lines = table.find_all('tr')
    ecar_info = {}
    for index, row in enumerate(lines):
        if index==0:
            ecar_info['model'] = row.find('h4').get_text(' ', strip=True)
        else:
            content = row.find_all('td')
            content_key = content[0].get_text(' ', strip=True)
            content_value = content[1].get_text(' ', strip=True)
            ecar_info[content_key] = content_value

    return ecar_info

ecars = [get_content(car) for car in tables]
ecars[0]


# In[38]:


# Create a DataFrame
data = pd.DataFrame(ecars)
data.head()


# ## 2. DATA CLEANING

# In[39]:


# Clean data and change types

# Model
data['Brand'] = data.model.apply(lambda x: x.split(' ')[0])
data['Model'] = data.model.apply(lambda x: ' '.join(x.split(' ')[1:]))

# Potencia máxima
data['Potencia máxima (CV)'] = data['Potencia máxima'].apply(lambda x: int(x.split(' ')[0]))

# Par máximo
data['Par máximo (mkg)'] = data['Par máximo'].apply(lambda x: x.split(' ')[0])
data['Par máximo (mkg)'] = data['Par máximo (mkg)'].replace({'n.d.': None})
data['Par máximo (mkg)'] = data['Par máximo (mkg)'].apply(lambda x: float(x.replace(',', '.')) if x !=None else x)

# Tracción
data['Tracción total'] = data.Tracción.map({'Total': 1, 'Delantera': 0, 'Trasera': 0})
data['Tracción delantera'] = data.Tracción.map({'Total': 0, 'Delantera': 1, 'Trasera': 0})

# Largo/Ancho/Alto (mm)
data['Largo/Ancho/Alto (mm)'] = data['Largo/Ancho/Alto (mm)'].apply(lambda x: x.split('/'))
data['Largo (mm)'] = data['Largo/Ancho/Alto (mm)'].apply(lambda x: float(x[0]))
data['Ancho (mm)'] = data['Largo/Ancho/Alto (mm)'].apply(lambda x: float(x[1]))
data['Alto (mm)'] = data['Largo/Ancho/Alto (mm)'].apply(lambda x: float(x[2]))

# Maletero
data['Maletero(l)'] = data['Maletero (l)'].apply(lambda x: x.replace('.', ''))
data['Maletero(l)'] = data['Maletero(l)'].apply(lambda x: x.split(' ')[0])
data['Maletero(l)'] = data['Maletero(l)'].apply(lambda x: x.split('+') if '+' in x else x)
data['Maletero(l)'] = data['Maletero(l)'].apply(lambda x: x.split('/') if '/' in x else x)
data['Maletero(l)'][14][0] = 0 # Exception, change 'nd' for 0, in order to be able to sum
int_list = lambda x: sum([int(i) for i in x])
data['Maletero(l)'] = data['Maletero(l)'].apply(lambda x: int(x) if type(x) != list else int_list(x))


data.head()


# In[49]:


# Capacidad bateria
data['Capacidad batería (kWh)'] = data['Capacidad batería'].apply(lambda x: x.split(' ')[0])
data['Capacidad batería (kWh)'] = data['Capacidad batería (kWh)'].apply(lambda x: float(x.replace(',','.')))

# 0 a 100 km/h
data['0 a 100 km/h (seg.)'] = data['0 a 100 km/h'].apply(lambda x: x.split(' ')[0])
data['0 a 100 km/h (seg.)'] = data['0 a 100 km/h (seg.)'].replace({'n.d.': None})
data['0 a 100 km/h (seg.)'] = data['0 a 100 km/h (seg.)'].apply(lambda x: float(x.replace(',', '.')) if x !=None else x)

# Velocidad máxima
data['Velocidad máxima (km/h)'] = data['Velocidad máxima'].apply(lambda x: int(x[:3]))

# Autonomía media
data['Autonomía media (km)'] = data['Autonomía media'].apply(lambda x: x.split(' ')[0])
data['Autonomía media (km)'] = data['Autonomía media (km)'].apply(lambda x: x.split('-') if '-' in x else x)
data['Autonomía media (km)'] = data['Autonomía media (km)'].apply(lambda x: [int(i) for i in x] if type(x) == list else int(x))
data['Autonomía media (km)'] = data['Autonomía media (km)'].apply(lambda x: sum(x)//2 if type(x) == list else x)

# Precio desde
data['Precio desde €'] = data['Precio desde'].apply(lambda x: x.split(' ')[0])
data['Precio desde €'] = data['Precio desde €'].replace({'N.D.': None})
data['Precio desde €'] = data['Precio desde €'].apply(lambda x: int(x.replace('.', '')) if x != None else x)

data.head()


# In[56]:


# Save final Data
new_columns = ['Model', 'Brand', 'Potencia máxima (CV)', 'Par máximo (mkg)',
       'Tracción total', 'Tracción delantera', 'Largo (mm)', 'Ancho (mm)',
       'Alto (mm)', 'Maletero(l)', 'Capacidad batería (kWh)',
       '0 a 100 km/h (seg.)', 'Velocidad máxima (km/h)',
       'Autonomía media (km)', 'Precio desde €']

final_data = data[new_columns]
final_data.to_csv('eCars.csv')


# In[ ]:




