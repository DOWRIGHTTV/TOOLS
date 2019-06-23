#!/usr/bin/env python3

import os

def Initialize():
    priv = os.geteuid()
    if (priv == 0):
        run = input('Run Lan Buster?: [Y/n]: ')
        if (run == '' or run.lower() == 'y'):
            return True
        else:
            return False
    else:
        print('DNX FWALL requires Root Priveledges. Exiting...')
        exit(1)
