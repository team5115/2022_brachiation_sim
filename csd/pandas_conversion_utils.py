# import the pandas lib as pd 
import pandas as pd
import numpy as np
import sys
import os
import copy

#_x=pandas_conversion_utils.dataframe_get_single_matching_row_as_series(df,'pixel_no',122)   

#
#
#
#
def dataframe_keep_rows_where_column_is_in_list(df,column_key,values_to_keep):
    return df[df[column_key].isin(values_to_keep)]

def dataframe_add_column_with_const_value_trivial(df,column_key,value):
    df_new=copy.deepcopy(df)
    df_new[column_key]=value
    return df_new

#### the trivial case doesn't work when value is a list or ndarray
def dataframe_add_column_with_const_value_nontrivial(df,column_key,value):
    list_of_dicts=dataframe_to_list_of_dicts(df)  

    for i, x_i in enumerate(list_of_dicts):
        x=list_of_dicts[i]
        x[column_key]=value
        list_of_dicts[i]=x

    df_new=pd.DataFrame(list_of_dicts)
    return df_new

#### the trivial case doesn't work when value is a list or ndarray
#
#
#   constant_column_dict={ "escape_direction": escape_vector,
#                           "tes_exit_direction": tes_exit_direction,
#                         "alg_name": "unknown"}
#   
#
#
#
def dataframe_add_columns_with_const_values_nontrivial(df,constant_column_dict):
    list_of_dicts=dataframe_to_list_of_dicts(df)  

    for i, x_i in enumerate(list_of_dicts):
        x=list_of_dicts[i]
        #x[column_key]=value
        x.update(constant_column_dict)
        list_of_dicts[i]=x

    df_new=pd.DataFrame(list_of_dicts)
    return df_new

def dataframe_get_single_matching_row_as_series(df,column_a_key,column_a_value):
    x=df[df[column_a_key]==column_a_value]

    ##x is a pandas dataframe
    assert len(x)==1
    series1=x.iloc[0,:]
    return series1

# def dataframe_get_single_value(df,column_a_key,column_a_value,column_b_key):
#     x=df[df[column_a_value]==column_a_value][column_b_key] 

#     ##x is a pandas series
#     assert len(x)==0
#     return x[0]


def dataframe_to_list_of_dicts(df):
    return df.to_dict(orient="records")

def dataframe_to_dict_of_lists(df):
    return df.to_dict()
    
def print_full_dataframe(x,file=sys.stdout):
    '''

    pd.set_option('display.max_columns', None) sets the number of the maximum columns shown
    pd.set_option('display.max_colwidth', -1) sets the maximum width of each single field.

     
    '''
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x,file=file)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')
    
def add_column_to_dataframe_based_on_dict_of_another_column(df,column_name_for_dict_key, new_column_name_for_dict_value, the_dict):
    #the key to dict should be old column name
    df[new_column_name_for_dict_value]= df[column_name_for_dict_key].map(the_dict)
    return df


def extract_two_columns_as_dict(df,key_column_name,value_column_name):
     return dict(zip(df[key_column_name],df[value_column_name]))
    
def get_column_of_dataframe_which_is_not_none(df,key):
    #valid_entries=df[key]!=None
    valid_entries=df[key].notnull()
    the_list=df[key][valid_entries].to_list()
    return the_list

def get_first_element_of_a_dict(the_dict):
    return the_dict[list(the_dict.keys())[0]]

def get_attributes_in_class_which_arent_callable(obj):

    the_list=[a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj, a))]
    return the_list
    

def class_to_dict(obj,list_of_attributes):

    data=dict()
    for x in list_of_attributes:
        data[x]=getattr(obj,x)

    return data


def convert_dict_of_objects_to_list_of_dicts(the_dict,list_of_attributes):
    assert isinstance(the_dict,dict)

    #if list_of_attributes is None:
    #    first_element_of_dict=list(my_dict.keys())[0]
    #    list_of_attributes=get_attributes_in_class_which_arent_callable(first_element_of_dict)


    
    the_list=list()
    for key,value in the_dict.items():
        #print(f"key={key} = ",end='')
        #print(f"value={value}")
        zi=value
        z_as_dict=class_to_dict(zi,list_of_attributes)  
        the_list.append(z_as_dict)

    return the_list


def convert_dict_of_objects_to_pandas_data_frame(dict_of_objects,list_of_attributes=None):   
    if list_of_attributes is None:
        #first_element_of_dict=list(dict_of_objects.keys())[0]
        #list_of_attributes=get_attributes_in_class_which_arent_callable(dict_of_objects[list(dict_of_objects.keys())[0]])
        first_element_of_dict=dict_of_objects[list(dict_of_objects.keys())[0]]
        list_of_attributes=get_attributes_in_class_which_arent_callable(first_element_of_dict)

    the_index_list=list(dict_of_objects.keys())
    list_of_dicts=convert_dict_of_objects_to_list_of_dicts(dict_of_objects,list_of_attributes)
    df = pd.DataFrame(list_of_dicts,index=the_index_list)
    return df

