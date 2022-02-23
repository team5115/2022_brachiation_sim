########################################
#
#
#
#
########################################

#import matplotlib.pyplot as plt
import scipy
#from scipy import stats
import numpy as np
import phidl

import quickplotter3
import os
import sys
import display_layout
import matplotlib.pyplot as plt

from csd import stats_utils
from csd import pickle_utils
from csd.stopwatch import *
from csd import plot_utils


import matplotlib.style as mplstyle
import plotting_utils2

from csd import pandas_conversion_utils
import shapely_utils

from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
import rectangle_utils
import vec2d
import list_line
import list_line_utils
import inspect
import geometry_utils
import route_bond_pads
import intersection_utils
import trace_utils
#import generate_bundle
import linestring_utils
import shapely
from weo_saving_utils import *
from csd import list_utils
from csd import plot_utils
import wire_counting_utils
import geo_superclass
from weo_saving_utils import *
from generate_gds_file_from_weo import *
import generate_mirrored_weo_traces

from stitcher import stitching_utils
import copy
from weo_saving_utils import *
import weo_routed_flag_utils
from csd import list_utils

import argparse
import get_working_scale
import global_configuration
import sextant_utils
import get_working_scale
import contiguous_trace_utils
import command_line_processor
import os
import inspect
from csd import pandas_utils
import geometrical_filters


class Plot_Bot:
    def __init__(self,graff=True):
        self.ax1=None
        self.graff=graff
        # self.df_pixels            = None
        # self.df_traces_n          = None

        # self.df_v_streets         = None
        # self.df_h_streets         = None

        # self.boundary_escape=None
        # self.reference_lines_dict=None

        # self.boundary_tight=None
        # #self.boundary_routing=None
        # self.boundary_reference=None
        # self.cfg=None

    def start_new_plot(self):
        

        if self.graff:
            plt.clf()
            figure_no=1
            fig = plt.figure(figure_no)
            ### subplot nrows, ncols, plot #
            self.ax1 = fig.add_subplot(111)

        
    def add_elements_from_df(self,df,column_name,color='lightgreen'):
        if self.graff:
            list_of_traces=list(filter(None,df[column_name])) 
            plotting_utils2.plot_shapely_object(self.ax1, list_of_traces,color=color)
    def add_element(self,obj,color='gray',show_points=False,linestyle='solid',linewidth=3):
        if self.graff:
            plotting_utils2.plot_shapely_object(self.ax1, obj,color=color,show_points=False,linestyle='solid',linewidth=3)

    def update(self):
        if self.graff:
            plt.draw()
            plt.pause(0.1)

        
    def close_up_and_display(self,title_str=""):
        if self.graff:
            if len(title_str) > 0:
                self.ax1.set_title(title_str)
            self.ax1.axis('equal')
            plt.draw()
            plt.pause(0.1)

    def pause(self):    
        plt.show()
        
