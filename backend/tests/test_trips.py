import pytest
import os
import logging

import trips_module as trips

def test_find_hotels():
    destination = "Boston, MA"
    num_hotels = 20
    result = trips.find_hotels(destination, num_hotels)
    assert result == True
    logging.info("find hotels test passed")

def test_get_directions():
    origin = "Boston, MA"
    destination = "NYC"
    dist, dur, direc = trips.get_directions(origin, destination)
    assert dist > 0
    logging.info("get directions test passed")

def test_get_gas_cost():
    origin = "NYC"
    destination = "Philadelphia"
    tank_size = 18
    mpg = 25
    assert trips.get_gas_cost(origin, destination, tank_size, mpg) == True
    logging.info("get gas cost test passed")