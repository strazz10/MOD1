#!/bin/bash	
export LC_NUMERIC="en_US.UTF-8"      #sistema le virgole dei decimali

gfortran test_loop.f90 -o test_loop.x

#loop through numbers from 0.4 to 0.8 
for i in $(seq 0.4 0.02 0.8); do
    output_file="ising_beta_${i}.txt"
    echo "Sending input beta= $i to simulation"
    # pipe 
    echo "$i" | ./test_loop.x > "$output_file"
done
echo "Done simulating"

