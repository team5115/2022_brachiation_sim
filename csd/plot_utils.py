import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import matplotlib.pyplot as plt

import itertools

def set_logscale_with_grid(ax1):
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.grid(True,which='both')
    #ax1.grid(True,which='minor')


def get_iterable_colors_and_markers():


    """
        Generates a rotatatable list of markers and colors

        [markers,colors]=plot_utils.get_iterable_colors_and_markers()
        ax1.plot(x1,y1,marker=next(markers),color=color_i,linestyle="None")
       

    """    
    good_marker_styles=["o","v","^","<",">","8","s","p","P","*","h","H","+","x","X","D","d","1","2","3","4",4,5,6,7,8,9,10,11]
    markers = itertools.cycle(good_marker_styles)
    
    #https://gist.github.com/thriveth/8560036
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                      '#f781bf', '#a65628', '#984ea3',
                      '#999999', '#e41a1c', '#dede00']
    
    colors=itertools.cycle(CB_color_cycle)
    
    return [markers,colors]

#https://www.delftstack.com/howto/matplotlib/how-to-place-legend-outside-of-the-plot-in-matplotlib/

# def plot_place_legend_outside_plot():
    
#     lg = plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

#     # plt.savefig('example.png', 
#     #             dpi=300, 
#     #             format='png', 
#     #             bbox_extra_artists=(lg,), 
#     #             bbox_inches='tight')

# It places the legend at location (1.05, 1) in the axes coordinate. (0, 0) is the lower-left corner, and (1.0, 1.0) is the upper right corner of the axes coordinate.

# The actual size and location of the legend bounding box are defined with the 4-tuple parameter of bbox_to_anchor and loc in the plt.legend.

# plt.legend(bbox_to_anchor=(x0, y0, width, height), loc=)
# width and height are the width and the height of the legend box, and (x0, y0) is the coordinate of the loc of the bounding box.
#bbox_extra_artists and bbox_inches to Prevent Legend Box From Being Cropped

#xx-small
#x-small
#small
#medium
#large
#x-large
#xx-large

def place_legend_outside_plot(ax1,legend_is_outside_plot=True, legend_location='best',legend_fontsize=None):

           if legend_is_outside_plot:
                # Shrink current axis by 20%
                box = ax1.get_position()
                ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                
                # Put a legend to the right of the current axis
                lg=ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
           else:
                lg=ax1.legend(loc=legend_location)


           if legend_fontsize is not None:     
               #plt.legend(legend_fontsize)
                plt.legend(fontsize=legend_fontsize)
                
           #plt.tight_layout()


           return lg


#plt.savefig("../generated_files/figs/shielding.pdf") 
def save_figure(basename,data_dir="../generated_files/figs", do_both_png_and_pdf=True):
    
    full_filename=os.path.join(data_dir,basename)
    print(f"Figure being saved to {full_filename}")
    if do_both_png_and_pdf:
               plt.savefig(full_filename+".png", dpi=300, format='png')
               plt.savefig(full_filename+".pdf", format='pdf')


    # bbox_extra_artists=(lg,), 
    # bbox_inches='tight')
    
    #plt.savefig('example.png', 
    #            dpi=300, 
    #            format='png', 
    #            bbox_extra_artists=(lg,), 
    #            bbox_inches='tight')


    #plt.savefig('example.png', 
    #            dpi=300, 
    #            format='png', 
    #            bbox_extra_artists=(lg,), 
    #            bbox_inches='tight')
#plt.savefig("../generated_files/figs/shielding.pdf") 

def save_figure_extra_artist(basename,data_dir="../generated_files/figs",artist=None):

    full_filename=os.path.join(data_dir,basename)
    print(f"Figure being saved to {full_filename}")
    plt.savefig(full_filename+".png", 
                dpi=300, 
                format='png', 
                bbox_extra_artists=(artist,), 
                bbox_inches='tight')

    plt.savefig(full_filename+".pdf", 
                format='pdf', 
                bbox_extra_artists=(artist,), 
                bbox_inches='tight')

    #plt.savefig('example.png', 
    #            dpi=300, 
    #            format='png', 
    #            bbox_extra_artists=(artist,), 
    #            bbox_inches='tight')

def quick_plot_1d(x):
        plt.clf()
        fig = plt.figure(1)

        ### subplot nrows, ncols, plot #
        ax1 = fig.add_subplot(111)
        ax1.plot(x)


        ax1.grid(True,which='both')
        #ax1.grid(True,which='minor')

        #plt.axis('equal')

        # #title_str=inspect.currentframe().f_code.co_name
        # title_str=f"Title String"
        # plt.title(title_str)
        plt.show()


#https://stackoverflow.com/questions/45729092/make-interactive-matplotlib-window-not-pop-to-front-on-each-update-windows-7/45734500#45734500

#If changing the backend is not an option, the following might
#help. The cause of the window constantly popping up to the front
#comes from plt.pause calling plt.show() internally. You therefore
#implement you own pause function, without calling show. This requires
#to be in interactive mode plt.ion() first and then at least once call
#plt.show(). Afterwards you may update the plot with the custom
#mypause function as shown below.

def my_pause(interval=0.001):
    return my_pause_v3(interval)

def my_pause_v1(interval=0.001):
    backend = plt.rcParams['backend']
    if backend in matplotlib.rcsetup.interactive_bk:
        figManager = matplotlib._pylab_helpers.Gcf.get_active()
        if figManager is not None:
            canvas = figManager.canvas
            if canvas.figure.stale:
                canvas.draw()
            canvas.start_event_loop(interval)
            return

def my_pause_v2(interval):
    manager = plt._pylab_helpers.Gcf.get_active()
    if manager is not None:
        canvas = manager.canvas
        if canvas.figure.stale:
            canvas.draw_idle()        
        #plt.show(block=False)
        canvas.start_event_loop(interval)
    else:
        time.sleep(interval)
        
def my_pause_v3(interval=0.001):
    fig.canvas.draw_idle()
    fig.canvas.start_event_loop(interval)