# def convert_dict_of_objects_to_pandas_data_frame_where_index_is_a_member(dict_of_objects,list_of_attributes, attribute_which_is_index=None):

    
#     list_of_dicts=convert_dict_of_objects_to_list_of_dicts(dict_of_objects,list_of_attributes)
#     df = pd.DataFrame(list_of_dicts)


#     if attribute_which_is_index is not None:
#         df.set_index(attribute_which_is_index, drop=True, append=False, inplace=True, verify_integrity=True)
    
#     return df

def get_row_for_minimum_element(df, key_for_minimum):
     rownum=df[key_for_minimum].idxmin()
     

def get_value_for_minimum_element(df, key_for_minimum, key_to_return):
     rownum=df[key_for_minimum].idxmin()
     return df.loc[rownum][key_to_return]

def sort_data_frame_on_two_axis_and_insert_sort_order_column(df, name_of_ordinal, first_key="x", second_key="y",first_ascending=True, second_ascending=True):
    # name_of_ordinal="sort_index"
    # first_key="x"
    # second_key="y"
    # first_ascending=True
    # second_ascending=True
    # df_sorted=sort_data_frame_on_two_axis_and_insert_sort_order_column(df,name_of_ordinal,first_key,second_key,first_ascending,second_ascending)

    
    df_sorted = df.sort_values([first_key, second_key], ascending = (first_ascending,second_ascending))
    n_rows=len(df_sorted.index)    
    sorted_index = list(range(0, n_rows))
    df_sorted[name_of_ordinal]=sorted_index

    return df_sorted

def sort_data_frame_on_two_axis(df,first_key, second_key,first_ascending=True, second_ascending=True):
    # name_of_ordinal="sort_index"
    # first_key="x"
    # second_key="y"
    # first_ascending=True
    # second_ascending=True
    # df_sorted=sort_data_frame_on_two_axis_and_insert_sort_order_column(df,name_of_ordinal,first_key,second_key,first_ascending,second_ascending)

    
    df_sorted = df.sort_values([first_key, second_key], ascending = (first_ascending,second_ascending))

    return df_sorted

def keep_rows_in_df1_which_also_occur_in_df2(df1, df1_key, df2, df2_key):

     return df1[df1[df1_key].isin(df2[df2_key])]
    
########################################
#
#
# main
#
#
########################################


if __name__ == '__main__':

    class A_Test:
         def __init__(self,name=None,A=0,B=0,C=0,D=0):
             self.name = name
             self.A    = 0
             self.B    = 0
             self.C    = False
             self.D    = 1.2

         def get_A(self):
             return A
    
    # dictionary = {'A' : 10, 'B' : 20, 'C' : 30} 
    # data1 = {'A' : 5, 'B' : True, 'C' : 'x', 'D' : 2.7}
    # data2 = {'A' : 8, 'B' : True, 'C' : 'y', 'D' : 3.1}
    # data3 = {'A' : 13, 'B' : False, 'C' : 'z', 'D' : 0}
    # data4 = {'A' : 1, 'B' : False, 'C' : 'a', 'D' : 0.1}
    # data5 = {'A' : -1, 'B' : True, 'C' : 'b', 'D' : -2}

    # #df2 = pd.DataFrame(rows_list)   


    # print("________________")

    x1=A_Test(name='obj1',A=1)
    x2=A_Test(name='obj2',A=2)
    x3=A_Test(name='obj3',A=2)
    x4=A_Test(name='obj4',A=2)

    the_dict={"x1":x1,
              "x2":x2,
              "x3":x3,
              "x4":x4}

    list_of_attributes=get_attributes_in_class_which_arent_callable(x1)
    df = convert_dict_of_objects_to_pandas_data_frame(the_dict,list_of_attributes)   

    print(f"\n df with index from the dict key")
    print(df)

    # index="name"
    # list_of_attributes=get_attributes_in_class_which_arent_callable(x1)
    # df = convert_dict_of_objects_to_pandas_data_frame_where_index_is_a_member(the_dict,list_of_attributes,attribute_which_is_index="name")
    
    # print(f"\ndf with index from attribute_which_is_index={index}")
    # print(df)


    
    

    # data1 = {'A' : 5, 'B' : True, 'C' : 'x', 'D' : 2.7}
    # data2 = {'A' : 8, 'B' : True, 'C' : 'y', 'D' : 3.1}
    # data3 = {'A' : 13, 'B' : False, 'C' : 'z', 'D' : 0}
    # data4 = {'A' : 1, 'B' : False, 'C' : 'a', 'D' : 0.1}
    # data5 = {'A' : -1, 'B' : True, 'C' : 'b', 'D' : -2}

    # #df2 = pd.DataFrame(rows_list)   
