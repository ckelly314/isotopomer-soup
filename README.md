# isotopomer-soup

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7810026.svg)](https://zenodo.org/badge/DOI/10.5281/zenodo.7810026.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Welcome to isotopomer-soup! isotopomer-soup is a model designed to solve for N2O production rates from 15N label experiments. Below is an overview of the directory structure and descriptions of each script.

<!-- TOC -->

- [isotopomer-soup](#isotopomer-soup)
    - [Citation](#citation)
    - [Files and Directories](#files-and-directories)
        - [Root Directory](#root-directory)
        - [figures/](#figures)
        - [sherlock_output/](#sherlock_output)
        - [scripts/](#scripts)
            - [functions submodule](#functions-submodule)
            - [initialization submodule](#initialization-submodule)
            - [model submodule](#model-submodule)
            - [montecarlo submodule](#montecarlo-submodule)
            - [optimization submodule](#optimization-submodule)
            - [postprocessing submodule](#postprocessing-submodule)
            - [preprocessing submodule](#preprocessing-submodule)
            - [runscripts submodule](#runscripts-submodule)
    - [Getting Started](#getting-started)
    - [License](#license)

<!-- /TOC -->

## Citation

A paper describing this model is freely available:

> C. L. Kelly, N. M. Travis, P. A. Baya, C. Frey, X. Sun, B. B. Ward, \& K. L. Casciotti (2024).  Isotopomer Labeling in Hybrid Nitrous Oxide Production.  *Biogeosciences* preprint. [doi:10.5194/egusphere-2023-2642](https://doi.org/10.5194/egusphere-2023-2642).


## Files and Directories

### Root Directory
* LICENSE: Contains the license information for the package.
* model.py: example script to run one instance of the model.
* montecarlo.py: run full monte carlo simulation with n optimizations for given station and feature.
* montecarlo.sh: SLURM batch script to submit montecarlo.py as a job to the Sherlock computer cluster.
* PS1Interface.py (and similar files): example Python script to run monte carlo simulation for PS1 Interface.
* PS1Interface.sh (and similar files): example SLURM batch script to submit PS1Interface.py to Sherlock computer cluster.
* README.md: The file you are currently reading. Provides an overview of the package and its structure.
* requirements.txt: Lists the dependencies required to run the package.
* runerrors.py: run mini-Monte Carlo simulation with only three model optimizations.
* runerrors.sh: SLURM batch script to submit runerrors.py to Sherlock computer cluster.

### figures/
Directory to save out model output figures.

### sherlock_output/
Directory to save .out files and .err files from Sherlock jobs.

### scripts/
This is the main package directory containing all the core code and submodules.
* __init__.py: Makes the directory a Python package. Can be used to import core modules or set up package-level variables.
* Data/: directory containing input and output data

#### functions submodule
* binomial.py: Probabilities of formation of different isotopic species of N2O based on binomial probability tree.
* binomial_stoichiometry.py: Probabilities of formation of different isotopic species of N2O based on binomial probability tree, taking the stoichiometry of NO+NH2OH into account
* convert_af.py: Convert atom fraction into 15R/14R ratio and d15N.
* convert_delta.py: Convert concentration and d15N into concentrations of 15N and 14N as well as atom fraction.

#### initialization submodule
* bgc.py: Initialize substrate concentrations and rates of transformation.
* initialize_n2o.py: Initialize concentrations of N2O isotopomers based on experimental t0.species of N2O based on binomial probability tree, taking the stoichiometry of NO+NH2OH into account
* intialize.py: Initialize inputs for model.
* isotope_effects.py: Define isotope effects to be used in the model.
* metadata.py: Giant dictionary containing relevant metadata for all N2O experiments.
* modelparams.py: Initialize model parameters.
* tracers.py: Initialize model parameters and arrays of state variables.

#### model submodule
* modelv1.py: Version of the model containing no intermediates; N2O is produced from NH4+, NO2-, NO3-, and two hybrid pathways, which produce N2O from a combination of NH4+ and NO2-.
* modelv2.py: Version of the model containing intermediates NH2OH and NO; N2O is produced from NH4+, NO2-, NO3-, and two hybrid pathways, which produce N2O from a combination of NH2OH and NO.
* modelv3.py: Version of the model containing intermediates NH2OH and NO; N2O is produced from NH4+, NO, NO3-, and two hybrid pathways, which produce N2O from a combination of NH2OH and NO.
* modelv4.py: Version of the model containing intermediates NH2OH and NO; N2O is produced from NH4+, NO2-, NO3-, and two hybrid pathways, which produce N2O from a combination of NH2OH and NO2-.
* modelv5.py: Version of the model used in publication. Version of the model containing no intermediates; N2O is produced from NH4+, NO2-, NO3-, and one hybrid pathway, which produces N2O from a combination of NH4+ and NO2-. In addition to rate constants, solve for "f" parameter, which is the proportion of the alpha nitrogen that is derived from nitrite.

#### montecarlo submodule
* genmontecarlo.py: Create nxm Numpy array of model parameters randomly sampled from a range of values from 75% to 125% of the parameter value, where n is the number of rows and m is the number of parameters.
* runmontecarlo.py: Run Monte Carlo simulation, running the model n times and varying key model parameters randomly by up to 25% for each iteration.

#### optimization submodule
* costfxn.py: Calculate cost from model output and N2O incubation data at each of 2-3 timepoints.
* initialguess_modelv1.py: Run the forward model, version 3, with 0 N2O production and estimate rate constants to feed to the optimization.
* initialguess.py: Run the forward model, version 3, with 0 N2O production and estimate rate constants to feed to the optimization.
* modelv5objective.py: Set up objective function that calculates cost of a model solution across all three tracer experiments.

#### postprocessing submodule
* plotmodeloutput.py: Plot model output with averaged incubation data at each timepoint and save figure as a PDF.
* plotmodeloutput2.py: Plot model output, showing triplicate incubation data at each timepoint and save figure as a PDF.
* postprocess.py: Calculate rates in nM/day from solved rate constants (x) and modeled substrate concentrations.

#### preprocessing submodule
* read_data.py: Read in incubation data to train N2O production model.

#### runscripts submodule
* datapath.py: Define paths to data files.
* errors.py: mini-Monte Carlo simulation with only three optimizations
* run.py: run one instance of a modelv1 optimization
* runmodelv5: run one instance of a modelv5 optimization

## Getting Started
To run the model, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/ckelly314/isotopomer-soup.git
cd isotopomer-soup
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Run the model:
```python
from isotopomer-soup import scripts
scripts.runmodelv5("PS3", "SCM")
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Thank you for using isotopomer-soup! If you have any questions or issues, feel free to open an issue or contact me.
