import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
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
number_of_runs = 10 # Set the number of runs

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
    4,8):
    # number_of_runs):
    # Construct the filename for each run
    filename = f"results/{folder}/seed1-increaseT/Results_model_run{i}.csv"
    
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Process the dataframe
    df['Agents recycling'] = df['Agents recycling'] / 10
    df['Agents selling'] = df['Agents selling'] / 10
    df['Agents landfilling'] = df['Agents landfilling'] / 10
    df['Yearly electricity production'] = df['Total product'] * 1.825 ## conversion from Wp to kWh/year considering 5 hours of peak sun per day
    df['Impact'] = df['Yearly electricity production'] * df['Impact count']
    # Calculate the cumulative impact over time
    df['Cumulative impact'] = df['Impact'].cumsum()
    # Calculate the cumulative impact per year
    # df['Cumulative impact'] = df.groupby('Year').apply(lambda x: (x['Total product'] * x['Impact count']).cumsum()).reset_index(level=0, drop=True)
    
    # Append the processed dataframe to the list
    dfs.append(df)

# Optionally, concatenate all dataframes into a single dataframe
all_data = pd.concat(dfs, ignore_index=True)

# Create a figure with a custom layout
fig = plt.figure(figsize=(16, 8))
gs = GridSpec(2, 3, height_ratios=[1, 1])

# Create the three subplots on top
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

# Create the single subplot underneath
ax4 = fig.add_subplot(gs[1, 0])
ax5 = fig.add_subplot(gs[1, 1])

# Create an empty subplot for the legend in the third column of the second row
ax_legend = fig.add_subplot(gs[1, 2])
ax_legend.axis('off')  # Hide the axis

# Plot the "Impact count" column on the first y-axis
linestyles = ['-', '--', ':', '-.']
for i, df in enumerate(dfs):
    df['Impact count'].plot(kind='line', ax=ax4, color='b', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                            label='Impact score')
    df['Cumulative impact'].plot(kind='line', ax=ax5, color='black', linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                            label='Cumulative impact')
    # if i==6:
    #     ax1.annotate(f'seed = {i}', xy=(df.index[-1], df['Impact count'].iloc[-1]), xytext=(-40, 5),
    #          textcoords='offset points', ha='left', va='bottom', fontsize=8, color='black')
# Add intercepts for thresholds
if threshold_concern != None:
    ax4.axhline(y=threshold_concern, color='black', linestyle='--', linewidth=1)
if threshold_no_concern != None:
    ax4.axhline(y=threshold_no_concern, color='black', linestyle='--', linewidth=1) #label='decreasing concern threshold = 0.75e-5')
    ax4.annotate('decreasing pro-environmental attitude', xy=(0, threshold_no_concern), xytext=(-5, -10),
                 textcoords='offset points', ha='left', va='top', fontsize=10, color='black', backgroundcolor='none')

# Set labels for first y-axis
ax4.set_xlabel('Time [years]', fontsize=14)
if USE:
    ax4.set_ylabel('Resources, minerals and metals [kgSb-eq/kWh]', fontsize=14, color='black')
    ax5.set_ylabel('Cumulative impact [kgSb-eq]', fontsize=14, color='black')   
else:
    ax4.set_ylabel('Climate change [kgCO2-eq/kWh]', fontsize=14, color='black')
    ax5.set_ylabel('Cumulative impact [kgCO2-eq]', fontsize=14, color='black')
ax4.tick_params(axis='y', labelcolor='black')
# Plot the "Agents recycling" and "Agents selling" columns on the second subplot
for i, df in enumerate(dfs):
    df['Agents recycling'].plot(kind='line', ax=ax1, color='r', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                                label='Agents recycling')
    df['Agents selling'].plot(kind='line', ax=ax2, color='g', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                              label='Agents selling')
    df['Agents landfilling'].plot(kind='line', ax=ax3, color='y', linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                                    label='Agents landfilling')  

# Set labels for second y-axis
ax1.set_xlabel('Time [years]', fontsize=14)
ax2.set_xlabel('Time [years]', fontsize=14)
ax3.set_xlabel('Time [years]', fontsize=14)
ax5.set_xlabel('Time [years]', fontsize=14)
ax1.set_ylabel('Agents [%]', fontsize=14, color='black')
# ax2.set_ylabel('Agents selling [%]', fontsize=14, color='black')
# ax3.set_ylabel('Agents landfilling [%]', fontsize=14, color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax1.set_ylim(0, 100)
ax2.set_ylim(0, 100)
ax3.set_ylim(0, 100)

# Add legends to the first three plots with only the first item
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles3, labels3 = ax3.get_legend_handles_labels()

ax1.legend(handles=[handles1[0]], labels=[labels1[0]], loc='upper left', fontsize=10, frameon=False)
ax2.legend(handles=[handles2[0]], labels=[labels2[0]], loc='upper left', fontsize=10, frameon=False)
ax3.legend(handles=[handles3[0]], labels=[labels3[0]], loc='upper left', fontsize=10, frameon=False)


# Create a single legend for the figure
# fig.legend(handles=handles1 + handles2, labels=labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 1), ncol=3, fontsize=12, frameon=False)

# Remove grid
ax1.grid(False)
ax2.grid(False)
ax3.grid(False)
ax4.grid(False)
ax5.grid(False)

custom_lines_1 = [
                  Line2D([0], [0], color='black', linestyle='-', lw=2, label='Increased concern threshold = 1.3e-5'),
                  Line2D([0], [0], color='black', linestyle='--', lw=2, label='Increased concern threshold = 1.1e-5'),
                  Line2D([0], [0], color='black', linestyle=':', lw=2, label='Increased concern threshold = 0.9e-5'),
                  Line2D([0], [0], color='black', linestyle='-.', lw=2, label='Increased concern threshold = 0.7e-5')
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
                # Line2D([0], [0], color='black', linestyle='-', lw=2, label='PEAM = 1'),
                # Line2D([0], [0], color='black', linestyle='--', lw=2, label='PEAM = 0.8'),
                # Line2D([0], [0], color='black', linestyle=':', lw=2, label='PEAM = 0.6'),
                # Line2D([0], [0], color='black', linestyle='-.', lw=2, label='PEAM = 0.4'),
                ] 
# fig.legend(handles=custom_lines_1, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=4, fontsize=12, frameon=False)    
ax_legend.legend(handles=custom_lines_1, labelspacing=1.5, loc='center', fontsize=12, frameon=False)

# Show the plot
plt.tight_layout()
plt.show()