import multiprocessing
import numpy as np
import pandas as pd

# import dask.dataframe as ddf
# df_dask = ddf.from_pandas(df, npartitions=4)   # where the number of partitions is the number of cores you want to use
# df_dask['output'] = df_dask.apply(lambda x: your_function(x), meta=('str')).compute(scheduler='multiprocessing')

#https://stackoverflow.com/questions/40357434/pandas-df-iterrows-parallelization

def parallelize_dataframe(df, func):
    num_cores = multiprocessing.cpu_count()-1  #leave one free to not freeze machine
    num_partitions = num_cores #number of partitions to split dataframe
    df_split = np.array_split(df, num_partitions)
    pool = multiprocessing.Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


if __name__ == '__main__':
    # freeze_support()
    # set_start_method('spawn')
    # p = Process(target=foo)
    # p.start()
    print("")    
