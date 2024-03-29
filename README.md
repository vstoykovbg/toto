# Quantum Randomness Mixers

To get integers in range (between 1 and your desired number) use `range_mixed.py` (or `range_mixed_unique.py` if you need the numbers to be unique - useful for lotteries).

The script will get random data from a quantum random number generator (qrng.anu.edu.au) and will mix it with local sources (your computer's microphone input, haveged, /dev/random).

The script `range.py` is getting randomness only from qrng.anu.edu.au (without mixing it with local sources of randomness). The numbers may not be unique (i.e. 4, 2, 2).

The script `6_from_49_mixed.py` is like `range_mixed.py` (but is with predefined parameters and produce unique numbers).

The script `6_from_49.py` is getting randomness only from qrng.anu.edu.au and is producing 6 uniqe numbers.

The file `qrng_mixer.py` contains the library used by `*_mixed*.py` scripts.

Scripts with `_unique.py` prefix are producing unique numbers (useflul for lotteries).

To test the presence of noise on the microphone input you can use `xoscope` (preferably compiled from source, the version from Ubuntu does not work for me). Also, you can check the presence of noise with the command `arecord | aplay`.

These scripts are intended to be used on Linux. But the simple versions (`range.py`, `6_from_49.py`) should work under Windows (I have not tested them on Windows).

Instead of a microphone, you can connect to the microphone input a noise generator like this:

[Noise generator without the need for additional power supply](https://rootvideochannel.blogspot.com/2021/05/noise-generator-without-need-for.html)

![Noise generator without the need for additional power supply](https://1.bp.blogspot.com/-sUH68-a_mWI/YJHBmaVrs9I/AAAAAAAAFZ4/MISOtCU5pWQNhMdL2PT9lq_UTB_PkwRjQCLcBGAsYHQ/s1073/noise-generator-1_captions.png "Noise generator")
