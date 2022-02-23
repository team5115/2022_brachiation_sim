import scipy
#from scipy import stats
import numpy as np
import phidl
import math
#import shapely_to_phidl as s2p
#import generate_escape_route_geometry
#import quickplotter3
import os
import sys
import dis
from csd import array_utils
import numbers
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import pandas as pd
import pandas

def pretty_print_stats_describe(label,d,f_stream=sys.stdout):
    #DescribeResult(nobs=198, minmax=(137.5, 2229.8076923076924), mean=1018.1209757543693, variance=186580.0976652972, skewn
        #       ess=0.17824131074977512, kurtosis=-0.43134444904705704)

    #d=scipy.stats.describe(x)          
    assert(isinstance(d,scipy.stats.stats.DescribeResult))
    print(f"Stats for {label}",file=f_stream)
    print(f"\t N={d.nobs}",file=f_stream)
    print(f"\t min={d.minmax[0]}",file=f_stream)
    print(f"\t max={d.minmax[1]}",file=f_stream)
    print(f"\t mean={d.mean}",file=f_stream)
    print(f"\t variance={d.variance}",file=f_stream)
    print(f"\t std_dev={math.sqrt(d.variance)}",file=f_stream)


    return d

def pretty_print_stats_on_df_column(df, column_name,verbosity=0):

    x=df[column_name]
    pretty_print_stats_on_df_series(x,column_name, verbosity)
    
def pretty_print_stats_on_df_series(x,column_name="", verbosity=0):
    assert(isinstance(x,pandas.core.series.Series))

    # try:
    #     x_unique=pd.Series(x.unique())
    #     is_uniquable=True
    # except Exception as e:
    #     print(e)
    #     return

    ## unique() gives ndarray() which handles None differently than pd Series
    x_unique=pd.Series(x.unique())
    x_clean=x.dropna()


    
    data_fully_unique=determine_if_is_non_repeating(x)
    
    N=len(x)
    N_unique=len(x_unique)
    ## count ignores None and maybe Nan
    N_good_values=x.count()

    N_none=N-N_good_values

    has_none=N_none>0

    
    # if has_none:
    #     #x_clean = [xi for xi in x if xi is not None]
    #     x_clean=x.dropna()
    #     fully_unique_ignoring_none = len(x_clean)==len(x_clean.unique())
    # else:
    #     fully_unique_ignoring_none = False

    # only numeric arrays can be a sequence
    #x0=np.array(x)[0]
    #x0=x.iloc[0]
    #is_numeric_0=isinstance(x0, numbers.Number)
    #is_numeric_1=is_numeric_0 and (N_none==0)
    
    is_numeric_2=pd.api.types.is_numeric_dtype(x)
    is_numeric=is_numeric_2

    # doesn't work on pandas
    #has_none=None in x

    sequence_data=determine_if_is_sequence(x)

    
    # data={"N":N,
    #       "N_unique":N_unique,
    #       "fully_unique":fully_unique,
    #       "is_sequence_1":is_sequence_1,
    #       "is_sequence_2":is_sequence_2

    #       }
    

    if len(column_name)>0:
        print(f"{column_name}:",end="\t")
        
    print(f"N={len(x)}",end=" ")

    if len(x_clean)==0:
        print(f"<all values are None>",end=" ")
        print(f"")
        return
        
    if has_none:
        print(f"N_not_None={len(x_clean)}",end=" ")
        print(f"N_None={N_none}",end=" ")
        if len(x_clean) > 0:
            print(f"[{min(x_clean)},{max(x_clean)},None]",end=" ")
    else:
        print(f"[{x.min()},{x.max()}]",end=" ")


 
    if data_fully_unique["fully_unique"]:
        print(f"<No repeated values>", end=" ")
    elif data_fully_unique["fully_unique_dropna"]:
        print(f"<No repeated values ignoring None>", end=" ")

    print(f" N_unique={len(x_unique)}", end=" ")
    print(f" ratio={len(x)/len(x_unique)}", end=" ")
        
    if has_none:
        x_unique_clean = [xi for xi in x_unique if xi is not None]

        if len(x_unique_clean) > 0:
            print(f"[{min(x_unique_clean)},{max(x_unique_clean)},None]",end=" ")
        else:
            print(f"[None]",end=" ")
        #print(f"[{x_unique_clean.min()},{x_unique_clean.max()},None]",end=" ")
    else:            
        print(f"[{x_unique.min()},{x_unique.max()}]",end=" ")

        
    # if has_none:
    #     print(f"+None")
    
    #print(f"is_sequence_1={is_sequence_1}", end=" ")
    #print(f"is_sequence_2={is_sequence_2}", end=" ")
        


    if sequence_data["is_sequence_1"]:
        print(f"is contiguous sequence with delta 1", end="\t")
    elif sequence_data["is_sequence_2"]:
        print(f"is contiguous sequence with delta 2", end="\t")
    elif sequence_data["is_sequence_1_unsorted"]:
        print(f"is non-contiguous sequence with delta 1", end="\t")
    elif sequence_data["is_sequence_2_unsorted"]:
        print(f"is non-contiguous sequence with delta 2", end="\t")
    elif sequence_data["is_sequence_1_dropna"]:
        print(f"is contiguous sequence with delta 1 (dropna)", end="\t")
    elif sequence_data["is_sequence_2_dropna"]:
        print(f"is contiguous sequence with delta 2 (dropna)", end="\t")
    elif sequence_data["is_sequence_1_unsorted_dropna"]:
        print(f"is non-contiguous sequence with delta 1 (dropna)", end="\t")
    elif sequence_data["is_sequence_2_unsorted_dropna"]:
        print(f"is non-contiguous sequence with delta 2 (dropna)", end="\t")
            
    print(f"")


