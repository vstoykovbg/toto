#!/usr/bin/python3

from hashlib import sha512
from Crypto.Util.strxor import strxor
from os import urandom
from os.path import exists
import subprocess
from os import devnull
DEVNULL = open(devnull, 'wb')

import json
import urllib.request
import binascii

global_accumulator = list()
global_user_entropy = bytes()

assert isinstance(global_accumulator, list)


def get_random_bytes(howmany):
    if exists("/dev/random"):
        with open("/dev/random", 'rb') as f:
            return f.read(howmany)
    else:
        print ("/dev/random not found, using os.urandom instead.")
        return urandom(howmany)

def get_random_sound():
    return subprocess.Popen(["arecord", "-f", "cd", "-t", "raw", "-d", "5"], 
                                  stdout=subprocess.PIPE,stderr=DEVNULL).communicate()[0]

def haveged_1024_bytes():
    return subprocess.Popen(["haveged", "-n", "1024", "-f", "-"], 
                                  stdout=subprocess.PIPE,stderr=DEVNULL).communicate()[0]

def print_tolerant_error(msg, detail):
    print("\n\n" + msg, detail)
    print("However, this script is fault tolerant, so we continue.\n")

def print_global_accumulator():
    print ("global accumulator:", binascii.b2a_base64(bytes(global_accumulator), newline=False).decode("utf-8"))

def refill_global_accumulator():
    print("Refilling global_accumulator...")
    global global_accumulator
    global global_user_entropy

    assert isinstance(global_accumulator, list)
    assert isinstance(global_user_entropy, bytes)

    hash_sound = get_random_bytes(64)

    assert isinstance(hash_sound, bytes)
    assert len(hash_sound) == 64

    my_range=1
    for counter in range(my_range):
        print("Reading chunk", counter + 1, "from", my_range)
        random_sound_chunk = get_random_sound()

        if len(random_sound_chunk) < 100000:
            print_tolerant_error("⚠ We got from arecord something unexpected.", "")

        assert isinstance(hash_sound, bytes)
        assert len(hash_sound) == 64

        hash_sound = sha512(random_sound_chunk + hash_sound + global_user_entropy).digest()

        assert isinstance(hash_sound, bytes)
        assert len(hash_sound) == 64

        hash_sound = strxor( hash_sound, get_random_bytes(64) )

        assert isinstance(hash_sound, bytes)
        assert len(hash_sound) == 64

    this_hash = b''

    try:
        haveged_chunk = haveged_1024_bytes()
        this_hash = strxor(hash_sound, sha512(haveged_chunk).digest() )
    except Exception as detail:
        print_tolerant_error("⚠ Trying to get data from haveged failed.", detail)
        this_hash = strxor(hash_sound, get_random_bytes(64) )

    assert isinstance(this_hash, bytes)
    assert len(this_hash) == 64

    print ("Fetching data from qrng.anu.edu.au....")
    try:
        url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=hex16&size=64"

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        values = json.loads(data)   


        for hexdata in values["data"]:

            qrng_data = b''

            try:
                qrng_data = binascii.a2b_hex(hexdata)
            except ValueError as detail:
                print("  It does not look like a hexadecimal.", detail)
            else:
                print("We got data from qrng.anu.edu.au:", binascii.b2a_base64(qrng_data, newline=False).decode("utf-8"))
                if len(qrng_data) == 64:
                    print("Length looks good.")
                else:
                    print("Length is not 64!")

            assert isinstance(qrng_data, bytes)
            assert len(qrng_data) == 64

            this_hash = strxor(this_hash, qrng_data )

            assert isinstance(this_hash, bytes)
            assert len(this_hash) == 64


    except Exception as detail:
        print_tolerant_error("⚠ Trying to get data from qrng.anu.edu.au failed.", detail)

    
    assert isinstance(this_hash, bytes)
    assert len(this_hash) == 64

    assert isinstance(global_accumulator, list)
    global_accumulator += list(this_hash)
    assert isinstance(global_accumulator, list)


def get_random_bytes_from_global_accumulator(howmany):
    assert isinstance(howmany, int)
    assert howmany > 0

    global global_accumulator

    while len(global_accumulator) < howmany:
        refill_global_accumulator()

    result = bytearray()

    for c in range(howmany):
        result += bytes(global_accumulator.pop(0).to_bytes(1, 'big'))

    assert len(result) == howmany
        
    return result
    

def how_many_bytes_are_needed(n):
    if n < 0:
        raise ValueError("The number should not be negative.")
    i = 0
    while(n > 0):
        n = n >> 8;
        i += 1;
    return i


def get_integer_from_accumulator(size):
    assert size > 0
    assert isinstance(size, int)
    return int.from_bytes(get_random_bytes_from_global_accumulator(size), 'big')


# get random integer from [0, exclusive_upper_bound)
def random_below(exclusive_upper_bound):

    if not (isinstance(exclusive_upper_bound, int) and (exclusive_upper_bound > 0)):
        raise ValueError("Upper bound must be positive integer.")

    if (exclusive_upper_bound == 1):
        return 0

    inclusive_upper_bound = exclusive_upper_bound - 1

    # Intentionally adding one more byte to reduce the cycles
    how_many_bytes = 1 + how_many_bytes_are_needed(inclusive_upper_bound)

    source_exclusive_upper_bound = 256 ** how_many_bytes
    source_inclusive_upper_bound = source_exclusive_upper_bound - 1

    assert source_exclusive_upper_bound >= exclusive_upper_bound

    # floor division is used
    buckets = source_inclusive_upper_bound // exclusive_upper_bound

    assert isinstance(buckets, int)
    assert buckets > 0

    while (True):
        r = get_integer_from_accumulator(how_many_bytes) // buckets
        if r < ( exclusive_upper_bound):
            return r


def first_refill():
    print("Please boost the microphone input volume and connect a microphone")
    print("or other noise source.")
    print("(Before hitting Enter you may write a random string here.)")

    global global_user_entropy
    global_user_entropy = input("Press Enter to continue.").encode('utf-8')
    print ("\033[A\033[A") # up up (and go to new line) = up
    print ("--- Collecting randomness from the microphone input ---")

    refill_global_accumulator()


def main():

    first_refill()

    print("")
    print("After the first refill:")

    print_global_accumulator()

    print("")
    print("")

    how_many = 30
    upper_range = 500

    exclusive_upper_range = upper_range + 1

    list_of_random_numbers = list()

    for c in range(how_many):
        list_of_random_numbers.append(random_below(exclusive_upper_range))

    print (how_many, "random numbers between 0 and", upper_range, ":")
    print (list_of_random_numbers)


if __name__ == "__main__":
    main()

