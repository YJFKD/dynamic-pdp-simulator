class Customer(object):
    def __init__(self, customer_id: str, lng: float, lat: float, order_time: int):
        '''
        Inputs: customer can connect to orders
        - customer_id: id of the customer
        - lng: latitude of the customer 
        - lat: latitude of the customer 
        - order_time: order time of the customer
        '''
        self.id = customer_id
        self.lng = lng
        self.lat = lat
        self.order_time = order_time