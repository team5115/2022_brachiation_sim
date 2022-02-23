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



from comp_geo import plotting_utils2

def get_last_point_in_a_linestring(L1):
    assert(isinstance(L1,LineString))
    return list(L1.coords)[-1]

def split_linestring_into_linesegments(L1):
    
    assert(isinstance(L1,LineString))

    return list(map(LineString, zip(L1.coords[:-1], L1.coords[1:])))


def reverse_line(L1):
    p_list=shapely_utils.linestring_to_array_of_points(L1)
    p_list.reverse()
    return LineString(p_list)

# def get_closest_point_in_list(Pa,list_of_points,verbosity=0):
#     '''
#         does the geometric distance

#     '''
#     assert(isinstance(Pa,Point))
#     assert(isinstance(list_of_points,list))
    
#     if verbosity > 8:
#         print("**************************************************")
#         print("In " + inspect.currentframe().f_code.co_name)
#         print(f"type(list_of_points)={type(list_of_points)}")
#         print(f"list_of_points={list_of_points}")
#         print(f"type(Pa)={type(Pa)}")
#         print(f"Pa={Pa}")
        
#     d_min=None
#     p_min=None
#     for i,Pi in enumerate(list_of_points):

#         di=Pa.distance(Pi)
        
#         if ((d_min is None) or (d_min > di)):
#             d_min=di
#             p_min=Pi

#     if verbosity > 8:
#         print(f"i={i}")
#         print(f"Pi={Pi}")
#         print(f"d_min={d_min}")
#         print(f"p_min={p_min}")

    
#     if verbosity > 9:
#         plt.clf()
#         fig = plt.figure(1)
#         ### subplot nrows, ncols, plot #
#         ax1 = fig.add_subplot(111)
#         plotting_utils2.plot_shapely_object(ax1, list_of_points,'b')
#         plotting_utils2.plot_shapely_object(ax1, Pa,'g')
#         plotting_utils2.plot_point(ax1, p_min,'r','x')
#         #plotting_utils2.plot_shapely_object(ax1, Pa,'g')
#         ax1.axis('equal')
#         ax1.set_title(inspect.currentframe().f_code.co_name)
#         plt.draw()
#         plt.pause(0.1)
#         plt.show()

    
#     return p_min

    
    

def start_line(P1):
    all_points=[P1]
    return all_points

def extend_line_along_vector(list_of_points,v_direction,dr):
    assert(isinstance(list_of_points,list))    
    P_last=list_of_points[-1]
    P_new=move_point_along_vector(P_last,v_direction,dr)
    list_of_points.append(P_new)
    return list_of_points

def extend_line_up(list_of_points,dr):
    v_direction=vec2d.v_up 
    return extend_line_along_vector(list_of_points,v_direction,dr)    

def extend_line_down(list_of_points,dr):
    v_direction=vec2d.v_down 
    return extend_line_along_vector(list_of_points,v_direction,dr)    

def extend_line_right(list_of_points,dr):
    v_direction=vec2d.v_right 
    return extend_line_along_vector(list_of_points,v_direction,dr)    

def extend_line_left(list_of_points,dr):
    v_direction=vec2d.v_left 
    return extend_line_along_vector(list_of_points,v_direction,dr)    



def split_line_at_point(list_of_points,P_split,graff=False):

    assert(isinstance(list_of_points, list))
    assert(isinstance(P_split, shapely.geometry.Point))

    
    
    L_full=LineString(list_of_points)

    assert(L_full.intersects(P_split))
    the_two_lines_as_geometry_collection = shapely.ops.split(L_full, P_split)

    if len(the_two_lines_as_geometry_collection) != 2:
        print(f"len(the_two_lines_as_geometry_collection)={len(the_two_lines_as_geometry_collection)}")
        print(f"the_two_lines_as_geometry_collection={the_two_lines_as_geometry_collection.wkt}")


    if graff:
          plt.clf()
          colors=plt.get_cmap('Set1')
          fig = plt.figure(1)

          ### subplot nrows, ncols, plot #
          ax1 = fig.add_subplot(111)

          plotting_utils2.plot_shapely_object(ax1,L_full, 'blue')
          plotting_utils2.plot_shapely_object(ax1,P_split, 'red')

          colors=plt.get_cmap('Set1')
          color_count=0
          for i, x_i in enumerate(the_two_lines_as_geometry_collection):
              print(f"i={i} = ",end='')
              print(f"x={x_i}")
              L_i=the_two_lines_as_geometry_collection[0]
              plotting_utils2.plot_shapely_object(ax1, L_i, colors(color_count))
              color_count += 1
          plt.axis('equal')
          plt.show()
                   
    #assert(len(the_two_lines_as_geometry_collection)==2)

    
    L1=the_two_lines_as_geometry_collection[0]
    list_of_points1=shapely_utils.linestring_to_array_of_points(L1)

    
    try:
        L2=the_two_lines_as_geometry_collection[1]
        list_of_points2=shapely_utils.linestring_to_array_of_points(L2)
    except:
        L2=None
        list_of_points2=[]

    



    return [list_of_points1, list_of_points2]


