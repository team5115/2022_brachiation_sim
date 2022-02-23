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
from csd import arrow_plotting_utils
#import geometry_utils3
from comp_geo import intersection_of_line_segments

############################################################
#
# --------D----------------------
#
#
#        Pa
#         *
#         |    
# line_a  |  V_direction  
#         |
#        \|/  
#   
#
#
#
# ---------c---------------------------
#
# a square boundary will have 4 sides or line segments
# a vertical extension will be parallel to 2 of these so no intersection
# it will intersect 2 of these (top and bottom)
# we calculate the intersection of the two infinte lines made from the boundary
# line segment and the direction vector
# the intersection that is parallel to the direction vector
#
#
#
############################################################
def extend_line_to_boundary(the_line,v_direction,boundary_escape):
    Pa=get_last_point_of_linestring(the_line)
    Pc=get_intersection_point_on_boundary_from_point_and_direction(Pa,v_direction,boundary_escape)
    new_trace=append_point_to_linestring(the_line,Pc)
    return new_trace

def create_line_to_boundary(Pa,v_direction,boundary_escape):
    verbosity=0
    Pc=get_intersection_point_on_boundary_from_point_and_direction(Pa,v_direction,boundary_escape)
    if verbosity > 8:
        print("In " + inspect.currentframe().f_code.co_name)
        print("Pa ", end='')
        pretty_print_geometry(Pa)
        if (Pc==None):
            print("Pc ", end='')
            pretty_print_geometry(Pc)
        else:
            print("Pc ", end='')
            pretty_print_geometry(Pc)        
        print(f"\t v_direction={v_direction}")
    return LineString([Pa,Pc])

# TODO: V2 solves for 45 degrees, but doesn't give parallel lines
#       V1 gives parallel lines but misses non ortho boundaries
#       
def get_intersection_point_on_boundary_from_point_and_direction(Pa,v_direction,boundary_escape,choose_first=True, verbosity=0, graff=False):
    # P3=get_intersection_point_on_boundary_from_point_and_direction_v3(Pa,v_direction, boundary_escape, choose_first, verbosity,graff)

    # P2=get_intersection_point_on_boundary_from_point_and_direction_v2(Pa,v_direction, boundary_escape, choose_first, verbosity,graff)
    P1=get_intersection_point_on_boundary_from_point_and_direction_v1(Pa,v_direction, boundary_escape, choose_first, verbosity,graff)

    # if (P1 is not None) and (P2 is not None) and (P3 is not None):
    #     #print("In " + inspect.currentframe().f_code.co_name,end="")
    #     # print(f" P1={P1}",end="")
    #     # print(f" P2={P2}",end="")
    #     # print(f" P3={P3}",end="")

    #     dx23=P2.x-P3.x
    #     dy23=P2.y-P3.y
    #     dist23=P2.distance(P3)

    #     dx21=P2.x-P1.x
    #     dy21=P2.y-P1.y
    #     dist21=P2.distance(P1)

    #     if dist21 > 1e-9:
    #         print("__________________________________________________________")
    #         print(f" P1={P1}")
    #         print(f" P2={P2}")
    #         print(f" P3={P3}")
    #         print(f"\t")


    #         print(f"")
    #         print(f" 2 vs 3")
    #         print(f" dist23={round(dist23,9)}",end="")
    #         print(f" dy23={round(dy23,9)}",end="")
    #         print(f" dx23={round(dx23,9)}",end="")

    #         print(f"")
    #         print(f" 2 vs 1")
    #         print(f" dist12={round(dist21,9)}",end="")
    #         print(f" dy12={round(dy21,9)}",end="")
    #         print(f" dx12={round(dx21,9)}",end="")
    
    # else:
    #     #print("In " + inspect.currentframe().f_code.co_name,end="")
    #     print(f" P1={P1}",end="")
    #     print(f" P2={P2}",end="")
    #     print(f" P3={P3}",end="")
    return P1

