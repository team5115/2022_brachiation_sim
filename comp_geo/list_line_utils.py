import list_line
import vec2d
import math
import numpy as np
import matplotlib.pyplot as plt
import copy
import sys
import config_params
import vec2d
import geometry_utils
import point_utils
import linestring_utils
import shapely
import intersection_utils
import polygon_utils
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.ops import nearest_points
from shapely.geometry import MultiPoint
# mp = MultiPoint(route)
# print nearest_points(mp, end)[0]
import plotting_utils2
import chamfer_utils
from csd import pandas_conversion_utils
import shapely_utils
import inspect
from csd import arrow_plotting_utils
import figure_utils

def extend_listline_to_point_and_contour_trace(L1, P_target, object_list, v_escape, dr_escape, v_strafe, dr_strafe, stitch_trace_width, graff=False,verbosity=0):


    assert(isinstance(L1,list_line.ListLine))
    
    loop_count=0



    while (True):



        loop_count += 1

        if loop_count > 300:
            raise Exception(f"Exceeeded loop_count In " + inspect.currentframe().f_code.co_name)

        if verbosity > 3:
            print("")
            print("=====================================================")
            print("In " + inspect.currentframe().f_code.co_name,end='')
            print(f" loop_count= {loop_count}")
            print(f" selfloop_count= {loop_count}")

            #print(f"L1.intersects(the_boundary)={L1.intersects(the_boundary)}")
            print(f"L1.length()={L1.length()}")
            #print(f"L1.data={L1.data}")

            sys.stdout.flush()


        P1=L1.get_last_point()
        P2=P_target

        #v_escape=vec2d.points_to_vec2d(P1,P2)
        #v_strafe=vec2d.points_to_vec2d(P1,P2)

        L1.extend_line_to_new_point(P_target)

        ## keep copies only if graphing so we can show steps
        # if graff:
        #     data1=copy.deepcopy(L1.data)



        #if verbosity > 8:
        #    sub_graff=True
        #else:
        #    sub_graff=False
        sub_graff=False    
        [ is_trimmed, P_closest_intersection, P_polygon_endpoint]=L1.trim_line_at_first_intersection_point_and_follow_boundary(object_list, dr_escape, v_strafe, dr_strafe, graff=sub_graff)

        ###########################################################################
        #
        #
        #
        ##########################################################################
        #if (len(list_of_intersecting_objects) > 1):
        # if graff:
        #     colors=plt.get_cmap('Set1')
        #     plt.clf()
        #     fig = plt.figure(1)
        #     ### subplot nrows, ncols, plot #
        #     ax1 = fig.add_subplot(111)
        #     plotting_utils2.plot_shapely_object(ax1,L1.to_LineString(),'green')
        #     plotting_utils2.plot_shapely_object(ax1,object_list, 'blue','o')
        #     #plotting_utils2.plot_shapely_object(ax1,points_of_intersection, 'orange','o')
        #     plotting_utils2.plot_point(ax1,P_closest_intersection, 'red','x')
        #     plotting_utils2.plot_point(ax1,P_polygon_endpoint, 'green','x')


        #     #object_list=list_of_intersecting_objects
        #     #the_intersecting_poly=list_of_intersecting_objects[0]
        #     #L1.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection, P_closest_intersection)
        #     title_str = f""
        #     title_str += f" L1.length()={L1.length()}"
        #     title_str += f"{inspect.currentframe().f_code.co_name}"
        #     title_str += f" GRAFF #1"
        #     plt.axis('equal')
        #     plt.title(title_str)
        #     #lt.show()
        #     plt.show()
        #     # if True:


        ######################################################################
        ##
        ## we found an intersection and are following this to the edge of the object
        ## if another object is above this one we will collide with it, so
        ## we need to check for collisions after the extension is made
        ## if there is a collision we return false
        ##
        ##
        ### check for intersection that happened due to the extension
        try:
            
            wide_trace_i=L1.to_wide_trace(stitch_trace_width)
            #is_intersecting=L1.intersects(MultiPolygon(object_list))
            #is_intersecting=L1.intersects_any_of_list_of_objects(object_list)


            is_intersecting=intersection_utils.does_trace_intersect_any_of_list_of_objects(wide_trace_i, object_list)
            #is_intersecting=False
        except:
            print("In " + inspect.currentframe().f_code.co_name)
            print(f"Geometry problem on intersects")
            print(f"THIS PROBABLY NEEDS TO BE FIXED")

            sys.stdout.flush()
            is_intersecting=True

            # if False:
            #     #data3=copy.deepcopy(L1.data)
            #     #data3=L1.data
            #     #L1.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection, P_closest_intersection)


            #     print("____________________________________________________")
            #     print("In " + inspect.currentframe().f_code.co_name)
            #     print(f"L1.length()={L1.length()}")
            #     print(f"L1.data={L1.data}")
            #     #is_intersecting=L1.intersects(object_list)
            #     print(f"is_intersecting={is_intersecting}")                
            #     sys.stdout.flush()

            #     if True:
            #         plt.clf()
            #         fig = plt.figure(1)

            #         ### subplot nrows, ncols, plot #
            #         ax1 = fig.add_subplot(111)
            #         plotting_utils2.plot_shapely_object(ax1,object_list,'green')
            #         plotting_utils2.plot_shapely_object(ax1, L1.to_LineString(),'red')


            #         title_str = f""
            #         title_str += f"Geo Problem "
            #         #title_str += f" L1.length()={L1.length()}"
            #         title_str += f"{inspect.currentframe().f_code.co_name}"
            #         #title_str += f" GRAFF #2"
            #         plt.axis('equal')
            #         plt.title(title_str)
            #         #lt.show()
            #         plt.show()
            #         #plt.draw()
            #         plt.pause(0.0001)


            

        if graff:
            #data3=copy.deepcopy(L1.data)
            #data3=L1.data
            #L1.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection, P_closest_intersection)


            print("____________________________________________________")
            print("In " + inspect.currentframe().f_code.co_name)
            print(f"L1.length()={L1.length()}")
            print(f"L1.data={L1.data}")
            #is_intersecting=L1.intersects(object_list)
            print(f"is_intersecting={is_intersecting}")                
            sys.stdout.flush()

            plt.clf()
            fig = plt.figure(1)

            ### subplot nrows, ncols, plot #
            ax1 = fig.add_subplot(111)
            plotting_utils2.plot_shapely_object(ax1,object_list,'green')
            plotting_utils2.plot_point(ax1,P_target,'red',symbol="x")
            #plotting_utils2.plot_shapely_object_reference(ax1, L1.to_LineString(),'yellored','x')
            plotting_utils2.plot_shapely_object(ax1, L1.to_LineString(),'red')
            # plotting_utils2.plot_shapely_object(ax1, LineString(old_data),'red')

            #if len(data1) > 1:
            #plotting_utils2.plot_shapely_object_reference(ax1, LineString(data1),'lightblue')
            # plotting_utils2.plot_shapely_object(ax1, LineString(data2),'yellow')
            # plotting_utils2.plot_shapely_object(ax1, LineString(data3),'orange')

            # plotting_utils2.plot_shapely_object(ax1, P_closest_intersection,'red','x')
            # plotting_utils2.plot_shapely_object(ax1, P_polygon_endpoint,'red','o')

            #plt.draw()
            #plt.pause(0.0001)

            title_str = f""
            title_str += f" L1.length()={L1.length()}"
            title_str += f"{inspect.currentframe().f_code.co_name}"
            title_str += f" GRAFF #2"
            plt.axis('equal')
            plt.title(title_str)
            #lt.show()
            #plt.show()
            #plt.draw()
            plt.pause(0.0001)

        if is_intersecting:
            return False

    
        if not is_trimmed:
            return True

