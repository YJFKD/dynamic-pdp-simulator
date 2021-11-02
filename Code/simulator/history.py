import sys
from Code.configuration.config import Configs

class History(object):
    def __init__(self):
        '''
        __driver_id_to_node_list, dict, {key: driver id, value: [driver information]}
        __order_id_to_status_list, dict, {key: order id, value: [order information]}
        '''
        self.__driver_id_to_node_list = {}
        self.__order_id_to_status_list = {}


    def add_driver_position_history(self, driver_id:str, update_time:int, curr_location_id:str):
        '''
        Update driver information (driver id, location, update time)
        Inputs:
        driver_id: id of driver
        update_time: information update time
        curr_location_id: current driver stop location
        '''
        if driver_id not in self.__driver_id_to_node_list:
            self.__driver_id_to_node_list[driver_id] = []
        
        if len(curr_location_id)> 0:
            self.__driver_id_to_node_list[driver_id].append({"location_id": curr_location_id,
                                                             "update time": update_time})


    def add_order_status_history(self, order_state:int ,update_time:int, del_time:int, order_id:str):
        '''
        Update order information (state, update time, finished time, order id)
        Inputs:
        - order_state: state of order, {0: initialization, 1: generated, 2: ongoing, 3: finished}
        - update_time: information update time
        - del_time: order delivery time
        - order_id: id of order
        '''
        if order_id not in self.__order_id_to_status_list:
            self.__order_id_to_status_list[order_id] = []
        self.__order_id_to_status_list[order_id].append({"state": order_state,
                                                         "update_time": update_time,
                                                         "finished time": del_time,
                                                         "order_id": order_id})


    def get_driver_position_history(self):
        return self.__driver_id_to_node_list
    

    def get_order_status_history(self):
        return self.__order_id_to_status_list
    

    def add_history_of_drivers(self, id_to_driver:dict, to_time=0):
        '''
        Inputs:
        - id_to_driver: dict, {key: driver id, value: driver}
        - to_time: the time update information
        '''
        # if not provide update time, set the to_time parameter as a very large number
        if to_time == 0:
            to_time = sys.maxsize
        
        for driver_id, driver in id_to_driver.items():
            # if driver is at a location
            if len(driver.current_location) > 0:
                if driver.leave_time_at_current_location <= to_time:
                    self.add_driver_position_history(driver_id, 
                                                     driver.leave_time_at_current_location, 
                                                     driver.current_location)

            # if driver is running to next destination
            if driver.destination is not None:
                if driver.destination.leave_time <= to_time:
                    self.add_driver_position_history(driver.id, 
                                                     driver.destination.leave_time,
                                                     driver.destination.id)
            
            for node in driver.planned_route:
                if node.leave_time <= to_time:
                    self.add_driver_position_history(driver.id, 
                                                     node.leave_time,
                                                     node.id)
    
    def add_history_of_order(self, id_to_driver:dict, to_time=0):
        '''
        Inputs:
        - id_to_driver: dict, {key: driver id, value: driver}
        - to_time: the time update information
        '''
        if to_time == 0:
            to_time = sys.maxsize
        
        for driver_id, driver in id_to_driver.items():
            # order in driver next destination
            if driver.destination is not None:
                if driver.destination.arrive_time <= to_time:
                    # set the update time equals to the arrive time at destination
                    update_time = driver.destination.arrive_time
                    # pickup orders
                    for order in driver.destination.pickup_orders:
                        self.add_order_status_history(Configs.ORDER_STATUS_TO_CODE.get("ONGOING"), 
                                                      update_time,
                                                      order.del_time,
                                                      order.id)
                    # delivery orders
                    for order in driver.destination.delivery_orders:
                        self.add_order_status_history(Configs.ORDER_STATUS_TO_CODE.get("FINISHED"), 
                                                      update_time,
                                                      order.del_time,
                                                      order.id)
            
            # order in planned route
            for node in driver.planned_route:
                if node.arrive_time <= to_time:
                    update_time = node.arrive_time
                    # pickup orders
                    for order in node.pickup_orders:
                        self.add_order_status_history(Configs.ORDER_STATUS_TO_CODE.get("ONGOING"), 
                                                      update_time,
                                                      order.del_time,
                                                      order.id)
                    # delivery orders
                    for order in node.delivery_orders:
                        self.add_order_status_history(Configs.ORDER_STATUS_TO_CODE.get("FINISHED"), 
                                                      update_time,
                                                      order.del_time,
                                                      order.id)



