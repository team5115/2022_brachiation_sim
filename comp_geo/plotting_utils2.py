import inspect

import matplotlib.pyplot as plt
import pandas
from shapely.geometry import *

from comp_geo import list_line
from comp_geo import vec2d


def zoom_plot_around_point(ax, Po,dx,dy=None):

    if dy is None:
        dy=dx
        

    xo=Po.x
    x1=xo-dx
    x2=xo+dx

    yo=Po.y
    y1=yo-dy
    y2=yo+dy
        
        
    plt.xlim(x1,x2)
    plt.ylim(y1,y2)
    #ax.xlim(x1,x2)
    #ax.ylim(y1,y2)


    

def plot_coords(ax, ob,color='#999999'):
    # Plot a line's coordinates
    x, y = ob.xy
    ax.plot(x, y, 'o', color=color, zorder=1)

def plot_bounds(ax, ob,color='#999999'):
    # Plot a line's boundary
    x, y = list(zip(*list((p.x, p.y) for p in ob.boundary)))
    ax.plot(x, y, 'o', color=color, zorder=1)

def plot_point(ax, ob,color='#999999',symbol='o'):
    if ob is None:
        return
    # Plot a line's coordinates
    x, y = ob.xy
    ax.plot(x, y, symbol, color=color, zorder=1)

def plot_line(ax, ob, color='#999999',show_points=False,linestyle='solid',linewidth=1):
    
    if (ob.is_empty):
        print("In " + inspect.currentframe().f_code.co_name,end="\t")
        print("Warning: Tried to plot an empty polygon (skipping)")
        return

    # Plot a line
    x, y = ob.xy
    ax.plot(x, y, color=color, alpha=0.7, linewidth=linewidth , linestyle=linestyle, solid_capstyle='round', zorder=2)
    if show_points:
        ax.plot(x, y, 'o', color=color, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
            
def plot_filled_line(ax, ob, color='#999999',show_points=False):
    # Plot a line
    x, y = ob.xy
    #ax.fill(x, y, color=color, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
    ax.fill(x, y, color=color, alpha=0.5)
    if show_points:
        ax.plot(x, y, 'o', color=color, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

def plot_line_with_points(ax, ob, color='#999999'):
    plot_line(ax,ob,color)
    plot_coords(ax,ob,color)

def plot_polygon(ax, poly, color='#999999',show_points=False):
    

    if (poly.is_empty):
        print("In " + inspect.currentframe().f_code.co_name,end="\t")
        print("Warning: Tried to plot an empty polygon (skipping)")
        return

    if (not getattr(poly, "exterior", None)):
        print("In " + inspect.currentframe().f_code.co_name,end="\t")
        print("Warning: Trying to plot a polygon with no exterior (maybe its a line?)")
        return

    #x, y = poly.exterior.coords.xy
    #ax.fill(x, y, color=color, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)    
    plot_filled_line(ax,poly.exterior.coords,color,show_points)

    for hole in poly.interiors:
        plot_coords(ax,hole.coords,color)

def plot_shapely_object(ax,ob,color='#999999',show_points=False,linestyle='solid',linewidth=3):
    if isinstance(ob,list):
        for ob_i in ob:
            plot_shapely_object(ax,ob_i,color)
    elif isinstance(ob,dict):
        for ob_i in ob.values():
            plot_shapely_object(ax,ob_i,color)
    elif isinstance(ob,pandas.core.series.Series):
        ob_as_list=ob.to_list()
        plot_shapely_object(ax,ob_as_list,color)
    elif isinstance(ob,MultiPolygon):
        ob_as_list=list(ob)
        plot_shapely_object(ax,ob_as_list,color)
    elif isinstance(ob,list_line.ListLine):
        plot_shapely_object(ax,ob.to_LineString(),color)
    elif isinstance(ob,LineString):
        plot_line(ax,ob,color,show_points)
    elif isinstance(ob,LinearRing):
        plot_line(ax,ob,color,show_points)
    elif isinstance(ob,Polygon):
        plot_polygon(ax,ob,color,show_points)
    elif isinstance(ob,Point):
        plot_point(ax,ob,color)
    elif ob is None:
        pass
    else:
        print("In " + inspect.currentframe().f_code.co_name)
        print(f"Unhandled type={type(ob)}")
        #print(f"Unhandled type={type(ob)}")
        #raise Exception(f"Unhandled type={type(ob)}")
        #    if type(a)==LineString:
#        plot_line(ax,ob,color)
        
    #ax.axis('equal')
    
def plot_shapely_object_reference(ax,ob,color='teal',show_points=False,linestyle='dashed',linewidth=1):
    if isinstance(ob,list):
        for ob_i in ob:
            plot_shapely_object_reference(ax,ob_i,color=color,show_points=show_points,linestyle=linestyle,linewidth=linewidth)
    elif isinstance(ob,dict):
        for ob_i in ob.values():
            plot_shapely_object_reference(ax,ob_i,color=color,show_points=show_points,linestyle=linestyle,linewidth=linewidth)
    elif isinstance(ob,LineString):
        plot_line(ax,ob,color,show_points,linestyle=linestyle,linewidth=linewidth)
    elif isinstance(ob,LinearRing):
        plot_line(ax,ob,color,show_points,linestyle=linestyle,linewidth=linewidth)
    elif isinstance(ob,Polygon):
        assert(False)
        ob_sub=value.exterior
        plot_line(ax,ob_sub,show_points,linestyle=linestyle,linewidth=linewidth)
    elif isinstance(ob,Point):
        plot_point(ax,ob,color)
    #elif ob is None:
    #    pass
    else:
        print("In " + inspect.currentframe().f_code.co_name)
        print(f"Unhandled type={type(ob)}")
        #raise Exception(f"Unhandled type={type(ob)}")
        #    if type(a)==LineString:
#        plot_line(ax,ob,color)
        
    #ax.axis('equal')
    
def add_text_labels_as_polar_array(ax1, r_0, list_of_labels):

    for sextant_no, label in enumerate(list_of_labels):
        #print(f"i={i} = ",end='')
        #print(f"x={x_i}")
        
        n_sextants=len(list_of_labels)
        dtheta=360/n_sextants
        #l_hexagon=weo.geo.misc_derived_values["l_hexagon"]*1.10
        v_unit=vec2d.v_right    
        v_0=r_0*v_unit
        
        theta_deg=(dtheta*(sextant_no))+dtheta/2
        v_i=vec2d.rotate_arbitrary(v_0,theta_deg)

        x=v_i[0]
        y=v_i[1]

        #print(f"label={label}")
        
        s=f'{label}'
        ax1.text(x,y, s,{'ha': 'center', 'va': 'center'}, rotation=theta_deg+90,color='black')