def extend_listline_to_point_and_manhattan_trace(L1, P_target, object_list, v_escape, dr_escape, v_strafe, dr_strafe, stitch_trace_width, graff=False,verbosity=0):


    assert(isinstance(L1,list_line.ListLine))
    
    loop_count=0


    direction_vector_is_escape=True
    while (True):



        loop_count += 1

        if loop_count > 300:
            raise Exception(f"Exceeeded loop_count In " + inspect.currentframe().f_code.co_name)

        if verbosity > 3:
            print("")
            print("=====================================================")
            print("In " + inspect.currentframe().f_code.co_name,end='')
            print(f" loop_count= {loop_count}")
            print(f" selfloop_count= {loop_count}")

            #print(f"L1.intersects(the_boundary)={L1.intersects(the_boundary)}")
            print(f"L1.length()={L1.length()}")
            #print(f"L1.data={L1.data}")

            sys.stdout.flush()


        P1=L1.get_last_point()
        P2=P_target

        # v_escape=vec2d.points_to_vec2d(P1,P2)
        # v_strafe=vec2d.points_to_vec2d(P1,P2)

        L1.extend_line_to_new_point(P_target)

        ## keep copies only if graphing so we can show steps
        # if graff:
        #     data1=copy.deepcopy(L1.data)



        #if verbosity > 8:
        #    sub_graff=True
        #else:
        #    sub_graff=False
        sub_graff=False    
        [ is_trimmed, P_closest_intersection, P_polygon_endpoint]=L1.trim_line_at_first_intersection_point_and_follow_boundary(object_list, dr_escape, v_strafe, dr_strafe, graff=sub_graff)

        ###########################################################################
        #
        #
        #
        ##########################################################################
        #if (len(list_of_intersecting_objects) > 1):
        # if graff:
        #     colors=plt.get_cmap('Set1')
        #     plt.clf()
        #     fig = plt.figure(1)
        #     ### subplot nrows, ncols, plot #
        #     ax1 = fig.add_subplot(111)
        #     plotting_utils2.plot_shapely_object(ax1,L1.to_LineString(),'green')
        #     plotting_utils2.plot_shapely_object(ax1,object_list, 'blue','o')
        #     #plotting_utils2.plot_shapely_object(ax1,points_of_intersection, 'orange','o')
        #     plotting_utils2.plot_point(ax1,P_closest_intersection, 'red','x')
        #     plotting_utils2.plot_point(ax1,P_polygon_endpoint, 'green','x')


        #     #object_list=list_of_intersecting_objects
        #     #the_intersecting_poly=list_of_intersecting_objects[0]
        #     #L1.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection, P_closest_intersection)
        #     title_str = f""
        #     title_str += f" L1.length()={L1.length()}"
        #     title_str += f"{inspect.currentframe().f_code.co_name}"
        #     title_str += f" GRAFF #1"
        #     plt.axis('equal')
        #     plt.title(title_str)
        #     #lt.show()
        #     plt.show()
        #     # if True:


        ######################################################################
        ##
        ## we found an intersection and are following this to the edge of the object
        ## if another object is above this one we will collide with it, so
        ## we need to check for collisions after the extension is made
        ## if there is a collision we return false
        ##
        ##
        ### check for intersection that happened due to the extension
        try:
            
            wide_trace_i=L1.to_wide_trace(stitch_trace_width)
            #is_intersecting=L1.intersects(MultiPolygon(object_list))
            #is_intersecting=L1.intersects_any_of_list_of_objects(object_list)


            is_intersecting=intersection_utils.does_trace_intersect_any_of_list_of_objects(wide_trace_i, object_list)
            #is_intersecting=False
        except:
            print("In " + inspect.currentframe().f_code.co_name)
            print(f"Geometry problem on intersects")
            print(f"THIS PROBABLY NEEDS TO BE FIXED")

            sys.stdout.flush()
            is_intersecting=True

            # if False:
            #     #data3=copy.deepcopy(L1.data)
            #     #data3=L1.data
            #     #L1.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection, P_closest_intersection)


            #     print("____________________________________________________")
            #     print("In " + inspect.currentframe().f_code.co_name)
            #     print(f"L1.length()={L1.length()}")
            #     print(f"L1.data={L1.data}")
            #     #is_intersecting=L1.intersects(object_list)
            #     print(f"is_intersecting={is_intersecting}")                
            #     sys.stdout.flush()

            #     if True:
            #         plt.clf()
            #         fig = plt.figure(1)

            #         ### subplot nrows, ncols, plot #
            #         ax1 = fig.add_subplot(111)
            #         plotting_utils2.plot_shapely_object(ax1,object_list,'green')
            #         plotting_utils2.plot_shapely_object(ax1, L1.to_LineString(),'red')


            #         title_str = f""
            #         title_str += f"Geo Problem "
            #         #title_str += f" L1.length()={L1.length()}"
            #         title_str += f"{inspect.currentframe().f_code.co_name}"
            #         #title_str += f" GRAFF #2"
            #         plt.axis('equal')
            #         plt.title(title_str)
            #         #lt.show()
            #         plt.show()
            #         #plt.draw()
            #         plt.pause(0.0001)


            

        if graff:
            #data3=copy.deepcopy(L1.data)
            #data3=L1.data
            #L1.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection, P_closest_intersection)


            print("____________________________________________________")
            print("In " + inspect.currentframe().f_code.co_name)
            print(f"L1.length()={L1.length()}")
            print(f"L1.data={L1.data}")
            #is_intersecting=L1.intersects(object_list)
            print(f"is_intersecting={is_intersecting}")                
            sys.stdout.flush()

            plt.clf()
            fig = plt.figure(1)

            ### subplot nrows, ncols, plot #
            ax1 = fig.add_subplot(111)
            plotting_utils2.plot_shapely_object(ax1,object_list,'green')
            plotting_utils2.plot_point(ax1,P_target,'red',symbol="x")
            #plotting_utils2.plot_shapely_object_reference(ax1, L1.to_LineString(),'yellored','x')
            plotting_utils2.plot_shapely_object(ax1, L1.to_LineString(),'red')
            # plotting_utils2.plot_shapely_object(ax1, LineString(old_data),'red')

            #if len(data1) > 1:
            #plotting_utils2.plot_shapely_object_reference(ax1, LineString(data1),'lightblue')
            # plotting_utils2.plot_shapely_object(ax1, LineString(data2),'yellow')
            # plotting_utils2.plot_shapely_object(ax1, LineString(data3),'orange')

            # plotting_utils2.plot_shapely_object(ax1, P_closest_intersection,'red','x')
            # plotting_utils2.plot_shapely_object(ax1, P_polygon_endpoint,'red','o')

            #plt.draw()
            #plt.pause(0.0001)

            title_str = f""
            title_str += f" L1.length()={L1.length()}"
            title_str += f"{inspect.currentframe().f_code.co_name}"
            title_str += f" GRAFF #2"
            plt.axis('equal')
            plt.title(title_str)
            #lt.show()
            #plt.show()
            #plt.draw()
            plt.pause(0.0001)

        if is_intersecting:
            return False

    
        if not is_trimmed:
            return True

    #######################################################################################
    #
    #
    #
    #
    ######################################################################################
