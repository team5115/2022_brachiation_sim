import matplotlib.pyplot as plt
import numpy as np
import math

import field_constants
import robot_constants
import robot_hanging_utils
from draw_robot import draw_robot

#####################################################################
#
# Shows the distance or error from the end of the second arm for various
# configurations
#
#
#
#
#########################################################################


P_a=field_constants.rung_top_points["mid"]
P_b=field_constants.rung_top_points["high"]

L_bd=robot_constants.robot_min_arm_length
w=robot_constants.robot_width

n_points=100
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


        theta=np.arctan((w/2)/L_bd_values)
        delta_L=L_ac_values-L_bd

        dx=w*np.cos(theta)+delta_L*np.sin(theta)
        dy=-w*np.sin(theta)+delta_L*np.cos(theta)


        x_error=dx-dx_target
        y_error=dy-dy_target            

        x_min=np.min(np.abs(x_error))
        y_min=np.min(np.abs(y_error))
        r_min=np.sqrt(x_min**2+y_min**2)


        x_min_index=np.where(np.abs(x_error) ==  x_min)
        L_ac_min=L_ac_values[x_min_index[0]]
        
        tol=(1/12.0)/8.0  # units are feet so if in 1/4 inch we are good

        #tol=(1/12.0)  # units are feet so if in 1/4 inch we are good

        
        if r_min < tol:
          success=True
        else:
          success=False

        
        if True:
                x1=L_ac_values
                y1=x_error
                label1="x_error"

                x2=L_ac_values
                y2=y_error
                label2="y_error"

                plt.clf()
                fig = plt.figure(1)

                ### subplot nrows, ncols, plot #
                ax1 = fig.add_subplot(111)

               
                        

                ax1.plot(x1,y1,label=label1)
                ax1.plot(x2,y2,label=label2)

                if success:
                        #ax1.plot(x_min,y_min,marker='o', color='red')
                        plt.axvline(x=L_ac_min,color='red')
                ax1.set_xlabel(f"L_ab [ft]")
                ax1.set_ylabel(f"dist [ft]")
                ax1.legend(loc='best')

                ax1.grid(True,which='both')
                title_str=f"Error in arm position for L_bd={L_bd:1.2f}, r_min={r_min:1.2f}"
                plt.title(title_str)
                #plt.show()

                plt.draw()
                plt.pause(.1)
