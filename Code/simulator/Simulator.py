import datetime
import math


def cal_distance(l1, l2):
    '''
    calculate the Euclidean distance between l1 and l2
    '''
    ans = math.sqrt((l1[0] - l2[0])**2 + (l1[1] - l2[1])**2)
    return round(ans, 2)


class Order():
    '''
    Orders class
    - index: order index
    - restaurant: order comes from
    - driver: dispatched driver, initial equals to 0
    - state: ['None', 'active', 'dispatching', 'finished', 'non-response']
    '''
    def __init__(self, index, x1, y1, x2, y2) -> None:
        self.index = index
        self.restaurant = 0
        self.driver = 0
        self.state = 'None'
        self.generate = datetime.datetime.now()
        self.promised_time = self.generate + datetime.timedelta(minutes=40)
        self.dropoff_time = self.generate
        self.pickup_loc = (x1, y1)
        self.dropoff_loc = (x2, y2)
    

class Driver():
    '''
    Driver (one drive represent a route) class
    - index: driver index
    - distance: traveled distance
    - capacity: maximum orders can carry, set to 10
    - state: ['None', 'serving', '']
    - orders: orders set, including finished orders and delivering orders
    - location: driver's location (update every dispatch epoch)
    '''
    def __init__(self, index):
        self.index = index
        self.distance = 0
        self.capacity = 10
        self.state = 'None'
        self.orders = []
        self.fin_orders = []
        self.on_orders = []
        self.location = [0, 0]

    def travel_distance(self):
        dist = 0
        for o in range(len(self.fin_orders) - 1):
            dist = cal_distance(self.fin_orders[o])


