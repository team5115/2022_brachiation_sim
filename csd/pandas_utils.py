import pandas as pd
import inspect
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy
from astropy import units as u
from astropy.table import QTable, Table, Column
from PyQt5.QtWidgets import QWidget,QScrollArea, QTableWidget, QVBoxLayout,QTableWidgetItem
   
from csd import unit_utils
from csd import list_utils

import os
import inspect

#### Version: 5
####  Added filter 
####  Added add_nan_column
####  Added add_const_column_with_units

"""
loc - label based
Allows you to pass 1-D arrays as indexers. Arrays can be either slices (subsets) of the index or column, or they can be boolean arrays which are equal in length to the index or columns.

Special Note: when a scalar indexer is passed, loc can assign a new index or column value that didn't exist before.


iloc - position based
Similar to loc except with positions rather that index values. However, you cannot assign new columns or indices.


at - label based
Works very similar to loc for scalar indexers. Cannot operate on array indexers. Can! assign new indices and columns.

Advantage over loc is that this is faster.
Disadvantage is that you can't use arrays for indexers.



loc: only work on index
iloc: work on position
at: get scalar values. It's a very fast loc
iat: Get scalar values. It's a very fast iloc

Also,

at and iat are meant to access a scalar, that is, a single element in the dataframe, while loc and iloc are ments to access several elements at the same time, potentially to perform vectorized operations.

http://pyciencia.blogspot.com/2015/05/obtener-y-filtrar-datos-de-un-dataframe.html


Updated for pandas 0.20 given that ix is deprecated. This demonstrates
not only how to use loc, iloc, at, iat, set_value, but how to
accomplish, mixed positional/label based indexing.

loc - label based

Allows you to pass 1-D arrays as indexers. Arrays can be either slices
(subsets) of the index or column, or they can be boolean arrays which
are equal in length to the index or columns.

Special Note: when a scalar indexer is passed, loc can assign a new
index or column value that didn't exist before.

# label based, but we can use position values
# to get the labels from the index object
df.loc[df.index[2], 'ColName'] = 3
df.loc[df.index[1:3], 'ColName'] = 3

iloc - position based
Similar to loc except with positions rather that index values. However, you cannot assign new columns or indices.

# position based, but we can get the position
# from the columns object via the `get_loc` method
df.iloc[2, df.columns.get_loc('ColName')] = 3
df.iloc[2, 4] = 3
df.iloc[:3, 2:4] = 3
at - label based
Works very similar to loc for scalar indexers. Cannot operate on array indexers. Can! assign new indices and columns.

Advantage over loc is that this is faster.
Disadvantage is that you can't use arrays for indexers.

# label based, but we can use position values
# to get the labels from the index object
df.at[df.index[2], 'ColName'] = 3
df.at['C', 'ColName'] = 3
iat - position based
Works similarly to iloc. Cannot work in array indexers. Cannot! assign new indices and columns.

Advantage over iloc is that this is faster.
Disadvantage is that you can't use arrays for indexers.

# position based, but we can get the position
# from the columns object via the `get_loc` method
IBM.iat[2, IBM.columns.get_loc('PNL')] = 3

set_value are non-checked
ix is deprecated
"""

# position based, but we can get the position
# from the columns object via the `get_loc` method
#df.iloc[2, df.columns.get_loc('ColName')] = 3

#https://stackoverflow.com/questions/28757389/pandas-loc-vs-iloc-vs-at-vs-iat/43968774#43968774

### this is such a mess
##   loc: only work on index
#   iloc: work on position
#
#at: get scalar values. It's a very fast loc
#iat: Get scalar values. It's a very fast iloc

#Also,

#at and iat are meant to access a scalar, that is, a single element in the dataframe, while #loc and iloc are ments to access several elements at the same time, potentially to perform vectorized operations.

# http://pyciencia.blogspot.com/2015/05/obtener-y-filtrar-datos-de-un-dataframe.html
## there are several functions and many use brackets
##
##
#def set_specifc_value(df,row,column):
#
#


#
def get_full_row_by_location(df,location_index):
   """
     This is not the index, this is the memory offset c-style
     so if you were to sort a df, you would use this to get the
     first element

   """
   return df.iloc[location_index]

def get_row_index_by_location(df,location_index):
   """
     This is not the index, this is the memory offset c-style
     so if you were to sort a df, you would use this to get the
     first element

   """
   return df.index[location_index]

def get_column_number_for_column_name(df,column_name):
   return df.columns.get_loc(column_name)

def get_row_number_for_row_name(df,row_name):
   return df.index.get_loc(row_name)

