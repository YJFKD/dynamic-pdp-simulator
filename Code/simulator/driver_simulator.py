from Code.common.driver import Driver
import datetime
import simpy


class DriverSimulator(object):
    def __init__(self, route_map, id_to_locations):
        '''
        Inputs:
        - route_map: travel distance and time matrix between locations
        - id_to_locations: dict, {key: id, value: locations}
        '''
        self.env = simpy.Environment()

        self.route_map = route_map
        self.id_to_locations = id_to_locations

        self.ongoing_order_ids = []
        self.finished_order_ids = []
        self.driver_id_to_destination = {}
        self.driver_id_to_cur_position_info = {}
        self.driver_id_to_carrying_orders = {}
    

    def run(self, id_to_driver: dict, from_time: int):
        """
        Inputs:
        - id_to_driver:  total drivers
        - from_time: unit is second, start time of the simulator
        """
        # initialize the simulation environment
        self.env = simpy.rt.RealtimeEnvironment(initial_time=from_time, factor=0.000000000001, strict=False)

        # sort_drivers by leave time in their locations
        sorted_drivers = self.__sort_drivers(id_to_driver, from_time)

        # in simulation, each driver starts to visit its route
        for driver in sorted_drivers:
            self.env.process(self.work(driver))
        self.env.run()


    def work(self, driver):
        '''
        Simulate the visiting process of each driver
        Inputs:
        - driver: driver object
        '''
        cur_location_id = driver.location

        if len(cur_location_id) > 0:
            driver.leave_time_at_current_location = self.env.now
        
        if driver.destination == None:
            if len(cur_location_id) == 0:
                print(f"Driver {driver.id}: both the current location and the destination are None!!!")
            return
        
        if len(cur_location_id) > 0:
            next_location_id = driver.destination.id
            transport_time = self.route_map.calculate_time_between_loc(cur_location_id, next_location_id)
            yield self.env.timeout(transport_time)
        else:
            # driving towards next location (a location is a node object)
            arr_time = driver.destination.arrive_time
            if arr_time >= self.env.now:
                yield self.env.timeout(arr_time - self.env.now)
            else:
                # arrival time is less than current time, wrong!
                print(f"Driver {driver.id} is driving toward the destination, "
                      f"however current time {datetime.datetime.fromtimestamp(self.env.now)} is greater than "
                      f"the arrival time {datetime.datetime.fromtimestamp(arr_time)} of destination!!!")

        # arriving the destination
        driver.destination.arrive_time = self.env.now
        service_time = driver.destination.service_time
        cur_location_id = driver.destination.id
        yield self.env.timeout(service_time)

        # leave the destination
        driver.destination.leave_time = self.env.now

        # driving towards left locations
        for node in driver.planned_route:
            next_location_id = node.id

            # calculate travel time
            transport_time = self.route_map.calculate_time_between_loc(cur_location_id, next_location_id)
            yield self.env.timeout(transport_time)

            # calculate service time
            arr_time = self.env.now
            service_time = node.service_time
            yield self.env.timeout(service_time)
            leave_time = self.env.now
            
            # update time and location
            node.arrive_time = arr_time
            node.leave_time = leave_time
            cur_location_id = next_location_id
    

    @staticmethod
    def __sort_drivers(id_to_driver:dict, start_time:int):
        '''
        Inputs:
        - id_to_driver: total drivers, {key: id, value: driver}
        - start_time: simulation start time
        '''
        # construct location_id_to_drivers, {key: location id, value: drivers}
        location_id_to_drivers = {}
        for driver_id, driver in id_to_driver.items():
            if len(driver.current_location) > 0 and driver.leave_time_at_current_location > start_time:
                location_id = driver.current_location
                if location_id not in location_id_to_drivers:
                    location_id_to_drivers[location_id] = []
                location_id_to_drivers[location_id].append(driver)
        
        # sort driver by leave time
        sorted_driver_ids = []
        for location_id, drivers in location_id_to_drivers.items():
            # sort by leave time
            tmp_dt = [(driver.id, driver.leave_time_at_current_location) for driver in drivers]
            tmp_dt.sort(key=lambda x: x[1])
            for dt in tmp_dt:
                sorted_driver_ids.append(dt[0])
        
        for driver_id in id_to_driver.keys():
            if driver_id not in sorted_driver_ids:
                sorted_driver_ids.append(driver_id)

        # get sorted driver object list 
        sorted_drivers = [id_to_driver.get(driver_id) for driver_id in sorted_driver_ids]
        return sorted_drivers
    

    def get_position_info_of_driver(self, id_to_driver:dict, to_time:int):
        '''
        Get the position information of each driver, construct the dict self.driver_id_to_cur_position_info
        Inputs:
        - id_to_driver: dict, {key: driver id, value: driver}
        - to time: time you want to get the position of driver
        Output: self attribute, driver_id_to_cur_position_info (dict)
        '''
        for driver_id, driver in id_to_driver.items():
            if len(driver.current_location) == 0 and driver.destination is None:
                print(f"Driver {driver_id}, the current position {driver.current_location}, the destination is None")
                continue
            
            # get the node information (location, arrive time, leave time) of a driver
            node_list = self.get_node_list_of_driver(driver)

            current_location = ""
            arrive_time_at_current_location = 0
            leave_time_at_current_location = 0
            
            # iterate the node list, find the location with time constraint
            for node in node_list:
                if node.arr_time <= to_time <= node.leave_time:
                    current_location = node.id
                    arrive_time_at_current_location = node.arr_time
                    leave_time_at_current_location = node.leave_time
            
            # if now time is larger than last node leave time
            if len(current_location) == 0 and node_list[-1].leave_time < to_time:
                current_location = node_list[-1].id
                arrive_time_at_current_location = node_list[-1].arr_time
                leave_time_at_current_location = max(node_list[-1].leave_time, to_time)
            
            self.driver_id_to_cur_position_info[driver_id] = {"current_location": current_location,
                                                                "arrive_time_at_current_factory": arrive_time_at_current_location,
                                                                "leave_time_at_current_factory": leave_time_at_current_location,
                                                                "update_time": to_time}


    def get_destination_of_driver(self, id_to_driver: dict, to_time: int):
        '''
        Inputs:
        - id_to_driver: dict, {key: driver id, value: driver}
        - to_time: time you want to get the destination of driver
        Output: self attribute, driver_id_to_destination (dict)
        '''
        for driver_id, driver in id_to_driver.items():
            # if no destination
            if driver.destination is None:
                self.driver_id_to_destination[driver_id] = None
                continue
            
            # if arrive time of destination is greater than now 
            if driver.destination.arrive_time > to_time:
                self.driver_id_to_destination[driver_id] = driver.destination
            # if arrive time of destination is less than now
            else:
                destination = None
                for node in driver.planned_route:
                    if node.arrive_time > to_time:
                        destination = node
                        break
                self.driver_id_to_destination[driver_id] = destination


    def get_loading_and_unloading_result_of_drivers(self, id_to_driver: dict, to_time: int):
        '''
        Update the driver's pickup and delivery behaviour
        '''
        for driver_id, driver in id_to_driver.items():
            carrying_orders = driver.carrying_orders
            
            # if no destination, no change
            if driver.destination is None:
                self.driver_id_to_carrying_orders[driver_id] = carrying_orders
                continue
            
            # if destination is passed already
            if driver.destination.arrive_time <= to_time:
                self.loading_and_unloading(driver.destination, carrying_orders, 
                                            self.finished_order_ids, self.ongoing_order_ids)
            
            # do the order list update for all other nodes in planned route
            for node in driver.planned_route:
                arr_time = node.arrive_time
                leave_time = node.leave_time
                if arr_time <= to_time:
                    self.loading_and_unloading(node, carrying_orders, self.finished_order_ids, self.ongoing_orders_ids)
                if leave_time > to_time:
                    break


    @staticmethod
    def loading_and_unloading(node, carrying_orders, finished_orders_ids, ongoing_orders_ids):
        '''
        Modify the orders list, one location can only be pickup location or dropoff location
        Inputs:
        - carrying_orders: orders is now carrying
        - finished_orders_ids: orders id which are already finished delivery
        - ongoing_orders_ids: orders id is now prepare to pickup or delivery
        '''
        # access orders waiting for delivery or pickup for each node (location)
        delivery_orders = node.delivery_orders
        pickup_orders = node.pickup_orders
        
        # remove delivery order from carrying orders list and add to finished orders list
        for order in delivery_orders:
            carrying_orders.pop()
            finished_orders_ids.append(order.id)
        
        # add pickup order into carrying orders list and on going order list
        for order in pickup_orders:
            carrying_orders.push(order)
            ongoing_orders_ids.append(order.id)


    @staticmethod
    def get_node_list_of_driver(driver):
        '''
        Get the list of node (location, arrive time, leave time) of each driver
        '''
        node_list = []
        
        # add driver current information
        if len(driver.current_location) > 0:
            node_list.append(EasyNode(driver.current_location,
                                        driver.arrive_time_at_current_location,
                                        driver.leave_time_at_current_location))
        
        # add driver next destination information
        if driver.destination is not None:
            node_list.append(EasyNode(driver.destination.id,
                                        driver.destination.arrive_time,
                                        driver.destination.leave_time))

        # add driver planned route information
        if len(driver.planned_route) > 0:
            for node in driver.planned_route:
                node_list.append(EasyNode(node.id, node.arrive_time, node.leave_time)) 



class EasyNode(object):
    '''
    A simply version of node class, only include the location id, arrive time, and leave time
    '''
    def __init__(self, location_id, arr_time, leave_time):
        self.id = location_id
        self.arr_time = arr_time
        self.leave_time = leave_time
        







            
