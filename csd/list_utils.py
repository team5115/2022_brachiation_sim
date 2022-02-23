import numpy as np

# def remove_elements_from_list_till_match(list_of_points, x_final):

#     while list_of_points[-1] != x_final:
#         list_of_points.pop()

#     return list_of_points

# more_itertools.sort_together([P_corners_as_points, angles])[0]
def test_sort_list_x_values_in_list_y():
     X = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
     Y = [ 0,   1,   1,    0,   1,   2,   2,   0,   1]
     Xs=sort_list_x_values_in_list_y
     print( "Xs:", Xs )
     # prints: Xs: ["a", "d", "h", "b", "c", "e", "i", "f", "g"]

def sort_list_x_values_in_list_y(X,Y):

     sorted_y_idx_list = sorted(range(len(Y)),key=lambda x:Y[x])
     Xs = [X[i] for i in sorted_y_idx_list ]

     return Xs
     
def remove_none(a):
     return list(filter(None,a))

def remove_none2(L):
     L_clean = [x for x in L if x is not None]
     return L_clean
#
#https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
#
def flatten_list(a):
     return [item for sublist in a for item in sublist]


# http://stackoverflow.com/q/3844948/
def are_all_elements_in_a_list_equal(the_list):
    '''
          uses the very fast count method 
    '''
    return not the_list or the_list.count(the_list[0]) == len(the_list)

#https://www.geeksforgeeks.org/python-get-unique-values-list/
def unique(the_list):
    '''
          uses set conversions
    '''

    # insert the list to the set 
    list_set = set(the_list) 
    # convert the set to the list 
    unique_list = (list(list_set)) 

    return unique_list

            
def unique_unhashable(the_list):

    new_list=[]
     
    for x in the_list:
         if x not in new_list:
              new_list.append(x)
    return new_list


 
#     '''
#           uses set conversions
#     '''

#     # insert the list to the set 
#     list_set = set(the_list) 
#     # convert the set to the list 
#     unique_list = (list(list_set)) 

#     return unique_list

#https://stackoverflow.com/questions/34985845/how-to-remove-adjacent-duplicate-elements-in-a-list-using-list-comprehensions/34986013
#https://www.geeksforgeeks.org/python-get-unique-values-list/
def remove_duplicated_elements_which_are_adjacent(l):
    '''

    '''
    # l=[1, 1, 2, 3, 4, 4, 4, 4, 5, 6, 3, 3, 5, 5, 7, 8, 8, 8, 9, 1, 2, 3, 3, 3, 10, 10]
    from itertools import zip_longest
    o = [p for p,n in zip_longest(l,l[1:]) if p != n] #By default fillvalue=None
    return o

#https://stackoverflow.com/questions/41125909/python-find-elements-in-one-list-that-are-not-in-the-other
def get_elements_in_list1_not_in_list2(list_1, list_2):
     main_list = np.setdiff1d(list_2,list_1)
     # yields the elements in `list_2` that are NOT in `list_1`
     return main_list


def get_elements_in_list1_not_in_list2_sorted(array1,array2,assume_unique=False):
    ans = np.setdiff1d(array1,array2,assume_unique).tolist()
    if assume_unique:
        return sorted(ans)
    return ans


def split_before_element(the_list,x):
     """
     the_list = ['a','b','c','d','e']
    

     
     [l_a, l_b]=split_at_element(the_list,x)

     
     [l_a, l_b]=split_at_element(the_list,x='c')
     l_a = ['a', 'b']
     l_b = ['c', 'd', 'e']

     [l_a, l_b]=split_at_element(the_list,x='x')
     l_a = ['a', 'b', 'c','d','e']
     l_b = []



     """

     if not x in the_list:
          return [the_list, []]
  
     x_index = the_list.index(x)

     l_a = the_list[:x_index]
     l_b = the_list[x_index:]
     
     return [l_a,l_b]

def split_after_element(the_list,x):
     """
     the_list = ['a','b','c','d','e']
    

     
     [l_a, l_b]=split_at_element(the_list,x)

     
     [l_a, l_b]=split_at_element(the_list,x='c')
     l_a = ['a', 'b', 'c']
     l_b = ['d', 'e']

     [l_a, l_b]=split_at_element(the_list,x='x')
     l_a = ['a', 'b', 'c','d','e']
     l_b = []



     """

     if not x in the_list:
          return [the_list, []]
  
     x_index = the_list.index(x)
     l_a = the_list[:x_index+1]
     l_b = the_list[x_index+1:]
          


     # if (x_index +1) > len(the_list):
     #      l_a = the_list[:x_index+1]
     #      l_b = the_list[x_index+1:]
     # else:
     #     return [the_list, []]

     return [l_a,l_b]


########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':



     print("________________")
     the_list = ['a','b','c','d','e']
     x='c'
     
     [l_a, l_b]=split_before_element(the_list,x)
     
     
     l_a_expected=['a','b','c']
     l_b_expected=['d','e']
     
     #self.assertEqual(l_a_expected, l_a, f"l_a={l_a} l_la_expected={l_a_expected}")
     #self.assertEqual(l_b_expected, l_b, f"l_b={l_b} l_la_expected={l_b_expected}")

     #print("In " + inspect.currentframe().f_code.co_name)
     print(f"         l_a={l_a}")
     print(f"         l_b={l_b}")
     print(f"         x={x}")
     print(f"l_a_expected={l_a_expected}")
     print(f"l_b_expected={l_b_expected}")
