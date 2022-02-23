import unittest
#import ..array_utils
#from ..subpkg2 import mod
#from .. import array_utils  #only works for a package

import sys
sys.path.append("../..") # Adds higher directory to python modules path.
from csd import array_utils
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
         x=array_utils.remove_elements_from_array_till_match(x,x_final)
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

 # if False:
 #     x=[0,1,2,3,4,5,6,7,8]
 #     x_final=5



 #     print("________________")
 #     print(f"x={x}")
 #     print(f"x_final={x_final}")

 #     x=remove_elements_from_array_till_match(x,x_final)
 #     print(f"x={x}")
 #     print(f"x_final={x_final}")