def trim_line_at_first_intersection_point_and_backtrack(the_line, object_list, dr_backtrack, graff=False, verbosity=0):
        '''
        [ is_trimmed, P_closest_intersection, the_intersecting_poly]
        [ is_trimmed, P_intersect]=x.trim_line_at_intersection_point(object_list, dr_backtrack)
        '''

        poi_df = the_line.get_all_intersections_as_df(object_list)

        if len(poi_df) == 0:
            is_trimmed = False
            P_closest_intersection = None
            the_intersecting_poly = None
            return [is_trimmed, P_closest_intersection, the_intersecting_poly]

        points_of_intersection = pandas_conversion_utils.get_column_of_dataframe_which_is_not_none(poi_df, key='Pi')

        if len(points_of_intersection) == 0:
            is_trimmed = False
            P_closest_intersection = None
            the_intersecting_poly = None
            return [is_trimmed, P_closest_intersection, the_intersecting_poly]

        assert (len(points_of_intersection) > 0)
        P_closest_intersection = point_utils.get_closest_point_in_list(the_line.get_second_last_point(),
                                                                       points_of_intersection)
        assert (P_closest_intersection is not None)

        #################################################################################
        #
        #
        # now do the trim with an optional backtrack
        #
        #
        ################################################################################

        if dr_backtrack != 0:
            ### we are backtracking along trace so vector is negative
            v_direction = -the_line.get_final_line_segment_direction()
            P_new_end = point_utils.move_point_along_vector(P_closest_intersection, v_direction, dr_backtrack)
        else:
            P_new_end = P_closest_intersection

        the_line.replace_last_point(P_new_end)
        is_trimmed = True

        ####################################################################################
        #
        # graff it!
        # 
        #
        ####################################################################################
        # if graff:
        #     #object_list=list_of_intersecting_objects
        #     #the_intersecting_poly=list_of_intersecting_objects[0]
        #     points_of_intersection=poi_df.Pi.to_list()
        #     list_of_intersecting_objects=poi_df.obj_i.to_list()

        #     colors=plt.get_cmap('Set1')
        #     plt.clf()
        #     fig = plt.figure(1)
        #     ### subplot nrows, ncols, plot #
        #     ax1 = fig.add_subplot(111)
        #     plotting_utils2.plot_shapely_object(ax1,the_line.to_LineString(),'green')
        #     for i, x_i in enumerate(list_of_intersecting_objects):
        #         #print(f"i={i} = ",end='')
        #         #print(f"x={x_i}")
        #         plotting_utils2.plot_shapely_object(ax1,x_i, colors(i),'o')
        #     plotting_utils2.plot_shapely_object(ax1,points_of_intersection, 'orange','o')
        #     plotting_utils2.plot_point(ax1,P_closest_intersection, 'red','x')

        #     P1=the_line.get_second_last_point()
        #     P2=the_line.get_last_point()

        #     v_arrow=vec2d.points_to_vec2d(P1,P2)
        #     v_arrow=vec2d.normalize_vec2d(v_arrow)
        #     L_seg=LineString([P1,P2])
        #     length_scale=L_seg.length

        #     arrow_plotting_utils.plot_arrow(ax1, P1, v_arrow, length_scale,color="black", plot_reference_line=False)
        #     plotting_utils2.plot_point(ax1,P1, 'blue','o')
        #     # plotting_utils2.plot_point(ax1,L_ab, 'orange')
        #     # plotting_utils2.plot_point(ax1,L_cd, 'orange')
        #     #title_str=
        #     plt.axis('equal')
        #     plt.show()
        #     title_str = f""
        #     title_str += f" the_line.length()={the_line.length()}"
        #     title_str += f"{inspect.currentframe().f_code.co_name}"

        #     plt.title(title_str)
        #     #lt.show()
        #     plt.show()
        #     # if True:

        #################if we have duplicate points at the end we want to drop it
        if len(the_line.data) > 2:
            P_last = the_line.data[-1]
            P_2nd_last = the_line.data[-2]
            if P_last.distance(P_2nd_last) == 0:
                if verbosity > 0:
                    print("In " + inspect.currentframe().f_code.co_name)
                    print(f"############################################")
                    print(f"found duplicate end point")
                    print(f"data={the_line.data}")
                    print(f"Pop-ing final point")
                the_line.pop()

        ################################################################33
        ##
        ## figure out which object we intersected with
        ##
        ##
        #################################################################
        poi_df_intersection_only = poi_df[poi_df['Pi'] == P_closest_intersection]
        list_of_intersecting_objects = poi_df_intersection_only['obj_i'].to_list()

        if graff:
            object_list = list_of_intersecting_objects
            the_intersecting_poly = list_of_intersecting_objects[0]
            the_line.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection,
                                                  P_closest_intersection)
            title_str = f""
            title_str += f" the_line.length()={the_line.length()}"
            title_str += f"{inspect.currentframe().f_code.co_name}"

            plt.title(title_str)
            plt.show()

        assert (len(poi_df_intersection_only) > 0)
        assert (len(list_of_intersecting_objects) > 0)
        the_intersecting_poly = list_of_intersecting_objects[0]

        return [is_trimmed, P_closest_intersection, the_intersecting_poly]
