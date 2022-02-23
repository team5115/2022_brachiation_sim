#!/usr/bin/python3

import copy
import inspect
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import shapely
from shapely.geometry import LineString
from shapely.geometry import MultiPolygon
from shapely.geometry import Point
from shapely.ops import nearest_points

#from comp_geo import chamfer_utils
from comp_geo import geometry_utils
from comp_geo import intersection_utils
# mp = MultiPoint(route)
# print nearest_points(mp, end)[0]
from comp_geo import plotting_utils2
from comp_geo import point_utils
from comp_geo import polygon_utils
from comp_geo import shapely_utils
from comp_geo import vec2d
from csd import arrow_plotting_utils
from csd import pandas_conversion_utils

# https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/#What%E2%80%99s_the_alternative_to_inheriting_from_list_and_dict?

verbosity = 0

import collections


class ListLine(collections.UserList):

    def length(self):
        return len(list(filter(None, self.data)))
        #return len(self.data)

    def to_list(self):
        return self.to_list_of_points()

    # def to_list_of_points(self):
    #     return list(filter(None, self.data))

    def to_list_of_points(self):
        return list(filter(None, self.data))

    def to_LineString(self):
        # print(f"################################################")
        # print(f"self.data={self.data}")
        # sys.stdout.flush()

        # if (data_f is None):
        #    return LineString()
        if (self.length() >= 2):
            return LineString(self.to_list_of_points())
        elif (self.length() == 1):
            print("\n Warning trying to convert ListLine of length 1 to LineString")
            return LineString()
        else :
            return LineString()
            #if (self.length() == 0):
            
    def to_wide_trace(self, trace_width,use_full_endcap=True):

        # The styles of caps are specified by integer values: 1 (round), 2
        # (flat), 3 (square). These values are also enumerated by the
        # object shapely.geometry.CAP_STYLE (see below).

        if use_full_endcap:
            cap_style=3
        else:
            cap_style=2
        
        # The styles of joins between offset segments are specified by
        # integer values: 1 (round), 2 (mitre), and 3 (bevel). These
        # values are also enumerated by the object
        # shapely.geometry.JOIN_STYLE (see below)

        the_line = self.to_LineString()

        the_trace = the_line.buffer(trace_width / 2.0, resolution=16, cap_style=cap_style, join_style=2, mitre_limit=10.0)
        return the_trace

    def get_first_point(self):
        Px = self.data[0]
        assert (isinstance(Px, shapely.geometry.Point))
        return Px

    def get_last_point(self):
        Px = self.data[-1]
        assert (isinstance(Px, shapely.geometry.Point))
        return Px

    def get_nth_point(self,n=-1):
        Px = self.data[n]
        assert (isinstance(Px, shapely.geometry.Point))
        return Px

       
    def move_endpoint_to_shorten_line_by_dr(self, dr):
        v_direction=self.get_final_line_segment_direction()
        self.move_endpoint_to_new_position(-v_direction,dr)

    # def move_endpoint_to_exteshorten_line_by_dr(self, dr):
    #     v_direction=L1.get_final_line_segment_direction()
    #     self.move_endpoint_to_new_position(-v_direction,dr)
        
    def move_endpoint_to_new_position(self, v_direction, dr):
        assert (isinstance(v_direction, np.ndarray))
        P_last = self.get_last_point()
        P_new = point_utils.move_point_along_vector(P_last, v_direction, dr)
        self.replace_last_point(P_new)

    def prepend_point(self, P_new):
        self.insert(0,P_new)

        
    def extend_line_to_new_point(self, P_new):
        self.append(P_new)

    def extend_line_along_vector(self, v_direction, dr):
        assert (isinstance(v_direction, np.ndarray))
        P_last = self.get_last_point()
        P_new = point_utils.move_point_along_vector(P_last, v_direction, dr)
        self.append(P_new)

    def extend_line(self, dr):
        v_direction=self.get_final_line_segment_direction()
        self.extend_line_along_vector(v_direction, dr)
        
    def extend_line_to_boundary(self, the_boundary, graff=False, graff_pause=False):
        v_direction=self.get_final_line_segment_direction()
        self.extend_line_along_vector_to_boundary(v_direction, the_boundary, graff=graff, graff_pause=graff_pause)    
        
    def extend_line_along_vector_to_boundary(self, v_direction, the_boundary, graff=False, graff_pause=False):
        assert (isinstance(v_direction, np.ndarray))
        P_last = self.get_last_point()

        ##############TODO THIS IS THE CALL THAT IS BREAKING

        Pc=geometry_utils.get_intersection_point_on_boundary_from_point_and_direction(P_last,v_direction,the_boundary)

        #Pc = geometry_utils2.get_intersection_point_on_boundary_from_point_and_direction(P_last, v_direction,the_boundary)

        if Pc is None:
            return
        
        #assert (P_last.distance(Pc) != 0)
        # check for corner case where you are already on the boundary
        if P_last.distance(Pc) != 0:
           self.append(Pc)

        if graff:
            plt.clf()
            fig = plt.figure(1)

            ### subplot nrows, ncols, plot #
            ax1 = fig.add_subplot(111)

            plotting_utils2.plot_shapely_object_reference(ax1, the_boundary.exterior, 'green')
            plotting_utils2.plot_shapely_object(ax1, self.to_LineString(), 'blue')

            plotting_utils2.plot_shapely_object(ax1, P_last, 'red')
            plotting_utils2.plot_shapely_object(ax1, Pc, 'orange', 'x')

            # ax2 = fig.add_subplot(122)
            # plotting_utils2.plot_shapely_object(ax2, L_top,'orange')
            # plotting_utils2.plot_shapely_object(ax2, L_bottom,'blue')
            # plotting_utils2.plot_shapely_object(ax2,P_split, 'red')
            plt.axis('equal')
            title_str = "In " + inspect.currentframe().f_code.co_name
            plt.title(title_str)

            plt.draw()
            if graff_pause:
                plt.show()
            
    def extend_up(self, dr):
        v_direction = vec2d.v_up
        self.extend_line_along_vector(v_direction, dr)

    def extend_down(self, dr):
        v_direction = vec2d.v_down
        self.extend_line_along_vector(v_direction, dr)

    def extend_right(self, dr):
        v_direction = vec2d.v_right
        self.extend_line_along_vector(v_direction, dr)

    def extend_left(self, dr):
        v_direction = vec2d.v_left
        self.extend_line_along_vector(v_direction, dr)

    def intersects(self, obj):
        if (isinstance(obj,list)):
            raise "for single object only maybe try intersects_any_of_list_of_objects("
        L_full = self.to_LineString()
        return L_full.intersects(obj)

