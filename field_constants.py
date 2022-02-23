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
x_low_rung_center=0*ft_

y_mid_rung_top=5*ft_+1.0/4.0*in_
x_mid_rung_center=x_low_rung_center+2*u.imperial.ft

y_high_rung_top=6*ft_+(3+5.0/8.0)*in_
x_high_rung_center=x_mid_rung_center+2*u.imperial.ft

y_traversal_rung_top=7*ft_+7*in_
x_traversal_rung_center=x_high_rung_center+2*u.imperial.ft




PP_low=Point(convert_to_target_units(x_low_rung_center),convert_to_target_units(y_low_rung_top))
PP_mid=Point(convert_to_target_units(x_mid_rung_center),convert_to_target_units(y_mid_rung_top))
PP_high=Point(convert_to_target_units(x_high_rung_center),convert_to_target_units(y_high_rung_top))
PP_traversal=Point(convert_to_target_units(x_traversal_rung_center),convert_to_target_units(y_traversal_rung_top))

rung_top_points={"low":PP_low,
                 "mid":PP_mid,
                 "high":PP_high,
                 "traversal":PP_traversal}
                 



