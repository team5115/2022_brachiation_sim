import pickle
import os
import re
def cleanup_py_pickle_extension(filename):
    ### the $ is end of string specifier
    new_filename=re.sub(r'\.py\.pickle$', '.pickle', filename)
    return new_filename

def write_object_to_file(obj,pickle_filename):
    
    with open(pickle_filename, 'wb') as f:
        pickle.dump(obj, f)

    print(f"pickle file was be written to {pickle_filename}")

def read_object_from_file(pickle_filename):
    
    with open(pickle_filename, 'rb') as f:
        obj=pickle.load(f)
    return obj



def read_object_or_run_func(read_from_pickle_file,pickle_filename,func):
    """
       read_from pickle_file is an enable/disable

       read_from_pickle_file=False
       read_from_pickle_file=True
    


       pickle_file=__file__ + ".pickle"
       func=generate_database
    
        data=pickle_utils.read_object_or_run_func(read_from_pickle_file,pickle_file,func)


    """
    
    pickle_filename=cleanup_py_pickle_extension(pickle_filename)
    
    if read_from_pickle_file and os.path.exists(pickle_filename):
        data=read_object_from_file(pickle_filename)        
    else:
        data=func()
        write_object_to_file(data,pickle_filename)

    return data
