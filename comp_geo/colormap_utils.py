import matplotlib.pyplot as plt
from csd import list_utils
from matplotlib.lines import Line2D
  
def generate_colormap_via_lut_for_uniques(all_values):
    theta_u=list_utils.unique(all_values)

    #if len(theta_u) < 5:
    #    colors=['red','blue','green','black']
    if len(theta_u) < 9:
        #colors=plt.get_cmap('Set2')
        colors=plt.get_cmap('Set1')
        colors=plt.get_cmap('tab10')
    else:
        colors=plt.get_cmap('tab20')
        
    my_colormap=dict()
    for i, x_i in enumerate(theta_u):
        #print(f"i={i} = ",end='')
        #3print(f"x={x_i}")
        my_colormap[x_i]=colors(i)
        

    return my_colormap

def build_legend(data):
    """
    Build a legend for matplotlib plt from dict
    """
    legend_elements = []
    for key in data:
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label=key,
                                        markerfacecolor=data[key], markersize=10))
    return legend_elements
