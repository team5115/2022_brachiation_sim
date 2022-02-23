#!/usr/bin/python3
import sys
import numpy
import inspect
import shapely
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import GeometryCollection
from shapely.geometry import MultiPolygon
from csd import list_utils
from comp_geo import vec2d



def point_and_vec2d_to_next_point(Pa, unit_vector_, length=1):
    assert(isinstance(Pa,Point))
    unit_vector=vec2d.normalize_vec2d(unit_vector_)

    #eps=1e-9
    #assert(abs(numpy.linalg.norm(unit_vector)-1) < eps)
    
    total_vector=unit_vector*length
    dx=total_vector[0]
    dy=total_vector[1]
    Pb=Point(Pa.x+dx,Pa.y+dy)

    return Pb

def point_and_vec2d_to_linestring(Pa, unit_vector_, length=1):
    unit_vector=vec2d.normalize_vec2d(unit_vector_)

    eps=1e-9
    assert(unit_vector is not None)
    #assert(abs(numpy.linalg.norm(unit_vector)-1) < eps)
    
    total_vector=unit_vector*length
    dx=total_vector[0]
    dy=total_vector[1]

    Pb=Point(Pa.x+dx,Pa.y+dy)

    the_line=LineString([Pa,Pb])
    return the_line

def polygon_exterior_to_array_of_linestrings(boundary_escape):

    coords=list(boundary_escape.exterior.coords)

    the_segments=list()
    for i in range(len(coords)-1):
        
        p1=coords[i]
        p2=coords[i+1]
        the_linestring=LineString([p1,p2])
        the_segments.append(the_linestring)

    return the_segments

def shapely_object_to_array_of_points(obj):
    if isinstance(obj,LineString):
        return linestring_to_array_of_points(obj)
    elif isinstance(obj,MultiLineString):
        return multilinestring_to_array_of_points(obj)
    elif isinstance(obj,Polygon):
        return polygon_exterior_to_array_of_points(obj)
    elif isinstance(obj,MultiPolygon):        
        return multipolygon_to_array_of_points(obj)
    elif isinstance(obj,GeometryCollection):
        return geometry_collection_to_array_of_points(obj)
    elif isinstance(obj,Point):
        return [obj]
    else:
        #if verbosity > 8:
        print("In " + inspect.currentframe().f_code.co_name)
        print(f"============Unhandled type - {type(obj)}")
        sys.stdout.flush()
        #raise(f"Unhandled type - {type(obj)}")
        #    if type(a)==LineString:
#        plot_line(ax,ob,color)
        
def polygon_exterior_to_array_of_points(x):
    assert(isinstance(x,Polygon))
    coords=list(x.exterior.coords)
    return [Point(i) for i in coords]

# def multipolygon_exterior_to_array_of_points(x):
#     assert(isinstance(x,MultiPolygon))
#     coords=list(x.exterior.coords)
#     return [Point(i) for i in coords]

def multipolygon_to_array_of_points(x):
    assert(isinstance(x,MultiPolygon))
    the_points=list()
    for xi in x:
        the_points += shapely_object_to_array_of_points(xi)
    return the_points

def multipolygon_to_array_of_points_lc(x):
    assert(isinstance(x,MultiPolygon))
    the_points=list()

    sub_list = [ shapely_object_to_array_of_points(xi) for xi in x]
    
    
    return list_utils.flatten_list(sub_list)

def linestring_to_array_of_points(the_linestring):
    assert(isinstance(the_linestring,LineString))
    coords=list(the_linestring.coords)
    return [Point(i) for i in coords]

    # the_points=list()
    # for coord in coords:
    #     the_point=Point(coord)
    #     the_points.append(the_point)

    # return the_points

def multilinestring_to_array_of_points(the_multlinestring):
    the_points=list()
    for linestring in the_multlinestring:
        the_points=the_points + linestring_to_array_of_points(linestring)
    return the_points

def geometry_collection_to_array_of_points(the_collection):
    verbosity=0
    if verbosity > 8:
        print("____________________________________")
        print("In " + inspect.currentframe().f_code.co_name)
        print(f"type(the_collection)={type(the_collection)}", end='')
        print(f" the_collection={the_collection}")
        
    the_points=list()
    for obj in the_collection: 
        list_i=shapely_object_to_array_of_points(obj)
        if verbosity > 8:
            print(f"type(obj)={type(obj)}",end='')
            print(f" obj={obj}")
            print(f"type(list_i)={type(list_i)}",end='')
            print(f" obj={list_i}")

        if (list_i is not None):
            the_points += list_i
    return the_points

# def linestring_merge(line1,line2):

#     coords1=list(line1.coords)
#     coords2=list(line2.coords)

