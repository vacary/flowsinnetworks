#
# GUI actions - Animation
#
# Functions to the visualization update and animation control
#
# Comment: A change on the slider value will emit a signal to render the scene
# (according to the GUI connections in main.py).
#

def update_for_animation(mw, vis, slider, slider_label):
    if (vis.animation == True):
        update_slider(slider, slider_label, vis)
        vis.timer = vis.timer + 1
        next_timer_value = vis.timer
        if (next_timer_value > vis.globalNumberOfTimeSteps):
            # current time frame is the end frame for the animation
            if (vis.repeat == False):
                # pause at the end of the animation
                vis.timer = vis.globalNumberOfTimeSteps
                pause(mw, vis)
            else:
                #restart animation with a True value for the repeat variable
                vis.timer = 0
                repeat(mw, vis)
 
def update_from_slider(mw, vis, slider, slider_label):
    vis.timer = slider.value()
    update_VTKWidget(vis)
    update_slider(slider, slider_label, vis)
 
def update_VTKWidget(vis):
    vis.update(vis.timer)
    vis.Render()
 
def update_slider(slider, slider_label, vis):
    slider.setSliderPosition(vis.timer)
    ftime = int(vis.timer*vis.time_step*10.0)/10.0
    slider_label.setText(str(ftime))
  
def play(mw, vis):
    vis.animation = True
    vis.repeat = False
    mw.QTimer.start(vis.renderTimeInterval)
 
def repeat(mw, vis):
    vis.animation = True
    vis.repeat = True
    mw.QTimer.start(vis.renderTimeInterval)
 
def pause(mw, vis):
    vis.animation = False
    mw.QTimer.stop()
 
def stop(mw, vis, slider, slider_label):
    vis.animation = False
    mw.QTimer.stop()
    vis.timer = 0
    update_slider(slider, slider_label, vis)
 
def first_frame(mw, vis, slider, slider_label):
    vis.animation = False
    mw.QTimer.stop()
    vis.timer = 0
    update_slider(slider, slider_label, vis)
 
def last_frame(mw, vis, slider, slider_label): 
    vis.animation = False
    mw.QTimer.stop()
    vis.timer = vis.globalNumberOfTimeSteps
    update_slider(slider, slider_label, vis)

def next_frame(mw, vis, slider, slider_label):
    vis.animation = False
    mw.QTimer.stop()
    aux = vis.timer
    if (vis.timer < vis.globalNumberOfTimeSteps):
        aux = vis.timer + 1
    vis.timer = aux
    update_slider(slider, slider_label, vis)

def preceding_frame(mw, vis, slider, slider_label):
    vis.animation = False
    mw.QTimer.stop()
    aux = vis.timer
    if (vis.timer > 0):
        aux = vis.timer - 1
    vis.timer = aux
    update_slider(slider, slider_label, vis)
    