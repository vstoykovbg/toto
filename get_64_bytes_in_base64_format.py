#!/usr/bin/python3

from qrng_mixer import first_refill
from qrng_mixer import print_global_accumulator

first_refill()

print("")
print("Random 64 bytes in base64 format:")
print("")

print_global_accumulator()


