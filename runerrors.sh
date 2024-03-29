#!/bin/bash
#
#SBATCH --job-name=runerrors # give a meaningful name.
#SBATCH --error=runerrors.err
#SBATCH --out=runerrors-1-%j.out
#SBATCH -N 1 -n 1 # How many nodes and cores do you need?
#SBATCH --mem=5G # How much memory?
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=clkelly@stanford.edu
#SBATCH --time=30:00 # how much time?
#

ml reset
module load python/3.9.0
module load py-numpy/1.20.3_py39
module load py-pandas/1.3.1_py39
module load viz py-matplotlib/3.4.2_py39

python3 runerrors.py
