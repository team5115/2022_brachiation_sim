# mp = MultiPoint(route)
# print nearest_points(mp, end)[0]
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import GeometryCollection
from shapely.geometry import MultiPolygon

from comp_geo import vec2d
from comp_geo import list_line
from comp_geo import point_utils
from comp_geo.list_line import ListLine as ListLine

from csd import arrow_plotting_utils
from comp_geo import plotting_utils2 

import field_constants
import robot_constants
import robot_hanging_utils
from draw_robot import draw_robot

#####################################################################
#
#
#
#
#
#
#########################################################################



v_down=vec2d.v_down


P_a=field_constants.rung_top_points["mid"]
P_b=field_constants.rung_top_points["high"]

L_ac=5

w=robot_constants.robot_width
d=w/2

#L_bd=7
#L_bd_values=[7,6,5,4,2]

n_points=100
L_bd_values=np.linspace(robot_constants.robot_max_arm_length,robot_constants.robot_min_arm_length,n_points)



for i, L_bd in enumerate(L_bd_values):

        # print(f"i={i} = ",end='')
        # print(f"x={x_i}")
        

        
        robot_data=robot_hanging_utils.calculate_robot_hanging_from_arm_b(P_b,L_ac,L_bd, w, d)

        field_data=field_constants.rung_top_points
        
        draw_robot(robot_data,field_data)
        plt.pause(.1)
                
                
    
