
class Node(object):
    def __init__(self, location_id:str, lng:float, lat:float, pickup_order_list: list, delivery_order_list: list,
                    arrive_time=0, leave_time=0):
        '''
        Node including both customer location and restaurant location;
        For meal delivery problem, a location is either pickup (restaurant) or delivery (customer) location.
        Inputs:
        - location_id
        - lng: longitude
        - lat: latitude
        - pickup_order_list: pickup orders at location
        - delivery_order_list: delivery orders at location
        - arrive_time: estimate arrive time at location
        - leave_time: estimate leave time at location
        '''
        self.__id = location_id
        self.__lng = lng
        self.__lat = lat

        # list of delivery orders
        self.__delivery_orders = delivery_order_list
        self.__unloading_time = self.calculate_unloading_time()

        # list of pickup orders
        self.__pickup_orders = pickup_order_list
        self.__loading_time = self.calculate_loading_time()

        # arrive, leave and service time
        self.arrive_time = arrive_time 
        self.leave_time = leave_time
        self.__service_time = self.__unloading_time + self.__loading_time

    # calculate loading and unloading time
    def calculate_loading_time(self):
        loading_time = 0
        for order in self.__pickup_orders:
            loading_time += order.load_time
        return loading_time

    def calculate_unloading_time(self):
        unloading_time = 0
        for order in self.__delivery_orders:
            unloading_time += order.unload_time
        return unloading_time

    def update_service_time(self):
        self.__loading_time = self.calculate_loading_time()
        self.__unloading_time = self.calculate_unloading_time()
        self.__service_time = self.__unloading_time + self.__loading_time

    # getter and setter function
    @property
    def id(self):
        return self.__id

    @property
    def lng(self):
        return self.__lng

    @property
    def lat(self):
        return self.__lat

    @property
    def service_time(self):
        return self.__service_time

    @property
    def pickup_orders(self):
        return self.__pickup_orders

    @pickup_orders.setter
    def pickup_orders(self, pickup_order_list):
        self.__pickup_orders = pickup_order_list

    @property
    def delivery_orders(self):
        return self.__delivery_orders

    @delivery_orders.setter
    def delivery_orders(self, delivery_order_list):
        self.__delivery_orders = delivery_order_list