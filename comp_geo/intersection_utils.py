#!/usr/bin/python3

########################
import inspect

# import pad
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import *

from comp_geo import linestring_utils
from comp_geo import list_line
from comp_geo import plotting_utils2
from comp_geo import point_utils
from comp_geo import shapely_utils
from csd import pandas_conversion_utils


############# starting trace


#import display_layout

def does_new_trace_intersect_traces_or_other_pixels(wide_trace,geo_filtered,pixel_no):

        

        traces_p_as_polys=pandas_conversion_utils.get_column_of_dataframe_which_is_not_none(geo_filtered.df_traces_n,'trace_i_as_polys')
        
        does_intersect_traces=does_trace_intersect_any_of_list_of_objects(wide_trace, traces_p_as_polys)

        ## we can short circuit pixels
        if does_intersect_traces:
                return True
        
        not_this_pixel=geo_filtered.df_pixels['pixel_no'] != pixel_no
        other_tes=geo_filtered.df_pixels['tes_i'][not_this_pixel].to_list()
        does_intersect_tes=does_trace_intersect_any_of_list_of_objects(wide_trace, other_tes)
        
        does_intersect=does_intersect_tes or does_intersect_traces
        
        return does_intersect

################################################################
#
#
# does_trace_intersect_any_of_objects(trace_i, all_objects):
#
#
#
################################################################

# def does_trace_intersect_any_of_objects(trace_i, all_objects):
#     if isinstance(all_objects,list):
#         #return does_trace_intersect_any_of_list_of_objects_multipolygon(trace_i, all_objects)
#         return does_trace_intersect_any_of_list_of_objects(trace_i, all_objects)
#     elif isinstance(all_objects,dict):
#         return does_trace_intersect_any_of_dict_of_objects(trace_i, all_objects)
#     else:
#        raise(f"Unhandled type - {type(obj)}")
   
#def does_trace_intersect_any_of_list_of_objects_skip_index(trace_i, all_tes, i_skip):
#     sub_list = [x for i,x in all_tes.items() if i!=i_skip]
#     return does_trace_intersect_any_of_list_of_objects(trace_i, sub_list)

# def does_trace_intersect_any_of_dict_of_objects_skip_index(trace_i, all_objects,i_skip):
#     #    assert(isinstance(all_objects,dict))

#     for pixel_no,obj in all_objects.items():
#         if ((pixel_no != i_skip) and trace_i.intersects(obj)):
#             return True
#     return False

def does_trace_intersect_any_of_list_of_objects(trace_i, all_objects: list):
    assert(trace_i is not None)
    assert(isinstance(all_objects,list))

    try:
      mp=MultiPolygon(all_objects)
      return trace_i.intersects(mp)
    except:    
      return does_trace_intersect_any_of_list_of_objects_overlapping(trace_i,all_objects)

def does_trace_intersect_any_of_list_of_objects_overlapping(trace_i, all_objects):
    assert(trace_i is not None)
    assert(isinstance(all_objects,list))
           
    for obj_i in all_objects:
        if obj_i is not None:
                if trace_i.intersects(obj_i):
                        return True
    return False

# def does_trace_intersect_any_of_dict_of_objects(trace_i, all_objects):
#     assert(isinstance(all_objects,dict))
#     for obj_i in all_objects.values():
#         if trace_i.intersects(obj):
#             return True
#     return False


# def get_all_intersections_multipolygon(trace_i, all_objects):
#     mp=MultiPolygon(all_objects)
#     return trace_i.intersection(mp)


###
###  This will fail if the polgons overlap to make a non-trivial multipolygon
###
###
###
### returns an empty list on no intersection
def get_all_intersections_as_points(trace_i, all_objects,verbosity=0):

    assert(isinstance(trace_i,LineString) or isinstance(trace_i,Polygon))
    try:
        return get_all_intersections_as_points_nonoverlapping(trace_i, all_objects,verbosity)
    except:
        if verbosity > 0:    
                print(f"###############################################")
                print(f"Warning overlapped objects in intersection")
                print(f"Going to slower algorithm")
                print(f"###############################################")
        return get_all_intersections_as_points_overlapping(trace_i, all_objects,verbosity)
        