def set_value_by_row_name_and_column_name(df,row_name,column_name,x):
    i=get_row_number_for_row_name(df,row_name)   
    j=get_column_number_for_column_name(df,column_name)
    df.iloc[i,j]=x

    
#    df.loc[df.index[i],column_name]=x 

#https://www.marsja.se/how-to-use-iloc-and-loc-for-indexing-and-slicing-pandas-dataframes/
##### pure by index
def set_value_by_index_and_row(df,i,row,x):
    df.iloc[i,row]=x 

def get_value_by_index_and_row(df,i,row):
    return df.iloc[i,row]

#### mixed by index
def set_value_by_row_slice_and_column_name(df,i1,i2,column_name,x):
   sl=slice(i1,i2)
   return set_value_by_row_index_and_column_name(df,sl,column_name,x)

def get_value_by_row_slice_and_column_name(df,i1,i2,column_name):
   sl=slice(i1,i2)
   return get_value_by_row_index_and_column_name(df,sl,column_name)
   
def set_value_by_row_index_and_column_name(df,i,column_name,x):
    j=df.columns.get_loc(column_name)
    df.iloc[i,j]=x    
#    df.loc[df.index[i],column_name]=x 

def get_value_by_row_index_and_column_name(df,i,column_name):
#    return df.loc[df.index[i],column_name]
    j=df.columns.get_loc(column_name) 
    return df.iloc[i,j]

### pure by label
def set_value_by_row_and_column(df,row,column_name,x):
    df.loc[row,column_name]=x 

def get_value_by_row_and_column(df,row,column_name):
    return df.loc[row,column_name]
 
def get_specific_value_by_name(df,column_name_for_index, row_name, column_name):
    #return df_round.set_index("packing").loc["hex","d_tombac"]
    return df_round.set_index(column_name_for_index).loc[row_name,column_name]

# def get_value_by_row_and_column_v2(df,colrow,column_name):
#     df2=df.set_index("packing").
#     return df.loc[row,column_name]

    


def is_column_constant(df,key):
    a = df[key].to_numpy()
    return (a[0] == a).all(0)

def get_value_for_constant_column(df,key):

    if not is_column_constant(df,key):
        msg="In " + inspect.currentframe().f_code.co_name
        msg+=f"key= {key} is not constant"
        raise Exception(msg)
    a = df[key].to_numpy()
    return a[0]

def unique_cols(df):
    a = df.to_numpy() # df.values (pandas<0.24)
    return (a[0] == a).all(0)


def get_columns_which_are_constant(df):
    u_cols=unique_cols(df)

    columns=df.columns

    columns_unique=[]
    for i, x_i in enumerate(u_cols):

        if x_i:
            columns_unique.append(columns[i])
        # print(f"i={i} = ",end='')
        # print(f"x={x_i}")


    return columns_unique


def add_none_column(df,column_name):
   return add_const_column(df,column_name,x=None)

def add_nan_column(df,column_name):
   return add_const_column(df,column_name,x=np.nan)

def add_zero_column(df,column_name):
   return add_const_column(df,column_name,x=0)

def add_const_column(df,column_name,x):
    if unit_utils.is_unit(x):
       return add_const_column_with_units(df,column_name,x)
    
    #n=len(df)
    new_col=np.full(len(df),x) 

    df[column_name]=new_col

def add_const_column_with_units(df,column_name,x):
    assert isinstance(x,astropy.units.quantity.Quantity)
    n=len(df)
    new_col=unit_utils.generate_np_array_of_units(n,x)
    
    df[column_name]=new_col

def add_columns_with_nan_units(df,column_name,the_units):

    n=len(df)
    x=unit_utils.generate_nan_array_with_units(n,the_units)

    df[column_name]=x

def reorder_columns_using_these_columns_first(df,column_names_new_order):
    
    all_columns=df.columns
    list_1=all_columns
    list_2=column_names_new_order
    new_list=list_utils.reorder_list_1_so_elements_which_match_list_2_go_first(list_1,list_2)

    df=df[new_list]
    
    return df

def del_attrs_keys_if_they_exist(df,keys_to_drop):
   for key_i in keys_to_drop:
      if key_i in df.attrs:
         del df.attrs[key_i]


def replace_elements_inside_df_by_df_f(df, df_f):
   """"
        copy the filtered df over to the original
        likely there is a faster way to do this



   """
   for index, record_i in df_f.iterrows():     
            df.at[index]=record_i


def convert_dataframe_to_record(df):
   if len(df) != 1:
      s=os.path.basename(__file__) + "."
      s+= inspect.currentframe().f_code.co_name
      print(f"In {s} ")

      print(f"df should only have one row")
      print(f"df={df}")
      
      assert(len(df)==1)
      
   return df.squeeze()

