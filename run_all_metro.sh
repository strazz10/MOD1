#!/bin/bash

echo "Running..."
gfortran metropolis.f90 -o metropolis.x
./metropolis.x

if [ $? -ne 0 ]; then
    echo "Failed. Exiting."
    exit 1
fi

python3 analisi_dati_mc.py

python3 plotter_metro.py