def pretty_print_stats_on_all_df_columns(df,verbosity=0):
    columns=df.columns

    for column_i in columns:
        pretty_print_stats_on_df_column(df,column_i)

def determine_if_is_non_repeating(x):
    fully_unique=is_non_repeating(x)

    if not fully_unique:
        fully_unique_dropna=is_non_repeating_dropna(x)
    else:
        fully_unique_dropna=True
        
    data={"fully_unique": fully_unique,
         "fully_unique_dropna": fully_unique_dropna}

    return data
    
def is_non_repeating(x):
    assert(isinstance(x,pandas.core.series.Series))
    return x.is_unique


def is_non_repeating_dropna(x):
    assert(isinstance(x,pandas.core.series.Series))
    x_dropna=x.dropna()
    fully_unique_dropna=is_non_repeating(x_dropna)
    return fully_unique_dropna
        
def determine_if_is_sequence(x):
    assert(isinstance(x,pandas.core.series.Series))

    x_dropna=x.dropna()
    [is_sequence_1, is_sequence_2,is_sequence_1_unsorted, is_sequence_2_unsorted]=determine_if_is_sequence_base(x_dropna)

    #if not any([is_sequence_1, is_sequence_2,is_sequence_1_unsorted, is_sequence_2_unsorted]):
    #    x_dropna=x.dropna()
    [is_sequence_1_dropna, is_sequence_2_dropna,is_sequence_1_unsorted_dropna, is_sequence_2_unsorted_dropna]=determine_if_is_sequence_base(x_dropna)
    # else:
    #     is_sequence_1_dropna=False
    #     is_sequence_2_dropna=False
    #     is_sequence_1_unsorted_dropna=False
    #     is_sequence_2_unsorted_dropna=False

    data={
        "is_sequence_1":is_sequence_1,
        "is_sequence_1_unsorted":is_sequence_1_unsorted,
        "is_sequence_1_dropna":is_sequence_1_dropna,
        "is_sequence_1_unsorted_dropna":is_sequence_1_unsorted_dropna,
        "is_sequence_2":is_sequence_2,
        "is_sequence_2_unsorted":is_sequence_2_unsorted,
        "is_sequence_2_dropna":is_sequence_2_dropna,
        "is_sequence_2_unsorted_dropna":is_sequence_2_unsorted_dropna}

    return data
          

    
def determine_if_is_sequence_base(x):
    assert(isinstance(x,pandas.core.series.Series))
    
    is_numeric=pd.api.types.is_numeric_dtype(x)

    if not is_numeric:
        is_sequence_1=False
        is_sequence_2=False
        is_sequence_1_unsorted=False
        is_sequence_2_unsorted=False
    else:
 
        [is_sequence_1, is_sequence_2]=is_sequence_1_or_sequence_2(x)
        
        #if not(is_sequence_1 or is_sequence_2):
        [is_sequence_1_unsorted, is_sequence_2_unsorted]=is_sequence_1_or_sequence_2_unsorted(x)
        #else:
        #    is_sequence_1_unsorted=True
        #    is_sequence_2_unsorted=True

    return [is_sequence_1, is_sequence_2,is_sequence_1_unsorted, is_sequence_2_unsorted]

