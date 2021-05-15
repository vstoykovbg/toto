# Quantum Randomness

To get integers in range (between 1 and your desired number) use `range_mixed.py`.

The script will get random data from a quantum random number generator (qrng.anu.edu.au) and will mix it with local sources (your computer's microphone input, haveged, /dev/random).

The script `range.py` is getting randomness only from qrng.anu.edu.au (without mixing it with local sources of randomness).

The script `6_from_49_mixed.py` is like `range_mixed.py` (but is with predefined parameters).

The script `6_from_49.py` is getting randomness only from qrng.anu.edu.au.

The file `qrng_mixer.py` contains the library used by `range_mixed.py` and `6_from_49_mixed.py`.
