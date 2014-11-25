import random
import matplotlib.pyplot as plt
import math
import numpy as np
import sys

def generate_points(point_num, list_boundaries=None):
    """
    generate fake random point for analysis
    :rtype : object
    :param point_num: number of points
    :param list_boundaries: MBR of the points, default as x[0.0, 100.0], y[0.0, 100.0]
    :return: list_points, structure as [[x0, y0],[x1, y1],...,[xn, yn]]
    """
    # default values of boundary box
    b_minx = 0.0
    b_maxx = 100.0
    b_miny = 0.0
    b_maxy = 100.0

    # customized boundary box
    if list_boundaries != None:
        b_minx = min(list_boundaries[0:2])
        b_maxx = max(list_boundaries[0:2])
        b_miny = min(list_boundaries[2:4])
        b_maxy = max(list_boundaries[2:4])

    # interval = min([(b_maxx-b_minx)/10000, (b_maxy-b_miny)/10000])
    x = []
    y = []
    for i in xrange(point_num):
        x.append(random.uniform(b_minx, b_maxx))
        y.append(random.uniform(b_miny, b_maxy))

    points = []
    for i in xrange(point_num):
        points.append([x[i], y[i]])

    return points

class MBR:
    """
    minimum bounding rectangle structure
    """

    def __init__(self, boundaries=None):
        """
        @:param boundaries list of the boundaries of the MBR, first two as X coordinates and last two as Y coordinates

        """
        self.x_min = float(sys.maxint)
        self.x_max = float(-sys.maxint - 1)
        self.y_min = float(sys.maxint)
        self.y_max = float(-sys.maxint - 1)
        if None != boundaries:
            self.x_min = min(boundaries[0:2])
            self.x_max = max(boundaries[0:2])
            self.y_min = min(boundaries[2:4])
            self.y_max = max(boundaries[2:4])

    def range_x(self):
        """
        return the X range of this MBR
        """
        return self.x_max - self.x_min

    def range_y(self):
        """
        return the Y range of this MBR
        """
        return self.y_max - self.y_min


class Manager_rectangle:
    """
    class for statistic and visualization of rectangle
    """

    def __init__(self, list_points, rectangle_width = 5.0, rectangle_height = 5.0, count_column = -1, count_row = -1):
        """

        :param list_points: list
        :param rectangle_width: float you should specify rectangle width/height or count column/row
        :param rectangle_height: float
        :param count_column: int
        :param count_row: int
        :return:
        """

        # calculate the MBB of points
        ps = np.array(list_points)
        self.mbr = MBR()
        self.mbr.x_min = ps[:, 0].min() # Get the minimum x value in the entire dataset
        self.mbr.x_max = ps[:, 0].max() # Get the maximum x value in the entire dataset
        self.mbr.y_min = ps[:, 1].min() # Get the minimum y value in the entire dataset
        self.mbr.y_max = ps[:, 1].max() # Get the maximum y value in the entire dataset

        # record the params here
        self.list_points = list_points
        if count_column > 0 and count_row > 0:
            self.count_column = count_column
            self.count_row = count_row
            # calculate the actual width and height of cell
            self.rectangle_width = self.mbr.range_x()/float(count_column)
            self.rectangle_height = self.mbr.range_y()/float(count_row)
        else:
            self.rectangle_width = rectangle_width
            self.rectangle_height = rectangle_height
            # calculate column count and row count of the net
            self.count_column = int(math.ceil(self.mbr.range_x() / rectangle_width))
            self.count_row = int(math.ceil(self.mbr.range_y() / rectangle_height))


    def point_location_sta(self):
        """
        check how is every point located in the rectangles
        :return: a dict with the keys as rectangle id and values as point_number in every rectangle
        """
        dict_id_count = {}
        for i in xrange(self.count_row):
            for j in xrange(self.count_column):
                dict_id_count[j+i*self.count_column] = 0

        for point in self.list_points:
            index_x = int((point[0]-self.mbr.x_min) / self.rectangle_width)
            index_y = int((point[1]-self.mbr.y_min) / self.rectangle_height)
            if index_x == self.count_column:
                index_x -= 1
            if index_y == self.count_row:
                index_y -= 1
            id = index_y * self.count_column + index_x
            dict_id_count[id] += 1
        return dict_id_count

    def plot(self, show_sta_label = True, point_size = 3, plot_use_mpld3 = False):
        """
        plot lines and points
        :param show_sta_label whether to show the statistic info of every cell as label (default as True)
        :param point_size default as 3
        :param plot_use_mpld3 draw the graph in an interactive way using the lib of mpld3. default as False. We suggest
                use this way in Ipython Notebook
        :return when set plot_use_mpld3=True, we return plt
        """
        line_width_mbr = 2
        line_color_mbr = 'blue'
        line_width_cell = 1
        line_color_cell = 'red'
        #draw the points
        points = np.array(self.list_points)
        fig, ax = plt.subplots()
        ax.plot(points[:,0],points[:,1],'o', markersize=point_size)
        #draw MBR
        list_points_mbr = []
        list_points_mbr.append([self.mbr.x_min, self.mbr.y_min])
        list_points_mbr.append([self.mbr.x_max, self.mbr.y_min])
        list_points_mbr.append([self.mbr.x_max, self.mbr.y_max])
        list_points_mbr.append([self.mbr.x_min, self.mbr.y_max])
        list_points_mbr.append([self.mbr.x_min, self.mbr.y_min])
        ax.plot(np.array(list_points_mbr)[:,0],np.array(list_points_mbr)[:,1],'--', lw=line_width_mbr, color=line_color_mbr)
        #draw cells
        for row in xrange(self.count_row + 1):
            y = self.mbr.y_min + row*self.rectangle_height
            x_min = self.mbr.x_min
            x_max = x_min + self.count_column*self.rectangle_width
            ax.plot([x_min, x_max], [y, y], lw = line_width_cell, color=line_color_cell)
        for column in xrange(self.count_column + 1):
            x = self.mbr.x_min + column*self.rectangle_width
            y_min = self.mbr.y_min
            y_max = y_min + self.count_row*self.rectangle_height
            ax.plot([x, x], [y_min, y_max], lw = line_width_cell, color=line_color_cell)
        #draw sta labels
        if show_sta_label:
            dict_id_count = self.point_location_sta()
            for x in xrange(self.count_column):
                for y in xrange(self.count_row):
                    id = x + y*self.count_column
                    count = dict_id_count[id]
                    position_x = self.mbr.x_min + self.rectangle_width*(x+0.5)
                    position_y = self.mbr.y_min + self.rectangle_height*(y+0.5)
                    ax.text(position_x, position_y, str(count))
        if plot_use_mpld3:
            return fig
        else:
            plt.show()

