import unittest
#import ..array_utils
#from ..subpkg2 import mod
#from .. import array_utils  #only works for a package
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import pandas as pd
import numpy as np
import pandas_conversion_utils
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

class TestPandasUtils(unittest.TestCase):
    


    def test_find_minimum_in_pandas_manual(self):
         #Create a DataFrame
         d = {
             'Name':['Alisa','Bobby','jodha','jack','raghu','Cathrine',
                     'Alisa','Bobby','kumar','Alisa','Alex','Cathrine'],
             'Age':[26,24,23,22,23,24,26,24,22,23,24,24],
             
             'Score':[85,63,55,74,31,77,85,63,42,62,89,77]}
         
         df = pd.DataFrame(d,columns=['Name','Age','Score'])
         
         rownum=df['Score'].idxmin()
         
         x=df.loc[rownum]['Name']
         x_expected='raghu'


         self.assertEqual(x_expected, x)


    def test_find_minimum_in_pandas(self):
         #Create a DataFrame
         d = {
             'Name':['Alisa','Bobby','jodha','jack','raghu','Cathrine',
                     'Alisa','Bobby','kumar','Alisa','Alex','Cathrine'],
             'Age':[26,24,23,22,23,24,26,24,22,23,24,24],
             
             'Score':[85,63,55,74,31,77,85,63,42,62,89,77]}
         
         df = pd.DataFrame(d,columns=['Name','Age','Score'])
         

         x_expected='raghu'

         x=pandas_conversion_utils.get_value_for_minimum_element(df, key_for_minimum='Score', key_to_return='Name')
         self.assertEqual(x_expected, x)



########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':

 run_tests()

