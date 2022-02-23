
import math

import comp_geo.vec2d as vec2d
from comp_geo import point_utils
from comp_geo.list_line import ListLine as ListLine


def calculate_robot_hanging_from_arm_a(P_a, P_b,L_ac,L_bd, w, d):
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
        theta_ac_rad=math.atan2(d,L_ac)        
        theta_ac_deg=math.degrees(theta_ac_rad)

        v_ac=vec2d.rotate_arbitrary(vec2d.v_down,-theta_ac_deg)
        
        P_c=point_utils.move_point_along_vector(P_a,v_ac, L_ac)
        v_cd=vec2d.rotate_arbitrary(v_ac,90)
        v_dc=-v_cd
        
        P_cg=point_utils.move_point_along_vector(P_c,v_cd, w/2)
        P_d=point_utils.move_point_along_vector(P_c,v_cd, w)
        
        v_db=vec2d.rotate_arbitrary(v_cd,90)
        v_bd=-v_db
        
        P_b=point_utils.move_point_along_vector(P_d,v_db, L_bd)
        
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
              # "w":w,
              # "L_ac":L_ac,
              # "L_bd":L_bd,
              # "alpha_bd_deg":alpha_bd_deg,
              # "theta_bd_deg":theta_bd_deg
              }

        return data

def calculate_robot_hanging_from_arm_b(P_a, P_b, L_ac,L_bd, w, d):
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
        
        v_bd=vec2d.rotate_arbitrary(vec2d.v_down,(theta_bd_deg))
        #v_ac=vec2d.rotate_arbitrary(v_down,(90-theta_ac_deg))
        
        P_d=point_utils.move_point_along_vector(P_b,v_bd, L_bd)
        v_dc=vec2d.rotate_arbitrary(v_bd,-90)

        P_cg=point_utils.move_point_along_vector(P_d,v_dc, w/2)
        P_c=point_utils.move_point_along_vector(P_d,v_dc, w)
        
        v_ca=vec2d.rotate_arbitrary(v_dc,90)
        v_ac=-v_ca
        
        P_a=point_utils.move_point_along_vector(P_c,v_ac, L_ac)

        #tilt_angle=vec2d.angle_between_vectors_degrees(v_cd,vec2d.v_right):
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
              # "w":w,
              # "L_ac":L_ac,
              # "L_bd":L_bd,
              #"tilt_angle":tilt_angle,
              # "alpha_bd_deg":alpha_bd_deg,
              # "theta_bd_deg":theta_bd_deg
              }

        return data

