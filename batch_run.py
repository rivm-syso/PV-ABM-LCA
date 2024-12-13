# -*- coding:utf-8 -*-
"""
Created on Wed Nov 21 12:43 2019

Author: Julien Walzberg - Julien.Walzberg@nrel.gov

Run - batch of simulations with final state of outputs
"""

from ABM_CE_PV_Model import *
from mesa.batchrunner import batch_run
import time
import pandas as pd

# Set the folder
if USE:
    folder = "Resources"
    max_impact_count_run_0 = 2.38e-5 # Set the maximum impact count for run 0
    min_impact_count_run_0 = 1.09e-5 # Set the minimum impact count for run 0
else:
    folder = "ClimateChange"
    max_impact_count_run_0 = 0.193
    min_impact_count_run_0 = 0.13

########################################################## Fixed seed and combined concern and indifference threshold #####################################################

# ### Set the parameters for the batch run
# step = 0.05 # Set the step for the threshold
# sample_size = 10 # Set the sample size for the threshold

# # create list for threshold of concern and indifference
# threshold_concern = [max_impact_count_run_0 - (max_impact_count_run_0*i*step) for i in range(sample_size)]
# threshold_indifference = [min_impact_count_run_0 + (min_impact_count_run_0*i*step) for i in range(sample_size)]

# # Batch run model 
# if __name__ == '__main__':
#     t0 = time.time()

#     # Define the variable parameters for the batch run
#     params = {
#         "seed": [1],
#         "threshold_concern": threshold_concern,
#         "threshold_indifference": threshold_indifference,
#         "positive_feedback": [1],
#         "negative_feedback": [-0.5],
#         "calibration_n_sensitivity": [0.544]
#     }

#     # Run the batch with a progress bar
#     results = batch_run(
#         ABM_CE_PV,
#         parameters=params,
#             iterations=1,
#             max_steps=30,
#             number_processes=None,
#             data_collection_period=1,
#             display_progress=True
#     )

#     results_df = pd.DataFrame(results)

#     # Save results
#     results_df.to_csv(f"results/{folder}/batch_run_results.csv")

#     t1 = time.time()
#     print(f"Batch run completed in {t1 - t0} seconds")

########################################################## Fixed threshold and 100 seeds #####################################################

### Set the parameters for the batch run
step = 0.05 # Set the step for the threshold
n=9 # Set for run with one threshold and different seeds

# Batch run model
if __name__ == '__main__':
    t0 = time.time()

    # Define the variable parameters for the batch run
    params = {
        "seed": range(100),
        "threshold_concern": [max_impact_count_run_0 - (step*n*max_impact_count_run_0)],
        "threshold_indifference": [0],
        "positive_feedback": [1],
        "negative_feedback": [-0.5],
        "calibration_n_sensitivity": [0.544]
    }

    # Run the batch with a progress bar
    results = batch_run(
        ABM_CE_PV,
        parameters=params,
            iterations=1,
            max_steps=30,
            number_processes=None,
            data_collection_period=1,
            display_progress=True
    )

    results_df = pd.DataFrame(results)

    # Save results
    results_df.to_csv(f"results/{folder}/batch_seed_results{n}.csv")

    t1 = time.time()
    print(f"Batch run completed in {t1 - t0} seconds")