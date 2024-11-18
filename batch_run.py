# -*- coding:utf-8 -*-
"""
Created on Wed Nov 21 12:43 2019

Author: Julien Walzberg - Julien.Walzberg@nrel.gov

Run - batch of simulations with final state of outputs
"""

from ABM_CE_PV_Model import *
from mesa.batchrunner import batch_run
from SALib.sample import saltelli
from SALib.analyze import sobol
import time
import pandas as pd

# Batch run model
if __name__ == '__main__':
    t0 = time.time()

    # Define the variable parameters for the batch run
    params = {
        "seed": list(range(5)),
        "threshold_concern": [0.3821, 0.35, 0.3],
        "threshold_no_concern": [0],
        "positive_feedback": [1, 0.5],
        "negative_feedback": [0],
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
    results_df.to_csv("results/batch_run_results.csv")

    t1 = time.time()
    print(f"Batch run completed in {t1 - t0} seconds")