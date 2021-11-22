from elements import *
import randomvar as rdv
import settings


class Event:
    def __init__(self,time) -> None:
        self.start_time = time

    def simulate(self,port) -> None:
        pass

    def __lt__(self,other):
        return self.start_time < other.start_time
    def __lg__(self,other):
        return self.start_time > other.start_time
    def __le__(self,other):
        return self.start_time <= other.start_time
    def __ge__(self,other):
        return self.start_time >= other.start_time
    def __gt__(self,other):
        return self.start_time > other.start_time
    def __eq__(self,other):
        return self.start_time == other.start_time
    def __ne__(self,other):
        return self.start_time != other.start_time

class NewShip(Event):
    """
    a new ship arrives to the port
    """
    def simulate(self,port):
        port.update_ship_id()
        ship = Ship(self.start_time,port.last_ship_id)
        ship.in_port = True
        tugboat = port.tugboat
        if tugboat.is_free:
            for dock in port.docks:
                if dock.is_free:
                    tugboat.busy = True
                    dock.busy = True
                    time = self.start_time
                    if tugboat.in_dock:
                        tugboat.in_dock = False
                        tugboat_to_port = rdv.exponential_dist(settings.TUGBOAT_MOVE_TIME)
                        time += tugboat_to_port
                        event = ShipToDocks(time,ship,tugboat,dock)
                        port.events.append(event)
                        next_arrival = self.start_time + rdv.exponential_dist(settings.SHIP_ARRIVAL_TIME)
                        if next_arrival<= port.max_time:
                            port.events.append(NewShip(next_arrival))
                        return
                    else:
                        tugboat.in_port = False
                        event = ShipToDocks(time,ship,tugboat,dock)
                        port.events.append(event)
                        next_arrival = self.start_time + rdv.exponential_dist(settings.SHIP_ARRIVAL_TIME)
                        if next_arrival<= port.max_time:
                            port.events.append(NewShip(next_arrival))
                        return

        port.entry_line.append(ship)
        next_arrival = self.start_time + rdv.exponential_dist(settings.SHIP_ARRIVAL_TIME)
        if next_arrival<= port.max_time:
            port.events.append(NewShip(next_arrival))
        return
        



class ShipToDocks(Event):
    """
    the tugboat takes a ship from the port to the docks
    """
    def __init__(self, time, ship:Ship, tugboat:TugBoat, dock:Dock) -> None:
        super().__init__(time)
        self.tugboat = tugboat
        self.dock = dock
        self.ship = ship

    def simulate(self,port) -> None:
        self.ship.to_dock_time = self.start_time
        self.dock.ship = self.ship
        self.dock.busy = True
        self.tugboat.busy = False
        self.tugboat.in_dock = True
        self.tugboat.in_port = False
        move_ship_time = rdv.exponential_dist(settings.TUGBOAT_TO_DOCKS) + self.start_time
        port.events.append(ShipReachesDocks(move_ship_time, self.ship, self.dock))
        port.events.append(TugboatStatusCheck(move_ship_time, self.tugboat))
        return
        

class ShipReachesDocks(Event):
    """
    the ship reaches the docks and starts the load process
    """
    def __init__(self, time,ship:Ship,dock:Dock) -> None:
        super().__init__(time)
        self.dock = dock
        self.ship = ship
    def simulate(self,port) -> None:
        load_time = self.ship.load_time + self.start_time
        port.events.append(ShipFinishedLoad(load_time,self.ship,self.dock))
        return

class ShipFinishedLoad(Event):
    """
    the ship is ready to leave when the tugboat is ready
    """
    def __init__(self, time, ship:Ship, dock:Dock) -> None:
        super().__init__(time)
        self.dock = dock
        self.ship = ship
    def simulate(self,port) -> None:
        self.dock.finished = True
        tugboat = port.tugboat
        if tugboat.is_free:
            tugboat.busy = True
            self.dock.isBusy = False
            self.dock.ship = None            
            if tugboat.in_dock:
                tugboat.in_dock = False
                port.events.append(ShipToPort(self.start_time,self.ship,tugboat))
                return
            else:
                port.events.append(ShipToPort(self.start_time + rdv.exponential_dist(settings.TUGBOAT_MOVE_TIME)
                                    ,self.ship,tugboat))
                return
        return