##############################################################################
#
#
#
#
##############################################################################
def get_closest_intersection_if_wide_trace(L1, trace_width, list_of_objects,use_full_endcap=False):
    assert(isinstance(L1,list_line.ListLine))
    T1=L1.to_LineString()
    W1=L1.to_wide_trace(trace_width,use_full_endcap=use_full_endcap)

    df_intersects_wide=intersection_utils.get_all_intersections_as_df(W1,list_of_objects)

    if len(df_intersects_wide)==0:
        P_c=None
    else:
        points_of_intersection=df_intersects_wide.Pi.to_list()
        P_endpoint=L1.get_second_last_point()
        P_closest_point_of_intersection=point_utils.get_closest_point_in_list(P_endpoint,points_of_intersection)
        
        v_line=L1.get_final_line_segment_direction()
        v_cross_1=vec2d.rotate_cw(v_line)
        #v_cross_2=vec2d.rotate_ccw(v_line)

        the_line_segment=L1.get_final_line_segment().to_LineString()
        P_a=P_closest_point_of_intersection
        P_c=geometry_utils.get_intersection_point_on_line_segment_from_point_and_direction_v1(P_a,v_cross_1,the_line_segment,choose_first=True, verbosity=0, graff=True)

    return [P_c,df_intersects_wide]
