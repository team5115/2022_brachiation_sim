#!/usr/bin/python3




from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
import shapely
#Trace_margin=1.5
#Trace_width=2.5
#Trace_width=int(155/5.0)/2

#Trace_width=5

from enum import Enum, IntEnum, unique, Flag,auto

# @unique
# class Rectangle_Origin_Type(IntEnum):
#     CENTROID=auto()
#     LOWER_LEFT=auto()
#     UPPER_RIGHT=auto()


def calculate_p_center_from_p_lower_left(p_lower_left, width, height):
#
#
#    
#              P4               P3
# y2 -->        *----------------*
#               |                |
#               |                |
#   y3->          |       *        |
#               |                |
#               |                |
#  y1 -->       *----------------*
#               P1      ^        P2
#                       |
#               ^       x3       ^
#               |                |
#               x1               x2
   

    x1=p_lower_left.x        
    y1=p_lower_left.y
    #x2=p_lower_left.x+width        
    #y2=p_lower_left.y+height               

    
    x3=x1+width/2.0
    y3=y1+height/2.0
    
    P_center=Point(x3,y3)

    return P_center
 


def get_width_and_height_from_rectangle(the_poly):
    [x1,x2,y1,y2]=get_extents_from_rectangle(the_poly)

    dx=x2-x1
    dy=y2-y1
    
    return [dx,dy]
    
def get_extents_from_rectangle(the_poly):
    """ [x1,x2,y1,y2]=get_extents_from_polygon(the_poly)"""
    points=list(the_poly.exterior.coords)
    x=list()
    y=list()
    for point in points:
        #print(f"x={x_i}")
        x.append(point[0])
        y.append(point[1])

    x1=min(x)
    x2=max(x)
    y1=min(y)
    y2=max(y)


    
    return [x1,x2,y1,y2]



def rotate_polygon(poly_i, angle, r_c):
    rpoly = shapely.affinity.rotate(poly_i, angle, r_c)
    return rpoly

# def gen_rectangle(rectangle_origin_type, p_origin, width, height, angle):
#     if rectangle_origin_type=Rectangle_Origin_Type.CENTROID
#       return gen_rectangle_from_centroid(p_origin, width, height, angle)
#     elif rectangle_origin_type=Rectangle_Origin_Type.LOWER_LEFT
#       return gen_rectangle_from_centroid(p_origin, width, height, angle)
#     else
#        raise "Not Implemented"
   
def gen_rectangle_from_centroid(p_origin, width, height, angle=0):   
#              P4               P3
# y2 -->        *----------------*
#               |                |
#               |                |
#               |                |
#               |                |
#               |                |
#  y1 -->       *----------------*
#               P1               P2
#
#               ^                ^
#               |                |
#               x1               x2
    
    minx=p_origin.x-width/2.0        
    miny=p_origin.y-height/2.0
    maxx=p_origin.x+width/2.0        
    maxy=p_origin.y+height/2.0               
        
    
    P1=Point(minx, miny)
    P2=Point(maxx, miny)
    P3=Point(maxx, maxy)
    P4=Point(minx, maxy)
    
    coords = [ P1, P2, P3, P4, P1]
    
    
    poly_i=Polygon(coords)

    if angle !=0:
        poly_i=rotate_polygon(poly_i,angle=angle,r_c=p_origin)

    
    return poly_i

def gen_rectangle_from_lower_left(p_origin, width, height, angle):
#
#   rotation is about lower left
#
#    
#              P4               P3
# y2 -->        *----------------*
#               |                |
#               |                |
#               |                |
#               |                |
#               |                |
#  y1 -->       *----------------*
#               P1               P2
#
#               ^                ^
#               |                |
#               x1               x2
   
    p_lower_left=p_origin
    minx=p_lower_left.x        
    miny=p_lower_left.y
    maxx=p_lower_left.x+width        
    maxy=p_lower_left.y+height               
        
    
    coords = [(maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]
    poly_i=Polygon(coords)

    if angle !=0:
        poly_i=rotate_polygon(poly_i,angle=angle,r_c=p_lower_left)

    return poly_i
 

####################################################
#
#              P4       P3       P2
# y2 -->        *-----+-----*
#               |     |     |
#               |     |     |
#               |     |     |           W0= perimeter
#               |     |     |           W9= boundaries
#               |     |     |
# y0 -->    P5  *---P0*-----* P1
#               |     |     |
#               |     |     |
#               |     |     |
#               |     |     |
#               |     |     |
#  y1 -->       *-----+-----* 
#               P6      P7      P8
#
#               ^       ^        ^
#               |       |        |
#               x1      x0       x2
#
#

def get_key_perimeter_points_rectangle(the_rectangle):

    
    [x1,x2,y1,y2]=get_extents_from_rectangle(the_rectangle)

    ## probably a cleaner syntax but I can't find it
    [(x0,y0)]=list(the_rectangle.centroid.coords)

    P=dict()
    
    P[0]=Point(x0,y0)
    P[1]=Point(x2,y0)
    P[2]=Point(x2,y2)
    P[3]=Point(x0,y2)
    P[4]=Point(x1,y2)
    P[5]=Point(x1,y0)
    P[6]=Point(x1,y1)
    P[7]=Point(x0,y1)
    P[8]=Point(x2,y1)

    return P

####################################################
#
#              P4       P3       P2
# y2 -->        *-----+-----*
#               |     |     |
#               |     |     |
#               | Q2  | Q1  |           W0= perimeter
#               |     |     |           W9= boundaries
#               |     |     |
# y0 -->    P5  *---P0*-----* P1
#               |     |     |
#               |     |     |
#               | Q3  | Q4  |
#               |     |     |
#               |     |     |
#  y1 -->       *-----+-----* 
#               P6      P7      P8
#
#               ^       ^        ^
#               |       |        |
#               x1      x0       x2
#
#

def get_quadrant_polys_from_rectangle(the_rectangle):

    P=get_key_perimeter_points_rectangle(the_rectangle)
    
    quadrant_polys=dict()
    quadrant_polys[1]=Polygon([P[0],P[1],P[2],P[3],P[0]])
    quadrant_polys[2]=Polygon([P[0],P[3],P[4],P[5],P[0]])
    quadrant_polys[3]=Polygon([P[0],P[5],P[6],P[7],P[0]])
    quadrant_polys[4]=Polygon([P[0],P[7],P[8],P[1],P[0]])

    return quadrant_polys
####################################################
#
#              P4       P3       P2
# y2 -->        *-----+-----*
#               |     |     |
#               |     |     |
#               | Q2  | Q1  |           W0= perimeter
#               |     |     |           W9= boundaries
#               |     |     |
# y0 -->    P5  *---P0*-----* P1
#               |     |     |
#               |     |     |
#               | Q3  | Q4  |
#               |     |     |
#               |     |     |
#  y1 -->       *-----+-----* 
#               P6      P7      P8
#
#               ^       ^        ^
#               |       |        |
#               x1      x0       x2
#
#

def get_half_polys_from_rectangle(the_rectangle):

    P=get_key_perimeter_points_rectangle(the_rectangle)
    
    the_dict=dict()
    the_dict["upper_half"]=Polygon([P[5],P[4],P[2],P[1],P[5]])
    the_dict["lower_half"]=Polygon([P[5],P[1],P[8],P[6],P[5]])
    # quadrant_polys[2]=Polygon([P[0],P[3],P[4],P[5],P[0]])
    # quadrant_polys[3]=Polygon([P[0],P[5],P[6],P[7],P[0]])
    # quadrant_polys[4]=Polygon([P[0],P[7],P[8],P[1],P[0]])

    return the_dict






        

