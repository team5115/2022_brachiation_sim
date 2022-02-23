from astropy import units as u
import astropy
import math
import copy

from scipy.integrate import quad
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#### an arrray of numbers with a single unit for the array
#In [31]: unit_utils.generate_np_array_with_units(3,1*u.m)                     # Out[31]: <Quantity [1., 1., 1.] m>
def generate_np_array_with_units(n,x0):
    assert isinstance(x0,astropy.units.quantity.Quantity)

    return np.ones(n)*x0

###
### In [30]: unit_utils.generate_np_array_of_units(3,1*u.m)                    ### Out[30]: [<Quantity 1. m>, <Quantity 1. m>, <Quantity 1. m>]
def generate_np_array_of_units(n,x0):
    y=generate_np_array_with_units(n,x0)
    return convert_list_with_units_to_list_of_units(y)


def is_unit(x):
    return isinstance(x,astropy.units.quantity.Quantity)

def generate_nan_array_with_units(n,the_units):
    x=np.ones(n)*np.nan*the_units
    x2=convert_list_with_units_to_list_of_units(x)

    return x2
    

def convert_list_with_units_to_list_of_units(x):

    #tt=type(x)
    
    x2=list(x)

    # x1_units=x2[0].unit

    # for i, x_i in enumerate(x):
    #     x2[i]=x_i.value

    # x2 *= x1_units

    return x2

def convert_list_of_units_to_list_with_unit(x):

    #tt=type(x)
    
    x2=list(x)

    x1_0=x2[0]
    
    if not (isinstance(x1_0,astropy.units.quantity.Quantity)):
        return x2
    
    x1_units=x2[0].unit

    for i, x_i in enumerate(x):
        x_i=x_i.to(x1_units)
        x2[i]=x_i.value

    x2 *= x1_units

    return x2

def get_df_col_with_units_as_list_with_unit(df, col_name):
    R_u=list(df[col_name])
    R=convert_list_of_units_to_list_with_unit(R_u)

    return R


def convert_list_of_units_to_different_units(x,new_units):


    for i, x_i in enumerate(x):
        x_i=x_i.to(new_units)
        x[i]=x_i

    return x

def round_list_of_units(x,precision):


    for i, x_i in enumerate(x):
        x[i]=np.round(x_i,precision)

    return x


def to_si_value(x):
    if (isinstance(x,pd.core.frame.DataFrame)):
        return convert_pandas_df_with_units_to_si_value(x)

    if (isinstance(x,pd.core.series.Series)):
        return convert_pandas_series_with_units_to_si_value(x)
    
    if not (isinstance(x,astropy.units.quantity.Quantity)):
        return x
    else:
        return x.si.value
  
def convert_pandas_df_with_units_to_si_value(df):

    df2=copy.deepcopy(df)
    

    for i, col_name in enumerate(df2.columns):


        col_i=get_df_col_with_units_as_list_with_unit(df, col_name)
        df2[col_name]=to_si_value(col_i)

    return df2

def convert_pandas_series_with_units_to_si_value(x):

    
    x2=copy.deepcopy(x)

    x1_0=x2[0]    
    if not (isinstance(x1_0,astropy.units.quantity.Quantity)):
        return x2
    
    for i, x_i in enumerate(x):
        x2[i]=x_i.si.value

    return x2

def convert_pandas_series_with_units_to_current_value_and_single_unit(x):

    
    x2=copy.deepcopy(x)

    x1_0=x2[0]    
    if not (isinstance(x1_0,astropy.units.quantity.Quantity)):
        return x2
    
    for i, x_i in enumerate(x):
        x2[i]=x_i.value

    the_unit=x1_0.unit
    return [x2, the_unit]

def add_units_to_pandas_column(df,column_name,the_units):

    
    x1=np.array(copy.deepcopy(df[column_name]))

    x2=x1*the_units

    x3=convert_list_with_units_to_list_of_units(x2)

    df[column_name]=x3


def replace_zeros_with_units_in_pandas_series_with_np_nans(x):

    
    x2=copy.deepcopy(x)

    x1_0=x2[0]    
    if not (isinstance(x1_0,astropy.units.quantity.Quantity)):
        return x2
    
    for i, x_i in enumerate(x):
        if x_i.value==0:
        
            x2[i]=np.nan*x_i.unit

    return x2


