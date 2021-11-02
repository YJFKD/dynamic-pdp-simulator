import datetime
import time
import pandas as pd

from Code.common.restaurant import Restaurant
from Code.common.customer import Customer
from Code.common.route import Map
from Code.common.route import Route
from Code.common.driver import Driver
from Code.configuration.config import Configs
from Code.utils.logging_engine import logger

def get_initial_data(data_file_path:str, driver_info_file_path:str, route_info_file_path:str,
                        customer_location_info_file_path:str, restaurant_location_info_file_path:str, initial_time:str):
    '''
    Get the input data for simulator
    Inputs:
    - data_file_path: information of orders
    - driver_info_file_path: information of driver
    - route_info_file_path: information of route
    - location_info_file_path: information of locations, including customer and restaurant
    - initial_time: timestamp, second
    Output:
    - id_to_order
    - id_to_driver
    - id_to_location
    - route_map
    '''
    # get the location information
    id_to_customer_location = get_customer_info(customer_location_info_file_path)
    id_to_restaurant_location = get_restaurant_info(restaurant_location_info_file_path)
    logger.info(f"Get {len(id_to_customer_location) + len(id_to_restaurant_location)} locations")


def get_customer_info(file_path:str):
    df = pd.read_csv(file_path)
    id_to_customer = {}
    for index, row in df.iterrows():
        customer_id = str(row['customer_id'])
        lng = float(row['longitude'])
        lat = float(row['latitude'])
        order_time = int(row['order_time'])
        customer = Customer(customer_id, lng, lat, order_time)
        if customer_id not in id_to_customer:
            id_to_customer[customer_id] = customer
    return id_to_customer


def get_restaurant_info(file_path:str):
    df = pd.read_csv(file_path)
    id_to_restaurant = {}
    for index, row in df.iterrows():
        restaurant_id = str(row['restaurant_id'])
        lng = float(row['longitude'])
        lat = float(row['latitude'])
        dispatch_radius = int(row['dispatch_radius'])
        customer_radius = int(row['customer_radius'])
        wait_time = int(row['wait_time'])
        restaurant = Restaurant(restaurant_id, lng, lat, dispatch_radius, customer_radius, wait_time)
        if restaurant_id not in id_to_restaurant:
            id_to_restaurant[restaurant_id] = restaurant
    return id_to_restaurant

