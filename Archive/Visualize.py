
from ABM_CE_PV_Model import USE 
import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns
import numpy as np

##CHANGE TRIGGERS HERE
# USE = True  # Set to False to use climate change labels
threshold_concern = None # Set the threshold of concern. Set to None if you don't want to use it.
threshold_no_concern = None # Set the threshold of no concern. Set to None if you don't want to use it.
number_of_runs = 4 # Set the number of runs

# Set the folder
if USE:
    folder = "Resources"
else:
    folder = "ClimateChange"

# Set the style of seaborn
sns.set_style("whitegrid")
sns.set_color_codes(palette='deep')

# Initialize an empty list to store dataframes
dfs = []

# Read the files
# Loop through the number of runs
for i in range(
    # 0,4):
    number_of_runs):
    # Construct the filename for each run
    filename = f"results/{folder}/Results_model_run{i}.csv"
    
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Process the dataframe
    df['Agents recycling'] = df['Agents recycling'] / 10
    df['Agents selling'] = df['Agents selling'] / 10
    df['Agents landfilling'] = df['Agents landfilling'] / 10
    
    # Append the processed dataframe to the list
    dfs.append(df)

# Optionally, concatenate all dataframes into a single dataframe
all_data = pd.concat(dfs, ignore_index=True)

# Create a figure and a set of subplots
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(12,6))

# Plot the "Impact count" column on the first y-axis
linestyles = ['-', '--', ':', '-.']
for i, df in enumerate(dfs):
    df['Impact count'].plot(kind='line', ax=ax1, color='b', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                            label=f'Impact score run {i+1}')
    # if i==6:
    #     ax1.annotate(f'seed = {i}', xy=(df.index[-1], df['Impact count'].iloc[-1]), xytext=(-40, 5),
    #          textcoords='offset points', ha='left', va='bottom', fontsize=8, color='black')
    
# Add intercepts for thresholds
if threshold_concern != None:
    ax1.axhline(y=threshold_concern, color='black', linestyle='--', linewidth=1)
if threshold_no_concern != None:
    ax1.axhline(y=threshold_no_concern, color='black', linestyle='--', linewidth=1) #label='decreasing concern threshold = 0.75e-5')
    ax1.annotate('decreasing pro-environmental attitude', xy=(0, threshold_no_concern), xytext=(-5, -10),
                 textcoords='offset points', ha='left', va='top', fontsize=10, color='black', backgroundcolor='none')

# Set labels for first y-axis
ax1.set_xlabel('Time [years]', fontsize=14)
if USE:
    ax1.set_ylabel('Impact “resources, minerals and metals” [kgSb-eq/kWh]', fontsize=14, color='black')
else:
    ax1.set_ylabel('Climate change [kgCO2-eq/kWh]', fontsize=14, color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Plot the "Agents recycling" and "Agents selling" columns on the second subplot
for i, df in enumerate(dfs):
    df['Agents recycling'].plot(kind='line', ax=ax2, color='r', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                                label=f'Agents recycling run {i+1}')
    df['Agents selling'].plot(kind='line', ax=ax2, color='g', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                              label=f'Agents selling run {i+1}')
    df['Agents landfilling'].plot(kind='line', ax=ax2, color='y', linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                                    label=f'Agents landfilling run {i+1}')  
    
# Set labels for second y-axis
ax2.set_xlabel('Time [years]', fontsize=14)
ax2.set_ylabel('Agents [%]', fontsize=14, color='black')
ax2.tick_params(axis='y', labelcolor='black')


# Get the handles and labels from both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Create a single legend for the figure
# fig.legend(handles=handles1 + handles2, labels=labels1 + labels2, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4)

# # # Create custom legend
from matplotlib.lines import Line2D

custom_lines = [
                Line2D([0], [0], color='r', lw=2, label='Agents recycling'),
                Line2D([0], [0], color='g', lw=2, label='Agents selling'),
                Line2D([0], [0], color='y', lw=2, label='Agents landfilling'),
                ]

fig.legend(handles=custom_lines, loc='upper center', bbox_to_anchor=(0.5, 1), ncol= 3, fontsize=12, frameon=False)    

custom_lines_1 = [
                #   Line2D([0], [0], color='black', linestyle='-', lw=2, label='ICT = 1.6e-5'),
                #   Line2D([0], [0], color='black', linestyle='--', lw=2, label='ICT = 1.4e-5'),
                #   Line2D([0], [0], color='black', linestyle=':', lw=2, label='ICT = 1.2e-5'),
                #   Line2D([0], [0], color='black', linestyle='-.', lw=2, label='ICT = 1e-5')
                #   Line2D([0], [0], color='black', linestyle='-', lw=2, label='ICT = 0.37'),
                #   Line2D([0], [0], color='black', linestyle='--', lw=2, label='ICT = 0.33'),
                #   Line2D([0], [0], color='black', linestyle=':', lw=2, label='ICT = 0.29'),
                #   Line2D([0], [0], color='black', linestyle='-.', lw=2, label='ICT = 0.25')
                #   Line2D([0], [0], color='black', linestyle='-', lw=2, label='DCT = 0.9e-5'),
                #   Line2D([0], [0], color='black', linestyle='--', lw=2, label='DCT = 1e-5'),
                #   Line2D([0], [0], color='black', linestyle=':', lw=2, label='DCT = 1.1e-5'),
                #   Line2D([0], [0], color='black', linestyle='-.', lw=2, label='DCT = 1.2e-5'),
                #   Line2D([0], [0], color='black', linestyle='-', lw=2, label='seed = 0'),
                #   Line2D([0], [0], color='black', linestyle='--', lw=2, label='seed = 1'),
                #   Line2D([0], [0], color='black', linestyle=':', lw=2, label='seed = 2'),
                #   Line2D([0], [0], color='black', linestyle='-.', lw=2, label='seed = 3'),
                #   Line2D([0], [0], color='black', linestyle='-', lw=2, label='increase factor = 2'),
                #   Line2D([0], [0], color='black', linestyle='--', lw=2, label='increase factor = 1.9'),
                #   Line2D([0], [0], color='black', linestyle=':', lw=2, label='increase factor = 1.8'),
                #   Line2D([0], [0], color='black', linestyle='-.', lw=2, label='increase factor = 1.7'),
                Line2D([0], [0], color='black', linestyle='-', lw=2, label='PEAM = 1'),
                Line2D([0], [0], color='black', linestyle='--', lw=2, label='PEAM = 0.8'),
                Line2D([0], [0], color='black', linestyle=':', lw=2, label='PEAM = 0.6'),
                Line2D([0], [0], color='black', linestyle='-.', lw=2, label='PEAM = 0.4'),
                ] 
fig.legend(handles=custom_lines_1, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=4, fontsize=12, frameon=False)    

# Remove grid
ax1.grid(False)
ax2.grid(False)

# Show the plot
plt.tight_layout(pad=4.0)   
plt.show()