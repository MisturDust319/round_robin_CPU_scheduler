"""
This is homework for my Operating Systems Class
Pt 1:
- generate 100 inter-arrival times between 4 and 8
- write a function to calculate arrival times
Pt 2:
- generate 100 service times between 2 and 5
"""

__author__ = "Stanislaus Slupecki"

import random
from cpu_tools import *

def generate_processes():
    """
    This function creates a list of 100 Process objects
    :return:
    100 process objects
    """
    processes = []
    arrival_times = inter_arrival_times_to_arrival_times(generate_inter_arrival_times())
    for i in range(len(arrival_times) - 1):
        arrival_time = arrival_times[i]
        # service time is an int between 2 and 5
        service_time = generate_service_times(1)
        new_process = Process(i + 1, service_time, arrival_time)
        processes.append(new_process)

    return processes
def generate_inter_arrival_times(number=100, min=4, max=8):
    """
    generate a number of inter arrival times
    between and including the numbers min and max
    :param number:
    The number of inter-arrival times to make
    Default value is 100
    :param min:
    The minimum time value
    :param max:
    The maximum time value
    :return:
    A list of |number| ints
    """
    times = [random.randint(min, max) for i in range(number)]
    # generate the list w/ a list comprehension
    return times

def inter_arrival_times_to_arrival_times(inter_arrival_times):
    """
    Takes a list of inter-arrival times and generates arrival times from these
    Assumes a first arrival time of 0
    :param inter_arrival_times:
    An iterable of inter-arrival times
    :return:
    A list of arrival times
    """
    # create a list of arrival times, init to 0
    # we assume the 1st arrival time is 0
    arrival_times = [0]
    if len(inter_arrival_times) == 1:
        # if only given one inter arrival time, return [0]
        return arrival_times
    else:
        for i in range(len(inter_arrival_times)):
            arrival_time = inter_arrival_times[i] + arrival_times[i]
            # arrival time is equal to the previous arrival time
            # plus the inter-arrival time between the current and previous process

            arrival_times.append(arrival_time)
            # add that value to the list of arrival times
    # return the arrival times
    return arrival_times

def generate_service_times(number=100, min=2, max=5):
    """
    Generate number of service times between and including min and max
    :param number:
    number of values to generate
    :param min:
    The minimum time value
    :param max:
    The maximum time value
    :return:
    A list of |number| ints
    if |number| is 1, it returns a single int
    """
    if(number < 2):
        return random.randint(min, max)
    else:
        times = [random.randint(min, max) for i in range(number)]
        # generate the list w/ a list comprehension
        return times

"""
def main():

    inter_arrival_times = generate_inter_arrival_times()
    print(inter_arrival_times)

    arrival_times = inter_arrival_times_to_arrival_times(inter_arrival_times)
    print(arrival_times)

    service_times = generate_service_times()
    print(service_times)
"""