#!/usr/bin/env python
"""
This is the the radiative transfer equation solver. Given conditions specified
by command line switches, the solver will determine where heat flows to over
time.

Since right now this is a simplistic model of a sphere with layers of fixed
temperatures, it simply determines how much power is radiated back to the ground
and how much escapes into space.
"""

import argparse
import loaders

def main_():
    parser = argparse.ArgumentParser()
    parser.add_argument("--atmosphere", dest="atmosphere", type=loaders.parse_atmosphere_file)
    args = parser.parse_args()

if __name__ == '__main__':
    main_()
