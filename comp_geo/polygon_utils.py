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
from comp_geo import point_utils
from comp_geo import linestring_utils
from comp_geo import plotting_utils2
from comp_geo import figure_utils
import pandas as pd
from csd import pandas_conversion_utils
from comp_geo import point_utils
from csd import arrow_plotting_utils
from csd import list_utils
from comp_geo import geometry_utils

def get_polygon_exterior_points_as_ccw_list_starting_at_theta0(the_polygon):
    P_corners=polygon_exterior_to_array_of_points(the_polygon)

    ### drop repeated point at the end 
    P_corners.pop(-1)
    
    angles=point_utils.list_of_points_to_list_of_polar_angles(P_corners)
    P_corners_sorted=list_utils.sort_list_x_values_in_list_y(P_corners,angles)
    angles_sorted=point_utils.list_of_points_to_list_of_polar_angles(P_corners_sorted)

    return P_corners_sorted
    
def get_width_and_height_from_bounds(the_poly):
    [x1,y1,x2,y2]=the_poly.bounds

    dx=x2-x1
    dy=y2-y1
    
    return [dx,dy]
   
def are_two_polygons_nearly_identical(poly_i, poly_j, thresh=0.05,graff=False):
    '''

    '''
    ## The two areas need to be similar
    tol=1e-6            
    percent_error_in_area =abs(poly_i.area-poly_j.area)/poly_i.area
    if (percent_error_in_area > thresh):
        return False

        
    ## if the union of the two has an area that is within 5%
    ## of a single one than it likely the same poly
    poly_ij=poly_i.union(poly_j)
    
    tol=0.05            
    percent_error=abs(poly_ij.area-poly_j.area)/poly_i.area

    if (percent_error < thresh):
        return True
    else:
        return False
            

def get_edge_of_polygon_which_intersects_point_robust_assuming_there_is_an_intersection(the_poly,Px,graff=False):
    '''
       Precision issues make the intersection algorithm fail, so we
    '''

    L_edge_segment=get_edge_of_polygon_which_intersects_point(the_poly,Px,graff=graff)

    if L_edge_segment is None:
         L_edge_segment=get_edge_of_polygon_which_is_closest_to_intersection_point(the_poly,Px,graff=graff)

    return L_edge_segment
    
def get_edge_of_polygon_which_intersects_point(the_poly,Px,graff=False):
    '''
       L_edge_segment=get_edge_of_polygon_which_intersects_point(the_poly,Px)

       L_edge_segment is a LineString with only two points (a line
    '''
    the_boundary_as_linestring=the_poly.boundary
    the_line_segments=linestring_utils.split_linestring_into_linesegments(the_boundary_as_linestring)

    intersecting_line_segments=[]
    for line_segment_i in the_line_segments:
        if line_segment_i.intersects(Px):
            intersecting_line_segments.append(line_segment_i)

    if graff:
        plt.clf()
        fig = plt.figure(1)
            
        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        
        colors=plt.get_cmap('Dark2')
        color_count=0
        #plotting_utils2.plot_shapely_object(ax1,T1, colors(color_count))
        #color_count += 1
        
        #plotting_utils2.plot_shapely_object(ax1,the_poly,'green')
        #color_count += 1
        
        plotting_utils2.plot_shapely_object(ax1,Px,'darkgreen')
        color_count += 1
        
        for line_segment_i in the_line_segments:
            plotting_utils2.plot_shapely_object(ax1,line_segment_i,colors(color_count))
            color_count += 1
        plt.axis('equal')
        plt.title(inspect.currentframe().f_code.co_name)
        plt.show()
            
            
    if (len(intersecting_line_segments)==1):
        return intersecting_line_segments[0]

    elif (len(intersecting_line_segments)==0):
        #return get_edge_of_polygon_which_is_closest_to_intersection_point(the_poly,Px,graff)
        return None
    else:
        str=f"In " + inspect.currentframe().f_code.co_name
        str += f"len(intersecting_line_segments)= {len(intersecting_line_segments)}"        
        raise Exception(str)
    
    return None

