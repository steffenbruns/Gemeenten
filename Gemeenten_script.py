#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
import glob
import time
import pandas as pd
import json
import ast
import Gemeenten


# In[2]:


# Opslag vullen met informatie van de drie plaatsen.
Gemeenten.create_plaats({"naam": "Plaats 1", "cbscode":"WPL001", "inwonersaantal": 100, "gemeente":"GEM001"})
Gemeenten.create_plaats({"naam": "Plaats 2", "cbscode":"WPL002", "inwonersaantal": 150, "gemeente":"GEM002"})
Gemeenten.create_plaats({"naam": "Plaats 3", "cbscode":"WPL003", "inwonersaantal": 250, "gemeente":"GEM002"})


# In[3]:


# Opslag vullen met de informatie van de gemeenten.
Gemeenten.create(input_dict={"naam":"Gemeente 1", "cbscode":"GEM001", "plaatsen":["WPL001"]})
Gemeenten.create(input_dict={"naam":"Gemeente 2", "cbscode":"GEM002", "plaatsen":["WPL002", "WPL003"]})


# In[4]:


# Woonplaats naar andere gemeente verplaatsen.
Gemeenten.move_plaats(cbs_plaats="WPL001", cbs_gemeente_old="GEM001", cbs_gemeente_new="GEM002")


# In[5]:


# Informatie voor specifieke gemeente opvragen.
Gemeenten.read(cbs_code="GEM002")


# In[6]:


# Lijst van alle gemeenten verkrijgen.
Gemeenten.read_all()


# In[7]:


# Informatie van specifieke gemeente updaten.
Gemeenten.update(input_dict={"naam":"Gemeente 2 Nieuw", "cbscode":"GEM002", "plaatsen":["WPL001", "WPL002", "WPL003"]})


# In[8]:


# Gemeente verwijderen.
Gemeenten.delete(cbs_code="GEM002")


# In[ ]:




