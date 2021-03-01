PATH = "../Data"
import pandas as pd
import sqlite3
import numpy as np

## Connect and pull everything from the db
con = sqlite3.connect(PATH+"/patents.db")
df = pd.read_sql_query("SELECT * FROM summary", con)
# con.close()

## Select IPC column
df_ipc = df[['applicationNum', 'ipc']]
## Replace empty string and None with np.nan
df_ipc = df_ipc.fillna(np.nan).replace("", np.nan)
## Split ipcs into list
df_ipc['ipc'] = df_ipc['ipc'].str.split("; ")


## Split into different components of IPC
df_ipc = df_ipc.explode('ipc', ignore_index=True)
df_ipc = df_ipc.dropna().reset_index(drop=True)
df_ipc['ipc'] = df_ipc['ipc'].str.replace(" ", "")

df_ipc['section'] = df_ipc['ipc'].str[0] # letter
df_ipc['class'] = df_ipc['ipc'].str[:3] # section + 2 digits
df_ipc['subclass'] = df_ipc['ipc'].str[:4] # class + letter
df_ipc['main_group'] = df_ipc['ipc'].str.split("/").str[0] # subclass + 0-3 digits before /
df_ipc['subgroup'] = df_ipc['ipc'] # ipc itself


## Check IPC validity

### Section ###
## Each section is designated by one of the capital letters A through H.
##
## Eg.H
# print(df_ipc['section'].unique())
# df_ipc[df_ipc['section'].isin(['I', '0'])]

## remove invalid ipcs
df_ipc = df_ipc[~df_ipc['section'].isin(['I', '0'])]


### Class ###
## Each class symbol consists of 
## - the section symbol 
## - a two-digit number
## 
## Eg. H01

## ipcs with invalid class
invaid_class = [x for x in df_ipc['class'].unique() if not x[1:].isdigit()]
# df_ipc[df_ipc['class'].isin(invaid_class)]


## remove invalid ipcs
df_ipc = df_ipc[~df_ipc['class'].isin(invaid_class)]


### Subclass
## Each subclass symbol consists of 
## - the class symbol 
## - a capital letter
## 
## Eg. H01L

## ipcs with invalid subclass, check if last char is letter
invaid_subclass = [x for x in df_ipc['subclass'].unique() if not x[-1].isalpha()]
# df_ipc[df_ipc['subclass'].isin(invaid_subclass)]

## remove invalid ipcs
df_ipc = df_ipc[~df_ipc['subclass'].isin(invaid_subclass)]


### Main group
## Each main group symbol consists of 
## - the subclass symbol 
## - a one- to three-digit number
## - the oblique stroke
## - the number 00.
## 
## Eg. H01L29/00

## ipcs with invalid main group, check if last 1-3 chars are digits
invaid_main_group = [x for x in df_ipc['main_group'].unique() if not x[4:].isdigit()]
# df_ipc[df_ipc['main_group'].isin(invaid_main_group)]


## remove invalid ipcs
df_ipc = df_ipc[~df_ipc['main_group'].isin(invaid_main_group)]


### Sub group
## Each subgroup symbol consists of 
## - the subclass symbol 
## - the one- to three-digit number of its main group
## - the oblique stroke
## - a number of at least two digits other than 00.
## 
## Eg. H01L29/49

## ipcs with invalid subgroup, check if last 1-3 chars are digits. Can have no subgroup too
invaid_subgroup = [x for x in df_ipc['subgroup'].str.split("/").str[1] if x!=np.nan or not x.isdigit()]
# df_ipc[df_ipc['subgroup'].isin(invaid_subgroup)]

# #remove invalid ipcs
df_ipc = df_ipc[~df_ipc['subgroup'].isin(invaid_subgroup)]

print(df_ipc.head())
## Connect and write to the db
cursor = con.cursor()
cursor.execute(
    '''
    DROP TABLE IF EXISTS app_ipc
    '''
    )
cursor.execute(
    '''
    CREATE TABLE app_ipc (
        applicationNum TEXT,
        ipc TEXT,
        section TEXT,
        class TEXT,
        subclass TEXT,
        mainGroup TEXT,
        subGroup TEXT
    );
    '''
    )
cursor.executemany('INSERT INTO app_ipc VALUES (?, ?, ?, ?, ?, ?, ?)',  df_ipc.values.tolist())
con.commit()
con.close()