#    def intersects_single_object(self, obj):
#        L_full = self.to_LineString()
#        return L_full.intersects(obj)

    def intersects_any_of_list_of_objects(self, list_of_objects):
        L_full = self.to_LineString()
        return intersection_utils.does_trace_intersect_any_of_list_of_objects(L_full,list_of_objects)

    def intersects_any_of_list_of_objects_wide_or_narrow(self, list_of_objects, use_wide_intersections):
        if use_wide_intersections:
            L_full= self.to_wide_trace()            
        else:
            L_full= self.to_LineString()

        return intersection_utils.does_trace_intersect_any_of_list_of_objects(L_full,list_of_objects)

        
 
    def get_final_line_segment_direction(self):
        """
           returns a vector for the last line segment

        """
        
        assert len(self.data) >= 2
        P1 = self.data[-2]
        P2 = self.data[-1]

        assert (P1.distance(P2) != 0)
        v_direction = vec2d.points_to_vec2d(P1, P2)
        v_direction = vec2d.normalize_vec2d(v_direction)
        return v_direction

    def get_final_line_segment(self):
        assert len(self.data) >= 2
        return ListLine([self.data[-2], self.data[-1]])

    def get_final_line_segment_length(self):
        """
           returns a vector for the last line segment

        """
        
        assert len(self.data) >= 2
        P1 = self.data[-2]
        P2 = self.data[-1]

        d=P1.distance(P2)
        return d

    def remove_last_point(self):
        return self.pop

    def get_last_point(self):
        return self.data[-1]

    def get_second_last_point(self):
        return self.data[-2]

    def replace_last_point(self, P_last):
        self.data[-1] = P_last


    def is_simple_line_segment(self):

        return self.length()==2

        
    def get_tangent_and_normal_vector_if_simple_line_segment(self) -> vec2d:
        """
           Returns a tangent and normal vector for a line

           [v_tangent,v_normal]=l1.get_tangent_and_normal_vector_if_simple_line_segment()
        """
        
        assert(self.is_simple_line_segment())        
        P1=self.get_first_point()
        P2=self.get_last_point()
        
        v_tangent=vec2d.points_to_vec2d(P1,P2,normalize=True)
        dx = P2.x - P1.x
        dy = P2.y - P1.y

        v_normal=vec2d.gen_vec2d(-dy,dx)

        v_normal=vec2d.normalize_vec2d(v_normal)

        #v_normal=vec2d.rotate_cw(v_tangent)

        return [v_tangent,v_normal]

    def get_midpoint_if_simple_line_segment(self) -> vec2d:
        """
           Returns the_midpoint for a line


        """
        
        assert(self.is_simple_line_segment())        
        P1=self.get_first_point()
        P2=self.get_last_point()
        
        v_tangent=vec2d.points_to_vec2d(P1,P2,normalize=True)
        x_mid = (P2.x + P1.x)/2.0
        y_mid = (P2.y + P1.y)/2.0

        P_mid=Point(x_mid,y_mid)
        
        return P_mid

    def get_all_intersections_as_points(self, object_list):
        points_of_intersection = intersection_utils.get_all_intersections_as_points(self.to_LineString(), object_list)
        return points_of_intersection

    def get_all_intersections_as_df(self, object_list):
        points_df = intersection_utils.get_all_intersections_as_df(self.to_LineString(), object_list)
        return points_df

    def get_closest_intersection_per_object_as_df(self, object_list, use_last_intersection=True, graff=False):
        points_df = intersection_utils.get_closest_intersection_per_object_as_df(self.to_LineString(), object_list,
                                                                                 use_last_intersection, graff)
        return points_df

    def estimate_split_point_for_non_intersecting_split(self, P_split, err=1e-6, verbosity=0):
        '''
          A point must be on a line to intersect,
          you should be able to use snap or nearest_points, but that
          wasnt working on a specific case, so here we buffer the point
          instead

        '''
        assert (isinstance(P_split, shapely.geometry.Point))

        L_full = self.to_LineString()
        tolerance = L_full.length * err
        #       tolerance=L_full.length*1e-3
        does_line_intersect = L_full.intersects(P_split)
        tolerance = 0.5
        if not does_line_intersect:

            # P_wide=P_split.buffer(tolerance)
            # points_of_intersection_to_buffered_point=L_full.intersection(P_wide)
            # list_of_points=shapely_utils.linestring_to_array_of_points(points_of_intersection_to_buffered_point)

            # print(f"")
            # print(f"################################################################")

            # for i, P_i in enumerate(list_of_points):

            #     print(f"i={i} = ",end='')
            #     print(f"P_i={P_i}")
            #     print(f"L_full.intersects(P_i)={L_full.intersects(P_i)}")

            # P_closest_intersection=point_utils.get_closest_point_in_list(P_split,list_of_points)

            dx = tolerance

            P_a = Point(P_split.x + dx, P_split.y)
            P_b = Point(P_split.x - dx, P_split.y)

            L_ab = LineString([P_a, P_b])

            if verbosity > 3:
                print(f"P_a={P_a}")
                print(f"P_b={P_b}")
                print(f"L_full.intersects(L_ab)={L_full.intersects(L_ab)}")

            P_c = Point(P_split.x + dx, P_split.y)
            P_d = Point(P_split.x - dx, P_split.y)

            L_cd = LineString([P_c, P_d])

            if verbosity > 3:
                print(f"P_c={P_c}")
                print(f"P_d={P_d}")
                print(f"L_full.intersects(L_cd)={L_full.intersects(L_cd)}")

            list_of_points = self.get_all_intersections_as_points([L_ab, L_cd])
            P_closest_intersection = point_utils.get_closest_point_in_list(P_split, list_of_points)
            P_split = P_closest_intersection

            if verbosity > 3:
                print(f"P_split={P_split}")
                if P_split is not None:
                    print(f"L_full.intersects(P_split)={L_full.intersects(P_split)}")

        #             P_split0=copy.deepcopy(P_split)
        #             P_split1=P_closest_intersection
        # #            P_split1=Point(P_split.x+0.1,P_split.y)
        #             P_split2=shapely.ops.snap(P_split1, L_full,tolerance=0.5)
        # #            P_split2=shapely.ops.nearest_points(L_full, P_split1)
        #             P_split3=shapely.ops.nearest_points(P_split1, L_full)[0]

        #             #P_split=copy.deepcopy(P_split2)
        #             print(f"")
        #             print(f"################################################################")

        #             print(f"points_of_intersection_to_buffered_point = {points_of_intersection_to_buffered_point}")
        #             print(f"P_split0={P_split0}")
        #             print(f"P_split1={P_split1}")
        #             print(f"P_split2={P_split2}")
        #             print(f"P_split3={P_split3}")
        # #            print(f"P_split4={P_split4}")
        #             print(f"P_split1==P_split2={P_split1==P_split2}")
        #             print(f"L_full.distance(P_split1)={L_full.distance(P_split1)}")
        #             print(f"L_full.distance(P_split2)={L_full.distance(P_split2)}")
        #             print(f"L_full.intersects(P_split1)={L_full.intersects(P_split1)}")
        #             print(f"L_full.intersects(P_split2)={L_full.intersects(P_split2)}")
        #             print(f"{P_split2.distance(P_split1)}={P_split2.distance(P_split1)}")
        #             print(f"################################################################")
        #             sys.stdout.flush()

        # if True:
        #     plt.clf()
        #     fig = plt.figure(1)
        #     ### subplot nrows, ncols, plot #
        #     ax1 = fig.add_subplot(111)
        #     plotting_utils2.plot_shapely_object(ax1,self.to_LineString(),'green')
        #     plotting_utils2.plot_point(ax1,P_closest_intersection, 'red','o')
        #     plotting_utils2.plot_point(ax1,P_split, 'blue','x')
        #     plotting_utils2.plot_point(ax1,L_ab, 'orange')
        #     plotting_utils2.plot_point(ax1,L_cd, 'orange')
        #     #title_str=
        #     plt.axis('equal')
        #     plt.show()

        # assert(L_full.intersects(P_split))
        # P_split=P_closest_intersection
        # return P_split

        if L_full.intersects(L_ab):
            return L_ab

        if L_full.intersects(L_cd):
            return L_cd

        return None

    #     def estimate_split_point_for_non_intersecting_split(self, P_split,err=1e-6):
    #         '''
    #           A point must be on a line to intersect,
    #           you should be able to use snap or nearest_points, but that
    #           wasnt working on a specific case, so here we buffer the point
    #           instead

    #         '''
    #         assert(isinstance(P_split, shapely.geometry.Point))

    #         L_full=self.to_LineString()
    #         tolerance=L_full.length*err
    # #       tolerance=L_full.length*1e-3
    #         does_line_intersect=L_full.intersects(P_split)

    #         if not does_line_intersect:

    #             P_wide=P_split.buffer(tolerance)
    #             points_of_intersection_to_buffered_point=L_full.intersection(P_wide)
    #             list_of_points=shapely_utils.linestring_to_array_of_points(points_of_intersection_to_buffered_point)

    #             P_closest_intersection=point_utils.get_closest_point_in_list(P_split,list_of_points)

    #             P_split0=copy.deepcopy(P_split)
    #             P_split1=P_closest_intersection
    # #            P_split1=Point(P_split.x+0.1,P_split.y)
    #             P_split2=shapely.ops.snap(P_split1, L_full,tolerance=0.5)
    # #            P_split2=shapely.ops.nearest_points(L_full, P_split1)
    #             P_split3=shapely.ops.nearest_points(P_split1, L_full)[0]

    #             #P_split=copy.deepcopy(P_split2)
    #             print(f"")
    #             print(f"################################################################")

    #             # for i in range(0,len(P_split2)):
    #             #     print(f"i={i} = ")
    #             #     print(f"P_split2[{i}] = {P_split2[i]}")

    #             # for i in range(0,len(P_split3)):
    #             #     print(f"i={i} = ")
    #             #     print(f"P_split3[{i}] = {P_split3[i]}")

    #             print(f"points_of_intersection_to_buffered_point = {points_of_intersection_to_buffered_point}")
    #             print(f"P_split0={P_split0}")
    #             print(f"P_split1={P_split1}")
    #             print(f"P_split2={P_split2}")
    #             print(f"P_split3={P_split3}")
    # #            print(f"P_split4={P_split4}")
    #             print(f"P_split1==P_split2={P_split1==P_split2}")
    #             print(f"L_full.distance(P_split1)={L_full.distance(P_split1)}")
    #             print(f"L_full.distance(P_split2)={L_full.distance(P_split2)}")
    #             print(f"L_full.intersects(P_split1)={L_full.intersects(P_split1)}")
    #             print(f"L_full.intersects(P_split2)={L_full.intersects(P_split2)}")
    #             print(f"{P_split2.distance(P_split1)}={P_split2.distance(P_split1)}")
    #             print(f"################################################################")
    #             sys.stdout.flush()

    #             if True:
    #                 plt.clf()
    #                 fig = plt.figure(1)
    #                 ### subplot nrows, ncols, plot #
    #                 ax1 = fig.add_subplot(111)
    #                 plotting_utils2.plot_shapely_object(ax1,self.to_LineString(),'green')
    #                 plotting_utils2.plot_point(ax1,P_split1, 'red','o')
    #                 plotting_utils2.plot_point(ax1,P_split2, 'blue','x')
    #                 #title_str=
    #                 plt.axis('equal')
    #                 plt.show()

    #         assert(L_full.intersects(P_split))
    #         return P_split

    def split_at_point(self, P_split, graff=False, verbosity=0):

        assert (isinstance(P_split, shapely.geometry.Point))

        non_intersection_hack = False
        L_full = self.to_LineString()
        tolerance = L_full.length * 1e-6
        #       tolerance=L_full.length*1e-3

        does_line_intersect = L_full.intersects(P_split)
        if not does_line_intersect:
            non_intersection_hack = True
            # graff=True
            P_split2 = self.estimate_split_point_for_non_intersecting_split(P_split, err=1e-6)

            assert (P_split2 is not None)

            if P_split2 is None:
                assert (False)
                L_top = self
                L_bottom = ListLine()
                return [L_top, L_bottom]

            if verbosity > 0:
                print(f"Warning P_split did not intersect, applied correction")
                print(f"P_split={P_split}")
                print(f"P_split2={P_split2}")
                print(f"P_split2.distance(P_split)={P_split2.distance(P_split)}")

            P_split = P_split2

        assert (L_full.intersects(P_split))
        the_two_lines_as_geometry_collection = shapely.ops.split(L_full, P_split)

        # if len(the_two_lines_as_geometry_collection) != 2:
        #     print(f"len(the_two_lines_as_geometry_collection)={len(the_two_lines_as_geometry_collection)}")
        #     print(f"the_two_lines_as_geometry_collection={the_two_lines_as_geometry_collection.wkt}")

        # assert(len(the_two_lines_as_geometry_collection)==2)

        L1 = the_two_lines_as_geometry_collection[0]

        ### the Px is the endpoint of L1
        if (len(the_two_lines_as_geometry_collection) == 1):
            L2 = LineString()
        else:
            L2 = the_two_lines_as_geometry_collection[1]

        list_of_points1 = shapely_utils.linestring_to_array_of_points(L1)
        list_of_points2 = shapely_utils.linestring_to_array_of_points(L2)

        L_top = ListLine(list_of_points1)
        L_bottom = ListLine(list_of_points2)

        if graff:
            plt.clf()
            fig = plt.figure(1)

            ### subplot nrows, ncols, plot #
            ax1 = fig.add_subplot(121)

            plotting_utils2.plot_shapely_object(ax1, L_full, 'green')
            plotting_utils2.plot_shapely_object(ax1, P_split, 'red')

            ax2 = fig.add_subplot(122)
            plotting_utils2.plot_shapely_object(ax2, L_top, 'orange')
            plotting_utils2.plot_shapely_object(ax2, L_bottom, 'blue')
            plotting_utils2.plot_shapely_object(ax2, P_split, 'red')
            plt.axis('equal')
            title_str = "In " + inspect.currentframe().f_code.co_name
            plt.title(title_str)
            # plt.show()
            # plt.display()
            plt.draw()
            plt.pause(0.0001)
            # plt.show()

        return [L_top, L_bottom]

    def split_at_intersection_point_with_objects(self, all_objects, use_last_intersection=True, graff=False):
        [list_of_points1, list_of_points2] = intersection_utils.split_line_at_intersection_point_with_objects(self.data,
                                                                                                              all_objects,
                                                                                                              use_last_intersection,
                                                                                                              graff)

        return [ListLine(list_of_points1), ListLine(list_of_points2)]

    def display_contour_routing_progress(self, object_list, the_intersecting_poly, points_of_intersection,
                                         P_closest_intersection):
        plt.clf()
        fig = plt.figure(1)

        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)

        colors = plt.get_cmap('Set1')
        color_count = 0
        # plotting_utils2.plot_shapely_object(ax1,T1, colors(color_count))
        # color_count += 1

        plotting_utils2.plot_shapely_object(ax1, object_list, 'green')
        color_count += 1

        plotting_utils2.plot_shapely_object(ax1, the_intersecting_poly, 'darkgreen')
        color_count += 1

        plotting_utils2.plot_shapely_object(ax1, self, 'blue')
        color_count += 1

        # plotting_utils2.plot_shapely_object(ax1,L1, colors(color_count))
        # color_count += 1

        plotting_utils2.plot_shapely_object(ax1, points_of_intersection, 'orange')
        color_count += 1

        plotting_utils2.plot_shapely_object(ax1, P_closest_intersection, 'red')
        color_count += 1

        P1 = self.get_second_last_point()
        P2 = self.get_last_point()

        v_arrow = vec2d.points_to_vec2d(P1, P2)
        v_arrow = vec2d.normalize_vec2d(v_arrow)
        L_seg = LineString([P1, P2])
        length_scale = L_seg.length

        arrow_plotting_utils.plot_arrow(ax1, P1, v_arrow, length_scale, color="black", plot_reference_line=False)
        plotting_utils2.plot_point(ax1, P1, 'blue', 'o')

        plt.axis('equal')
        # plt.show()
        plt.draw()
        plt.pause(0.0001)

    def trim_line_at_first_intersection_point_and_backtrack(self, object_list, dr_backtrack, graff=False, verbosity=0):
        '''
        [ is_trimmed, P_closest_intersection, the_intersecting_poly]
        [ is_trimmed, P_intersect]=x.trim_line_at_intersection_point(object_list, dr_backtrack)
        '''

        poi_df = self.get_all_intersections_as_df(object_list)

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
        P_closest_intersection = point_utils.get_closest_point_in_list(self.get_second_last_point(),
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
            v_direction = -self.get_final_line_segment_direction()
            P_new_end = point_utils.move_point_along_vector(P_closest_intersection, v_direction, dr_backtrack)
        else:
            P_new_end = P_closest_intersection

        self.replace_last_point(P_new_end)
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
        #     plotting_utils2.plot_shapely_object(ax1,self.to_LineString(),'green')
        #     for i, x_i in enumerate(list_of_intersecting_objects):
        #         #print(f"i={i} = ",end='')
        #         #print(f"x={x_i}")
        #         plotting_utils2.plot_shapely_object(ax1,x_i, colors(i),'o')
        #     plotting_utils2.plot_shapely_object(ax1,points_of_intersection, 'orange','o')
        #     plotting_utils2.plot_point(ax1,P_closest_intersection, 'red','x')

        #     P1=self.get_second_last_point()
        #     P2=self.get_last_point()

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
        #     title_str += f" self.length()={self.length()}"
        #     title_str += f"{inspect.currentframe().f_code.co_name}"

        #     plt.title(title_str)
        #     #lt.show()
        #     plt.show()
        #     # if True:

        #################if we have duplicate points at the end we want to drop it
        if len(self.data) > 2:
            P_last = self.data[-1]
            P_2nd_last = self.data[-2]
            if P_last.distance(P_2nd_last) == 0:
                if verbosity > 0:
                    print("In " + inspect.currentframe().f_code.co_name)
                    print(f"############################################")
                    print(f"found duplicate end point")
                    print(f"data={self.data}")
                    print(f"Pop-ing final point")
                self.pop()

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
            self.display_contour_routing_progress(object_list, the_intersecting_poly, points_of_intersection,
                                                  P_closest_intersection)
            title_str = f""
            title_str += f" self.length()={self.length()}"
            title_str += f"{inspect.currentframe().f_code.co_name}"

            plt.title(title_str)
            plt.show()

        assert (len(poi_df_intersection_only) > 0)
        assert (len(list_of_intersecting_objects) > 0)
        the_intersecting_poly = list_of_intersecting_objects[0]

        return [is_trimmed, P_closest_intersection, the_intersecting_poly]

    ###########################################################################################################
    ##
    ##   We find an intesection at point Pa
    ##   we then want to follow the line segment in a direction
    ##   to get point B
    ##
    ##   We then calculate Points C and D which are fixed offset
    ##   from A and B respectively
    ##   finally we offset to point E
    ##
    ##  
    ##                        |
    ##                        v
    ##                        |                        D      E
    ##                       C*------->----------->----*----- *->
    ##         
    ##                                                                ---> v_direction_to_move          
    ##    --------------------*------------------------*
    ##    |                   A                        |B
    ##    |                                            |
    ##    |                                            |
    ##    |                                            |
    ##    |                                            |
    ##    |                                            |
    ##    |                                            |
    ##    ----------------------------------------------
    ##
    ##
    ########################################################################################################
    def trim_line_at_first_intersection_point_and_follow_boundary(self, object_list, dr_escape, v_strafe, dr_strafe,
                                                                  graff=False):
        '''

        trim_line_at_first_intersection_point_and_follow_boundary

        [ is_trimmed, P_closest_intersection, P_polygon_endpoint]=L2.trim_line_at_first_intersection_point_and_follow_boundary(object_list, dr_escape, v_strafe, dr_strafe, graff=False):
        '''

        ###########################################################################
        ###
        ### save original data for later
        ###
        ############################################################################
        if graff:
            data1 = copy.deepcopy(self.data)

        [is_trimmed, P_closest_intersection,
         the_intersecting_poly] = self.trim_line_at_first_intersection_point_and_backtrack(object_list, dr_escape,
                                                                                           graff=graff)

        Pa = P_closest_intersection
        Pc = self.get_last_point()

        #############################################################################
        ###
        ### plot result of trim line at intersection point
        ###
        #############################################################################

        if graff:
            plt.clf()
            fig = plt.figure(1)

            ### subplot nrows, ncols, plot #
            ax1 = fig.add_subplot(111)

            colors = plt.get_cmap('Set1')
            color_count = 0
            # plotting_utils2.plot_shapely_object(ax1,T1, colors(color_count))
            # color_count += 1
            plotting_utils2.plot_shapely_object(ax1, self.to_LineString(), 'red')
            plotting_utils2.plot_shapely_object_reference(ax1, LineString(data1), 'gray')
            plotting_utils2.plot_shapely_object(ax1, object_list, 'gray')
            if the_intersecting_poly is not None:
                plotting_utils2.plot_shapely_object(ax1, the_intersecting_poly.exterior, 'green')

            if P_closest_intersection is not None:
                plotting_utils2.plot_point(ax1, P_closest_intersection, color='red', symbol='x')

            plt.axis('equal')
            #plt.title(inspect.currentframe().f_code.co_name + "after trim line call")
            title_str=""
            title_str+=f"list_line.tlafipaf  GRAFF #WWW"
            title_str+=f"\nlen(object_list)={len(object_list)}"

            plt.title(title_str)
            plt.show()

        #############################################################################
        ###
        ###  if something happened return Nones and False
        ###  i think this is only for pathological cases
        ###
        #############################################################################

        if not is_trimmed:
            is_trimmed = False
            P_closest_intersection = None
            P_polygon_endpoint = None
            return [is_trimmed, P_closest_intersection, P_polygon_endpoint]

        # #intersection_objs=[]

        # sub_list = [x for x in object_list if x.intersects(P_closest_intersection)]

        # if (len(sub_list) ==0):
        #    self.display_contour_routing_progress(object_list, points_of_intersection, P_closest_intersection)

        #    assert(len(sub_list) > 0)

        # the_poly=sub_list[0]
        ### we are backtracking along trace so vector is negative

        #############################################################################
        ###
        ###  we are now going to follow the edge to the end of the object
        ###  whether we go left or right depends on the v_direction vector
        ###
        #############################################################################

        v_direction = v_strafe
        P_polygon_endpoint = polygon_utils.get_endpoint_from_following_edge(the_intersecting_poly,
                                                                            P_closest_intersection, v_direction,
                                                                            graff=graff)

        Pb = P_polygon_endpoint

        #############################################################################
        ###
        ###  we are now have two points on the polygon
        ###  whether we go left or right depends on the v_direction vector
        ###
        #############################################################################

        # # ###################################################################################
        # if graff:
        #     #object_list=list_of_intersecting_objects
        #     #the_intersecting_poly=list_of_intersecting_objects[0]
        #     #points_of_intersection=poi_df.Pi.to_list()
        #     #list_of_intersecting_objects=[the_intersecting_poly]

        #     colors=plt.get_cmap('Set1')
        #     plt.clf()
        #     fig = plt.figure(1)
        #     ### subplot nrows, ncols, plot #
        #     ax1 = fig.add_subplot(111)
        #     plotting_utils2.plot_shapely_object(ax1,self.to_LineString(),'green')
        #     plotting_utils2.plot_shapely_object(ax1,the_intersecting_poly, 'blue','o')
        #     #plotting_utils2.plot_shapely_object(ax1,points_of_intersection, 'orange','o')
        #     plotting_utils2.plot_point(ax1,P_closest_intersection, 'red','x')
        #     plotting_utils2.plot_point(ax1,P_polygon_endpoint, 'green','x')

        #     P1=self.get_second_last_point()
        #     P2=self.get_last_point()

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
        # title_str = f""
        # title_str += f" self.length()={self.length()}"
        # title_str += f"{inspect.currentframe().f_code.co_name}"

        # plt.title(title_str)
        # #lt.show()
        # plt.show()
        # # if True:

        if P_polygon_endpoint is None:
            points_of_intersection = []
            is_trimmed = False
            return [is_trimmed, P_closest_intersection, P_polygon_endpoint]

        v_escape = -self.get_final_line_segment_direction()

        ### push back from edge opposite to thrust
        Pd = point_utils.move_point_along_vector(Pb, v_escape, dr_escape)

        v_strafe = vec2d.points_to_vec2d(Pa, Pb, normalize=True)

        ### push away from edge (strafe axis)
        Pe = point_utils.move_point_along_vector(Pd, v_strafe, dr_strafe)

        assert (dr_strafe == dr_escape)
        self.append(Pe)

        # self.display_contour_routing_progress(object_list, points_of_intersection=[], P_closest_intersection=P_new_end)
        #############################################################################
        ###
        ###
        ###

        if graff:
            plt.clf()
            fig = plt.figure(1)

            ### subplot nrows, ncols, plot #
            ax1 = fig.add_subplot(111)

            colors = plt.get_cmap('Set1')
            color_count = 0
            # plotting_utils2.plot_shapely_object(ax1,T1, colors(color_count))
            # color_count += 1
            plotting_utils2.plot_shapely_object(ax1, self.to_LineString(), 'red')
            plotting_utils2.plot_shapely_object(ax1, the_intersecting_poly.exterior, 'green')
            plotting_utils2.plot_point(ax1, Pa, color='orange', symbol='x')
            plotting_utils2.plot_point(ax1, Pb, color='orange', symbol='x')
            plotting_utils2.plot_point(ax1, Pc, color='red', symbol='x')
            plotting_utils2.plot_point(ax1, Pd, color='orange', symbol='x')
            plotting_utils2.plot_point(ax1, Pe, color='red', symbol='x')
            # plotting_utils2.plot_point(ax1,P_polygon_endpoint,color='gray',symbol='x')
            # plotting_utils2.plot_point(ax1,P_new_end,color='red',symbol='x')
            plt.axis('equal')
            plt.title(inspect.currentframe().f_code.co_name)
            plt.show()

        return [is_trimmed, P_closest_intersection, P_polygon_endpoint]

    def extend_to_boundary_and_contour_trace(self, the_boundary, object_list, v_escape, dr_escape, v_strafe, dr_strafe, graff):

        max_loop_count = 1000
        loop_count = 0

        while (True):

            loop_count += 1

            if loop_count > max_loop_count:
                raise Exception(
                    f"Exceeeded max loop_count {max_loop_count} In " + inspect.currentframe().f_code.co_name)

            if verbosity > 3:
                print("")
                print("=====================================================")
                print("In " + inspect.currentframe().f_code.co_name, end='')
                print(f" loop_count= {loop_count}")
                print(f" selfloop_count= {loop_count}")

                print(f"self.intersects(the_boundary)={self.intersects(the_boundary)}")
                print(f"self.length()={self.length()}")
                # print(f"self.data={self.data}")

                sys.stdout.flush()

            # if graff:
            #    data1=copy.deepcopy(self.data)
            # debug_graff=False
            debug_graff=False
            debug_graff_pause=False
            self.extend_line_along_vector_to_boundary(v_direction=v_escape, the_boundary=the_boundary, graff=debug_graff, graff_pause=debug_graff_pause)
            

            # if graff:
            #    data2=copy.deepcopy(self.data)
            debug_graff=False
            #debug_graff=True
            [is_trimmed, P_closest_intersection,
             P_polygon_endpoint] = self.trim_line_at_first_intersection_point_and_follow_boundary(object_list,
                                                                                                  dr_escape, v_strafe,
                                                                                                  dr_strafe,
                                                                                                  graff=debug_graff)
            
            ######################################################################
            ##
            ## we found an intersection and are following this to the edge of the object
            ## if another object is above this one we will collide with it, so
            ## we need to check for collisions after the extension is made
            ## if there is a collision we return false
            ##
            ##
            ### check for intersection that happened due to the extension
            is_intersecting = self.intersects(MultiPolygon(object_list))
            # print(f"is_intersecting={is_intersecting}")
            # sys.stdout.flush()

            if graff:
                plt.clf()
                fig = plt.figure(1)

                if is_intersecting:
                    color = 'red'
                else:
                    color = 'green'

                ### subplot nrows, ncols, plot #
                ax1 = fig.add_subplot(111)
                plotting_utils2.plot_shapely_object(ax1, object_list, 'lightgrey')
                plotting_utils2.plot_shapely_object_reference(ax1, the_boundary.exterior, 'blue')
                # plotting_utils2.plot_shapely_object_reference(ax1, self.to_LineString(),'yellored','x')
                # plotting_utils2.plot_shapely_object(ax1, self.to_LineString(),'orange','x')
                # plotting_utils2.plot_shapely_object(ax1, LineString(old_data),'red')

                # plotting_utils2.plot_shapely_object(ax1, LineString(data1),'lightblue')
                # plotting_utils2.plot_shapely_object(ax1, LineString(data2),'yellow')
                # plotting_utils2.plot_shapely_object(ax1, LineString(data3),color=color)
                plotting_utils2.plot_shapely_object(ax1, LineString(self.data), color=color)

                plotting_utils2.plot_shapely_object(ax1, P_closest_intersection, 'red', 'x')
                # plotting_utils2.plot_shapely_object(ax1, P_polygon_endpoint,'red','o')
                plt.axis('equal')
                title_str = f"list_line GRAFF #1"
                title_str += f" self.length()={self.length()}"
                #title_str += f"\n list_line.tlafipadb()"
                #title_str += f"\n list_line."
                title_str += f"{inspect.currentframe().f_code.co_name}"
                
                plt.title(title_str)
                #figure_utils.resize_figure()
                plt.draw()
                plt.pause(0.0001)

                # lt.show()
                # plt.show()
                # if is_intersecting:
                #    plt.show()

            if is_intersecting:
                return False

            if not is_trimmed:
                return True

    def generate_chamfered_version(self, dy, dx):
        new_list = chamfer_utils.chamfer_line(self.data, dx, dy)

        return ListLine(new_list)

    def get_slope(self):
        assert (len(self.data) == 2)

        x1 = data[0].x
        x2 = data[1].x
        y1 = data[0].y
        y2 = data[1].y

        slope = (x2 - x1) / (y2 - y1)

    # fails due to numerical precision
    # def is_vertical(self):
    #     assert( len(self.data)>=2)

    #     x0=self.data[0].x

    #     the_iterator = iter(self.data)
    #     next(the_iterator)

    #     for P_i in the_iterator:
    #         if P_i.x != x0:
    #             return False

    #     return True

    def get_angle_of_line_segment(self):
        assert (len(self.data) == 2)

        x0 = self.data[0].x
        x1 = self.data[1].x

        y0 = self.data[0].y
        y1 = self.data[1].y

        dy = y1 - y0
        dx = x1 - x0
        theta_rad = math.atan2(dy, dx)
        theta_deg = math.degrees(theta_rad)

        return theta_deg

    def is_vertical(self):
        assert (len(self.data) == 2)

        theta_deg = self.get_angle_of_line_segment()

        tol = 1e-9

        if abs(90 - abs(theta_deg)) < tol:
            return True
        else:
            return False

        # the_iterator = iter(self.data)
        # next(the_iterator)

        # for P_i in the_iterator:
        #    if P_i.x != x0:
        #        return False

        return True

    # def is_horizontal(self):
    #     assert len(self==2)

    #     x0=data[0].x

    #     for P_i in data:
    #         if P_i.x != x0:
    #             return False

    #     return True


# def LineString_to_ListLine(the_linestring):
#     return ListLine(shapely_utils.linestring_to_array_of_points(the_linestring)):

def linestring_to_listline(the_linestring: LineString):
    return ListLine(shapely_utils.linestring_to_array_of_points(the_linestring))

def concatentate_two_linestrings(L1: LineString,L2: LineString):

            
    list_of_points1=L1.to_list_of_points()
    list_of_points2=L2.to_list_of_points()
    
    list_of_points3=list_of_points1+list_of_points2

    L3=ListLine(list_of_points3)

    return L3


########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':
    P1 = Point(0, 25)
    P2 = Point(0, 15)
    P3 = Point(0, 5)

    print("________________")

    L1 = ListLine([P1, P2, P3])

    strafe_length = 5
    L1.extend_right(strafe_length)
    L1.extend_down(20)
    L1.extend_right(strafe_length)
    L1.extend_down(10)
    L1.extend_right(strafe_length)
    L1.extend_down(30)

    print(f"L1={L1}")

    T1 = L1.to_LineString()
    W1 = L1.to_wide_trace(trace_width=10)

    print(f"T1={T1}")
    print(f"W1={W1}")