def plot_line_segment_searching(the_poly,line_segment_i, the_line_segments, Px, d, i , N):
        assert(isinstance(the_line_segments,list))
        plt.clf()
        fig = plt.figure(1)

        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)

        colors=plt.get_cmap('Set1')
        color_count=0
        plotting_utils2.plot_shapely_object(ax1,line_segment_i,'red')
        color_count += 1

        #plotting_utils2.plot_shapely_object(ax1,the_poly,'green')
        #color_count += 1

        plotting_utils2.plot_shapely_object(ax1,Px,'blue')
        color_count += 1           

        for line_segment_j in the_line_segments:
            #            plotting_utils2.plot_shapely_object(ax1,line_segment_i,colors(color_count))
            plotting_utils2.plot_shapely_object(ax1,line_segment_j,'gray')
            #color_count += 1
            plt.axis('equal')

        plotting_utils2.plot_shapely_object(ax1,line_segment_i,'red')
        color_count += 1

        title_str=inspect.currentframe().f_code.co_name
        plt.title(f"{title_str} {i}/{N} d={d} ")
        #figure_utils.resize_figure()

        plt.show()


def get_edge_of_polygon_which_is_closest_to_intersection_point(the_poly,Px,graff=False):
    '''
       L_edge_segment=get_edge_of_polygon_which_intersects_point(the_poly,Px)

       L_edge_segment is a LineString with only two points (a line
    '''
    
    the_boundary_as_linestring=the_poly.boundary
    the_line_segments=linestring_utils.split_linestring_into_linesegments(the_boundary_as_linestring)


    list_of_records=list()
    for line_segment_i in the_line_segments:
        d_i=line_segment_i.distance(Px)
        record_i={"d_i":d_i, "line_segment_i": line_segment_i}
        list_of_records.append(record_i)
        if graff:
            N=len(the_line_segments)
            count=len(list_of_records)
            print(f"Px={Px} {count}/{N} d={d_i}, line_segment_i={line_segment_i.wkt}")
            plot_line_segment_searching(the_poly,line_segment_i, the_line_segments, Px,d_i,count,len(the_line_segments))              

    
    df_line_segments=pd.DataFrame(list_of_records)       
    #row_with_minimum_distance=df_line_segments[df_line_segments.d_i==df_line_segments.d_i.min()]
    
    #line_segment_min=row_with_minimum_distance["line_segment_i"][0]
    line_segment_min=pandas_conversion_utils.get_value_for_minimum_element(df_line_segments, key_for_minimum='d_i', key_to_return='line_segment_i')
      
    

    return line_segment_min