def get_all_intersections_as_points_nonoverlapping(trace_i, all_objects,verbosity):
    if verbosity >9:
        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        print("In " + inspect.currentframe().f_code.co_name)

       
     
    mp=MultiPolygon(all_objects)
    all_trace_intersections=trace_i.intersection(mp)
    all_points=shapely_utils.shapely_object_to_array_of_points(all_trace_intersections)

    #import pdb;
    #pdb.set_trace()
    
    if verbosity >9:
            print(f"type(all_trace_intersections)={type(all_trace_intersections)}")
            print(f"all_points={all_points}")
 
    if verbosity==10:
        plt.clf()
        fig = plt.figure(1)
        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        plotting_utils2.plot_shapely_object(ax1, all_objects,'b')
        plotting_utils2.plot_shapely_object(ax1, trace_i,'g')
        plotting_utils2.plot_shapely_object(ax1, all_points,'r')
        #plotting_utils2.plot_shapely_object(ax1, Pa,'g')
        ax1.axis('equal')
        ax1.set_title(inspect.currentframe().f_code.co_name)
        plt.draw()
        plt.pause(0.1)
        plt.show()


    if all_points is None:
            all_points=list()
            
    return all_points


# def get_all_intersections_as_points_slow1(trace_i, all_objects):
#     assert(isinstance(all_objects,list))

#     all_points=list()
#     for obj_i in all_objects:
#         polygon_i=trace_i.intersection(obj_i)
#         points_i=shapely_utils.shapely_object_to_array_of_points(polygon_i)
#         all_points += points_i

#     return list(filter(None,all_points))

def get_all_intersections_as_points_overlapping(trace_i, all_objects,verbosity):
        
    
    assert(isinstance(trace_i,LineString) or isinstance(trace_i,Polygon))
     
    if verbosity >9:
        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        print("In " + inspect.currentframe().f_code.co_name)

       
    all_points=list()
    for obj_i in all_objects:
        polygon_i=trace_i.intersection(obj_i)
        if verbosity >9:
                print(f"type(polygon_i)={type(polygon_i)}")
                print(f"polygon_i={polygon_i}")
                
        points_i=shapely_utils.shapely_object_to_array_of_points(polygon_i)
        all_points.append(points_i)

    # convert list of list to a flat list
    flat_list = [item for sublist in all_points for item in sublist]     
        
    if verbosity>=10:
        plt.clf()
        fig = plt.figure(1)
        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        plotting_utils2.plot_shapely_object(ax1, all_objects,'b')
        plotting_utils2.plot_shapely_object(ax1, trace_i,'g')
        plotting_utils2.plot_shapely_object(ax1, all_points,'r')
        #plotting_utils2.plot_shapely_object(ax1, Pa,'g')
        ax1.axis('equal')
        ax1.set_title(inspect.currentframe().f_code.co_name)
        plt.draw()
        plt.pause(0.1)
        plt.show()
    
   
    return flat_list

def get_all_intersections_as_df(trace_i, all_objects,verbosity=0):
        
    assert(isinstance(all_objects,list))
    
    if verbosity >9:
        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        print("In " + inspect.currentframe().f_code.co_name)

    #df_pixel_coords = pd.DataFrame(columns=["Pi","poly_i"])

    list_of_records=[]


    for obj_i in all_objects:
        poly_i=trace_i.intersection(obj_i)
            
    #    try:
    #            poly_i=trace_i.intersection(obj_i)
    #    except Exception as e:
    #
    #            print(e)
    #            #import os
    #            #import inspect
    #            s=os.path.basename(__file__) + "."
    #            s+= inspect.currentframe().f_code.co_name
    #            print(f"WARNING: ################## In {s} ")
    #            print(f"Caught exception {e}")
    #            poly_i=None
    #        #raise(e)



            
     #   if poly_i is None:
     #            pass
        if verbosity >9:
                print(f"type(poly_i)={type(poly_i)}")
                print(f"poly_i={poly_i}")
                
        points_i=shapely_utils.shapely_object_to_array_of_points(poly_i)

        for point_i in points_i:
                record_i={"Pi":point_i, "obj_i": obj_i}
                list_of_records.append(record_i)

    df_pixel_coords=pd.DataFrame(list_of_records)

    
   
    return df_pixel_coords

def get_closest_intersection_per_object_as_df(trace_i, all_objects, use_last_intersection=True, sort_order_ascending=False, verbosity=0):
        
    assert(isinstance(all_objects,list))
    
    if verbosity >9:
        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        print("In " + inspect.currentframe().f_code.co_name)

    #df_pixel_coords = pd.DataFrame(columns=["Pi","poly_i"])

    list_of_records=[]
    
    list_of_points=shapely_utils.linestring_to_array_of_points(trace_i)
    if use_last_intersection:
        P_endpoint=list_of_points[-1]
    else:
        P_endpoint=list_of_points[0]


            
    for obj_i in all_objects:
        poly_i=trace_i.intersection(obj_i)
        if verbosity >9:
                print(f"type(poly_i)={type(poly_i)}")
                print(f"poly_i={poly_i}")
                
        points_of_intersection=shapely_utils.shapely_object_to_array_of_points(poly_i)

        P_closest_point_of_intersection=point_utils.get_closest_point_in_list(P_endpoint,points_of_intersection)

        if P_closest_point_of_intersection is not None:
                distance_i=P_endpoint.distance(P_closest_point_of_intersection)
                
                record_i={"distance_i":distance_i, "Pi": P_closest_point_of_intersection, "obj_i": obj_i}
                list_of_records.append(record_i)

        

    df_pixel_coords=pd.DataFrame(list_of_records)
    #assert(len(df_pixel_coords) > 0)
    if len(df_pixel_coords) > 0:
            df_pixel_coords.sort_values('distance_i', ascending=sort_order_ascending, inplace=True)
    

    return df_pixel_coords

