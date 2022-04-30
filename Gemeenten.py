#!/usr/bin/env python
# coding: utf-8

# In[169]:


import numpy as np
import os
import glob
import time
import pandas as pd
import json
import ast


# In[170]:


def open_database(plaats_type):
    database_name = ""
    for file in glob.glob("*.xlsx"):
        if plaats_type==1:
            if "Plaatsen" in file:
                database_name = file
        if plaats_type==2:
            if "Gemeenten" in file:
                database_name = file
    if os.path.isfile(database_name):
        print("Opening the database " + database_name) 
        df = pd.read_excel(database_name, usecols="B:E")
        data_dict = df.to_dict('records')
    else:
        data_dict = []
    return data_dict


# In[171]:


def write_database(data_dict, plaats_type):   
    df = pd.DataFrame(data_dict)
    if plaats_type==1:
        df.to_excel('Plaatsen{}.xlsx'.format(str(time.time())))
    if plaats_type==2:
        df.to_excel('Gemeenten{}.xlsx'.format(str(time.time())))


# In[172]:


def create_plaats(input_dict):
    cbs_code = input_dict['cbscode']
    if len(cbs_code) != 6 or "WPL" not in cbs_code[:3] or cbs_code[3:].isdecimal() is False:
        raise ValueError('CBS code niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "WPL" gevolgd worden door drie cijfers.')
    Plaatsen = open_database(plaats_type=1)
    if any(d['cbscode'] == cbs_code for d in Plaatsen):
        print("De plaats met CBS code {} bestaat al.".format(cbs_code))
    else:
        Plaatsen.append(input_dict)
        write_database(data_dict=Plaatsen, plaats_type=1)


# In[173]:


def create(input_dict):
    cbs_code = input_dict['cbscode']
    if len(cbs_code) != 6 or "GEM" not in cbs_code[:3] or cbs_code[3:].isdecimal() is False:
        raise ValueError('CBS code niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "GEM" gevolgd worden door drie cijfers.')
    Gemeenten = open_database(plaats_type=2) 
    if any(d['cbscode'] == cbs_code for d in Gemeenten):
        print("De gemeente met CBS code {} bestaat al.".format(cbs_code))
    else:
        plaatsen_gemeente = input_dict['plaatsen']
        inwoners_gemeente = 0
        Plaatsen = open_database(plaats_type=1)
        for plaats in plaatsen_gemeente:
            #print(plaats)
            place = next(item for item in Plaatsen if item["cbscode"] == plaats)
            inwoners_gemeente += place["inwonersaantal"]
        input_dict['inwonersaantal'] = inwoners_gemeente
        Gemeenten.append(input_dict)
        write_database(data_dict=Gemeenten, plaats_type=2)


# In[174]:


def read(cbs_code):
    if len(cbs_code) != 6 or "GEM" not in cbs_code[:3] or cbs_code[3:].isdecimal() is False:
        raise ValueError('CBS code niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "GEM" gevolgd worden door drie cijfers.')
    Gemeenten = open_database(plaats_type=2) 
    gemeente = next(item for item in Gemeenten if item["cbscode"] == cbs_code)
    print(gemeente)


# In[175]:


def read_all():
    Gemeenten = open_database(plaats_type=2) 
    print(Gemeenten)


# In[176]:


def update(input_dict):
    cbs_code = input_dict['cbscode']
    if len(cbs_code) != 6 or "GEM" not in cbs_code[:3] or cbs_code[3:].isdecimal() is False:
        raise ValueError('CBS code niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "GEM" gevolgd worden door drie cijfers.')
    Gemeenten = open_database(plaats_type=2) 
    if any(d['cbscode'] == cbs_code for d in Gemeenten):
        Gemeenten_new = [i for i in Gemeenten if not (i['cbscode'] == cbs_code)]
        plaatsen_gemeente = input_dict['plaatsen']
        inwoners_gemeente = 0
        Plaatsen = open_database(plaats_type=1)
        for plaats in plaatsen_gemeente:
            #print(plaats)
            place = next(item for item in Plaatsen if item["cbscode"] == plaats)
            inwoners_gemeente += place["inwonersaantal"]
        input_dict['inwonersaantal'] = inwoners_gemeente
        Gemeenten_new.append(input_dict)
        write_database(data_dict=Gemeenten_new, plaats_type=2)
    else:
        print("De gemeente met CBS code {} bestaat niet.".format(cbs_code))


