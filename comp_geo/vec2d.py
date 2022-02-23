import math
import numpy
import numpy as np
import shapely
from shapely.geometry import Point

#import pytest

# import contextlib
# with contextlib.redirect_stdout(None):
#     import pygame.math
#     from pygame.math import Vector2
    

v_down=numpy.array([0,-1])
v_up=numpy.array([0,1])
v_right=numpy.array([1,0])
v_left=numpy.array([-1,0])
v_nan=numpy.array([np.nan,np.nan])

all_directions_manhattan={ "right": v_right,
                           "up": v_up,
                           "left": v_left,
                           "down": v_down}


def is_likely_vec2d(v):
    if isinstance(v,numpy.ndarray):
        return len(v)==2    
    return False

def gen_vec2d(x,y):
    return numpy.array([x,y])

def rotation_matrix(theta_deg):
    theta = np.radians(theta_deg)

    r = np.array(( (np.cos(theta), -np.sin(theta)),
                   (np.sin(theta),  np.cos(theta)) ))
    return r

def rotate_arbitrary(V1,theta_deg):
    R=rotation_matrix(theta_deg)

    V2=R.dot(V1)
    return V2

def rotate_ccw(V1):

    R = np.array((
                   (0, -1),
                   (1,0)
                 ))
    return R.dot(V1)

def rotate_cw(V1):

    R = np.array((
                   (0, 1),
                   (-1,0)
                 ))
    return R.dot(V1)

def vec2d_to_point(V):
    assert(isinstance(V,numpy.ndarray))
    return Point(V[0],V[1])

def point_to_vec2d(P):
    assert(isinstance(P,Point))
    return numpy.array([P.x,P.y])

def points_to_vec2d(P1: shapely.geometry.Point ,P2: shapely.geometry.Point,normalize=False):
    assert(isinstance(P1,shapely.geometry.Point))
    assert(isinstance(P2,shapely.geometry.Point))
    
    dx=P2.x-P1.x
    dy=P2.y-P1.y
    v=numpy.array([dx,dy])

    if normalize:
        v=normalize_vec2d(v)
    return v

def coords_to_vec2d(P1,P2):
    dx=P2[0]-P1[0]
    dy=P2[1]-P1[1]
    return numpy.array([dx,dy])

def length(V):
    return norm(V)

def mag(V):
    return norm(V)

def norm(V):
    return numpy.linalg.norm(V)

def to_polar_coordinates(V):
    x=V[0]
    y=V[1]
    r = np.sqrt(x**2+y**2)
    theta = np.arctan2(y,x)

#    return [r,theta]
    return gen_vec2d(r,theta)

def polar_coordinates_to_vector(r,theta,theta_is_in_degrees=False):

    if theta_is_in_degrees:
        theta=math.radians(theta)
    
    x=r*math.cos(theta)
    y=r*math.sin(theta)

#    return [x,y]
    return gen_vec2d(x,y)

def to_polar_angle_deg(V):
    # x_hat = 0 deg
    # y_hat = 90 deg
    #r = np.sqrt(x**2+y**2)
    theta = np.arctan2(V[1],V[0])

    if theta < 0:
        theta=2*math.pi+theta


    
    theta=math.degrees(theta)
    

    return theta

def normalize_vec2d(V):
    V_mag=norm(V)

    if (V_mag==0):
        return V
    #assert(V_mag != 0)
    return V/V_mag

def dot_product(V1,V2):    
    return V1.dot(V2)

def cross_product_2d(V1,V2):    
    cx=np.cross(V1,V2)

    ### scalar for 2d
    return cx.tolist()

def points_to_normalized_vec2d(P1,P2):
    return normalize_vec2d(points_to_vec2d(P1,P2))

def angle_between_vectors_degrees(v1,v2):
     theta_rad=math.acos(v1.dot(v2))
     theta_deg=math.degrees(theta_rad)
     return theta_deg
                         
def are_vectors_orthogonal(v1,v2):

    direction=numpy.dot(normalize_vec2d(v1),normalize_vec2d(v2))
    epsilon=1e-12
    err=abs(direction)
    verbosity=0
    
    if verbosity > 0:
        print(f"v1={v2}")
        print(f"v2={v2}")
        print(f"direction={direction}")
        print(f"err={err}")
        print(f"epsilon={epsilon}")
    
    if err < epsilon:
        return True
    else:
        return False


def are_vectors_parallel(v1,v2,verbosity=0):

    direction=numpy.dot(normalize_vec2d(v1),normalize_vec2d(v2))
    epsilon=1e-6
    err=abs(1.0-direction)

    if err < epsilon:
        result=True
    else:
        result=False
    
    
    if verbosity > 0:
        print(f"v1={v2}")
        print(f"v2={v2}")
        print(f"direction={direction}")
        print(f"err={err}")
        print(f"epsilon={epsilon}")
        print(f"is_parallel={result}")

    return result

def are_vectors_antiparallel(v1,v2,verbosity=0):
    direction=numpy.dot(normalize_vec2d(v1),normalize_vec2d(v2))
    epsilon=1e-12
    err=abs(-1.0-direction)

    
    if verbosity > 0:
        print(f"v1={v2}")
        print(f"v2={v2}")
        print(f"direction={direction}")
        print(f"err={err}")
        print(f"epsilon={epsilon}")

    if err < epsilon:
        return True
    else:
        return False


######################################################
#
#
# main
#  
#
#######################################################
if __name__ == '__main__':
    # from vec2d import *
    R=rotation_matrix(-90)

    print("__________________________________")
    print("R")
    print(R)


    V1=v_right
    print("__________________________________")
    print("V1")
    print(V1)

    
    V2=R.dot(V1)
    print("__________________________________")
    print("V2")
    print(V2)

    V3=rotate_ccw(V1)
    print("__________________________________")
    print("V3")
    print(V3)

    
    # print("__________________________________")
    # print("Set #1")
    # A=numpy.array([7,0])
    # B=numpy.array([-1,0])

    # print(f"A={A}")
    # print(f"B={B}")


    # result=are_vectors_parallel(A,B)
    # print(f"are_vectors_parallel={result}")

    # result=are_vectors_antiparallel(A,B)
    # print(f"are_vectors_antiparallel={result}")

    # print("__________________________________")
    # print("Set #2")
    
    # A=numpy.array([7,1])
    # B=numpy.array([-14,-2])

    # print(f"A={A}")
    # print(f"B={B}")


    # result=are_vectors_parallel(A,B)
    # print(f"are_vectors_parallel={result}")

    # result=are_vectors_antiparallel(A,B)
    # print(f"are_vectors_antiparallel={result}")
  

    # print("__________________________________")
    # print("Set #3")
    
    # A=numpy.array([7,1])
    # B=numpy.array([14,2])

    # print(f"A={A}")
    # print(f"B={B}")


    # result=are_vectors_parallel(A,B)
    # print(f"are_vectors_parallel={result}")

    # result=are_vectors_antiparallel(A,B)
    # print(f"are_vectors_antiparallel={result}")
  
