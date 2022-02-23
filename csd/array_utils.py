import unittest
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numbers
def remove_elements_from_array_till_match(list_of_points, x_final):

    while list_of_points[-1] != x_final:
        list_of_points.pop()

    return list_of_points

def are_all_elements_in_array_the_same(x):
    assert(isinstance(x,np.ndarray))
    
    result = np.all(x == x[0])

    return result

def is_array_a_sequence_with_a_delta_of_x(x, target_delta=1,verbosity=0):

    # only numeric arrays can be a sequence
    #assert(isinstance(x[0], numbers.Number))

    if not isinstance(x[0], numbers.Number):
        return False
    
    if len(x) < 2:
        return False
    
    dx=np.diff(x)

    if verbosity > 0:
        print(x)
        print(dx)
    
    if dx[0] != target_delta:
        if verbosity > 0:
            print(f"target_delta={target_delta}")            
            print(f"dx[0]={dx[0]}")
            print(f"Not equal")
        return False

    all_the_same=are_all_elements_in_array_the_same(dx)
    if verbosity >0:
        print(f"all_the_same={all_the_same}")

    return all_the_same
    
##############################################################
#
#
#
#
#
#
############################################################

def run_tests():
    unittest.main()

class TestArrayUtils(unittest.TestCase):
    


     def test_remove_elements_from_array_till_match(self):
         x=[0,1,2,3,4,5,6,7,8]
         x_final=5
         x=remove_elements_from_array_till_match(x,x_final)
         x_expected=[0,1,2,3,4,5]
         self.assertEqual(x_expected, x, f"x={x} x_expected={x_expected}")



########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':

 run_tests()

 if False:
     x=[0,1,2,3,4,5,6,7,8]
     x_final=5



     print("________________")
     print(f"x={x}")
     print(f"x_final={x_final}")

     x=remove_elements_from_array_till_match(x,x_final)
     print(f"x={x}")
     print(f"x_final={x_final}")
