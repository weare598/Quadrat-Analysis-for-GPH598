# Function "rectangle" does quadrat analysis using rectangles.
def rectangle(point_num, recwidth, recheight, list_points = None):

    from random import randrange as rd
    import matplotlib.pyplot as plt
    import numpy as np

    x=[]
    y=[]
    for i in xrange(point_num):
        x.append(rd(0, 100, 0.01))
        y.append(rd(0, 100, 0.01))

    if list_points != None:
        x=[]
        y=[]
        for point in list_points:
            x.append(point[0])
            y.append(point[1])


    minx = min(x) # Get the minimum x value in the entire dataset
    maxx = max(x) # Get the maximum x value in the entire dataset
    miny = min(y) # Get the minimum y value in the entire dataset
    maxy = max(y) # Get the maximum y value in the entire dataset

    fig = plt.figure()
    plt.plot(x,y,'+')
    plt.plot(min(x), min(y), 'o', color='black') # Plot the SW cornor of the smallest rectangle
    plt.plot(max(x), min(y), 'o', color='black') # SE cornor
    plt.plot(max(x), max(y), 'o', color='black') # NE cornor
    plt.plot(min(x), max(y), 'o', color='black') # NW cornor

    # Draw the smallest rectangle for the entire dataset
    plt.plot([minx, maxx], [miny, miny], '--', lw=.5, color='black') # Draw a line between the SW and SE cornors
    plt.plot([maxx, maxx], [miny, maxy], '--', lw=.5, color='black') # Draw a line between the SE and NE cornors
    plt.plot([maxx, minx], [maxy, maxy], '--', lw=.5, color='black') # Draw a line between the NE and NW cornors
    plt.plot([minx, minx], [maxy, miny], '--', lw=.5, color='black') # Draw a line between the NW and SW cornors

    # Create a list of x-nods on the x-axis and a list of y-nods on the y-axis based on the width and height of the defined rectangle
    xnods = np.arange(minx, maxx+recwidth, recwidth)
    ynods = np.arange(miny, maxy+recheight, recheight)

    # Calculate the x- and y-coordinates of the middle point in each rectangle
    xmidpoints = []
    ymidpoints = []
    for i in xrange(len(xnods)-1):
        xmidpoints.append((xnods[i]+xnods[i+1])/2.)
    for i in xrange(len(ynods)-1):
        ymidpoints.append((ynods[i]+ynods[i+1])/2.)

    # Use a list "rectangles" to store the number of points in each rectangle
    rectangles = []

    # Calculate the x- and y-coordinates of four cornors for each rectangle and then draw the grid
    for i in xrange(len(xmidpoints)):
        for j in xrange(len(ymidpoints)):
            # SW cornor
            SW_x = xmidpoints[i] - recwidth/2.
            SW_y = ymidpoints[j] - recheight/2.
            # SE cornor
            SE_x = xmidpoints[i] + recwidth/2.
            SE_y = ymidpoints[j] - recheight/2.
            # NE cornor
            NE_x = xmidpoints[i] + recwidth/2.
            NE_y = ymidpoints[j] + recheight/2.
            # NW cornor
            NW_x = xmidpoints[i] - recwidth/2.
            NW_y = ymidpoints[j] + recheight/2.
            # Draw the rectangle
            plt.plot([SW_x, SE_x], [SW_y, SE_y], lw=2, color='black')
            plt.plot([SE_x, NE_x], [SE_y, NE_y], lw=2, color='black')
            plt.plot([NE_x, NW_x], [NE_y, NW_y], lw=2, color='black')
            plt.plot([NW_x, SW_x], [NW_y, SW_y], lw=2, color='black')

            # Update the "rectangles" list
            # Use "q" to store the number of points
            q = 0
            for p in xrange(len(x)):
                if x[p]>= SW_x and x[p]<=SE_x and y[p]>= SW_y and y[p]<=NE_y:
                    q+=1
                    x[p] = []
                    y[p] = []
            rectangles.append(q)

    # Print out the "rectangles" list
    print 'There are', len(rectangles) ,'quadrats in total.'
    for i in xrange(len(rectangles)):
        print 'Quadrat', i+1, 'has', rectangles[i], 'points.'

    ax = fig.gca()
    ax.set_xticks(np.arange(minx-recwidth, maxx+recwidth*2, recwidth))
    ax.set_yticks(np.arange(miny-recheight, maxy+recheight*2, recheight))
    plt.show()

    # This function has two returns. "rec_num" is the total number of rectangles.
    # "rectangles" is the list that stores the number of points in each rectangle.
    return len(rectangles), rectangles


