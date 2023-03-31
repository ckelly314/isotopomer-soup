#!/bin/bash
#
#SBATCH --job-name=PS1Surface # give a meaningful name.
#SBATCH --error=sherlock_output/PS1Surface.err
#SBATCH --out=sherlock_output/PS1Surface-1-%j.out
#SBATCH -N 1 -n 20 # How many nodes and cores do you need?
#SBATCH --mem=5G # How much memory?
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=clkelly@stanford.edu
#SBATCH --time=2:00:00 # how much time?
#

ml reset
module load python/3.9.0
module load py-numpy/1.20.3_py39
module load py-pandas/1.3.1_py39
module load viz py-matplotlib/3.4.2_py39

python3 PS1Surface.py

