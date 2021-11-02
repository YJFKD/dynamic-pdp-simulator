import sys

class Route(object):
    def __init__(self, route_id: str, start_id: str, end_id: str, distance: float, time: float):
        '''
        Inputs:
        - route_id: index of the route
        - start_id: start location id
        - end_id: end location id
        - distance: route distance
        - time: route travel time 
        '''
        self.route_id = str(route_id)
        self.start_id = str(start_id)
        self.end_id = str(end_id)
        self.distance = float(distance)
        self.time = float(time)



class Map(object):
    def __init__(self, id_to_route):
        '''
        Input:
        - id_to_route: dict, {key: route_id, value: route}
        '''
        self.__id_to_route = id_to_route
        self.__loc_id_pair_to_distance = self.__get_distance_matrix_between_loc()
        self.__loc_id_pair_to_time = self.__get_time_matrix_between_loc()


    def __get_distance_matrix_between_loc(self):
        '''
        Output: dict, {key: (start location, end location), value: distance}
        '''
        if len(self.__id_to_route) == 0:
            return
        # define distance matrix
        dist_matrix = {}
        for route_id, route in self.__id_to_route.items():
            if (route.start_id, route.end_id) not in dist_matrix:
                dist_matrix[(route.start_id, route.end_id)] = route.distance
        
        return dist_matrix
    
    
    def __get_time_matrix_between_loc(self):
        '''
        Output: dict, {key: (start location, end location), value: travel time}
        '''
        if len(self.__id_to_route) == 0:
            return 
        # define time matrix
        time_matrix = {}
        for route_id, route in self.__id_to_route.items():
            if (route.start_id, route.end_id) not in time_matrix:
                time_matrix[(route.start_id, route.end_id)] = route.time 
        
        return time_matrix


    def calculate_distance_between_loc(self, org_loc_id, dest_loc_id):
        if org_loc_id == dest_loc_id:
            return 0
        
        if (org_loc_id, dest_loc_id) in self.__loc_id_pair_to_distance:
            return self.__loc_id_pair_to_distance.get((org_loc_id, dest_loc_id))
        else:
            print(f"({org_loc_id}, {dest_loc_id}) is not in distance matrix.")
            return sys.maxsize
    

    def calculate_time_between_loc(self, org_loc_id, dest_loc_id):
        if org_loc_id == dest_loc_id:
            return 0
        
        if (org_loc_id, dest_loc_id) in self.__loc_id_pair_to_time:
            return self.__loc_id_pair_to_time.get((org_loc_id, dest_loc_id))
        else:
            print(f"({org_loc_id}, {dest_loc_id}) is not in time matrix.")
            return sys.maxsize