import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import inspect



# def move_figure(position="top-right"):
#     '''
#     Move and resize a window to a set of standard positions on the screen.
#     Possible positions are:
#     top, bottom, left, right, top-left, top-right, bottom-left, bottom-right
#     '''

#     mgr = plt.get_current_fig_manager()
#     mgr.full_screen_toggle()  # primitive but works to get screen size
#     py = mgr.canvas.height()
#     px = mgr.canvas.width()

#     d = 10  # width of the window border in pixels
#     if position == "top":
#         # x-top-left-corner, y-top-left-corner, x-width, y-width (in pixels)
#         mgr.window.setGeometry(d, 4*d, px - 2*d, py/2 - 4*d)
#     elif position == "bottom":
#         mgr.window.setGeometry(d, py/2 + 5*d, px - 2*d, py/2 - 4*d)
#     elif position == "left":
#         mgr.window.setGeometry(d, 4*d, px/2 - 2*d, py - 4*d)
#     elif position == "right":
#         mgr.window.setGeometry(px/2 + d, 4*d, px/2 - 2*d, py - 4*d)
#     elif position == "top-left":
#         mgr.window.setGeometry(d, 4*d, px/2 - 2*d, py/2 - 4*d)
#     elif position == "top-right":
#         mgr.window.setGeometry(px/2 + d, 4*d, px/2 - 2*d, py/2 - 4*d)
#     elif position == "bottom-left":
#         mgr.window.setGeometry(d, py/2 + 5*d, px/2 - 2*d, py/2 - 4*d)
#     elif position == "bottom-right":
#         mgr.window.setGeometry(px/2 + d, py/2 + 5*d, px/2 - 2*d, py/2 - 4*d)

def resize_figure(position="top-right"):
    '''
    Move and resize a window to a set of standard positions on the screen.
    Possible positions are:
    top, bottom, left, right, top-left, top-right, bottom-left, bottom-right
    '''

    mgr = plt.get_current_fig_manager()
    #mgr.full_screen_toggle()  # primitive but works to get screen size
    #py = mgr.canvas.height()
    #px = mgr.canvas.width()

    window = plt.get_current_fig_manager().window
    screen_x, screen_y = window.wm_maxsize()

    #or
    screen_y = window.winfo_screenheight()
    screen_x = window.winfo_screenwidth()

    px=screen_x
    py=screen_y
    
    d = 10  # width of the window border in pixels
    if position == "top":
        # x-top-left-corner, y-top-left-corner, x-width, y-width (in pixels)
        mgr.window.setGeometry(d, 4*d, px - 2*d, py/2 - 4*d)
    elif position == "bottom":
        mgr.window.setGeometry(d, py/2 + 5*d, px - 2*d, py/2 - 4*d)
    elif position == "left":
        mgr.window.setGeometry(d, 4*d, px/2 - 2*d, py - 4*d)
    elif position == "right":
        mgr.window.setGeometry(px/2 + d, 4*d, px/2 - 2*d, py - 4*d)
    elif position == "top-left":
        mgr.window.setGeometry(d, 4*d, px/2 - 2*d, py/2 - 4*d)
    elif position == "top-right":
        mgr.window.setGeometry(px/2 + d, 4*d, px/2 - 2*d, py/2 - 4*d)
    elif position == "bottom-left":
        mgr.window.setGeometry(d, py/2 + 5*d, px/2 - 2*d, py/2 - 4*d)
    elif position == "bottom-right":
        mgr.window.setGeometry(px/2 + d, py/2 + 5*d, px/2 - 2*d, py/2 - 4*d)

def resize_figure(full_size_factor=0.75, position="top-right"):

    try:
        resize_figure_tkagg(full_size_factor,position)
    except:
        print("In " + inspect.currentframe().f_code.co_name)
        print("An exception occurred")    
        

    
def resize_figure_tkagg(full_size_factor=0.75, position="top-right"):
    '''
    Move and resize a window to a set of standard positions on the screen.
    Possible positions are:
    top, bottom, left, right, top-left, top-right, bottom-left, bottom-right
    '''

    mgr = plt.get_current_fig_manager()
    #mgr.full_screen_toggle()  # primitive but works to get screen size
    #py = mgr.canvas.height()
    #px = mgr.canvas.width()

    window = plt.get_current_fig_manager().window
    screen_x, screen_y = window.wm_maxsize()

    #or
    screen_y = window.winfo_screenheight()
    screen_x = window.winfo_screenwidth()

    px=screen_x
    py=screen_y

    nx=int(px*full_size_factor)
    ny=int(py*full_size_factor)

    ny=nx
    
    d=0
    
    xo=int(d)
    yo=int(4*d)
    window_size_string=f"{nx}x{ny}+{xo}+{yo}"
    mgr.window.geometry(window_size_string)
    
    # d = 10  # width of the window border in pixels
    # if position == "top":
    #     # x-top-left-corner, y-top-left-corner, x-width, y-width (in pixels)
    #     mgr.window.setGeometry(d, 4*d, px - 2*d, py/2 - 4*d)
    # elif position == "bottom":
    #     mgr.window.setGeometry(d, py/2 + 5*d, px - 2*d, py/2 - 4*d)
    # elif position == "left":
    #     mgr.window.setGeometry(d, 4*d, px/2 - 2*d, py - 4*d)
    # elif position == "right":
    #     mgr.window.setGeometry(px/2 + d, 4*d, px/2 - 2*d, py - 4*d)
    # elif position == "top-left":
    #     mgr.window.setGeometry(d, 4*d, px/2 - 2*d, py/2 - 4*d)
    # elif position == "top-right":
    #     mgr.window.setGeometry(px/2 + d, 4*d, px/2 - 2*d, py/2 - 4*d)
    # elif position == "bottom-left":
    #     mgr.window.setGeometry(d, py/2 + 5*d, px/2 - 2*d, py/2 - 4*d)
    # elif position == "bottom-right":
    #     mgr.window.setGeometry(px/2 + d, py/2 + 5*d, px/2 - 2*d, py/2 - 4*d)


########################################
#
#
#   main
#
#
########################################


if __name__ == '__main__':



    print("________________")

    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)
    
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()
    
    fig.savefig("test.png")
    resize_figure_tkagg()
    #plt.axis('equal')
    plt.show()
