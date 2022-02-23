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
import math


from comp_geo import plotting_utils2

def round_point(P, n_digits=11):

    x=round(P.x,n_digits)
    y=round(P.y,n_digits)

    P2=Point(x,y)
    return P2

def list_of_points_to_list_of_xy_coords(list_of_points):

    l2=[]
    
    for i, x_i in enumerate(list_of_points):
     #print(f"i={i} = ",end='')
     #print(f"x={x_i}")
     pi=[x_i.x,x_i.y]
     l2.append(pi)

    return l2




def list_of_points_to_list_of_polar_angles(list_of_points,angle_is_in_degrees=True):

    return [point_to_polar_angle(Pi,angle_is_in_degrees) for Pi in list_of_points]
    

def point_to_polar_angle(Po,angle_is_in_degrees=False):
    Vo=vec2d.point_to_vec2d(Po)
    [r,theta]=vec2d.to_polar_coordinates(Vo)
    if theta <0:
        theta+=2*math.pi

    if angle_is_in_degrees:
        theta=math.degrees(theta)
    return theta

def point_to_polar_angle_degrees(Po):
    return theta
    
def get_closest_point_in_list(Pa,list_of_points,verbosity=0):
    '''
        does the geometric distance

    '''
    assert(isinstance(Pa,Point))
    assert(isinstance(list_of_points,list))
    
    if verbosity > 8:
        print("**************************************************")
        print("In " + inspect.currentframe().f_code.co_name)
        print(f"type(list_of_points)={type(list_of_points)}")
        print(f"list_of_points={list_of_points}")
        print(f"type(Pa)={type(Pa)}")
        print(f"Pa={Pa}")
        
    d_min=None
    p_min=None
    for i,Pi in enumerate(list_of_points):

        di=Pa.distance(Pi)
        
        if ((d_min is None) or (d_min > di)):
            d_min=di
            p_min=Pi

    if verbosity > 8:
        print(f"i={i}")
        print(f"Pi={Pi}")
        print(f"d_min={d_min}")
        print(f"p_min={p_min}")

    
    if verbosity > 9:
        plt.clf()
        fig = plt.figure(1)
        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        plotting_utils2.plot_shapely_object(ax1, list_of_points,'b')
        plotting_utils2.plot_shapely_object(ax1, Pa,'g')
        plotting_utils2.plot_point(ax1, p_min,'r','x')
        #plotting_utils2.plot_shapely_object(ax1, Pa,'g')
        ax1.axis('equal')
        ax1.set_title(inspect.currentframe().f_code.co_name)
        plt.draw()
        plt.pause(0.1)
        plt.show()

    
    return p_min

    
    
def move_point_along_vector(P, v_direction, dr):
        assert(isinstance(P,shapely.geometry.Point))
        assert(isinstance(v_direction,numpy.ndarray))
        v_delta=dr*v_direction
        #P_new=Point(P.x-v_delta[0],P.y-v_delta[1])
        P_new=Point(P.x+v_delta[0],P.y+v_delta[1])
        return P_new

def move_point_up(P, dr):
        v_direction=vec2d.v_up 
        return move_point_along_vector(P,v_direction,dr)

def move_point_down(P, dr):
        v_direction=vec2d.v_down 
        return move_point_along_vector(P,v_direction,dr)

def move_point_right(P, dr):
        v_direction=vec2d.v_right 
        return move_point_along_vector(P,v_direction,dr)

def move_point_left(P, dr):
        v_direction=vec2d.v_left 
        return move_point_along_vector(P,v_direction,dr)