def get_endpoint_from_following_edge(the_poly,Px,v_direction_to_move,graff=False,verbosity=0):

    '''
       P_polygon_endpoint=get_endpoint_from_following_edge(the_poly,Px,v_direction_to_move,graff=False)

       
       We find an intesection at point Px
       we then want to follow the line segment and either
       return A or B, the trick here is the direction
       we prefer

                            | 
                            |   ---> v_direction_to_move
                            |
       A--------------------*-------------------------B
                            Px   

                             ---> v_line


       so we look at the dot product of v_direction_to_move and v_line



      Corner Case:
                                  ^
                                  |
                                  | v_direction_to_move
                        ____
       A--------------------*-------------------------B
                            Px   

                             ---> v_line

      

    '''
    
    #L_edge_segment=get_edge_of_polygon_which_intersects_point(the_poly,Px)

    #if L_edge_segment is None:
    L_edge_segment=get_edge_of_polygon_which_is_closest_to_intersection_point(the_poly,Px)

            
    list_of_points=shapely_utils.linestring_to_array_of_points(L_edge_segment)

    assert(len(list_of_points)==2)

    P1=list_of_points[0]
    P2=list_of_points[1]
    
    v1=vec2d.points_to_vec2d(Px,P1)
    v2=vec2d.points_to_vec2d(Px,P2)

    len1=vec2d.length(v1)
    len2=vec2d.length(v2)

    if len1==0:
        return Px

    if len2==0:
        return Px

    v1=vec2d.normalize_vec2d(v1)
    v2=vec2d.normalize_vec2d(v2)
    
    
    dot1=numpy.dot(v1,v_direction_to_move)
    dot2=numpy.dot(v2,v_direction_to_move)

    P_result=None
    
    if (dot1 > 0):
        P_result=P1
    elif ( dot2 > 0 ):
        P_result=P2
    else:
        if verbosity > 0:
            print(f"Px={Px}")
            print(f"P1={P1}")
            print(f"P2={P2}")
            print(f"len1={len1}")
            print(f"len2={len2}")

            print(f"v_direction_to_move={v_direction_to_move}")
            print(f"v1={v1}")
            print(f"v2={v2}")
            print(f"dot1={dot1}")
            print(f"dot2={dot2}")

            L12=LineString([P1,P2])
            L1=LineString([Px,P1])
            L2=LineString([Px,P2])

            f1=L1.length/L12.length
            f2=L2.length/L12.length

            print(f"L12.length={L12.length}")
            print(f"L1.length={L1.length}",end='')
            print(f"\tf1={f1}")
            print(f"L2.length={L2.length}",end='')
            print(f"\tf2={f2}")

            print(f"*** WARNING ***")
            print("In " + inspect.currentframe().f_code.co_name)
            print(f"no vectors have a dot product greater than 1 to  edge")
            msg=f"Neither line segment hase a dot product greater than 1 to movement direction"
            msg+=f"\n"
            msg+=f"direction to move vector is perpendicular to the line segments"
            print(msg)
            #raise Exception(f"no vectors have a dot product greater than 1 to  edge")
            #graff=True
    
    if graff:
        plt.clf()
        fig = plt.figure(1)
            
        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        
        colors=plt.get_cmap('Set1')
        color_count=0
        #plotting_utils2.plot_shapely_object(ax1,T1, colors(color_count))
        #color_count += 1
        
        plotting_utils2.plot_shapely_object(ax1,the_poly.exterior,'green')

        #plotting_utils2.plot_shapely_object(ax1,L_edge_segment,'blue')

        plotting_utils2.plot_point(ax1,Px,color='orange',symbol='x')
        
        C1='gray'
        C2='gray'
        S1='o'
        S2='o'
        
        if P_result==P1:
            C1='red'
            S1='x'
        if P_result==P2:
            C2='red'
            S2='x'
            
        plotting_utils2.plot_point(ax1,P1,color=C1,symbol=S1)
        plotting_utils2.plot_point(ax1,P2,color=C2,symbol=S2)

        #plotting_utils2.plot_shapely_object(ax1,P_result,'red',symbol='x')

        L1=LineString([Px,P1])
        #plotting_utils2.plot_shapely_object(ax1,L1,C1)
        L2=LineString([Px,P2])
        #plotting_utils2.plot_shapely_object(ax1,L2,C2)


        length_scale=min([L1.length,L2.length])
        v_arrow1=vec2d.points_to_vec2d(Px,P1)
        v_arrow1=vec2d.normalize_vec2d(v_arrow1)
        arrow_plotting_utils.plot_arrow(ax1, Px, v_arrow1, length_scale,color=C1, plot_reference_line=False)
        #plotting_utils2.plot_point(ax1,P1, 'blue','o')


        v_arrow2=vec2d.points_to_vec2d(Px,P2)
        v_arrow2=vec2d.normalize_vec2d(v_arrow2)
        arrow_plotting_utils.plot_arrow(ax1, Px, v_arrow2, length_scale,color=C2, plot_reference_line=False)


        v_arrow0=v_direction_to_move
        v_arrow0=vec2d.normalize_vec2d(v_arrow0)

        Px_back=point_utils.move_point_along_vector(Px, v_arrow0, -length_scale)
        #Px_back=Px
        arrow_plotting_utils.plot_arrow(ax1, Px_back, v_arrow0, length_scale,color="Black", plot_reference_line=False)

        
        # for line_segment_i in the_line_segments:
        #     plotting_utils2.plot_shapely_object(ax1,line_segment_i,colors(color_count))
        #     color_count += 1
        plt.axis('equal')
        plt.title(inspect.currentframe().f_code.co_name)
        plt.show()
    
    # if (dot1 > 0):
    #     return P1
    # elif ( dot2 > 0 ):
    #     return P2
    # else:
    #     print(f"Px={Px}")
    #     print(f"P1={P1}")
    #     print(f"P2={P2}")
    #     print(f"len1={len1}")
    #     print(f"len2={len2}")
            
    #     print(f"v_direction_to_move={v_direction_to_move}")
    #     print(f"v1={v1}")
    #     print(f"v2={v2}")
    #     print(f"dot1={dot1}")
    #     print(f"dot2={dot2}")

    #     L12=LineString([P1,P2])
    #     L1=LineString([Px,P1])
    #     L2=LineString([Px,P2])

    #     f1=L1.length/L12.length
    #     f2=L2.length/L12.length
        
    #     print(f"L12.length={L12.length}")
    #     print(f"L1.length={L1.length}",end='')
    #     print(f"\tf1={f1}")
    #     print(f"L2.length={L2.length}",end='')
    #     print(f"\tf2={f2}")

    #if P_result is None:
    #    msg=f"Neither line segment hase a dot product greater than 1 to movement direction"
    #    msg+=f"\n"
    #    msg+=f"direction to move vector is perpendicular to the line segments"
    #    raise Exception(msg)
    
    return P_result

    
    

