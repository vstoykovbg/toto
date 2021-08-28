#!/usr/bin/python3

from qrng_mixer import first_refill
from qrng_mixer import random_below
from qrng_mixer import print_global_accumulator


top_number = int(input("Inclusive upper bound: "))
assert top_number > 1
how_many = int(input("How many numbers to be generated: "))
assert how_many > 0
print ("Generating", how_many, "numbers from 1 to", top_number, "(inclusive range)...")

first_refill()

print("")
print("After the first refill:")

print_global_accumulator()

set_of_random_numbers = set()

while len(set_of_random_numbers) < how_many:
    set_of_random_numbers.add(random_below(top_number) + 1)

print (how_many, "unique random numbers from 1 to", top_number, "(inclusive range):")
print (set_of_random_numbers)

