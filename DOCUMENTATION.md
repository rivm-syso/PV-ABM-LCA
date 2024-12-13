## Changes and General Description of Preexistent Scripts

### 1. ABM_CE_PV_Model
This script defines the primary rules and functions of the Agent-Based Model (ABM). At every timestep, these functions are executed to ensure the model operates as intended.
Key tasks include:
- Importing the metamodel.
- Defining initialization and update functions for metamodel inputs.
- Calculating environmental impacts.
- Incorporating the effects of environmental impacts on agents’ pro-environmental attitudes.
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
##### Function: `impact_calculation()`
- **Description**: This function calculates the environmental impact based on the current state of the model. It uses the metamodel to estimate the impact of various actions and decisions made by the agents.
- **Purpose**: To provide an accurate estimation of the environmental impact resulting from the agents' actions and decisions.
- **How it Works**:
  - Collects inputs for the metamodel.
  - Uses the metamodel to estimate the impact based on the collected data
  - Updates the model with the calculated impact values.
##### Function: `impact_effect()`
- **Description**: This function calculates the effect of environmental impacts on the pro-environmental attitude level of agents.
- **Purpose**: To adjust the pro-environmental attitude of agents based on the environmental impacts.
- **How it Works**:
  - Checks the current impact count against the concern and no concern thresholds.
  - Checks whether the impact count is above the concern threshold, below the indifference threshold, or in between to decide between a positive_feedback (default=1), negative_feedback(default=-0.5) or no feedback.
  - Returns the calculated effect.

### 2. ABM_CE_PV_ConsumerAgents
This script defines the rules at the agent level, which are applied to each agent at every timestep. The most important rule is the theory of planned behavior, based on which the agents make a choice about the end of life. A key function, tpb_attitude, has been modified to incorporate the impact_effect() function.
##### Function: `tpb_attitude()`
- **Description**: Assigns an attitude level to each agent based on their decision-making process. Options considered pro-environmental get a higher score than other options by default. Then the attitude is modified by multiplying it with `1+effect`. The effect is calculated with impact_eff() function. 
- **Purpose**: To ensure that pro-environmental options are favored in the decision-making process.
- **How it Works**:
  - Iterates through the attitude levels for each decision option
  - For EoL pathways, it adjusts the attitude level based on whether the option is considered pro-environmental (repair, sell, recycle) or not.
  - For purchase choices, it adjusts the attitude level based on whether the option is considered pro-environmental (used, certified) or not.
  - Returns the weighted attitude levels.

### 3. ABM_CE_PV_MultipleRun
This script defines the number of runs and fixes variable parameters for each run. It was used to find the values for max and min impact.

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
- `threshold_concern`: A list of concern thresholds for each run.
- `threshold_indifference`: A list of indifference thresholds for each run.
- `seed`: Specifies the random seed to ensure reproducibility in simulations.
- `positive_feedback`: Value or list of values according to modeller's choice. Defines the adjustment factor applied when agents exceed the concern threshold, encouraging pro-environmental behavior. Default is 1 (100% increase of pro-environmental attitude level).
- `negative_feedback`: Value or list of values according to modeller's choice. Defines the adjustment factor applied when agents fall below the indifference threshold, discouraging pro-environmental behavior. Default is -0.5(50% decrease of pro-environmental attitude level).
- `calibration_n_sensitivity`: Value = 0.544. Represents the calibrated mean of agents' pro-environmental attitude level according to Walzberg et al., 2021. 
#### How it Works
1. **Set the Folder and Impact Counts**: Depending on the `USE` variable, set the folder and the maximum and minimum impact counts for run 
2. **Define Variable Parameters**: Define the variable parameters for the batch run.
3. **Run the Batch with a Progress Bar**: Execute the batch run using the batch_run function from the mesa library, with a progress bar to display the progress.
4. **Save the Results**: Save the results of the batch run to a csv file.

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
This script implements the high-dimensional model representation (HDMR) for abiotic resource depletion (RD) analysis.

### 7. LegendreShiftPoly
This script contains functions for working with Legendre shifted polynomials, which are used in the HDMR metamodel.

### 8. LCA_output
This script processes the life cycle assessment (LCA) output data for use in the metamodel.