# def get_intersection_point_on_boundary_from_point_and_direction_v3(Pa,v_direction,boundary_escape,choose_first=True, verbosity=0, graff=False):
#     return geometry_utils3.get_intersection_point_on_boundary_from_point_and_direction_v3(Pa,v_direction, boundary_escape, choose_first, verbosity,graff)
    
# def get_intersection_point_on_boundary_from_point_and_direction_v2(Pa,v_direction,boundary_escape,choose_first=True, verbosity=0, graff=False):
#     return geometry_utils2.get_intersection_point_on_boundary_from_point_and_direction_v2(Pa,v_direction, boundary_escape, choose_first, verbosity,graff)

# def get_intersection_point_on_boundary_from_point_and_direction_v3(Pa,v_direction,boundary_escape,choose_first=True, verbosity=0, graff=False):
#     return geometry_utils3.get_intersection_point_on_boundary_from_point_and_direction_v3(Pa,v_direction, boundary_escape, choose_first, verbosity,graff)


 
def get_intersection_point_on_boundary_from_point_and_direction_v1(Pa,v_direction,boundary_escape,choose_first=True, verbosity=0, graff=False):
    #verbosity=10
    line_ab=point_and_vec2d_to_linestring(Pa,v_direction)
    Pb=get_last_point_of_linestring(line_ab)
    
    intersection_points=list()    

    boundary_escape_as_line_segments=polygon_exterior_to_array_of_linestrings(boundary_escape)
    for i,boundary_segment in enumerate(boundary_escape_as_line_segments):
        #Pc=intersection_of_line_segments.intersection_of_last_segments_of_infinite_lines_v1(line_ab,boundary_segment)
        #Pc=intersection_of_line_segments.intersection_of_last_segments_of_infinite_lines_v2(line_ab,boundary_segment)
        Pc=intersection_of_line_segments.intersection_of_last_segments_of_infinite_lines_v3(line_ab,boundary_segment)

        #point_good=False
        if Pc is not None:
            vec_bc=vec2d.points_to_normalized_vec2d(Pb,Pc)
            is_parallel=vec2d.are_vectors_parallel(v_direction,vec_bc)
            #is_antiparallel=vec2d.are_vectors_antiparallel(v_direction,vec_bc)
            if (is_parallel):
                if (choose_first):
                    if graff:
                        plt.clf()
                        fig = plt.figure(1)
                        ### subplot nrows, ncols, plot #
                        ax1 = fig.add_subplot(111)

                        #### let's get a length scale so we can see the vector
                        L1=LineString([Pa,Pc])
                        l=L1.length

                        ### draw direction vectors
                        L_escape=point_and_vec2d_to_linestring(Pa,v_direction,length=l/3)
                        
                        plotting_utils2.plot_shapely_object(ax1, boundary_escape.exterior,'b')
                        plotting_utils2.plot_shapely_object(ax1, Pa,'g')
                        plotting_utils2.plot_shapely_object(ax1, Pc,'r')
                        plotting_utils2.plot_shapely_object(ax1, L_escape,'orange')
                        ax1.axis('equal')
                        plt.draw()
                        plt.pause(0.1)
                        plt.show()
                    return Pc
                #point_good=True
                intersection_points.append(Pc)
                
        if verbosity > 8:
            print("")
            print(f"Segment {i}", end='')
            pretty_print_geometry(boundary_segment)
            print(f"\t v_direction={v_direction}")
            print(f"\t Point found: ",end='')
            if Pc is None:
                print("None")
            else:
                pretty_print_geometry(Pc)
                print(f"\t is_parallel={is_parallel}")
                #print(f"\t is_antiparallel={is_antiparallel}")
            #print(f"\t point_good={point_good}")
            print("")
            #pretty_print_geometry_array(intersection_points,"intersection_points")
              
    if (verbosity > 8):
        print("--------------Loop Done--------------------------------------")
        print(f"len(intersection_points)={len(intersection_points)}")
        pretty_print_geometry_array(intersection_points,"intersection_points")

    if graff:
        plt.clf()
        fig = plt.figure(1)
        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        plotting_utils2.plot_shapely_object(ax1, boundary_escape.exterior,'b')
        plotting_utils2.plot_shapely_object(ax1, Pa,'g')
        for Pi in intersection_points:
            plotting_utils2.plot_shapely_object(ax1, Pi,'r')
        ax1.axis('equal')
        plt.draw()
        plt.pause(0.1)
        #plt.show()

    # if graff:
    #     plt.clf()
    #     fig = plt.figure(1)

    #     ### subplot nrows, ncols, plot #
    #     ax1 = fig.add_subplot(111)

    #     plotting_utils2.plot_shapely_object_reference(ax1, the_escape_boundary.exterior,'green')
    #     plotting_utils2.plot_shapely_object(ax1,P1, 'black')
    #     plotting_utils2.plot_shapely_object(ax1,list_of_points, 'red','x')
        
    #     plt.axis('equal')
    #     title_str=inspect.currentframe().f_code.co_name
    #     plt.title(title_str)
    #     plt.show()

    if (len(intersection_points)==1):
        return intersection_points[0]
    else:
        print("##################################################################")
        print("In " + inspect.currentframe().f_code.co_name)
        print("Pa=",end="")
        pretty_print_geometry(Pa)
        print("v_direction=",end="")
        print(v_direction)
        print("boundary_escape=",end="")
        pretty_print_geometry(boundary_escape.exterior)
        print("--------------No intersection points found--------------------------------------")
        print("--------------No intersection points found--------------------------------------")
        pretty_print_geometry_array(intersection_points,"intersection_points")        
        str=f"len(intersection_points)={len(intersection_points)}"
        print(str)
        sys.stdout.flush()
        return None        
        #raise Exception(intersection_points)

    



