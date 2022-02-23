#!/usr/bin/python3

import numpy
import matplotlib.pyplot as plt
import inspect
from comp_geo import vec2d
import shapely
from shapely.ops import split
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import LineString
from comp_geo import shapely_utils
from comp_geo.shapely_utils import *
from comp_geo import line_segment_utils
from comp_geo import geometry_utils
from comp_geo import point_utils
from comp_geo import plotting_utils2
#from geometry_utils import *


def plot_arrow(ax1, Pa, v_arrow, length_scale,color="black", plot_reference_line=False):

    if length_scale==0:
        return

    if vec2d.norm(v_arrow)==0:
        return
    
    line_ab=point_and_vec2d_to_linestring(Pa,v_arrow,length_scale)
    

    Pa1=shapely_utils.get_first_point_of_linestring(line_ab)
    Pa2=shapely_utils.get_last_point_of_linestring(line_ab)

    
    fudge_factor=1
    arrow_scale=line_ab.length/fudge_factor
    arrow_dx=(Pa2.x-Pa1.x)/fudge_factor
    arrow_dy=(Pa2.y-Pa1.y)/fudge_factor
    head_width_scale_factor=5
    head_length_scale_factor=5

    if plot_reference_line:
        plotting_utils2.plot_shapely_object_reference(ax1, line_ab,'blue')
    ax1.arrow(Pa.x,Pa.y,arrow_dx,arrow_dy,length_includes_head=True,head_width=arrow_scale/head_width_scale_factor,head_length=arrow_scale/head_length_scale_factor,color=color)


    return Pa2


def plot_two_arrows_end_to_end(ax1, length_scale, P_start, v_arrow_1, v_arrow_2, color_1="red", color_2="orange", plot_reference_line=False,verbosity=0):

    plot_reference_line=False
    show_points=False

    if verbosity > 0:
        print(f"v_arrow_1={v_arrow_1}")
        print(f"v_arrow_2={v_arrow_2}")
    
    P1=P_start
    plot_arrow(ax1, P1, v_arrow_1, length_scale,color=color_1, plot_reference_line=plot_reference_line)

                    
    P2=point_utils.move_point_along_vector(P1,v_arrow_1,dr=length_scale)


    plot_arrow(ax1, P2, v_arrow_2, length_scale,color=color_2, plot_reference_line=plot_reference_line)

    
    if show_points:
        plotting_utils2.plot_shapely_object(ax1, P1,'lightblue')        
        plotting_utils2.plot_shapely_object(ax1, P2,'lightblue')        
        P3=point_utils.move_point_along_vector(P2,v_arrow_2,dr=length_scale)
        plotting_utils2.plot_shapely_object(ax1, P3,'lightblue')
