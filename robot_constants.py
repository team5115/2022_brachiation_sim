import astropy
from astropy import units as u
from astropy.table import QTable, Table, Column

from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import GeometryCollection
from shapely.geometry import MultiPolygon

from unit_utils import convert_to_target_units

ft_=u.imperial.ft
in_=u.imperial.inch


robot_width=3*ft_
robot_min_arm_length=2*ft_
robot_max_arm_length=7*ft_


##########################
##
## convert the units to pure numbers
##
###########################

robot_width=convert_to_target_units(robot_width)
robot_min_arm_length=convert_to_target_units(robot_min_arm_length)
robot_max_arm_length=convert_to_target_units(robot_max_arm_length)