def split_line_at_intersection_point_with_objects(list_of_points,all_objects,use_last_intersection=True, graff=True):
        '''
             will chop a line into two parts before and after the last intersection between
             the line and a list of objects.

             the last intersection point is based on the closest point routine
                                                   _______
                                    ____          |       |
                                   |    |         |       |
                  A----------------*----*---------*-------C--------B
                                   |____|         |_______|

               will split L_AB--> [L_AC, L_CB]

        '''
        
        L_full=LineString(list_of_points)

        #points_of_intersection=get_all_intersections_as_points(L_full,all_objects)


        poi_df=get_all_intersections_as_df(L_full,all_objects)
        list_of_points=list(poi_df['Pi'])
        ########################################################
        #
        # the trace should intersect the h_street at many points
        # we will 
        #
        ########################################################

        if use_last_intersection:
                P_endpoint=list_of_points[-1]
        else:
                P_endpoint=list_of_points[0]

        #P_closest_point_of_intersection=point_utils.get_closest_point_in_list(P_endpoint,points_of_intersection)
        P_closest_point_of_intersection=point_utils.get_closest_point_in_list(P_endpoint,list_of_points)



        if graff:
          plt.clf()
          colors=plt.get_cmap('Set1')
          fig = plt.figure(1)

          ### subplot nrows, ncols, plot #
          ax1 = fig.add_subplot(111)

          plotting_utils2.plot_shapely_object(ax1,L_full, 'blue')
          plotting_utils2.plot_shapely_object(ax1,list_of_points, 'green')
          plotting_utils2.plot_shapely_object(ax1,P_closest_point_of_intersection, 'red')

          # colors=plt.get_cmap('Set1')
          # color_count=0
          # for i, x_i in enumerate(the_two_lines_as_geometry_collection):
          #     print(f"i={i} = ",end='')
          #     print(f"x={x_i}")
          #     L_i=the_two_lines_as_geometry_collection[0]
          #     plotting_utils2.plot_shapely_object(ax1, L_i, colors(color_count))
          #     color_count += 1
          plt.axis('equal')
          plt.show()
                  
        
        ########################################################
        #
        # Now we are going to watch the the trace should intersect the h_street at many points
        # we will 
        #
        ########################################################

        [list_of_points1, list_of_points2]=linestring_utils.split_line_at_point(list_of_points,P_closest_point_of_intersection)

        return [list_of_points1,list_of_points2]

def trim_linestring_at_edge_of_boundary(the_linestring,the_boundary,graff=False):
        L1=list_line.linestring_to_listline(the_linestring)
        L2=trim_listline_at_edge_of_boundary(L1,the_boundary,graff)
        return L2.to_LineString()
        
def trim_listline_at_edge_of_boundary(L1,the_boundary,graff=False):
        assert(isinstance(L1,list_line.ListLine))
        
        objects=[the_boundary.boundary]
        points_of_intersection=L1.get_all_intersections_as_points(objects)

        if len(points_of_intersection) > 0:
                P_split=points_of_intersection[0]    
                [La, Lb]=L1.split_at_point(P_split,graff=False)
        else:
                La=L1
                Lb=None
        if graff:
                plt.clf()
                fig = plt.figure(1)

                ### subplot nrows, ncols, plot #
                ax1 = fig.add_subplot(121)
                
                plotting_utils2.plot_shapely_object(ax1, L1,'green')
                plotting_utils2.plot_shapely_object(ax1,P_split, 'red')
                plotting_utils2.plot_shapely_object_reference(ax1, the_boundary.boundary,'black')
                plt.axis('equal')
        
                ax2 = fig.add_subplot(122)
                plotting_utils2.plot_shapely_object(ax2, La,'red')
                plotting_utils2.plot_shapely_object(ax2, Lb,'gray')
                plotting_utils2.plot_shapely_object(ax2,P_split, 'red')
                plotting_utils2.plot_shapely_object_reference(ax2, the_boundary.boundary,'black')
                
                plt.axis('equal')     
                plt.show()
    
        
        return La

######################################################
#
#
# main
#  
#
#######################################################
if __name__ == '__main__':

    print("__________________________________")
