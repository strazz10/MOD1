#!/bin/bash

input_dir="/home/strazz/Magistrale/NumMeth/MOD1/Clock"           
python_script="clock_loop.py"              #target python script 
output_file="clock_L.dat"                   #output file 
> "$output_file"                                   #clear the output 

echo "#beta		e		sigma_e		m		sigma_m		C		sigma_C		chi		sigma_chi    U" > "$output_file"
#loop over each input file in the directory
for input_file in "$input_dir"/*; do
    #check if the item is a txt file
    if [[ -f "$input_file" && "$input_file" == *.txt ]]; then
        echo "Processing $input_file..."
        #run the Python script with the input file, append the output to the output file
        python3 "$python_script" "$input_file" >> "$output_file"
        echo "Done processing $input_file"
    else
        echo "Skipping non-txt file: $input_file"
    fi
done

echo "All files processed. Output saved to $output_file."
