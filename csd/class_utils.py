# import the pandas lib as pd 
import pandas as pd
import numpy as np
import sys
import os

def get_first_element_of_a_dict(the_dict):
    return the_dict[list(the_dict.keys())[0]]

def get_attributes_in_class_which_arent_callable(obj):

    the_list=[a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj, a))]
    return the_list
    

def class_to_dict(obj,list_of_attributes=None):

    if list_of_attributes is None:
        list_of_attributes=get_attributes_in_class_which_arent_callable(obj)
    
    data=dict()
    for x in list_of_attributes:
        data[x]=getattr(obj,x)

    return data


