#how many hours will the simulation run
TOTAL_HOURS= 24

#small = 1, medium = 2, big = 3
SHIP_TYPES = [1,2,3]
SHIP_PROB = [0.25,0.25,0.5]
#(mean, variance) for each ship load time
SHIP_TIMES = {1:(9,1), 2:(12,2), 3:(18,3)}
SHIP_ARRIVAL_TIME = 8

#time messured in hours
TUGBOAT_MOVE_TIME = 0.25
TUGBOAT_TO_DOCKS = 2
TUGBOAT_TO_PORT = 1