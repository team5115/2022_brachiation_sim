########################
import inspect
import math
from comp_geo import plotting_utils2


import matplotlib.pyplot as plt
import math
import pandas as pd


from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import MultiLineString

from shapely.geometry import *

from comp_geo import geometry_utils
from comp_geo import shapely_utils
from comp_geo import vec2d
from csd import pandas_conversion_utils
import sys
############# starting trace
# https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment

# def is_on(a, b, c):
#     "Return true iff point c intersects the line segment from a to b."
#     # (or the degenerate case that all 3 points are coincident)
#     return (collinear(a, b, c)
#             and (within(a.x, c.x, b.x) if a.x != b.x else 
#                  within(a.y, c.y, b.y)))

# def collinear(a, b, c):
#     "Return true iff a, b, and c all lie on the same line."
#     return (b.x - a.x) * (c.y - a.y) == (c.x - a.x) * (b.y - a.y)

# def within(p, q, r):
#     "Return true iff q is between p and r (inclusive)."
#     return p <= q <= r or r <= q <= p

def is_on(a, b, c):
    verbosity=0
    
    #epsilon=2*sys.float_info.epsilon
    epsilon=1e-9
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    if verbosity:
        print("In " + inspect.currentframe().f_code.co_name)
        print(f"epsilon= {epsilon}")
        print(f"crossproduct= {crossproduct}")
        print(f"abs(crossproduct)= {abs(crossproduct)}")
        print(f"abs(crossproduct) > epsilon= {abs(crossproduct) > epsilon}")

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > epsilon:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if verbosity:
        print(f"dotproduct= {dotproduct}")
        print(f"dotproduct < 0= {dotproduct < 0}")

    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if verbosity:
        print(f"squaredlengthba= {squaredlengthba}")
        print(f"dotproduct > squaredlengthba= {dotproduct > squaredlengthba}")

    if dotproduct > squaredlengthba:
        return False

    return True

# def intersection_of_last_segments_of_infinite_lines_v2(line1,line2):
#     #assert(isinstance(line1,list))
#     #sassert(isinstance(line2,list))

#     assert(isinstance(line1,LineString))
#     assert(isinstance(line2,LineString))

#     #assert(len(line1.coords)==2)
#     #assert(len(line2.coords)==2)
    
#     (line1_P1,line1_P2)=line1.coords[-2:]
#     (line2_P1,line2_P2)=line2.coords[-2:]

#     # x1,y1  / x4,y4
#     #  \    /
#     #   \  / 
#     #    \/
#     #    /\
#     #   /  \
#     #  /    \
#     # x3,y3  \ x2,y2


#     x1=line1_P1[0]
#     y1=line1_P1[1]
#     x2=line1_P2[0]
#     y2=line1_P2[1]

#     x3=line2_P1[0]
#     y3=line2_P1[1]
#     x4=line2_P2[0]
#     y4=line2_P2[1]

    
#     #https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
#     Px_top=(x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)
#     Px_bottom=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

#     Py_top=(x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)
#     Py_bottom=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    

#     if Px_bottom==0:
#         return None #parallel lines
#     else:
#         x=Px_top/Px_bottom
#         y=Py_top/Py_bottom
#         return Point(x,y)

# def intersection_of_last_segments_of_infinite_lines_v3(line1,line2):

#     #assert(isinstance(line1,list))
#     #sassert(isinstance(line2,list))

#     assert(isinstance(line1,LineString))
#     assert(isinstance(line2,LineString))

#     assert(len(line1.coords)==2)
#     assert(len(line2.coords)==2)
    
#     (line1_P1,line1_P2)=line1.coords[-2:]
#     (line2_P1,line2_P2)=line2.coords[-2:]

#     (A,B)=line1.coords[-2:]
#     (C,D)=line2.coords[-2:]

#     R=B-A
#     S=D-C

#     bottom=vec2d.cross(R,S)

#     if bottom==0:
#         return None #parallel lines
    
#     t=vec2d.cross((C-A),S)/bottom
#     u=vec2d.cross((C-A),R)/bottom
    

#     if t >= 0 and t<=1:
#         P=A+t*R

#     if u >= 0 and u<=1:
#         P=C+u*S

#     #P=[0,0]    
#     return vec2d.vec_to_point(P)
    
