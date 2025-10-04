#!/bin/bash

echo "Running..."
gfortran ising2d.f90 -o ising2d.x
./ising2d.x

if [ $? -ne 0 ]; then
    echo "Failed. Exiting."
    exit 1
fi

python3 analisi_ising.py

