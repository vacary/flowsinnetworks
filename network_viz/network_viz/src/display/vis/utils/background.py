#
# Set background color function

def setBackground(renderer):

    """ Set the scene background color

    Args:

        renderer: visualization renderer

    To change the background color, consider the following
    choices:

    1) Gradient Background

        Example:

        renderer.GradientBackgroundOn()

        renderer.SetBackground(color1[0],color1[1],color1[2])

        renderer.SetBackground(color2[0],color2[1],color2[2])

    2) Simple Background

        renderer.SetBackground(color[0],color[1],color[2])

    """

    # Default v.0.1

    renderer.SetBackground(17/255.0, 17/255.0, 17/255.0)

    # Black to gray

    #renderer.GradientBackgroundOn()

    #renderer.SetBackground(0,0,0)

    #renderer.SetBackground2(0.5,0.5,0.5)


    # Lightgray

    #renderer.SetBackground(70/255.0,80/255.0,90/255.0)

    # Gray

    #renderer.SetBackground(47/255.0,47/255.0,47/255.0)

    # Black

    #renderer.SetBackground(5/255.0,5/255.0,20/255.0)

    #renderer.SetBackground(70/255.0,80/255.0,90/255.0)

    return None
