#!/usr/bin/python3

import json
import urllib.request

url = "https://qrng.anu.edu.au/API/jsonI.php?length=10&type=uint16"

global_accumulator = list()

def refill_global_accumulator():

    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = response.read()
    values = json.loads(data)   

    for number in values["data"]:
        global_accumulator.append(number)

    print ("Raw random numbers downloaded from the server:", global_accumulator)
    
def get_integer_from_accumulator():

    while len(global_accumulator) < 1:
        refill_global_accumulator()

    return global_accumulator.pop(0)    


# get random integer from [0, exclusive_upper_bound)
def random_below(exclusive_upper_bound):

    if not (isinstance(exclusive_upper_bound, int) and (exclusive_upper_bound > 0)):
        raise ValueError("Upper bound must be positive integer.")

    if (exclusive_upper_bound == 1):
        return 0

    inclusive_upper_bound = exclusive_upper_bound - 1

    how_many_bytes = 2

    source_exclusive_upper_bound = 256 ** how_many_bytes
    source_inclusive_upper_bound = source_exclusive_upper_bound - 1

    assert source_exclusive_upper_bound >= exclusive_upper_bound

    # floor division is used
    buckets = source_inclusive_upper_bound // exclusive_upper_bound

    assert isinstance(buckets, int)
    assert buckets > 0

    while (True):
        r = get_integer_from_accumulator() // buckets
        if r < ( exclusive_upper_bound):
            return r

inclusive_top = int(input("Inclusive upper bound: "))
how_many = int(input("How many numbers to be generated: "))
print ("Generating", how_many, "numbers from 1 to", inclusive_top, "(inclusive range)")

# to avoid infinite loops
assert how_many < inclusive_top

# using set to avoid duplicate numbers
numbers = set()

while len(numbers) < how_many:
    numbers.add(random_below(inclusive_top)+1)

assert how_many == len(numbers) 

print ("Printing", len(numbers), "unique numbers:")
print (numbers)