class Manager_hexagon:
    """
    class for statistic and visualization of hexagon
    """
    def __init__(self, list_points, cell_side_length):
        """

        :param list_points: the list of points for test
        :param cell_side_length: the side length of every hexagon
        :return:
        """
        # record the params here
        self.list_points = list_points
        self.cell_side_length = cell_side_length
        # calculate the MBB of points
        ps = np.array(list_points)
        self.mbr = MBR()
        self.mbr.x_min = ps[:, 0].min()  # Get the minimum x value in the entire dataset
        self.mbr.x_max = ps[:, 0].max()  # Get the maximum x value in the entire dataset
        self.mbr.y_min = ps[:, 1].min()  # Get the minimum y value in the entire dataset
        self.mbr.y_max = ps[:, 1].max()  # Get the maximum y value in the entire dataset

        # calculate column count of network
        self.count_column = 1 # Starting from the first column and count to the right side
        if self.cell_side_length/2 < self.mbr.range_x():
            self.count_column += int(math.ceil((self.mbr.range_x() - self.cell_side_length/2) / (1.5 * self.cell_side_length)))

        # calculate row count of network
        # for the even column
        self.semi_height = cell_side_length * math.cos(math.pi/6)
        self.count_row_even = 1
        if self.semi_height < self.mbr.range_y():
            self.count_row_even += int(math.ceil((self.mbr.range_y()-self.semi_height)/(self.semi_height*2)))
        # for the odd column
        self.count_row_odd = int(math.ceil(self.mbr.range_y()/(self.semi_height*2)))

    def point_location_sta(self):
        """
        check how is every point located in the rectangles
        :return: a dict with the keys as rectangle id and values as point_number in every rectangle
        """
        semi_cell_length = self.cell_side_length / 2.0
        dict_id_count = {}
        for i in xrange(self.count_row_even):  # even row may be equal with odd row or 1 more than odd row
            for j in xrange(self.count_column):
                if self.count_row_even != self.count_row_odd and i == self.count_row_even-1:
                    if j % 2 == 1:
                        continue
                dict_id_count[j+i*self.count_column] = 0

        for point in self.list_points:
            # find the possible x index
            intercept_degree_x = int((point[0]-self.mbr.x_min)/semi_cell_length)  # optimized algorithm

            # find the possible y index
            possible_y_index_even = int((point[1]+self.semi_height-self.mbr.y_min)/(self.semi_height*2))
            possible_y_index_odd = int((point[1]-self.mbr.y_min)/(self.semi_height*2))
            if intercept_degree_x % 3 != 1:  # only one column is possible
                center_index_x = (intercept_degree_x+1)/3
                center_index_y = possible_y_index_odd
                if center_index_x % 2 == 0:
                    center_index_y = possible_y_index_even
                dict_id_count[center_index_x + center_index_y*self.count_column] += 1
            else: # two columns of cells can be possible
                center_index_x = intercept_degree_x/3
                center_x = center_index_x*semi_cell_length*3 + self.mbr.x_min
                center_index_y = possible_y_index_odd
                center_y = (center_index_y*2+1)*self.semi_height + self.mbr.y_min
                if center_index_x % 2 == 0:
                    center_index_y = possible_y_index_even
                    center_y = center_index_y*self.semi_height*2 + self.mbr.y_min
                # the formula of line is Y=(y0-y1)/(x0-x1)*X + (x0y1-x1y0)/(x0-x1)
                # or (x0 - x1)Y - (y0 - y1)X = x0y1 - x1y0
                indicator = 0
                if point[1] > center_y:  # compare the upper bound
                    x0 = center_x+self.cell_side_length
                    y0 = center_y
                    x1 = center_x+semi_cell_length
                    y1 = center_y+self.semi_height
                    indicator = -(point[1] - ((y0-y1)/(x0-x1)*point[0] + (x0*y1-x1*y0)/(x0-x1)))
                else:  #compare the lower bound
                    x0 = center_x+semi_cell_length
                    y0 = center_y-self.semi_height
                    x1 = center_x+self.cell_side_length
                    y1 = center_y
                    indicator = point[1] - ((y0-y1)/(x0-x1)*point[0] + (x0*y1-x1*y0)/(x0-x1))
                if indicator <= 0: # we select right hexagon instead of left
                    center_index_x += 1
                    center_index_y = possible_y_index_odd
                    if center_index_x % 2 == 0:
                        center_index_y = possible_y_index_even
                dict_id_count[center_index_x + center_index_y*self.count_column] += 1
        return dict_id_count

    def plot(self, show_sta_label = True, point_size = 3, plot_use_mpld3 = False):
        """
        plot lines and points
        :param show_sta_label whether to show the statistic info of every cell as label (default as True)
        :param point_size default as 3
        :param plot_use_mpld3 draw the graph in an interactive way using the lib of mpld3. default as False. We suggest
                use this way in Ipython Notebook
        :return when set plot_use_mpld3=True, we return plt
        """
        line_width_mbr = 2
        line_color_mbr = 'blue'
        line_width_cell = 1
        line_color_cell = 'red'
        #draw the points
        points = np.array(self.list_points)
        fig, ax = plt.subplots()
        ax.plot(points[:,0],points[:,1],'o', markersize=point_size)
        #draw MBR
        list_points_mbr = []
        list_points_mbr.append([self.mbr.x_min, self.mbr.y_min])
        list_points_mbr.append([self.mbr.x_max, self.mbr.y_min])
        list_points_mbr.append([self.mbr.x_max, self.mbr.y_max])
        list_points_mbr.append([self.mbr.x_min, self.mbr.y_max])
        list_points_mbr.append([self.mbr.x_min, self.mbr.y_min])
        ax.plot(np.array(list_points_mbr)[:,0],np.array(list_points_mbr)[:,1],'--', lw=line_width_mbr, color=line_color_mbr)
        #draw cells and sta labels
        dict_id_count = self.point_location_sta()
        for id in dict_id_count.keys():
            index_x = id % self.count_column
            index_y = int(id / self.count_column)
            center_x = index_x*self.cell_side_length/2.0*3.0 + self.mbr.x_min
            center_y = index_y*self.semi_height*2.0 + self.mbr.y_min
            if index_x % 2 == 1:  # for the odd columns
                center_y = (index_y*2.0+1)*self.semi_height + self.mbr.y_min
            list_points_cell = []
            list_points_cell.append([center_x+self.cell_side_length, center_y])
            list_points_cell.append([center_x+self.cell_side_length/2, center_y+self.semi_height])
            list_points_cell.append([center_x-self.cell_side_length/2, center_y+self.semi_height])
            list_points_cell.append([center_x-self.cell_side_length, center_y])
            list_points_cell.append([center_x-self.cell_side_length/2, center_y-self.semi_height])
            list_points_cell.append([center_x+self.cell_side_length/2, center_y-self.semi_height])
            list_points_cell.append([center_x+self.cell_side_length, center_y])
            ax.plot(np.array(list_points_cell)[:,0],np.array(list_points_cell)[:,1], lw=line_width_cell, color=line_color_cell)
            if show_sta_label:
                ax.text(center_x, center_y, str(dict_id_count[id]))
        if plot_use_mpld3:
            return fig
        else:
            plt.show()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# test lines
# print generate_points(300,[12.4,23.5,-98.435,-453])
# manager_rectangle(generate_points(200),23,32)


# for i in xrange(100000):
#     m = Manager_hexagon(generate_points(300),random.uniform(6,12))
#     m.point_location_sta()
#     if i % 10000 == 0:
#         print 'i=',i
# print "finished"

# p = Manager_rectangle(generate_points(3000),5,6)
# p.plot(plot_use_mpld3=True)


# p = Manager_rectangle(generate_points(300),5,6, count_column=11, count_row=13)
# p.point_location_sta()

# m = Manager_hexagon(generate_points(300),random.uniform(6,12))
# m.plot()

# def ca():
#     print "dafs"
#     fig, ax = plt.subplots()
#     np.random.seed(0)
#     x, y = np.random.normal(size=(2, 200))
#     color, size = np.random.random((2, 200))
#
#     ax.scatter(x, y, c=color, s=500 * size, alpha=0.3)
#     ax.grid(color='lightgray', alpha=0.7)
#     plt.show()
#     import mpld3
#     mpld3.display(fig)
#     return fig
# # ca()




























