import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy
from astropy import units as u
from astropy.table import QTable, Table, Column
import math
import numpy as np
import matplotlib.pyplot as plt
import copy
import sys
#import config_params
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
from list_line import *

# importing movie py libraries
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
 
# importing editor from movie py
from moviepy.editor import *
#import boundary_intersection_utils


def calculate_frame(P_b,L_ac,L_bd, w, d):
        """
               B
                \    
        A        \
         \       _D
          \    _/
           \ _/ 
            C 
        """

        #theta_ac_rad=math.atan2(d,L_ac)
        theta_bd_rad=math.atan2(d,L_bd)
        
        #theta_ac_deg=math.degrees(theta_ac_rad)
        theta_bd_deg=math.degrees(theta_bd_rad)

        alpha_bd_deg=90-theta_bd_deg
        
        #theta_bd_deg=45/2
        #theta_ac_deg=0
        
        v_bd=vec2d.rotate_arbitrary(v_down,(theta_bd_deg))
        #v_ac=vec2d.rotate_arbitrary(v_down,(90-theta_ac_deg))
        
        P_d=point_utils.move_point_along_vector(P_b,v_bd, L_bd)
        v_dc=vec2d.rotate_arbitrary(v_bd,-90)

        P_cg=point_utils.move_point_along_vector(P_d,v_dc, w/2)
        P_c=point_utils.move_point_along_vector(P_d,v_dc, w)
        
        v_ca=vec2d.rotate_arbitrary(v_dc,90)
        v_ac=-v_ca
        
        P_a=point_utils.move_point_along_vector(P_c,v_ac, L_ac)
        
        #L_ac=linestring_utils.start_line(P1)
        
        ll_ac = ListLine([P_a, P_c])
        ll_cd = ListLine([P_c, P_d])
        ll_bd = ListLine([P_b, P_d])
        
        data={"P_a":P_a,
              "P_b":P_b,
              "P_c":P_c,
              "P_d":P_d,
              "P_cg":P_cg,
              "ll_ac":ll_ac,
              "ll_cd":ll_cd,
              "ll_bd":ll_bd,
              "v_bd":v_bd,
              "v_dc":v_dc,
              "v_ac":v_ac,
              "theta_bd_deg":theta_bd_deg,
              "alpha_bd_deg":alpha_bd_deg              
              }

        return data

def make_frame(data):        
        P_a=data["P_a"]
        P_b=data["P_b"]
        P_c=data["P_c"]
        P_d=data["P_d"]
        P_cg=data["P_cg"]

        ll_ac=data["ll_ac"]
        ll_cd=data["ll_cd"]
        ll_bd=data["ll_bd"]

        v_ac=data["v_ac"]
        v_dc=data["v_dc"]
        v_bd=data["v_bd"]

        alpha_bd_deg=data["alpha_bd_deg"]
        # theta_deg1=vec2d.angle_between_vectors_degrees(v_ac,v_dc)
        # theta_deg2=vec2d.angle_between_vectors_degrees(v_dc,v_bd)

        # print(f"theta_deg1={theta_deg1}")
        # print(f"theta_deg2={theta_deg2}")

        graff=True
        graff_pause=True
        if graff:
                # duration of the video
                duration = 2
 
                # matplot subplot
                #fig, ax1 = plt.subplots()
 
                plt.clf()
                fig = plt.figure(1)

                ### subplot nrows, ncols, plot #
                ax1 = fig.add_subplot(111)


                length_scale=1
                #arrow_plotting_utils.plot_arrow(ax1, P_a, v_ac, length_scale,color="black", plot_reference_line=False)
                #arrow_plotting_utils.plot_arrow(ax1, P_b, v_bd, length_scale,color="black", plot_reference_line=False)
                #arrow_plotting_utils.plot_arrow(ax1, P_d, v_dc, length_scale,color="black", plot_reference_line=False)
                #arrow_plotting_utils.plot_arrow(ax1, P_a, v_ac, length_scale,color="black", plot_reference_line=False)

                arrow_plotting_utils.plot_arrow(ax1, P_cg, v_down, length_scale,color="red", plot_reference_line=False)
                arrow_plotting_utils.plot_arrow(ax1, P_b, -v_down, length_scale,color="red", plot_reference_line=False)

                plotting_utils2.plot_shapely_object(ax1, PP_a, 'black', 'O')
                plotting_utils2.plot_shapely_object(ax1, PP_b, 'black', 'O')

                plotting_utils2.plot_shapely_object(ax1, P_a, 'black', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_b, 'blue', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_c, 'blue', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_d, 'blue', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_cg, 'red', 'x')

                # ax2 = fig.add_subplot(122)
                plotting_utils2.plot_shapely_object(ax1, ll_ac,'blue')
                plotting_utils2.plot_shapely_object(ax1, ll_cd,'blue')
                plotting_utils2.plot_shapely_object(ax1, ll_bd, 'blue')

                
                title_str = f"w={w:1.2f} L_ac={L_ac:1.2f} L_bd={L_bd:1.2f} alpha_bd={alpha_bd_deg:1.2f}"
                plt.title(title_str)

                #axes.get_ylim()

                plt.xlim([-1,10])
                plt.ylim([-1,10])
                #ax1.axis('equal')
                ax1.grid(True,which='both')
                ax1.set_aspect('equal', 'box')

                # if graff_pause:
                #         plt.show()


                #         ax.view_init(30, angle)
                plt.draw()
                #plt.pause(.1)


            # # clear
            # ax.clear()

            # # plotting line
            # ax.plot(x, np.sinc(x**2) + np.sin(x + 2 * np.pi / duration * t), lw = 3)
            # ax.set_ylim(-1.5, 2.5)

            # returning numpy image
        return [fig,ax1]

 
#####################################################################
#
#
#
#
#
#
#########################################################################

v_down=vec2d.v_down

PP_a=Point(0, 5)
PP_b=Point(3, 7)

P_b=PP_b

L_ac=5

w=3
d=w/2

#L_bd=7
#L_bd_values=[7,6,5,4,2]

L_bd_values=np.linspace(7,2,30)


frames=[]
for i, L_bd in enumerate(L_bd_values):

        # print(f"i={i} = ",end='')
        # print(f"x={x_i}")
        data=calculate_frame(P_b,L_ac,L_bd, w, d)        

        [fig,ax1]=make_frame(data)


        f=mplfig_to_npimage(fig)
        frames.append(f)



clip = ImageSequenceClip(frames, fps = 10)
  
# showing  clip 
clip.ipython_display(width = 360) 
