#!/bin/bash	
export LC_NUMERIC="en_US.UTF-8"      #sistema le virgole dei decimali

gfortran clock.f90 -O2 -o clock.x

#loop through desired numbers 
for i in $(seq 0.75 0.01 0.90); do
    output_file="clock_beta_${i}.txt"
    echo "Sending input beta= $i to simulation"
    # pipe 
    echo "$i" | ./clock.x > "$output_file"
done
echo "Done simulating"

