

def convert_key_to_int(the_dict):
    # dictionary comprehension
    # Type conversion of dictionary items
    new_dict = { int(key):[ val ] for key, val in the_dict.items()}
    return new_dict


def get_key_if_exists(the_dict,the_key):

    if the_key in the_dict:
        return the_dict[the_key]
    else:
        return None

#https://www.geeksforgeeks.org/python-merging-two-dictionaries/
def merge_dictionaries(dict1, dict2):
    return(dict2.update(dict1))





def test_merge_dictionaries():
    # Driver code
    dict1 = {'a': 10, 'b': 8}
    dict2 = {'d': 6, 'c': 4}
 
    # This return None
    print(Merge(dict1, dict2))
 
    # changes made in dict2
    print(dict2)
