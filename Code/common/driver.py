class Driver(object):
    def __init__(self, driver_id: str, capacity=5, state=0, carrying_orders=None, 
                    finished_orders=None, ongoing_orders=None):
        '''
        Inputs:
        - driver_id: index of driver
        - capacity: maximum number of orders driver can delivery at the same time
        - state: {0: initialization, 1: servering, 2: rest}
        - carring_orders: list, orders not finished delivery
        - finished_orders: list, orders already deliveried
        - on_orders: list, servering orders (deliverying)
        '''
        self.id = driver_id
        self.capacity = capacity
        self.state = state

        # private attributes
        if carrying_orders is None:
            carrying_orders = []
        self.__carrying_orders = carrying_orders

        if finished_orders is None:
            finished_orders = []
        self.__finished_orders = finished_orders
        
        if ongoing_orders is None:
            ongoing_orders = []
        self.__ongoing_orders = ongoing_orders

        '''
        gps_update_time: update time of current location, unit is second
        current_location: current location of driver，if no in any location (restaurant or customer location), equals to ""
        arrive_time_at_current_location: time driver arrive current location
        leave_time_at_current_location: time driver leave current location
        destination: next location in driver planned route
        planned_route: list of nodes, visiting sequence of driver
        '''
        self.gps_update_time = 0
        self.current_location = ""
        self.arrive_time_at_current_location = 0
        self.leave_time_at_current_location = 0
        self.destination = None
        self.planned_route = []

    def add_order(self, order):
        '''
        Add new order to the driver
        '''
        self.__carrying_orders.append(order)
    
    def dropoff_order(self, order):
        '''
        Remove old order from the driver
        '''
        self.__carrying_orders.remove(order)

    def add_complete_order(self, order):
        '''
        Add completed order to finished orders set
        '''
        self.__finished_orders.append(order)

    def add_servering_order(self, order):
        '''
        Add now servering order to on orders set
        '''
        self.__on_orders.append(order)

    # getter method
    @property
    def carrying_orders(self):
        return self.__carrying_orders

    @property
    def finished_orders(self):
        return self.__finished_orders

    @property
    def ongoing_orders(self):
        return self.__ongoing_orders

    # setter method
    @carrying_orders.setter
    def carrying_orders(self, carrying_orders):
        self.__carrying_orders = carrying_orders
    

    