# def filter_for_column_value(df,column_name, column_value):
#    return df[df[column_name]==column_value]


def filter_rows(df,match_name,match_value,invert_match=False):

   if not invert_match:
      df_sub=df[df[match_name]==match_value]
   else:
      df_sub=df[df[match_name]!=match_value]
      
   return df_sub

def filter_rows_for_list(df,match_name,match_values):

   df_sub=df[df[match_name].isin(match_values)]
   
   return df_sub

def get_row_unique(df,match_name,match_value, return_none_for_no_match=False):

    df_f=filter_rows(df,match_name,match_value)

    if len(df_f)==0:
       if return_none_for_no_match:
          return None
       else:
          raise Exception(f"No Match! len(df_f) = {len(df_f)}")

    if len(df_f)!=1:
       raise Exception(f"Too Many/Too Few Matches! len(df_f) = {len(df_f)}")

    assert(len(df_f) ==1)
    row=convert_dataframe_to_record(df_f)
    return row

def get_value_unique(df,match_name,match_value, extract_name, return_none_for_no_match=False):
    """
      

    """
    df_f=filter_rows(df,match_name,match_value)

    row_i=get_row_unique(df,match_name,match_value,return_none_for_no_match)
    
    if row_i is None:
       return None    

    return row_i[extract_name]


def reset_index_even_if_already_a_column(df):
   """
      if the index is a duplicate of a column, drop it.
      otherwise make it back to a column

      this is an inplace operation

   """
   index_name=df.index.name
   cols=list(df.columns)

   if index_name in cols:
      df.reset_index(drop=True,inplace=True)    
   else:
      df.reset_index(inplace=True)

def df_viewer(df):
   """"
   https://stackoverflow.com/questions/10636024/python-pandas-gui-for-viewing-a-dataframe-or-matrix

   """
   #%gui qt5 

   #import pandas as pd

   win = QWidget()
   scroll = QScrollArea()
   layout = QVBoxLayout()
   table = QTableWidget()
   scroll.setWidget(table)
   layout.addWidget(table)
   win.setLayout(layout)    


   #df = pd.DataFrame({"a" : [4 ,5, 6],"b" : [7, 8, 9],"c" : [10, 11, 12]},index = [1, 2, 3])
   table.setColumnCount(len(df.columns))
   table.setRowCount(len(df.index))
   for i in range(len(df.index)):
       for j in range(len(df.columns)):
           table.setItem(i,j,QTableWidgetItem(str(df.iloc[i, j])))

   win.show()


def is_column_unique(df,column_name):
   return df[column_name].is_unique

def get_duplicates(df):
   return df[df.duplicated(keep=False)]

def are_all_columns_independently_unique(df):

   columns=df.columns

   for column_name_i in df:
      if not is_column_unique(df,column_name_i):
         return False

   return True


   
   return df[column_name].is_unique



def write_df_to_csv_file(df, csv_filename, index=False):
   print(f"Writing df to file {csv_filename}")
   df.to_csv(csv_filename, index=False)

def are_series_equal(ds_a, ds_b):
   assert(isinstance(ds_a,pd.core.series.Series))
   assert(isinstance(ds_b,pd.core.series.Series))   

   return ds_a.equals(ds_b)

   
# def are_rows_unique(df,column_name):
#    return df[df["pad_id"].duplicated()]


#def reset_index_in_place_with_drop(df):
#   df_pixel_no_to_sextant_equipartition_map.reset_index(drop=True,inplace=True)

########################################
#
#
#   main
#
#
########################################


#if __name__ == '__main__':
 # see test script
 # import pandas_utils

 # print("________________")
 # df = pd.DataFrame({'num_legs': [2, 4, 8, 0],
 #                    'num_wings': [2, 0, 0, 0],
 #                    'num_specimen_seen': [10, 2, 1, 8]},
 #                    index=['falcon', 'dog', 'spider', 'fish'])

 
 # pandas_utils.get_column_number_for_column_name(df,'num_specimen_seen')

 # pandas_utils.get_row_number_for_row_name(df,'fish')
 
 # print(df)

 # print(f"")
 # i=3
 # column_name="num_specimen_seen"
 # x=get_value_by_index_and_column_name(df,i,column_name)

 # print(f"get_value_by_index_and_column_name")
 # print(f"column_name={column_name}")
 # print(f"i={i}")
 # print(f"x={x}")

 # print(f"")

 # i=3
 # column_name="num_specimen_seen"
 # x2=99
 # set_value_by_index_and_column_name(df,i,column_name,x2)
 
 # print(f"set_value_by_index_and_column_name")
 # print(f"column_name={column_name}")
 # print(f"i={i}")
 # print(f"x={x}")
 # print(df)
