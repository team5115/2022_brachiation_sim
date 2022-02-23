import matplotlib.pyplot as plt
import numpy as np

import field_constants
import robot_constants
import robot_hanging_utils
from draw_robot import draw_robot



w=robot_constants.robot_width
P_a=field_constants.rung_top_points["mid"]
P_b=field_constants.rung_top_points["high"]


#####################################################################
#
#
#
#  Phase 1
#
#
#########################################################################


L_bd=robot_constants.robot_min_arm_length
n_points=20
L_ac_values=np.linspace(robot_constants.robot_max_arm_length,robot_constants.robot_min_arm_length,n_points)



for i, L_ac in enumerate(L_ac_values):

       

        
        robot_data=robot_hanging_utils.calculate_robot_hanging_from_arm_a(P_a, P_b,L_ac,L_bd, w)

        field_data=field_constants.rung_top_points
        
        draw_robot(robot_data,field_data)
        plt.pause(.1)
                
                
#####################################################################
#
#
#
#  Phase 2
#
#
#########################################################################
    
L_ac_previous_phase=L_ac
L_bd_previous_phase=L_bd

L_ac=L_ac_previous_phase
n_points=20
L_bd_values=np.linspace(L_bd_previous_phase,robot_constants.robot_max_arm_length,n_points)



for i, L_bd in enumerate(L_bd_values):

       

        
        robot_data=robot_hanging_utils.calculate_robot_hanging_from_arm_a(P_a, P_b,L_ac,L_bd, w)

        field_data=field_constants.rung_top_points
        
        draw_robot(robot_data,field_data)
        plt.pause(.1)
                
                
#####################################################################
#
#
#
#  Phase 3
#
#
#########################################################################
    



L_ac=5
n_points=10
L_bd_values=np.linspace(robot_constants.robot_max_arm_length,robot_constants.robot_min_arm_length,n_points)



for i, L_bd in enumerate(L_bd_values):
        
        robot_data=robot_hanging_utils.calculate_robot_hanging_from_arm_b(P_a, P_b,L_ac,L_bd, w)

        field_data=field_constants.rung_top_points
        
        draw_robot(robot_data,field_data)
        plt.pause(.1)
                
                
    