# Function "hexagon" does quadrat analysis using hexagons.
def hexagon(point_num, side):
    from random import randrange as rd
    import matplotlib.pyplot as plt
    import numpy as np
    from math import sqrt

    x=[]
    y=[]
    for i in xrange(point_num):
        x.append(rd(0,101,1))
        y.append(rd(0,101,1))

    minx = min(x) # Get the minimum x value in the entire dataset
    maxx = max(x) # Get the maximum x value in the entire dataset
    miny = min(y) # Get the minimum y value in the entire dataset
    maxy = max(y) # Get the maximum y value in the entire dataset

    fig = plt.figure()
    plt.plot(x, y, '+')
    plt.plot(minx, miny, 'o', color='black') # Plot the SW cornor of the smallest rectangle
    plt.plot(maxx, miny, 'o', color='black') # SE cornor
    plt.plot(maxx, maxy, 'o', color='black') # NE cornor
    plt.plot(minx, maxy, 'o', color='black') # NW cornor

    # Draw the smallest rectangle for all the points
    plt.plot([minx, maxx], [miny, miny], '--', lw=.5, color='black') # Draw a line between the SW and SE cornors
    plt.plot([maxx, maxx], [miny, maxy], '--', lw=.5, color='black') # Draw a line between the SE and NE cornors
    plt.plot([maxx, minx], [maxy, maxy], '--', lw=.5, color='black') # Draw a line between the NE and NW cornors
    plt.plot([minx, minx], [maxy, miny], '--', lw=.5, color='black') # Draw a line between the NW and SW cornors

    # This below determines the number of hexagon columns, or the easternmost point where the hexagons can reach
    column_num = 1            # Starting from the first column and count to the right side
    x_tip = minx + 0.5*side   # x_tip variable controls the farthest point that the current column can reach
    while x_tip < maxx:       # x_tip is compared with the maxmium x value to see if it needs to continue
        x_tip += 1.5*side
        column_num += 1

    length_x = column_num     # Use length_x to represent the number of columns

    # This below determines the number of hexagon rows for odd columns, or the northernmost point where the odd column hexagons can reach
    row_num = 1
    up_lmt = miny + side/2.*sqrt(3)
    while up_lmt < maxy:
        up_lmt += side*1.*sqrt(3)
        row_num += 1

    length_y_odd = row_num

    # This below determines the number of hexagon rows for even columns, or the northernmost point where the even column hexagons can reach
    row_num = 1
    up_lmt = miny + side*1.*sqrt(3)
    while up_lmt < maxy:
        up_lmt += side*1.*sqrt(3)
        row_num += 1

    length_y_even = row_num

    # Define the starting point (minx, miny) where to build the first hexagon
    start_x = minx*1.
    start_y = miny*1.
    mid_x = start_x
    mid_y = start_y
    midpoints = [] # Used to store all the coordinates of center points for all the hexagons
    # i controls columns(x's); j controls rows (y's)
    # Starting from the SW cornor and then build up to the north
    for i in xrange(length_x):
        if i%2 == 0:
            for j in xrange(length_y_odd):
                midpoints.append([mid_x, mid_y])
                mid_y += side*1.*sqrt(3)
            mid_y = start_y + side/2.*sqrt(3)
        if i%2 == 1:
            for j in xrange(length_y_even):
                midpoints.append([mid_x, mid_y])
                mid_y += side*1.*sqrt(3)
            mid_y = start_y
        mid_x += 1.5*side

    # Use "hexagons" list to store the number of points in each hexagon
    hexagons = []
    for midpoint in midpoints:
            # Calculate the coordinates of six hexagon vertex
            NE_x = midpoint[0]*1. + side/2.
            NE_y = midpoint[1]*1. + side/2.*sqrt(3)
            E_x  = midpoint[0]*1. + side*1.
            E_y  = midpoint[1]*1.
            SE_x = midpoint[0]*1. + side/2.
            SE_y = midpoint[1]*1. - side/2.*sqrt(3)
            SW_x = midpoint[0]*1. - side/2.
            SW_y = midpoint[1]*1. - side/2.*sqrt(3)
            W_x  = midpoint[0]*1. - side*1.
            W_y  = midpoint[1]*1.
            NW_x = midpoint[0]*1. - side/2.
            NW_y = midpoint[1]*1. + side/2.*sqrt(3)

            # Draw the hexagon
            plt.plot([NE_x, E_x], [NE_y, E_y], lw=2, color='black')
            plt.plot([E_x, SE_x], [E_y, SE_y], lw=2, color='black')
            plt.plot([SE_x, SW_x], [SE_y, SW_y], lw=2, color='black')
            plt.plot([SW_x, W_x], [SW_y, W_y], lw=2, color='black')
            plt.plot([W_x, NW_x], [W_y, NW_y], lw=2, color='black')
            plt.plot([NW_x, NE_x], [NW_y, NE_y], lw=2, color='black')

            # Calculate the slope (a's) and intercept (b's) between each two hexagon vertex
            a1 = (NE_y - E_y)/(NE_x - E_x)*1. # The slope of line NE-E
            b1 = NE_y - a1 * NE_x             # The intercept of line NE-E
            a2 = (E_y - SE_y)/(E_x - SE_x)*1. # The slope of line E-SE
            b2 = E_y - a2 * E_x               # The intercept of line E-SE
            a3 = 0                            # The slope of line SE-SW is 0
            b3 = SE_y                         # The intercept of line SE-SW is the y-coordinate of either one
            a4 = (SW_y - W_y)/(SW_x - W_x)*1. # The slope of line SW-W
            b4 = SW_y - a4 * SW_x             # The intercept of line SW-W
            a5 = (W_y - NW_y)/(W_x - NW_x)*1. # The slope of line W-NW
            b5 = W_y - a5 * W_x               # The intercept of line W-NW
            a6 = 0                            # The slope of line NW-NE is 0
            b6 = NW_y                         # The intercept of line NW-NE is the y-coordinate of either one

            # The code below is to decide if a point is in the hexagon just built
            # Use "q" to store the number of points
            q = 0
            for p in xrange(len(x)):
                if x[p] == [] and y[p] == []:
                    continue
                else:
                    x_test_NE_E  = (y[p]*1. - b1)/a1
                    x_test_E_SE  = (y[p]*1. - b2)/a2
                    y_test_SE_SW = a3 * x[p] + b3
                    x_test_SW_W  = (y[p]*1. - b4)/a4
                    x_test_W_NW  = (y[p]*1. - b5)/a5
                    y_test_NW_NE = a6 * x[p] + b6
                    if x_test_NE_E >= x[p] and x_test_E_SE >= x[p] and y_test_SE_SW <= y[p] and x_test_SW_W <= x[p] and x_test_W_NW <= x[p] and y_test_NW_NE >= y[p]:
                        q += 1
                        x[p] = []
                        y[p] = []
            hexagons.append(q)

    # Print out the "hexagons" list
    print 'There are', len(hexagons) ,'quadrats in total.'
    for i in xrange(len(hexagons)):
        print 'Quadrat', i+1, 'has', hexagons[i], 'points.'

    ax = fig.gca()
    ax.set_xticks(np.arange(minx-side, maxx+side+1, side))
    ax.set_yticks(np.arange(miny-side, maxy+side+1, side))
    plt.show()

    return len(hexagons), hexagons



def main():
    point_num = input('Enter the total number of points:')
    shape = input('Which type of quadrat? Type in "1" for rectangle and "2" for hexagon')

    if shape == 1:
        recwidth = input('Enter the rectangle width:')
        recheight = input('Enter the rectangle height:')
        [rec_num, rectangles] = rectangle(point_num, recwidth, recheight)
    elif shape == 2:
        side = input('Enter the hexagon side:')
        [hex_num, hexagons] = hexagon(point_num, side)
    else:
        print "Invalid input!"


if __name__ == '__main__':
    main()

