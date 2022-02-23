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

def intersection_of_last_segments_of_infinite_lines_v1(line1,line2):

    #assert(isinstance(line1,list))
    #sassert(isinstance(line2,list))

    assert(isinstance(line1,LineString))
    assert(isinstance(line2,LineString))

    assert(len(line1.coords)==2)
    assert(len(line2.coords)==2)
    
    (line1_P1,line1_P2)=line1.coords[-2:]
    (line2_P1,line2_P2)=line2.coords[-2:]
    
    # Line1
    A1 = line1_P2[1] - line1_P1[1];
    B1 = line1_P2[0] - line1_P1[0];
    C1 = A1*line1_P1[0] + B1*line1_P1[1];

    A2 = line2_P2[1] - line2_P1[1];
    B2 = line2_P2[0] - line2_P1[0];
    C2 = A2*line2_P1[0] + B2*line2_P1[1];

    det = A1*B2 - A2*B1;

    if det==0:
        return None #parallel lines
    else:
        x = (B2*C1 - B1*C2)/det;
        y = (A1 * C2 - A2 * C1) / det;
        return Point(x,y)

    

def intersection_of_last_segments_of_infinite_lines_v2(line1,line2):
    #assert(isinstance(line1,list))
    #sassert(isinstance(line2,list))

    assert(isinstance(line1,LineString))
    assert(isinstance(line2,LineString))

    #assert(len(line1.coords)==2)
    #assert(len(line2.coords)==2)
    
    (line1_P1,line1_P2)=line1.coords[-2:]
    (line2_P1,line2_P2)=line2.coords[-2:]

    # x1,y1  / x4,y4
    #  \    /
    #   \  / 
    #    \/
    #    /\
    #   /  \
    #  /    \
    # x3,y3  \ x2,y2


    x1=line1_P1[0]
    y1=line1_P1[1]
    x2=line1_P2[0]
    y2=line1_P2[1]

    x3=line2_P1[0]
    y3=line2_P1[1]
    x4=line2_P2[0]
    y4=line2_P2[1]

    
    #https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    Px_top=(x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)
    Px_bottom=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    Py_top=(x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)
    Py_bottom=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    

    if Px_bottom==0:
        return None #parallel lines
    else:
        Px=Px_top/Px_bottom
        Py=Py_top/Py_bottom
        return Point(Px,Py)
    


    
def intersection_of_last_segments_of_infinite_lines_v3(line1,line2, keep_within_line_segments=False):

    #assert(isinstance(line1,list))
    #sassert(isinstance(line2,list))
    
    assert(isinstance(line1,LineString))
    assert(isinstance(line2,LineString))

    assert(len(line1.coords)==2)
    assert(len(line2.coords)==2)

    list_of_points1=shapely_utils.linestring_to_array_of_points(line1)
    list_of_points2=shapely_utils.linestring_to_array_of_points(line2)
     
    (P1,P2)=list_of_points1[-2:]
    (P3,P4)=list_of_points2[-2:]

    assert(isinstance(P1,Point))
    assert(isinstance(P2,Point))
    assert(isinstance(P3,Point))
    assert(isinstance(P4,Point))

    A=vec2d.point_to_vec2d(P1)
    B=vec2d.point_to_vec2d(P2)
    C=vec2d.point_to_vec2d(P3)
    D=vec2d.point_to_vec2d(P4)
    
    #(A,B)=line1.coords[-2:]
    #(C,D)=line2.coords[-2:]

    R=B-A
    S=D-C

    bottom=vec2d.cross_product_2d(R,S)

    if abs(bottom) < 1e-9:
        return None #parallel lines
    
    t=vec2d.cross_product_2d((C-A),S)/bottom
    u=vec2d.cross_product_2d((C-A),R)/bottom
    
    Pt=A+t*R
    Pr=A+t*R


    if keep_within_line_segments:
        if abs(t) >= 0 and t<=1:
            P=Pt            
        elif abs(u) >= 0 and u<=1:
            P=Pr
        else:
            P=None

        return P


    PP1=vec2d.vec2d_to_point(Pt)
    PP2=vec2d.vec2d_to_point(Pr)

    # print(f"Pt={Pt}")
    # print(f"Pr={Pr}")
    # print(f"t={t}")
    # print(f"u={u}")
    # print(f"PP1.distance(PP2)={PP1.distance(PP2)}")

    
    return PP1
    
    

    
