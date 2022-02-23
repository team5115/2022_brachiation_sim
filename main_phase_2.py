import matplotlib.pyplot as plt
import numpy as np

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
w=robot_constants.robot_width
d=w/2


L_ac=robot_constants.robot_min_arm_length
#L_bd=robot_constants.robot_min_arm_length
n_points=20
L_bd_values=np.linspace(robot_constants.robot_min_arm_length,robot_constants.robot_max_arm_length,n_points)



for i, L_bd in enumerate(L_bd_values):

       

        
        robot_data=robot_hanging_utils.calculate_robot_hanging_from_arm_a(P_a, P_b,L_ac,L_bd, w, d)

        field_data=field_constants.rung_top_points
        
        draw_robot(robot_data,field_data)
        plt.pause(.1)
                
                
    
