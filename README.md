# PV-ABM-ERA

PV-ABM-ERA is the pilot integration of two existing solar panel models (ABM and ERA).

The source code for the ABM model can be accessed at https://github.com/NREL/ABSiCE.

## How to Run the Model

 1. Create a new environment using the abm_mesa.yml file provided, using the command: conda env create -f environment.yml
 2. Activate the environment 
 3. Open ABM_CE_PV_Model and modify the trigger on line 10 to specify whether use the climate change or resource depletion metamodel.
 4. Open batch_run and set the step and sample_size for the batch run. The choice will genereate two lists for the concern/indifference threshold threshold with lenght=sample_size and step between the values of 5% the max/min impact (found running the ABM_CE_PV_MultipleRun script with concern threshold = None(high number)/0). Threshold_no_concern defines the value below which impacts discourage recycling and selling(reuse). Threshold_concern defines the value above which impacts encourage recycling and selling(reuse).
 5. The model produces one CSV file (model results and agent results). Open batch_visualize.ipynb, adapt the USE trigger and run the script to produce figures where .

## Changes and General Description of Preexistent Scripts

### 1. ABM_CE_PV_Model
This script defines the main rules of the model. Every time step, these functions are triggered. Here I import the metamodel, define the functions to initialize and calculate (t>0) the inputs for the metamodel, define and use the function to calculate impact. I also added a function to calculate the material depletion effect on the pro-environmental attitude level of agents.
#### Key Additions
##### Function: `eol_rate_update()`
- **Description**: This function updates the end-of-life (EoL) rates for products based exclusevely on the EoL pathways that were selected, i.e, reuse, recycle and landfill.
- **Purpose**: To ensure that the metamodel receives accurate EoL rates.
- **How it Works**:
  - Removes the repair and storage pathways by setting their rates to 0.
  - Calculates the remaining percentage of reuse, recycle, and landfill pathways.
  - Normalizes the shares of reuse, recycle, and landfill pathways so they sum to 1.
  - Updates the model's EoL rates with the calculated values.
##### Function: `init_hdmr()`
- **Description**: This function initializes the inputs for the high-dimensional model representation (HDMR) metamodel. It sets up the fixed and linking parameters required by the metamodel.
- **Purpose**: To ensure that the HDMR metamodel receives the correct initial values for its parameters.
- **How it Works**:
  - Defines the minimum, maximum, and mode values for each fixed parameter.
  - Defines the minimum and maximum values for each linking parameter.
  - Uses statistical functions to calculate the values for lognormal and normal distributions.
##### Function: `update_metamodel_inputs()`
- **Description**: This function updates the inputs for the metamodel based on the current state of the model. It collects data from various agents and aggregates it to form the inputs required by the metamodel.
- **Purpose**: To ensure that the metamodel receives accurate and up-to-date inputs reflecting the current state of the simulation.
- **How it Works**:
  - Collects data from consumer, recycler, and refurbisher agents.
  - Aggregates the collected data to form the inputs for the metamodel.
  - Updates the metamodel inputs with the aggregated data.
- **Impact Calculation**: Defined and used a function to calculate the impact.
- **Pro-Environmental Attitude**: Added a function to calculate the material depletion effect on the pro-environmental attitude level of agents.

### 2. ABM_CE_PV_ConsumerAgents
This script defines the rules at the agent level, which are applied to each agent at every timestep. The most important rule is the theory of planned behavior, based on which the agents make a choice about the end of life. Here I modified the function `tpb_attitude`, which assigns an attitude level to each agent, doubling the attitude when the impact is higher than a threshold of concern or halving the attitude when the impact is lower than a threshold of no concern.

### 3. ABM_CE_PV_MultipleRun
This script defines the number of runs and fixes variable parameters for each run. I used it to produce scenarios, a sort of local sensitivity analysis with different thresholds.

### 4. ABM_CE_PV_ProducerAgents, ABM_CE_PV_RecyclerAgents, ABM_CE_PV_RefurbisherAgents, and ABM_CE_PV_BatchRun
These scripts define the behavior of different types of agents (producers, recyclers, refurbishers) and the batch run process. These scripts have not been modified.

## General Description of Additional Scripts

### 1. batch_run
This script runs multiple simulations in batch mode, allowing for the analysis of different scenarios and parameter settings.
#### Key Parameters
- `step`: The step size for adjusting the thresholds.
- `sample_size`: The number of values to test for each thresholds.
- `max_impact_count_run_0`: The maximum impact count for run 0 (can be calculated using ABM_CE_PV_MultipleRun).
- `min_impact_count_run_0`: The minimum impact count for run 0 (can be calculated using ABM_CE_PV_MultipleRun).
- `folder`: The folder to save the results, determined by the `USE` variable.
- `threshold_concern`: A list of concern thresholds for each run.
- `threshold_indifference`: A list of indifference thresholds for each run.

### 2. batch_visualize
This script visualizes the results of the batch runs, creating plots and charts to help analyze the outcomes of the simulations.

### 3. visualize_metamodel
This script visualizes the metamodel results, providing insights into the behavior and performance of the metamodel.

### 4. math_functions
This script, `math_functions.py`, contains a collection of mathematical functions for statistical calculations and normalization. The functions provided are useful for working with lognormal and normal distributions, as well as for normalizing values within a specified range.

#### Functions

- **lognormal_stats(mu, sigma)**
  - **Description**: Calculates the minimum, maximum, and mode values for a lognormal distribution given the mean (`mu`) and standard deviation (`sigma`) of the underlying normal distribution.
  - **Parameters**:
    - `mu` (float): The mean of the underlying normal distribution.
    - `sigma` (float): The standard deviation of the underlying normal distribution.
  - **Returns**: A tuple containing the minimum value, maximum value, and mode value of the lognormal distribution.

- **normal_stats(mu, sigma)**
  - **Description**: Calculates the minimum, maximum, and mode values for a normal distribution given the mean (`mu`) and standard deviation (`sigma`).
  - **Parameters**:
    - `mu` (float): The mean of the normal distribution.
    - `sigma` (float): The standard deviation of the normal distribution.
  - **Returns**: A tuple containing the minimum value, maximum value, and mode value of the normal distribution.

- **normalize_value(value, min_value, max_value)**
  - **Description**: Normalizes a value between a specified minimum and maximum value.
  - **Parameters**:
    - `value` (float): The value to be normalized.
    - `min_value` (float): The minimum value of the range.
    - `max_value` (float): The maximum value of the range.
  - **Returns**: The normalized value.
  - **Raises**: `ValueError` if `min_value` and `max_value` are the same.

### 5. Metamodel_HDMR_CC
This script implements the high-dimensional model representation (HDMR) for climate change (CC) analysis.

### 6. Metamodel_HDMR_RD
This script implements the high-dimensional model representation (HDMR) for resource depletion (RD) analysis.

### 7. LegendreShiftPoly
This script contains functions for working with Legendre shifted polynomials, which are used in the HDMR metamodel.

### 8. LCA_output
This script processes the life cycle assessment (LCA) output data for use in the metamodel.
