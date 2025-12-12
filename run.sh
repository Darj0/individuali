#!/bin/bash

for n_proc in 1 2 4 6 8; do
    echo ""
    echo "Su $n_proc procesais"
    mpirun -n $n_proc python ind.py 
done



