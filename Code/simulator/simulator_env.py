import datetime
import os
import sys
import time

from Code.simulator.driver_simulator import DriverSimulator
from Code.simulator.history import History

class SimulationEnvironment(object):
    def __init__(self, initial_time: int, time_interval: int, id_to_orders: dict, id_to_drivers: dict,
                 id_to_locations: dict, route_map):
        '''
        Inputs:
        initial_time: unix timestamp, unit is second
        time_interval: unit is second
        id_to_orders: total orders
        id_to_drivers: total drivers
        id_to_locations: total locations (customer + restaurant)
        route_map: map of route
        '''
        self.initial_time = initial_time
        self.time_interval = time_interval
        self.cur_time = initial_time
        self.pre_time = initial_time

        # order, driver, location, route map
        self.id_to_orders = id_to_orders
        self.id_to_driver = id_to_drivers
        self.id_to_location = id_to_locations
        self.route_map = route_map

        # order type with different state
        self.id_to_generated_order = {}
        self.id_to_ongoing_order = {}
        self.id_to_finished_order = {}

        # driver simulator
        self.driver_simulator = DriverSimulator(route_map, id_to_locations)

        # dispatch result for each time interval
        self.time_to_dispatch_result = {}

        # save the visited node of each driver and different status of orders for evaluation
        self.history = self.__ini_history()

        # objective value
        self.total_score = sys.maxsize

        # dispatch algorithm calling
        self.algorithm_calling_command = ''
    
    
    def __ini_history(self):
        history = History()
        # initialize the history of drivers and orders
        for driver_id, driver in self.id_to_driver.items():
            history.add_driver_position_history(driver_id, driver.gps_update_time, driver.current_location)
        for order_id, order in self.id_to_orders.items():
            history.add_order_status_history(order.delivery_state, self.initial_time, order.del_time, order.id)

        return history

    
    # # simulation
    # def run(self):
    #     used_seconds = 0

    #     while True:


        