class ShipToPort(Event):
    """
    the tugboat takes the ship to the ports
    """
    def __init__(self, time, ship: Ship, tugboat:TugBoat) -> None:
        super().__init__(time)
        self.tugboat = tugboat
        self.ship = ship
    def simulate(self,port) -> None:
        take_to_port_time = rdv.exponential_dist(settings.TUGBOAT_TO_PORT) + self.start_time
        self.ship.leave_time = take_to_port_time
        self.ship.in_port = False
        self.ship.has_left = True
        port.ships.append(self.ship)
        self.tugboat.is_free = True
        self.tugboat.in_dock = False
        self.tugboat.in_port = True

        if port.entry_line:
            for dock in port.docks:
                if dock.is_free:
                    ship = port.entry_line.pop(0)
                    dock.reset()
                    dock.ship = ship
                    self.tugboat.in_dock = True
                    self.tugboat.in_port = False
                    self.tugboat.is_free = False
                   
                    port.events.append(ShipToDocks(self.start_time,ship,self.tugboat,dock))
                    return
            else:
                for event in port.events:
                    if isinstance(event,ShipFinishedLoad):
                        port.events.append(TugboatStatusCheck(self.start_time,self.tugboat))
                        return
                    elif isinstance(event,NewShip):
                        self.tugboat.is_free = True
                        self.tugboat.in_dock = False
                        return
        else:
            for event in port.events:
                    if isinstance(event,ShipFinishedLoad):
                        self.tugboat.is_free = False
                        self.tugboat.in_dock = True
                        port.events.append(TugboatStatusCheck(self.start_time + rdv.exponential_dist(settings.TUGBOAT_MOVE_TIME)
                                    ,self.tugboat))
                        return
                    elif isinstance(event,NewShip):
                        self.tugboat.is_free = True
                        self.tugboat.in_dock = False
                        return
        

class TugboatStatusCheck(Event):
    """
    check the tugboat status to see if it can do an action
    """
    def __init__(self, time, tugboat:TugBoat) -> None:
        super().__init__(time)
        self.tugboat = tugboat

    def simulate(self,port) -> None:
        if port.leave_line:
            dock:Dock = port.leave_line.pop(0)
            dock.is_free = True
            ship = dock.ship
            dock.ship = None
            self.tugboat.busy= True
            self.tugboat.in_dock = False
            self.start_time += rdv.exponential_dist(settings.TUGBOAT_TO_PORT)
            port.events.append(ShipToPort(self.start_time,ship, self.tugboat))
        
        elif port.entry_line:
            for dock in port.docks:
                if dock.is_free:
                    dock.is_free = False
                    self.tugboat.busy = True
                    self.tugboat.in_dock = False
                    ship = port.entry_line.pop(0)
                    time_to_port = rdv.exponential_dist(settings.TUGBOAT_MOVE_TIME) + self.start_time
                    port.events.append(ShipToDocks(time_to_port,ship,self.tugboat,dock))
                    return
            else:
                self.tugboat.busy = False
                self.tugboat.in_dock = True
        else:
            for dock in port.docks:
                if dock.has_ship():
                    self.tugboat.is_free = True
                    self.tugboat.in_dock = True
            else:
                free_move = rdv.exponential_dist(settings.TUGBOAT_MOVE_TIME) + self.start_time
                port.events.append(WaitingNewShip(free_move,self.tugboat))

class WaitingNewShip(Event):
    """
    the tugboat is in the port waiting for a new arrival
    """
    def __init__(self, time, tugboat: TugBoat) -> None:
        super().__init__(time)
        self.tugboat = tugboat

    def simulate(self, port) -> None:
        self.tugboat.busy = False
        self.tugboat.dock = False
        self.tugboat.port = True
        