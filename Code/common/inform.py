class InputInform(object):
    def __init__(self, id_to_undispatched_order: dict, id_to_ongoing_order: 
                    dict, id_to_driver: dict, id_to_location: dict, route_map):
        '''
        Including all information, such as drivers (locations, carrying order), orders (undispatched and ongoing), routes
        Inputs: 
        - id_to_undispatched_order: dict, {key: id, value: order object (state: 'GENERATED')}
        - id_to_ongoing_order: dict, {key: id, value: order object (state: 'ONGOING')}
        - id_to_driver: dict, {key: driver id, value: driver object}
        - id_to_location: dict, {key: location id, value: location object (customer + restaurant + driver)}
        - route_map: travel distance and time matrix between locations
        '''
        self.id_to_undispatched_order = id_to_undispatched_order
        self.id_to_ongoing_order = id_to_ongoing_order
        self.id_to_driver = id_to_driver
        self.id_to_location = id_to_location
        self.route_map = route_map