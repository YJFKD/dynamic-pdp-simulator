class Restaurant(object):
    def __init__(self, restaurant_id: str, lng: float, lat: float, d_radius: int, c_radius: int, wait_time: int):
        '''
        Inputs: 
        - restaurant_id: index of restaurant
        - lng: restaurant longitude
        - lat: restaurant latitude
        - d_radius: radius of courier dispatch area
        - c_radius: radius of customer service area 
        - wait_time: avg waiting time at restaurant
        '''
        self.id = str(restaurant_id)
        self.lng = float(lng)
        self.lat = float(lat)
        self.dispatch_radius = int(d_radius)
        self.customer_radius = int(c_radius)
        self.wait_time = int(wait_time)

        