# def intersection_of_last_segments_of_infinite_lines_v1(line1,line2):

#     #assert(isinstance(line1,list))
#     #sassert(isinstance(line2,list))

#     assert(isinstance(line1,LineString))
#     assert(isinstance(line2,LineString))

#     assert(len(line1.coords)==2)
#     assert(len(line2.coords)==2)
    
#     (line1_P1,line1_P2)=line1.coords[-2:]
#     (line2_P1,line2_P2)=line2.coords[-2:]
    
#     # Line1
#     A1 = line1_P2[1] - line1_P1[1];
#     B1 = line1_P2[0] - line1_P1[0];
#     C1 = A1*line1_P1[0] + B1*line1_P1[1];

#     A2 = line2_P2[1] - line2_P1[1];
#     B2 = line2_P2[0] - line2_P1[0];
#     C2 = A2*line2_P1[0] + B2*line2_P1[1];

#     det = A1*B2 - A2*B1;

#     if det==0:
#         return None #parallel lines
#     else:
#         x = (B2*C1 - B1*C2)/det;
#         y = (A1 * C2 - A2 * C1) / det;
#         return Point(x,y)

    
def get_intersection_point_on_line_segment_from_point_and_direction_v1(Pa,v_direction,the_line_segment,choose_first=True, verbosity=0, graff=False):
    #verbosity=10
    line_ab=point_and_vec2d_to_linestring(Pa,v_direction)
    Pb=get_last_point_of_linestring(line_ab)
    
    intersection_points=list()    
    Pc=intersection_of_line_segments.intersection_of_last_segments_of_infinite_lines_v3(line_ab,the_line_segment)



    return Pc    
        
    # #point_good=False
    # if Pc is not None:
    #     vec_bc=vec2d.points_to_normalized_vec2d(Pb,Pc)
    #     is_parallel=vec2d.are_vectors_parallel(v_direction,vec_bc)
    #     #is_antiparallel=vec2d.are_vectors_antiparallel(v_direction,vec_bc)
    #     if (is_parallel):
    #             if (choose_first):
    #                 if graff:
    #                     plt.clf()
    #                     fig = plt.figure(1)
    #                     ### subplot nrows, ncols, plot #
    #                     ax1 = fig.add_subplot(111)

    #                     #### let's get a length scale so we can see the vector
    #                     L1=LineString([Pa,Pc])
    #                     l=L1.length

    #                     ### draw direction vectors
    #                     L_escape=point_and_vec2d_to_linestring(Pa,v_direction,length=l/3)
                        
    #                     plotting_utils2.plot_shapely_object(ax1, boundary_escape.exterior,'b')
    #                     plotting_utils2.plot_shapely_object(ax1, Pa,'g')
    #                     plotting_utils2.plot_shapely_object(ax1, Pc,'r')
    #                     plotting_utils2.plot_shapely_object(ax1, L_escape,'orange')
                  

    #                     ax1.axis('equal')
    #                     plt.draw()
    #                     plt.pause(0.1)
    #                     plt.show()
    #                 return Pc
    #             #point_good=True
    #             intersection_points.append(Pc)
                
    #     if verbosity > 8:
    #         print("")
    #         print(f"Segment {i}", end='')
    #         pretty_print_geometry(boundary_segment)
    #         print(f"\t v_direction={v_direction}")
    #         print(f"\t Point found: ",end='')
    #         if Pc is None:
    #             print("None")
    #         else:
    #             pretty_print_geometry(Pc)
    #             print(f"\t is_parallel={is_parallel}")
    #             #print(f"\t is_antiparallel={is_antiparallel}")
    #         #print(f"\t point_good={point_good}")
    #         print("")
    #         #pretty_print_geometry_array(intersection_points,"intersection_points")
              
    # if (verbosity > 8):
    #     print("--------------Loop Done--------------------------------------")
    #     print(f"len(intersection_points)={len(intersection_points)}")
    #     pretty_print_geometry_array(intersection_points,"intersection_points")

    # if graff:
    #     plt.clf()
    #     fig = plt.figure(1)
    #     ### subplot nrows, ncols, plot #
    #     ax1 = fig.add_subplot(111)
    #     plotting_utils2.plot_shapely_object(ax1, the_line_segment,'b')
    #     plotting_utils2.plot_shapely_object(ax1, Pa,'g')
    #     for Pi in intersection_points:
    #         plotting_utils2.plot_shapely_object(ax1, Pi,'r')

    #     Px=Pa
    #     length_scale=the_line_segment.length/5
        
    #     Px2=arrow_plotting_utils.plot_arrow(ax1,Px,v_direction,length_scale,color='red',plot_reference_line=False)
    #     ax1.axis('equal')
    #     plt.draw()
    #     plt.pause(0.1)
    #     #plt.show()

    # # if graff:
    # #     plt.clf()
    # #     fig = plt.figure(1)

    # #     ### subplot nrows, ncols, plot #
    # #     ax1 = fig.add_subplot(111)

    # #     plotting_utils2.plot_shapely_object_reference(ax1, the_escape_boundary.exterior,'green')
    # #     plotting_utils2.plot_shapely_object(ax1,P1, 'black')
    # #     plotting_utils2.plot_shapely_object(ax1,list_of_points, 'red','x')
        
    # #     plt.axis('equal')
    # #     title_str=inspect.currentframe().f_code.co_name
    # #     plt.title(title_str)
    # #     plt.show()

    # if (len(intersection_points)==1):
    #     return intersection_points[0]
    # else:
    #     print("##################################################################")
    #     print("In " + inspect.currentframe().f_code.co_name)
    #     print("Pa=",end="")
    #     pretty_print_geometry(Pa)
    #     print("v_direction=",end="")
    #     print(v_direction)
    #     print("boundary_escape=",end="")
    #     pretty_print_geometry(the_line_segment)
    #     print("--------------No intersection points found--------------------------------------")
    #     print("--------------No intersection points found--------------------------------------")
    #     pretty_print_geometry_array(intersection_points,"intersection_points")        
    #     str=f"len(intersection_points)={len(intersection_points)}"
    #     print(str)
    #     sys.stdout.flush()
    #     return None        
    #     #raise Exception(intersection_points)

    