# In[177]:


def delete(cbs_code):
    if len(cbs_code) != 6 or "GEM" not in cbs_code[:3] or cbs_code[3:].isdecimal() is False:
        raise ValueError('CBS code niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "GEM" gevolgd worden door drie cijfers.')
    Gemeenten = open_database(plaats_type=2) 
    if any(d['cbscode'] == cbs_code for d in Gemeenten):
        Gemeenten_new = [i for i in Gemeenten if not (i['cbscode'] == cbs_code)]
        write_database(data_dict=Gemeenten_new, plaats_type=2)
    else:
        print("De gemeente met CBS code {} bestaat niet.".format(cbs_code))


# In[178]:


def move_plaats(cbs_plaats, cbs_gemeente_old, cbs_gemeente_new):
    if len(cbs_plaats) != 6 or "WPL" not in cbs_plaats[:3] or cbs_plaats[3:].isdecimal() is False:
        raise ValueError('CBS code van de plaats is niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "WPL" gevolgd worden door drie cijfers.')
    if len(cbs_gemeente_old) != 6 or "GEM" not in cbs_gemeente_old[:3] or cbs_gemeente_old[3:].isdecimal() is False:
        raise ValueError('CBS code van de oorspronkelijke gemeente is niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "GEM" gevolgd worden door drie cijfers.')
    if len(cbs_gemeente_new) != 6 or "GEM" not in cbs_gemeente_new[:3] or cbs_gemeente_new[3:].isdecimal() is False:
        raise ValueError('CBS code van de nieuwe gemeente is niet geldig. Het moet uit precies 6 tekens bestaan waarbij de eerste drie tekens "GEM" gevolgd worden door drie cijfers.')
    Gemeenten = open_database(plaats_type=2)
    if any(d['cbscode'] == cbs_gemeente_old for d in Gemeenten) and any(j['cbscode'] == cbs_gemeente_new for j in Gemeenten):
        gemeente_old = next(item for item in Gemeenten if item["cbscode"] == cbs_gemeente_old)
        Gemeenten_1 = [i for i in Gemeenten if not (i['cbscode'] == cbs_gemeente_old)]
        plaatsen_gemeente_old = gemeente_old['plaatsen']
        plaatsen_gemeente_old_list = ast.literal_eval(plaatsen_gemeente_old)
        plaatsen_gemeente_old_list.remove(cbs_plaats)
        Plaatsen = open_database(plaats_type=1)
        if len(plaatsen_gemeente_old_list) > 0:
            inwoners_gemeente_old_updated = 0
            for plaats in plaatsen_gemeente_old_list:
                place = next(item for item in Plaatsen if item["cbscode"] == plaats)
                inwoners_gemeente_old_updated += place["inwonersaantal"]
            gemeente_old['inwonersaantal'] = inwoners_gemeente_old_updated
            gemeente_old['plaatsen'] = plaatsen_gemeente_old_list
            Gemeenten_1.append(gemeente_old)
            
        gemeente_new = next(item for item in Gemeenten_1 if item["cbscode"] == cbs_gemeente_new)
        Gemeenten_2 = [i for i in Gemeenten_1 if not (i['cbscode'] == cbs_gemeente_new)]
        plaatsen_gemeente_new = gemeente_new['plaatsen']
        plaatsen_gemeente_new_list = ast.literal_eval(plaatsen_gemeente_new)
        plaatsen_gemeente_new_list.append(cbs_plaats)
        inwoners_gemeente_new_updated = 0
        for plaats in plaatsen_gemeente_new_list:
            place = next(item for item in Plaatsen if item["cbscode"] == plaats)
            inwoners_gemeente_new_updated += place["inwonersaantal"]
        gemeente_new['inwonersaantal'] = inwoners_gemeente_new_updated
        gemeente_new['plaatsen'] = plaatsen_gemeente_new_list
        Gemeenten_2.append(gemeente_new)
        write_database(data_dict=Gemeenten_2, plaats_type=2)
        plaats_old = next(item for item in Plaatsen if item["cbscode"] == cbs_plaats)
        Plaatsen_1 = [j for j in Plaatsen if not (j['cbscode'] == cbs_plaats)]
        plaats_old["gemeente"] = cbs_gemeente_new
        Plaatsen_1.append(plaats_old)
        write_database(data_dict=Plaatsen_1, plaats_type=1)
    else:
        print("Een van de gemeenten staat niet in de database.")

