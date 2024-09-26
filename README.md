# PV-ABM-ERA

PV-ABM-ERA is the pilot integration on two existing solar panel models (ABM and ERA).

The source code for the ABM model can be accessed at https://
github.com/NREL/ABSiCE.
The source code for the ERA model can be accessed at https://
github.com/rivm-syso/dynamic-era-energy.

 # How to run the model

 1. Create a new environment using the abm_mesa.yml file provided, using the command: conda env create -f environment.yml
 2. Activate the environment 
 3. Open ABM_CE_PV_Model and modify the trigger on line 10 to specify whether use the climate change or resource depletion metamodel.
 4. Open ABM_CE_PV_MultipleRun.py, model parameters can be assigned a value in the for loop (line 22). Adapt triggers in line 16, the number of runs can be changed as desired. Threshold_no_concern defines the value below which impacts discourage recycling and selling(reuse). Threshold_concern defines the value above which impacts encourage recycling and selling(reuse). Climate change impacts are in the range 0.2-0.4 kg Co2-eq and resource depletion impacts are in the range 0.6e-5 and 2.1e-5 kg Sb-eq.
 5. The model produces multiple excel files (number_runs (for model results) + 1(for agent results)). Open Visualize.py, adapt the triggers in line 8 to 11 and run the script to produce figures where impacts are compared to % of agents recycling and selling(reusing).

 # Changes and general description of scripts

 1. ABM_CE_PV_Model
 This script defines the main rules of the model. Every time step, this functions are triggered. Here I import the metamodel, define the functions to initialize and calculate (t>0) the inputs for the metamodel, define and use the function to calculate impact. I also added a function to calculate the material depletion effect on the pro-environmental attitude level of agents.

 2. ABM_CE_PV_ConsumerAgents
 This script defines the rules at the agent level, these are applied to each agent at every timestep. The most important being the theory of planned behaviour, based on which the agents make a choice about the end of life. Here I modified the function tpb_attitude, that assigns an attitude level to each agent, doubling the attitude when the impact is higher than a threshold of concern or halving the attitude when the impact is lower than a threshold of no concern.

 3. ABM_CE_PV_MultipleRun
This scripts defines the number of runs and fixes variables parameters for each run. I used it to produce scenarios, a sort of local sensitivity analisys with different thresholds.

 4. ABM_CE_PV_ProducerAgents, ABM_CE_PV_RecyclerAgents, ABM_CE_PV_RefurbisherAgents and ABM_CE_PV_BatchRun
 These scripts I haven't modified.