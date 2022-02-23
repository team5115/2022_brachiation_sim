import astropy
from astropy import units as u
from astropy.table import QTable, Table, Column



def convert_to_target_units(x,target_units=u.imperial.ft):
  """
      converts to the target unit and just gives the value as a float
  """
  return x.to(target_units).value

#####################################################################
#
#
# Rung locations on the 
#
#
#
#########################################################################

#### these are dimensions for the top of the rung
###

#                        *   Traversal
#
#
#                 *      high
#
#            *     mid
#
#       *  low
#
#



ft_=u.imperial.ft
in_=u.imperial.inch

### the 3.0 vs 3 is not necessary in python but good habit for other langauges
y_low_rung_top=4*ft_+3.0/4.0*in_
x_low_rung_top=0*ft_

y_mid_rung_top=5*ft_+1.0/4.0*in_
x_mid_rung_top=x_low_rung_top+2*u.imperial.ft

y_high_rung_top=6*ft_+(3+5.0/8.0)*in_
x_high_rung_top=x_mid_rung_top+2*u.imperial.ft

y_traversal_rung_top=7*ft_+7*in_
x_traversal_rung_top=x_high_rung_top+2*u.imperial.ft




PP_low=Point(convert_to_target_units(x_low_rung_low),convert_to_target_units(y_low_rung_top))
PP_mid=Point(convert_to_target_units(x_mid_rung_mid),convert_to_target_units(y_mid_rung_top))
PP_high=Point(convert_to_target_units(x_high_rung_top),convert_to_target_units(y_high_rung_top))
PP_traversal=Point(convert_to_target_units(x_high_rung_traversal),convert_to_target_units(y_high_rung_traversal))



robot_width=3*u.ft_
robot_min_arm_length=2*u.ft_
robot_max_arm_length=7*u.ft_


robot_width=convert_to_target_units(robot_width)
robot_min_arm_length=convert_to_target_units(robot_min_arm_length)
robot_max_arm_length=convert_to_target_units(robot_max_arm_length)