#     return Linestring(coords1+coords2)

def pretty_print_list_of_points(obj):
    print(f"[ ",end="")
    for i,obj_i in enumerate(obj):
            print(f"{obj_i} ",end="")
    print(f"] ",end="")
    print(f"N={len(obj)}")
        
def pretty_print_geometry(obj):
    if isinstance(obj,list):
        for i,obj_i in enumerate(obj):
            print(f"obj[{i}]=",end="")
            pretty_print_geometry(obj_i)
    elif obj is None:
        print("None")
        return
    elif hasattr('obj','wkt'):
        print(obj.wkt)
    else:
        l1=list(obj.coords)
        print("<",end='')
        for p in l1:
           print("(" + str(p[0]) + "," + str(p[1])+")" ,end='')
        print(">")
        
def pretty_print_geometry_array(the_array,label_str=""):
    print(f"len({label_str}) ={len(the_array)}")
    for i,element in enumerate(the_array):
        print(f"{label_str}[{i}] = ", end='')
        pretty_print_geometry(element)
    
def append_point_to_linestring(the_linestring,point_next):
    l1=list(the_linestring.coords)
    l2=list(point_next.coords)
    trace2=LineString(l1+l2)
    return trace2

def last_segment_of_linestring_to_vec2d(the_linestring):
    points=list(the_linestring.coords)[-2:]
    P1=points[0]
    P2=points[1]
    return vec2d.coords_to_vec2d(P1,P2)

def first_segment_of_linestring_to_vec2d(the_linestring):
    points=list(the_linestring.coords)[:2]
    P1=points[0]
    P2=points[1]
    return vec2d.coords_to_vec2d(P1,P2)

def get_first_segment_of_linestring(the_linestring):
    return LineString(list(the_linestring.coords)[:2])

def get_last_segment_of_linestring(the_linestring):
    return LineString(list(the_linestring.coords)[-2:])

def get_last_point_of_linestring(the_linestring):
    return Point(list(the_linestring.coords)[-1:])

def get_first_point_of_linestring(the_linestring):
    return Point(list(the_linestring.coords)[0])

def gen_rectangle_centered(p_origin,width,height):
    minx=p_origin.x-width/2.0        
    miny=p_origin.y-height/2.0
    maxx=p_origin.x+width/2.0        
    maxy=p_origin.y+width/2.0               
        
    """Returns a rectangular polygon with configurable normal vector"""
    coords = [(maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]

    the_polygon=Polygon(coords)
    return the_polygon
 
def gen_rectangle_corners(p_lower_left,p_upper_right):
    minx=p_lower_left.x        
    miny=p_lower_left.y
    maxx=p_upper_right.x        
    maxy=p_upper_right.y               
        
    """Returns a rectangular polygon with configurable normal vector"""
    coords = [(maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]

    the_polygon=Polygon(coords)
    return the_polygon


def get_boundary_crosshairs(boundary_escape):
    #           A
    #   *-------+--------*
    #   |                |
    #   |                |
    #  C*                *D
    #   |                |
    #   |                |
    #   *-------+--------*
    #           B
    #
    #
    #

    points=list(boundary_escape.exterior.coords)

    x=list()
    y=list()
    for point in points:
        x.append(point[0])
        y.append(point[1])



    x=numpy.array(x)
    y=numpy.array(y)

    x_mid=(x.max()-x.min())/2+x.min()
    y_mid=(y.max()-y.min())/2+y.min()

    Pa=Point(x_mid,y.max())
    Pb=Point(x_mid,y.min())

    Pc=Point(x.min(),y_mid)
    Pd=Point(x.max(),y_mid)


    vline=LineString([Pa,Pb])
    hline=LineString([Pc,Pd])

    return [vline,hline]


def get_boundary_crosshairs_cross(boundary_escape):
    #  C                  B
    #   *-------+--------*
    #   |                |
    #   |                |
    #   *                *
    #   |                |
    #   |                |
    #   *-------+--------*
    #  A                  D
    #
    #
    #

    points=list(boundary_escape.exterior.coords)

    x=list()
    y=list()
    for point in points:
        x.append(point[0])
        y.append(point[1])



    x=numpy.array(x)
    y=numpy.array(y)

    #x_mid=(x.max()-x.min())/2+x.min()
    #y_mid=(y.max()-y.min())/2+y.min()

    Pa=Point(x.min(),y.min())
    Pb=Point(x.max(),y.max())

    Pc=Point(x.min(),y.max())
    Pd=Point(x.max(),y.min())


    xline1=LineString([Pa,Pb])
    xline2=LineString([Pc,Pd])

    return [xline1,xline2]
