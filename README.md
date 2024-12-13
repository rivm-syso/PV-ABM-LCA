# PV-ABM-LCA

PV-ABM-LCA is the pilot integration of two existing solar panel models (ABM and LCA).

The source code for the ABM model can be accessed at [https://github.com/NREL/ABSiCE](https://github.com/NREL/ABSiCE).
The LCA model code is not open source, but the metamodel and the stocastic inputs and outputs are available in the [metamodel folder](./metamodel).

## How to Run the Model

1. **Create a new environment**: Use the `abm_mesa.yml` file provided to create a new environment with the command:
   ```sh
   conda env create -f environment.yml
   ```
2. **Activate the environment**:
   ```sh
   conda activate <environment_name>
   ```
3. **Modify the metamodel trigger**: Open `ABM_CE_PV_Model.py` and modify the trigger on line 10 to specify whether to use the climate change or resource depletion metamodel.
4. **Configure batch run parameters**:
   - Open `batch_run.py` 
   - Set step and sample_size:
      - step: Determines the %increment between consecutive values in the thresholds list.
      - sample_size: Specifies the number of values in the generated thresholds list.
   - This choice will generate two lists for the concern/indifference thresholds with `length=sample_size` and `% increment=step`. Max threshold of concern = max impact and min threshold of indifference = min impact.
   - The max impact is found by running the `ABM_CE_PV_MultipleRun.py` script without thresholds (threshold_concern=high number, threshold_indifference=0)
   - The min impact is found by running the script batch_run.py with concern threshold but without indifference threshold (threshold_concern=[max_impact - (max_impact*i*step) for i in range(sample_size)], threshold_indifference=0).
   - **Thresholds**:
     - `threshold_indifference`: Defines the value below which impacts discourage recycling and selling (reuse).
     - `threshold_concern`: Defines the value above which impacts encourage recycling and selling (reuse).
5. **Run the model**: The model produces one CSV file (model results and agent results). Open `batch_visualize.ipynb`, adapt the `USE` trigger, and run the script to produce figures where impacts are compared to the percentage of landfill and circular EoL pathways.

## Changes and Documentation
For detailed documentation about the new scripts and the changes in the old ones, please refer to the [DOCUMENTATION.md](DOCUMENTATION.md) file.
