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

from comp_geo import *

import inspect
from csd import arrow_plotting_utils
#import figure_utils
#from list_line import *

# importing movie py libraries
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
 
# importing editor from movie py
from moviepy.editor import *
#import boundary_intersection_utils


def draw_robot(robot_data,field_data):        
        P_a=robot_data["P_a"]
        P_b=robot_data["P_b"]
        P_c=robot_data["P_c"]
        P_d=robot_data["P_d"]
        P_cg=robot_data["P_cg"]

        ll_ac=robot_data["ll_ac"]
        ll_cd=robot_data["ll_cd"]
        ll_bd=robot_data["ll_bd"]

        v_ac=robot_data["v_ac"]
        v_dc=robot_data["v_dc"]
        v_bd=robot_data["v_bd"]

        w=robot_data["w"]
        L_ac=robot_data["L_ac"]
        L_bd=robot_data["L_bd"]
        alpha_bd_deg=robot_data["alpha_bd_deg"]
        
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



                arrow_plotting_utils.plot_arrow(ax1, P_cg, vec2d.v_down, length_scale,color="red", plot_reference_line=False)
                arrow_plotting_utils.plot_arrow(ax1, P_b, -vec2d.v_down, length_scale,color="red", plot_reference_line=False)

                

                plotting_utils2.plot_shapely_object(ax1, P_a, 'black', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_b, 'blue', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_c, 'blue', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_d, 'blue', 'x')
                plotting_utils2.plot_shapely_object(ax1, P_cg, 'red', 'x')

                # ax2 = fig.add_subplot(122)
                plotting_utils2.plot_shapely_object(ax1, ll_ac,'blue')
                plotting_utils2.plot_shapely_object(ax1, ll_cd,'blue')
                plotting_utils2.plot_shapely_object(ax1, ll_bd, 'blue')


                
                
                #plotting_utils2.plot_shapely_object(ax1, PP_b, 'black', 'O')

                for label, P_rung_top in field_data.items():
                        #print(f"key={key} = ",end='')
                        #print(f"value={value}")
                        plotting_utils2.plot_shapely_object(ax1, P_rung_top, 'black', 'O')
                
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

 