##############################################################################################33
#
#
#
#
#
##################################################################################
def trim_wide_line_at_first_intersection_point_and_backtrack(the_line, list_of_objects, dr_backtrack, trace_width,graff=False, verbosity=0):

    #assert(False)
    #graff=True
    if graff:
        the_line_orig=copy.deepcopy(the_line)

    ###################################################
    #
    #
    # Check 1 does mathematical line intersect
    #
    #
    ##################################################
        
    [is_trimmed, P_closest_intersection, the_intersecting_poly]=trim_line_at_first_intersection_point_and_backtrack(the_line,list_of_objects,dr_backtrack,graff=False,verbosity=verbosity)

    
    if is_trimmed:
        if verbosity > 1:
            print("In " + inspect.currentframe().f_code.co_name, end="")
            print(f" is_trimmed {is_trimmed}")
            sys.stdout.flush()

        #return [is_trimmed, P_closest_intersection, the_intersecting_poly]
        return the_line
    
    ############################################3
    #print("In " + inspect.currentframe().f_code.co_name, end="")
    #print(f" is_trimmed {is_trimmed}")


    ###########################################################
    #
    #
    # Check 2 does wide line (polygon) w/o endcap intersect?
    #
    #
    #########################################################


    [P_c,df_intersects_wide]=get_closest_intersection_if_wide_trace(the_line,trace_width,list_of_objects,use_full_endcap=False)
    intersection_is_end_on_case=False

    if P_c is None:
        ###########################################################
        #
        #
        # Check 3 does wide line (polygon) w endcap intersect?
        #  this is the end-on special case
        # where point B is close enough to the adjacent trace that
        # when the trace is widened it will intersect
        # we need to backtrack by an additional amount in this case
        #                      _________________________________
        #                   B  |  _____________________________
        #  *------------->--*  | |
        #                      | |
        #
        #########################################################
        [P_c,df_intersects_wide]=get_closest_intersection_if_wide_trace(the_line,trace_width,list_of_objects,use_full_endcap=True)

        ###unesecarry I think, but keeps it consistent
        if P_c is not None:  
            intersection_is_end_on_case=True

    

    
    if P_c is not None:
        if verbosity > 0:
            print("In " + inspect.currentframe().f_code.co_name, end="")
            print(f" is_trimmed {is_trimmed}",end=" ")
            print(f" P_c {P_c}",end=" ")
            print(f" intersection_is_end_on_case {intersection_is_end_on_case}",end=" ")
            print("")

        ####################################################################
        #
        #
        # now do the trim with an optional backtrack
        #
        #
        ####################################################################

        if dr_backtrack != 0:
            ### we are backtracking along trace so vector is negative
            v_direction = -the_line.get_final_line_segment_direction()

            total_backtrack=dr_backtrack

            if intersection_is_end_on_case:
                dr_end_on_backtrack=trace_width
                total_backtrack+=dr_end_on_backtrack
                
            P_new_end = point_utils.move_point_along_vector(P_c, v_direction, total_backtrack)
        else:
            P_new_end = P_closest_intersection

        the_line.replace_last_point(P_new_end)
        is_trimmed = True
        
    #assert(isinstance(the_line,list_line.ListLine))
    #graff=True
    if graff and P_c is not None:
        print("In " + inspect.currentframe().f_code.co_name)

        plt.clf()
        fig = plt.figure(1)

        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        
        # print(f"df_intersects_wide={df_intersects_wide}")
        if len(df_intersects_wide)>0:
            points_of_intersection=df_intersects_wide.Pi.to_list()
        else:
            points_of_intersection=[]

        #plotting_utils2.plot_shapely_object(ax1,T1, colors(color_count))
        # if the_boundary is not None:
        #     plotting_utils2.plot_shapely_object(ax1, the_boundary.boundary,'black')
        W1=the_line_orig.to_wide_trace(trace_width,use_full_endcap=True)
        W2=the_line.to_wide_trace(trace_width,use_full_endcap=True)
        
        plotting_utils2.plot_shapely_object(ax1,list_of_objects,'green')
        plotting_utils2.plot_shapely_object(ax1,the_line_orig,'gray')
        plotting_utils2.plot_shapely_object(ax1,W1,'lightgray')
        plotting_utils2.plot_shapely_object(ax1,P_c,'red')
        plotting_utils2.plot_shapely_object(ax1,points_of_intersection,'orange')
        plotting_utils2.plot_shapely_object(ax1,the_line,'red')
        plotting_utils2.plot_shapely_object(ax1,W2,'salmon')
        
        title_str = f""
        #title_str += f" self.length()={self.length()}"
        
        title_str = f""
        #title_str += f" self.length()={self.length()}"
        title_str += f"{inspect.currentframe().f_code.co_name}"
        plt.title(title_str)
        #title_str += f"x={x_i}"
        #plt.title(title_str)

        plt.axis('equal')     

        
        graff_pause=True
        #graff_pause=False
        plt.draw()
        plt.pause(0.0001)
        if graff_pause:
            plt.show()

    
    return the_line
