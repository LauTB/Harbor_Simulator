import randomvar as rdv
import settings 


class Ship:
    def __init__(self, current_time, id) -> None:
        self.stype = rdv.discrete_uniform(settings.SHIP_TYPES,settings.SHIP_PROB)
        self.arrival_time = current_time
        mu,sigma = settings.SHIP_TIMES[self.stype]
        self.load_time = rdv.box_muller(mu,sigma)
        self.to_dock_time = 0
        self.to_port_time = 0
        self.has_left = False
        self.leave_time = 0
        self.id = id
        self.in_port = False
        self.in_dock = False

class Dock:
    def __init__(self,id) -> None:
        self.id = id
        self.busy = False
        self.ship = None
        self.finished = False

    def is_free(self):
        return not self.isBusy

    def has_ship(self):
        return self.ship is not None
        
    def reset(self):
        self.isBusy = False        
        self.ship = None
        self.end_loading = False 

class TugBoat:
    def __init__(self,id) -> None:
        self.id = id
        self.port = True
        self.dock = False
        self.busy = False

    def is_free(self):
        return not self.busy

    def in_dock(self):
        return self.dock

    def in_port(self):
        return self.port

    def reset(self):
        self.busy = False
        self.dock = False
        self.port = False


