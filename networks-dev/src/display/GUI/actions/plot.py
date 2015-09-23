#
# GUI actions - Plot
#
# Functions to manage the simulation data plot by edge
#

#Standard library imports
import unicodedata
import HTMLParser

def call_to_plot_dialog(mw, vis):
    if (vis.TYPE in ['network']):
        time = vis.timer*vis.time_step
        mw.dialog_plot.update(time)
    
def edge_data_plot_update(fig, current_frame_time ,edge_dict):
    
    """ Plots for inflow/outflow rates and queue levels
    
    The plots are generated with matplotlib using the 
    simulation data for the selected edge which stored 
    in the dictionary considered argument.
    
    Args:

        fig: matplotlib figure.
        current_frame_time: current time at the moment
        of the graph generation. 
        edge_dict: dictionary with simulation data for
        the selected edge.
    
    Returns:
    
        The figure title. If the graph source is a osm
        file (openstreetmap file) the title will show
        the name of the street associated to the selected
        edge.
    
    """
    
    # Get edge capacity
    
    edge_capacity = edge_dict['capacity']
    
    # Compute max value reference for the inflow/outflow plots
    
    max_fe_1 = max(edge_dict['f_e_plus_overtime'] )
    max_fe_2 = max(edge_dict['f_e_minus_overtime'] )
    max_fe_3 = edge_capacity 
    
    y_lim = 1.05*max(max_fe_1,max_fe_2,max_fe_3)
    
    # z_e_overtime arrays
    
    ax = fig.add_subplot(311)
    x_data = edge_dict['switching_times']
    y_data = edge_dict['z_e_overtime']
    ax.plot(x_data,y_data,'b')
    
    time = current_frame_time
    ax.axvline(x=time,color='r')
    ax.set_title('z_e overtime')
    
    # f_e_plus_overtime
       
    vx = edge_dict['ntail_label_overtime']
    vy = edge_dict['f_e_plus_overtime'] 
       
    x_data = []
    y_data = []
       
    for i in xrange(len(vx)-1):
        x_data.append(vx[i])
        y_data.append(vy[i])
        x_data.append(vx[i+1])
        y_data.append(vy[i])
    
    ax = fig.add_subplot(312)
    ax.plot(x_data,y_data,'b')
    ax.plot([time,time],[0,y_lim],'r',linewidth="2")
    ax.plot([0,max(x_data)],[edge_capacity,edge_capacity],'g')
    ax.set_title('f_e_plus_overtime')
    
    # f_e_minus_overtime
       
    vx = edge_dict['nhead_label_overtime']
    vy = edge_dict['f_e_minus_overtime']
       
    x_data = []
    y_data = []
       
    for i in xrange(len(vx)-1):
        x_data.append(vx[i])
        y_data.append(vy[i])
        x_data.append(vx[i+1])
        y_data.append(vy[i])
    
    ax = fig.add_subplot(313)
    ax.plot(x_data,y_data,'b')
    ax.plot([time,time],[0,y_lim],'r',linewidth="2")
    ax.plot([0,max(x_data)],[edge_capacity,edge_capacity],'g')
    ax.set_title('f_e_minus_overtime')
    
    title = "Simulation results for edge %s" %( edge_dict['selected_edge'] )
    
    if (edge_dict['name'] != '[]'):
        name = HTMLParser.HTMLParser().unescape(edge_dict['name'])
        name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
        title = title +" - "+name 
        
    return title
