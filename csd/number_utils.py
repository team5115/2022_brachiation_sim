import math
import numpy as np



def get_factors(x):
    """
         brute force factor search

    """

    return [i for i in range(1, x+1) if x % i ==0]

def is_x_a_factor_of_y(x,y):
    return y % x ==0


def get_largest_factor_less_than_value_v1(x, value_max_factor=10):
    """
        gets all factors and then filters

    """
       
    all_factors=get_factors(x)

    all_factors_np=np.array(all_factors)
    
    return all_factors_np[all_factors_np <= value_max_factor].max()

def get_factors_less_than_value(x, value_max_factor=10):
    """
        more efficient version limits brute force search

    """
    x=np.array([i for i in range(1, value_max_factor+1) if x % i ==0])

    return x

def get_largest_factor_less_than_value(x, value_max_factor=10):
    """
        more efficient version limits brute force search

    """
    x=np.array([i for i in range(1, value_max_factor+1) if x % i ==0])

    return x.max()

def get_range_with_integer_only_elements( x1, x2, value_max_n=10):
    """
     mostly for colorbars

    """

    # get_factors(x)
    
    factors=get_factors_less_than_value(x2,value_max_n)

    factors=np.flip(factors)
    
    for f in factors:
        #print(f"f={f}")

        r=np.linspace(x1,x2,f)

        are_integers=[i.is_integer() for i in r]

        if all(are_integers):
           return r
        
        #print(r)
        #print(z)

    
    return [x1,x2]



########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':



    print("________________")
    x=get_largest_factor_less_than_value(96, value_max_factor=16)

    assert(x==16)

    x=get_largest_factor_less_than_value(96, value_max_factor=15)
    assert(x==12)

    r=get_range_with_integer_only_elements(1,96)

    print(f"r={r}")
    #assert(x==12)
