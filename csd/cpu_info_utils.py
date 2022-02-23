
import sys
import platform

# pip install py-cpuinfo

def print_platform_info(f_stream=sys.stdout):
    #print(f"OS version= {platform.version()}",file=f_stream)
    #print(f"OS description= {platform.platform()}",file=f_stream)
    #print(f"Machine = {platform.machine()}",file=f_stream)
    #print(f"Processor = {platform.processor()}",file=f_stream)
    #print(f"Architecture = {platform.architecture()}",file=f_stream)
    print(f"Python version = {platform.python_version()}",file=f_stream)
    print(f"Python Implementation = {platform.python_implementation()}",file=f_stream)      
 
    print(f"OS name= {platform.system()}",file=f_stream)
    print(f"OS release= {platform.release()}",file=f_stream)
    print(f"OS version= {platform.version()}",file=f_stream)
    print(f"OS description= {platform.platform()}",file=f_stream)
    print(f"Machine = {platform.machine()}",file=f_stream)
    print(f"Processor = {platform.processor()}",file=f_stream)
    print(f"Architecture = {platform.architecture()}",file=f_stream)
 

def print_cpu_info(f_stream=sys.stdout):
    try:
        import cpuinfo

        data=cpuinfo.get_cpu_info()


        keys={'brand_raw': "Model",
              'arch': "Arch",
              'bits': "Bits",
              'count'                 : "count",
              'hz_advertised_friendly': "Hz Advertised",
              'hz_actual_friendly'    : "Hz Actual",
              'l3_cache_size': 'L3 cache size',
              'l2_cache_size': 'L2 cache size',
              'l1_data_cache_size':'L1 data cache size',
              'l1_instruction_cache_size':'L1 instruction cache size',
              'l2_cache_line_size':'L2 cache line size',
              'l2_cache_associativity':'L2 cache associativity'}

        for key,value in keys.items():
            print(f"{value} = {data[key]}",file=f_stream)


    except:
        pass
            #    d['brand_raw']: 'Intel(R) Core(TM) i7-7600U CPU @ 2.80GHz',
            # 'hz_advertised_friendly': '2.8000 GHz',
            # 'hz_actual_friendly': '3.6962 GHz',
