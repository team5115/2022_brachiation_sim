import matplotlib.pyplot as plt
import numpy as np
import math

import field_constants
import robot_constants
import robot_hanging_utils
from draw_robot import draw_robot

#####################################################################
#
#
#
#
#
#
#########################################################################


P_a=field_constants.rung_top_points["mid"]
P_b=field_constants.rung_top_points["high"]

L_bd=robot_constants.robot_min_arm_length
w=robot_constants.robot_width



n_points=10
L_ac_values=np.linspace(robot_constants.robot_min_arm_length,robot_constants.robot_max_arm_length,n_points)

L_bd_values=np.linspace(robot_constants.robot_min_arm_length,robot_constants.robot_max_arm_length,n_points)

"""
               B
                \    
        A        \
         \       _D
          \    _/
           \ _/ 
            C 
"""



dx_target=P_b.x-P_a.x
dy_target=P_b.y-P_a.y

print(f"dx_target={dx_target:1.2f}")
print(f"dy_target={dy_target:1.2f}")


for i, L_bd in enumerate(L_bd_values):
   for j, L_ac in enumerate(L_ac_values):



        
        theta=np.arctan((w/2)/L_bd)
        delta_L=L_ac-L_bd

        dx=w*np.cos(theta)+delta_L*np.sin(theta)
        dy=-w*np.sin(theta)+delta_L*np.cos(theta)


        x_error=dx-dx_target
        y_error=dy-dy_target

        print(f"dx={dx}, dy={dy}")
        #title_str=f"dx={dx:1.2f}, dy={dy:1.2f}"
        
        if True:
                robot_data=robot_hanging_utils.calculate_robot_hanging_from_arm_a(P_a, P_b,L_ac,L_bd, w)

                field_data=field_constants.rung_top_points
                
                draw_robot(robot_data,field_data)

                title_str=f"dx={dx:1.2f}, dy={dy:1.2f}"
                plt.title(title_str)
                plt.pause(.1)
                
                
                
