import datetime

class Order(object):
    def __init__(self, order_id: str, order_restaurant_id: str, order_customer_id: str, create_time: int, 
                    estimate_time: int, pickup_time: int, loading_time: int, unloading_time: int,
                    delivery_time: int, lng: float, lat: float, state=0):
        '''
        Inputs:
        - order_id: index of order
        - order_restaurant: id of restaurant where the order comes from
        - order_customer_id: id of customer who place it
        - create_time: order creat time
        - estimate_time: estimate delivery time
        - pickup_time: the time driver pickup order
        - delivery_time: the time driver delivery order
        - load_time: load time for pickup
        - unload_time: unload time for dropoff
        - lng: order longitude
        - lat: order latitude
        - state: state of the order; {0: initialization, 1: generated, 2: ongoing, 3: finished}
        '''
        # id
        self.id = order_id
        self.res_id = order_restaurant_id
        self.cus_id = order_customer_id
        # time
        self.creat_time = create_time
        self.est_time = estimate_time
        self.del_time = delivery_time
        self.pickup_time = pickup_time
        self.load_time = loading_time
        self.unload_time = unloading_time
        # location
        self.lng = lng
        self.lat = lat
        # state
        self.delivery_state = int(state)


        # def update_state(self):
        #     INI_STATE = 100
        #     min_state = INI_STATE
        #     if self.delivery_state < min_state:
        #         min_state = self.delivery_state



        


