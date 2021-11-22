import randomvar as rdv
import settings 
from events import NewShip
class Port:
    def __init__(self,docks,tugboat):
        self.docks = docks
        self.tugboat = tugboat
        self.free_docks = len(self.docks)
        self.current_time = 0
        self.max_time = settings.TOTAL_HOURS
        self.entry_line = []
        self.leave_line = []
        self.last_ship_id = 0
        self.events = []
        self.ships = []

    def update_ship_id(self):
        self.last_ship_id+=1

    def run(self) -> None:
            self.reset()
            while self.events:
                event = self.events.pop(0)
                self.current_time = event.start_time
                if self.current_time > self.max_time:
                    continue
                event.simulate(self)
                self.events.sort()
    
    def reset(self):
        self.time = 0
        self.time_limit = settings.TOTAL_HOURS
        self.tugboat.reset()
        for dock in self.docks:
            dock.reset()
        self.entry_line = []
        self.leave_line = []
        self.last_ship_id = 0
        self.events = [NewShip(self.time  + rdv.exponential_dist(settings.SHIP_ARRIVAL_TIME))]
        self.ships = []