from Integrated_ABM.ABM_CE_PV_Model import *
from mesa.batchrunner import batch_run
import time
import pandas as pd
import os

# Set the folder
if USE:
    folder = "Resources"
    max_impact_count_run_0 = 2.38e-5 # Set the maximum impact count for run 0
    min_impact_count_run_0 = 1.09e-5 # Set the minimum impact count for run 0
else:
    folder = "ClimateChange"
    max_impact_count_run_0 = 0.193
    min_impact_count_run_0 = 0.13

# Set the use case
Seed = True # Set the seed. If True, the seed is fixed. If False, the 100 seeds are used.

if Seed: 
    step = 0.05 # Set the step for the threshold
    sample_size = 10 # Set the sample size for the threshold
    threshold_concern = [max_impact_count_run_0 - (max_impact_count_run_0*i*step) for i in range(sample_size)]
    threshold_indifference = [min_impact_count_run_0 + (min_impact_count_run_0*i*step) for i in range(sample_size)]
    seed = 1
    name = 'batch_fixed_seed'
else:
    step = 0.05 # Set the step for the threshold
    n=9
    threshold_concern = [max_impact_count_run_0 - (step*n*max_impact_count_run_0)]
    threshold_indifference = [0]
    seed = range(100)
    name = f'batch_seed_results{n}'

# Batch run model 
if __name__ == '__main__':
    t0 = time.time()

    # Ensure the output directory exists
    output_dir = f"results/{folder}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the variable parameters for the batch run
    params = {
        "seed": seed,
        "threshold_concern": threshold_concern,
        "threshold_indifference": threshold_indifference,
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
    results_df.to_csv(f"{output_dir}/{name}.csv")

    t1 = time.time()
    print(f"Batch run completed in {t1 - t0} seconds")