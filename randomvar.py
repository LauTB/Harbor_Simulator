import random as rd
import math

#necesary to choose the boat type
def discrete_uniform(xi,pi):
    u = rd.random()
    i = 0
    f_xi = pi[0]
    while f_xi<=u:
        i +=1
        f_xi += pi[i]
    else:
        return xi[i]

def exponential_dist(lam):
    u = rd.random()
    return - math.log(u, math.e) / lam

#normal distribution simulation
def box_muller(mean, sd):
    u1 = rd.random()
    u2 = rd.random()
    #standard normal distribution
    z = math.sqrt(-2*math.log(u1, math.e)) * math.cos(2 * math.pi * u2)
    z1 = math.sqrt(-2*math.log(u1, math.e)) * math.sin(2 * math.pi * u2)
    # if z < 0:
    #     return z*sd + mean
    return z1*sd + mean
