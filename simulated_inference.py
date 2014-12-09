import scipy.stats
import numpy as np
import random
import quadrats_new as qd

def csr(n=100, x_bound=[0,100],y_bound=[0,100],simulate="uniform"):
    """
    This function generates point patterns which apply with complete spatial randomness (csr).
    
    Parameters
    ----------
    n       : interger
              Number of observed points. 
    x_bound : list
              Minimum and maximum x coordinates of study area
    y_bound : list
              Minimum and maximum y coordinates of study area    
    simulate: string
              Specifies how to generate the simulated point patterns. Can be "uniform" or "poisson".
                       
    Returns
    -------
    ps_sim  : float
              Simulated point patterns.
    """  
    if simulate == "poisson": #if CSR distribution is Possion distribution, number of points should apply with possion distribution
        n = np.random.poisson(n)
    
    x_temp = np.array([random.uniform(x_bound[0],x_bound[1]) for j in range(n)])
    #x_temp = x_temp.astype('int')  #current quadrat function doesn't support floating type
    x_temp = x_temp[:,np.newaxis]
    y_temp = np.array([random.uniform(y_bound[0],y_bound[1]) for j in range(n)])
    #y_temp = y_temp.astype('int')
    y_temp = y_temp[:,np.newaxis]
    list_points = np.concatenate((x_temp,y_temp), axis=1)
    return list_points  
    
def quadrats_simulate(points,x_bound=[0,100],y_bound=[0,100],simulate="uniform",nsim = 99,nx = 20, ny = 20,lh = 10,t = "rectangular" ):
    """
    This function calculates p-value of obeserved point patterns using monte carlo testing in which simulated point patterns
    apply with csr (uniform or poisson)
    
    Parameters
    ----------
    points  : n*2 list
              Coordinates of obeserved point patterns. (n points) 
    x_bound : list
              Minimum and maximum x coordinates of study area
    y_bound : list
              Minimum and maximum y coordinates of study area    
    simulate: string
              Specifies how to generate the simulated point patterns. Can be "uniform" or "poisson".
    nsim    : integer
              Number of simulated point patterns to be generated.
    nx      : integer
              Numbers of rectangular quadrats in the x direction. (rectangular)
    ny      : integer
              Numbers of rectangular quadrats in the y direction. (rectangular)
    lh      : integer
              hexagon length (hexagon) - incompatible with nx & ny
    t       : integer
              grid structure. can be "rectangular" or "hexagon"
              
    Returns
    -------
    p       : float
              P value.
    """  
    if t== "rectangular":
        mr = qd.Manager_rectangle(points,0,0,count_column=nx,count_row=ny)
    elif t == "hexagon":
        mr = qd.Manager_hexagon(points,lh)
        
    dict_id_count = mr.point_location_sta()
    test_statistic_o,p = scipy.stats.chisquare(dict_id_count.values())  #test statisitc of observed point patterns
     
    test_statistic_list = [] #store test statisitcs for all the simulated samples
    for i in range(nsim):
        points_simulated = csr(len(points), x_bound=x_bound,y_bound=y_bound,simulate=simulate) #simulate point patterns
        if t== "rectangular":
            mr_temp = qd.Manager_rectangle(points_simulated,count_column=nx,count_row=ny)
        elif t == "hexagon":
            mr_temp = qd.Manager_hexagon(points_simulated,lh)
        dict_id_count_temp = mr_temp.point_location_sta()
        test_statistic,p = scipy.stats.chisquare(dict_id_count_temp.values()) #calculate test statistic
        test_statistic_list.append(test_statistic)
    test_statistic_list = np.array(test_statistic_list)
    
    #calculate p-value
    test_statistic_larger = test_statistic_list[np.nonzero(test_statistic_list >=test_statistic_o)]
    num_larger = test_statistic_larger.shape[0]
    p = (float(num_larger)+1)/(nsim+1)
    return p