import time
import sys
from datetime import timedelta
#>>> str(timedelta(seconds=elapsed))
class Stopwatch(object):
    def __init__(self, name=None,verbosity=0):
        self.name = name
        self.t_stop = time.time()
        self.t_start = time.time()
        self.is_running = False
        self.verbosity = verbosity   

    def start(self):
        if not self.is_running:
            self.is_running=True
            self.t_start = time.time()

    def stop(self):
        if self.is_running:
            self.is_running=False
            self.t_stop= time.time()
            if (self.verbosity >0):
                self.pretty_print()       
   
    def etime_s(self,f_file=sys.stdout):
        dt=self.t_stop - self.t_start
        return dt

    def pretty_print(self,f_file=sys.stdout):
        if self.name:
            print('Stopwatch %s ' % self.name,end='',file=f_file)
        dt=self.t_stop - self.t_start
        #str(timedelta(seconds=dt))
        print('Elapsed time: %s' % ( str(timedelta(seconds=dt))),file=f_file)
        #sys.stdout.flush()
