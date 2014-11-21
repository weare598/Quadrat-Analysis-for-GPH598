import scipy.stats
import numpy as np
import random
import quadrats as qu

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
    x_temp = x_temp.astype('int')  #current quadrat function doesn't support floating type
    x_temp = x_temp[:,np.newaxis]
    y_temp = np.array([random.uniform(y_bound[0],y_bound[1]) for j in range(n)])
    y_temp = y_temp.astype('int')
    y_temp = y_temp[:,np.newaxis]
    list_points = np.concatenate((x_temp,y_temp), axis=1)
    return list_points  
    
def quadrats_simulate(points,x_bound=[0,100],y_bound=[0,100],simulate="uniform",nsim = 99):
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
    nsim    : interger
              Number of simulated point patterns to be generated.
              
    Returns
    -------
    p       : float
              P value.
    """  
    quadrats_num_o, points_num_list_o = qu.rectangle(points.shape[0], 20, 20, points) #counts
    test_statistic_o = scipy.stats.chisquare(points_num_list_o)  #test statisitc of observed point patterns
     
    test_statistic_list = [] #store test statisitcs for all the simulated samples
    for i in range(nsim):
        points_simulated = csr(points.shape[0], x_bound=[0,100],y_bound=[0,100],simulate="uniform") #simulate point patterns
        quadrats_num, points_num_list = qu.rectangle(points_simulated.shape[0], 20, 20, points_simulated) #counts
        test_statistic,p = scipy.stats.chisquare(points_num_list) #calculate test statistic
        test_statistic_list.append(test_statistic)
    test_statistic_list = np.array(test_statistic_list)
    
    #calculate p-value
    test_statistic_larger = test_statistic_list[np.nonzero(test_statistic_list >=test_statistic_o)]
    num_larger = test_statistic_larger.shape[0]
    p = (float(num_larger)+1)/(nsim+1)
    return p