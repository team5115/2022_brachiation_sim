import unittest
import inspect
#import ..array_utils
#from ..subpkg2 import mod
#from .. import array_utils  #only works for a package
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import list_utils
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
    


     # def test_remove_elements_from_array_till_match(self):
     #     x=[0,1,2,3,4,5,6,7,8]
     #     x_final=5
     #     x=list_utils.remove_elements_from_array_till_match(x,x_final)
     #     x_expected=[0,1,2,3,4,5]
     #     self.assertEqual(x_expected, x, f"x={x} x_expected={x_expected}")

     def test_remove_duplicated_elements_which_are_adjacent(self):
         l=[1, 1, 2, 3, 4, 4, 4, 4, 5, 6, 3, 3, 5, 5, 7, 8, 8, 8, 9, 1, 2, 3, 3, 3, 10, 10]

         x=list_utils.remove_duplicated_elements_which_are_adjacent(l)
         
         x_expected=[1,2,3,4,5,6,3,5,7,8,9,1,2,3,10]
         self.assertEqual(x_expected, x, f"x={x} x_expected={x_expected}")

         # print("In " + inspect.currentframe().f_code.co_name)
         # print(f"         l={l}")
         # print(f"         x={x}")
         # print(f"x_expected={x_expected}")

     def test_split_before_element_mid(self):

         the_list = ['a','b','c','d','e']
         x='c'
         
         [l_a, l_b]=list_utils.split_before_element(the_list,x)

         
         l_a_expected=['a','b']
         l_b_expected=['c','d','e']
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")

     def test_split_before_element_first(self):

         the_list = ['a','b','c','d','e']
         x='a'
         
         [l_a, l_b]=list_utils.split_before_element(the_list,x)

         
         l_a_expected=[]
         l_b_expected=the_list
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")
             
     def test_split_before_element_last(self):

         the_list = ['a','b','c','d','e']
         x='e'
         
         [l_a, l_b]=list_utils.split_before_element(the_list,x)

         
         l_a_expected=['a','b','c','d']
         l_b_expected=['e']
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")
             
     def test_split_before_element_none(self):

         the_list = ['a','b','c','d','e']
         x='z'
         
         [l_a, l_b]=list_utils.split_before_element(the_list,x)

         
         l_a_expected=the_list
         l_b_expected=[]
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")
             
     def test_split_after_element_mid(self):

         the_list = ['a','b','c','d','e']
         x='c'
         
         [l_a, l_b]=list_utils.split_after_element(the_list,x)

         
         l_a_expected=['a','b','c']
         l_b_expected=['d','e']
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")

     def test_split_after_element_last(self):

         the_list = ['a','b','c','d','e']
         x='e'
         
         [l_a, l_b]=list_utils.split_after_element(the_list,x)

         
         l_a_expected=the_list
         l_b_expected=[]
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")

     def test_split_after_element_first(self):

         the_list = ['a','b','c','d','e']
         x='a'
         
         [l_a, l_b]=list_utils.split_after_element(the_list,x)

         
         l_a_expected=['a']
         l_b_expected=['b','c','d','e']
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")
             
     def test_split_after_element_none(self):

         the_list = ['a','b','c','d','e']
         x='z'
         
         [l_a, l_b]=list_utils.split_after_element(the_list,x)

         
         l_a_expected=the_list
         l_b_expected=[]
         
         self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
         self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

         # if False:
         #     print("In " + inspect.currentframe().f_code.co_name)
         #     print(f"         l_a={l_a}")
         #     print(f"         l_b={l_b}")
         #     print(f"         x={x}")
         #     print(f"l_a_expected={l_a_expected}")
         #     print(f"l_b_expected={l_b_expected}")
         
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
