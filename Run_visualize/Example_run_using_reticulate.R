# script to run the model in R-studio
library(reticulate)

# see conda environmental available
conda_list()

# run if abm_mesa env is not available
conda_create("abm_mesa", channel = c("conda-forge"), environment = "abm_mesa.yml")

#Activate the environment
use_condaenv("abm_mesa")

# NOTE: this run takes a lot of cpu resources.
source_python("batch_run.py")
