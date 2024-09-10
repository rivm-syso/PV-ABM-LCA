import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns
import numpy as np

##CHANGE TRIGGERS HERE
USE = True  # Set to False to use climate change labels
threshold_concern = None # Set the threshold of concern. Set to None if you don't want to use it.
threshold_no_concern = None # Set the threshold of no concern. Set to None if you don't want to use it.
number_of_runs = 1 # Set the number of runs

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
for i in range(number_of_runs):
    # Construct the filename for each run
    filename = f"results/{folder}/Results_model_run{i}.csv"
    
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Process the dataframe
    df['Agents recycling'] = df['Agents recycling'] / 10
    df['Agents selling'] = df['Agents selling'] / 10
    
    # Append the processed dataframe to the list
    dfs.append(df)

# Optionally, concatenate all dataframes into a single dataframe
all_data = pd.concat(dfs, ignore_index=True)

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(7, 5))

# Plot the "Impact count" column on the first y-axis
linestyles = ['-', '--', ':', '-.']
for i, df in enumerate(dfs):
    df['Impact count'].plot(kind='line', ax=ax1, color='b', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                            label=f'Impact score run {i+1}')

# Set labels for first y-axis
ax1.set_xlabel('Time [years]', fontsize=10)
if USE:
    ax1.set_ylabel('Impact “resources, minerals and metals” [kg Sb-eq]', fontsize=10, color='black')
else:
    ax1.set_ylabel('climate change [kg CO2-eq]', fontsize=10, color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Create a second y-axis
ax2 = ax1.twinx()

# Plot the "Agents recycling" column on the second y-axis for each dataframe
for i, df in enumerate(dfs):
    df['Agents recycling'].plot(kind='line', ax=ax2, color='r', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                                label=f'Agents recycling run {i+1}')
    
# Plot the "Agents selling" column on the second y-axis for each dataframe
for i, df in enumerate(dfs):
    df['Agents selling'].plot(kind='line', ax=ax2, color='g', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                              label=f'Agents selling run {i+1}')
    
# Set labels for second y-axis
ax2.set_ylabel('Agents [%]', fontsize=10, color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Add intercepts for thresholds
if threshold_concern != None:
    ax1.axhline(y=threshold_concern, color='black', linestyle='--', linewidth=1)
if threshold_no_concern != None:
    ax1.axhline(y=threshold_no_concern, color='black', linestyle='--', linewidth=1)

# Get the handles and labels from both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Create a single legend for the figure
fig.legend(handles=handles1 + handles2, labels=labels1 + labels2, loc='lower right', bbox_to_anchor=(0.9, 0.21))

# Remove grid
ax1.grid(False)
ax2.grid(False)

# Show the plot
plt.show()