def is_sequence_1_or_sequence_2(x):

    assert(pd.api.types.is_numeric_dtype(x))


    ## we sort for sequence testing, not necessary for non-numeric
    #x_unique.sort_values(inplace=True)
    is_sequence_1=array_utils.is_array_a_sequence_with_a_delta_of_x(x,target_delta=1)

    if not is_sequence_1:
        is_sequence_2=array_utils.is_array_a_sequence_with_a_delta_of_x(x,target_delta=2)
    else:
        is_sequence_2=False
        
    return [is_sequence_1, is_sequence_2]

def is_sequence_1_or_sequence_2_unsorted(x):

    x_unique=pd.Series(x.unique())
    x_unique.sort_values(inplace=True)
    
    is_sequence_1_unsorted=False
    is_sequence_2_unsorted=False


    [is_sequence_1_unsorted, is_sequence_2_unsorted]=is_sequence_1_or_sequence_2(x_unique)
    
    return [is_sequence_1_unsorted, is_sequence_2_unsorted]



def generate_stats_series_from_ds(x, verbosity=0):

    the_dict={}
    
    ## unique() gives ndarray() which handles None differently than pd Series
    x_unique=pd.Series(x.unique())
    x_dropna=x.dropna()
    
    data_fully_unique=determine_if_is_non_repeating(x)
    
    N=len(x)
    N_unique=len(x_unique)
    
    ## count ignores None and maybe Nan
    N_dropna=x_dropna.count()

    N_none=N-N_dropna

    has_none=N_none>0


    # the_dict["N"]=N
    # the_dict["N_unique"]=N_unique
    # the_dict["N_dropna"]=N_dropna


    

    ### this doesn't seem to be what I want
    
    is_numeric=pd.api.types.is_numeric_dtype(x)

    the_dict["is_numeric"]=is_numeric


    sequence_data=determine_if_is_sequence(x)


    the_dict["N"]=len(x)

    ### min(x) breaks on None
    ### pd.Series.min() is ok

    try:
        the_dict["min"]=x.min()
        the_dict["max"]=x.max()
    except Exception as e:
        ## pandas doenst dropna on string arrays
        ## the numeric test isn't working for me
        the_dict["min"]=x_dropna.min()
        the_dict["max"]=x_dropna.max()

    the_dict["is_fully_unique"]=data_fully_unique["fully_unique"]
    the_dict["N_unique"]=len(x_unique)
    the_dict["ratio_N_to_N_unique"]=len(x)/len(x_unique)

    the_dict["is_fully_unique_dropna"]=data_fully_unique["fully_unique_dropna"]
    the_dict["N_dropna"]=len(x_dropna)

    the_dict["has_none"]=has_none
    all_values_none=len(x_dropna)==0
    the_dict["all_values_none"]=all_values_none
    the_dict["N_none"]=N_none








    ### append dicts

    #the_dict.update(sequence_data)
    
    seq_data_as_string=sequence_data_to_sequence_code(sequence_data)
    
    the_dict["seq"]=seq_data_as_string
    
    return     pd.Series(the_dict)

def sequence_data_to_sequence_code(sequence_data):

    
    if sequence_data["is_sequence_1"]:
        s="seq_1"
    elif sequence_data["is_sequence_1_unsorted"]:
        s="seq_1_unsrt"
    elif sequence_data["is_sequence_1_dropna"]:
        s="seq_1_dropna"
    elif sequence_data["is_sequence_1_unsorted_dropna"]:
        s="seq_1_dropna_unsrt"
    elif sequence_data["is_sequence_2"]:
        s="seq_2"
    elif sequence_data["is_sequence_2_unsorted"]:
        s="seq_2_unsrt"
    elif sequence_data["is_sequence_2_dropna"]:
        s="seq_2_dropna"
    elif sequence_data["is_sequence_2_unsorted_dropna"]:
        s="seq_2_dropna_unsrt"
    else:
        s=None


    return s


def generate_df_stats_from_dataframe(df, verbosity=0):
    columns=df.columns

    the_dict={}
    for column_i in columns:
        #print(f"processing column={column_i}")
        sys.stdout.flush()
        x_i=df[column_i]
        xs_i=generate_stats_series_from_ds(x_i)

        the_dict[column_i]=xs_i

    df_stats=pd.DataFrame(the_dict)
    return df_stats
