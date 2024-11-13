import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from ABM_CE_PV_Model import USE 
import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.patches as patches

##CHANGE TRIGGERS HERE
# USE = False  # Set to False to use climate change labels
threshold = "Concern" # Set the threshold to concern or indifference.
step = 0.05 # Set the step for the threshold
number_of_runs = 10 # Set the number of runs

# Set the folder
if USE:
    folder = "Resources"
else:
    folder = "ClimateChange"

# Set the style of seaborn
sns.set_style("whitegrid")
sns.set_color_codes(palette='dark')

# Initialize an empty list to store dataframes
dfs = []

# Read the files
# Loop through the number of runs
for i in range(
    # 3,5):
    number_of_runs):
    # Construct the filename for each run
    
 
    filename = f"results/{folder}/Results_model_run{i}.csv"   

    # filename = f"results/{folder}/Figure_6/Results_model_run{i}.csv"
    
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Process the dataframe
    df['Agents recycling'] = df['Agents recycling'] / 10
    df['Agents selling'] = df['Agents selling'] / 10
    df['Agents choosing circular pathways'] = df['Agents selling'] + df['Agents recycling']
    df['Agents landfilling'] = df['Agents landfilling'] / 10
    df['Yearly electricity production'] = df['Total product'] * 1.825 ## conversion from Wp to kWh/year considering 5 hours of peak sun per day
    df['Impact'] = df['Yearly electricity production'] * df['Impact count']
    # Calculate the total end-of-life paths
    total_end_of_life = df['End-of-life - sold'] + df['End-of-life - recycled'] + df['End-of-life - landfilled']

    # Avoid division by zero by replacing zero totals with NaN
    total_end_of_life = total_end_of_life.replace(0, float('nan'))

    # Calculate the percentages
    df['End-of-life - sold'] = 100 * df['End-of-life - sold'] / total_end_of_life
    df['End-of-life - recycled'] = 100 * df['End-of-life - recycled'] / total_end_of_life
    df['End-of-life - circular pathways'] = df['End-of-life - sold'] + df['End-of-life - recycled']
    df['End-of-life - landfilled'] = 100 * df['End-of-life - landfilled'] / total_end_of_life
    # Calculate the cumulative impact over time
    df['Cumulative impact'] = df['Impact'].cumsum()
    # Fill NaN values with 0
    df = df.fillna(0)
    # Append the processed dataframe to the list
    dfs.append(df)


# Optionally, concatenate all dataframes into a single dataframe
all_data = pd.concat(dfs, ignore_index=True)

# Create a figure with a custom layout
fig = plt.figure(figsize=(10, 6))
gs = GridSpec(2, 2, height_ratios=[1, 1])

# Create the subplots
ax3 = fig.add_subplot(gs[0, 0])
ax4 = fig.add_subplot(gs[0, 1])
ax5 = fig.add_subplot(gs[1, 0])
ax6 = fig.add_subplot(gs[1, 1])

#set dotted linestyle for run 0 and solid for the rest

blue=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
# run = 0 in grey and for the rest divide the color palette in the number of runs-1
linecolors = [blue(i / (number_of_runs - 2)) for i in range(number_of_runs-1)]
linecolors.insert(0, 'grey')
 
if USE:
    for i, df in enumerate(dfs):
        linestyles = ':' if i == 0 else '-'
        df['Impact count'].plot(kind='line', ax=ax5, color=linecolors[i % len(linecolors)], linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                            label='Impact score [kgSb-eq/kWh]')
        df['Cumulative impact'].plot(kind='line', ax=ax6, color=linecolors[i % len(linecolors)], linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                            label='Cumulative impact [kgSb-eq]')
else:   
    for i, df in enumerate(dfs):
        linestyles = ':' if i == 0 else '-'
        df['Impact count'].plot(kind='line', ax=ax5, color=linecolors[i % len(linecolors)], linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
                            label='Impact score [kgCO2-eq/kWh]')
        df['Cumulative impact'].plot(kind='line', ax=ax6, color=linecolors[i % len(linecolors)], linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                            label='Cumulative impact [kgCO2-eq]')

# Plot the Agents  and EoL percentages        
for i, df in enumerate(dfs):
    linestyles = ':' if i == 0 else '-'
    # df['Agents choosing circular pathways'].plot(kind='line', ax=ax1, color='g', linewidth=2.0, linestyle=linestyles[i % len(linestyles)], 
    #                             label='circular pathways')
    # df['Agents landfilling'].plot(kind='line', ax=ax2, color='y', linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
    #                                 label='landfilling')  
    df['End-of-life - circular pathways'].plot(kind='line', ax=ax3, color=linecolors[i % len(linecolors)], linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                                    label='circular pathways')
    df['End-of-life - landfilled'].plot(kind='line', ax=ax4, color=linecolors[i % len(linecolors)], linewidth=2.0, linestyle=linestyles[i % len(linestyles)],
                                    label='landfilling')


# Set labels for impact y-axis
if USE:
    ax5.set_ylabel('Mineral depletion [kgSb-eq/kWh]', fontsize=14, color='black')
    ax6.set_ylabel('Mineral depletion [kgSb-eq]', fontsize=14, color='black')
    ax5.set_title('Impact Score', fontsize=14)
    ax6.set_title('Cumulative Impact', fontsize=14)
else:
    ax5.set_ylabel('Climate change [kgCO2-eq/kWh]', fontsize=14, color='black')
    ax6.set_ylabel('Climate change [kgCO2-eq]', fontsize=14, color='black')
    ax5.set_title('Impact Score', fontsize=14)
    ax6.set_title('Cumulative Impact', fontsize=14)
ax4.tick_params(axis='y', labelcolor='black')


# Set labels for x-axis
# ax4.set_xlabel('  ', fontsize=14)
ax5.set_xlabel('Time [years]', fontsize=14)
ax6.set_xlabel('Time [years]', fontsize=14)

# Set labels for y-axis
# ax1.set_ylabel('Agents [%]', fontsize=14, color='black')
ax3.set_ylabel('EoL product [%]', fontsize=14, color='black')
ax4.set_ylabel('EoL product [%]', fontsize=14, color='black')

# Set the y-axis limits
ax3.set_ylim(-1, 102)
ax4.set_ylim(-1, 102)
# ax5.set_ylim(0.8e-5, 2.7e-5)

# Remove grid
ax3.grid(False)
ax4.grid(False)
ax5.grid(False)
ax6.grid(False)

#Add title for the plots
ax3.set_title('Circular Pathways', fontsize=14)
ax4.set_title('Landfilling', fontsize=14)

# Add grey line for linear coupling
custom_lines_1 = [Line2D([0], [0], color='grey', linestyle=':', lw=2, label='Without concern threshold')]

fig.legend(handles=custom_lines_1, loc='lower center', bbox_to_anchor=(0.5, 0), fontsize=12, frameon=False)   

# Create a custom color bar with an arrow shape
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.8])  # [left, bottom, width, height]
gradient = np.linspace(0, 1, 256).reshape(256, 1)
cbar_ax.imshow(gradient, aspect='auto', cmap=blue)
# cbar_ax.set_axis_off()

# Set the ticks based on linecolors function
cbar_ax.set_yticks(np.linspace(0, 255, (number_of_runs-1)))
# Assuming dfs is a list of DataFrames
max_impact_count_run_0 = dfs[0]['Impact count'].max()
print(max_impact_count_run_0)
cbar_ax.set_yticklabels([f'{max_impact_count_run_0 - (max_impact_count_run_0*(i+1)*0.05):.2e}' for i in range(number_of_runs-1)])
cbar_ax.xaxis.set_visible(False)  # Remove the x-axis


# # Add an arrow next to the color bar using annotate
# fig.add_artist(patches.FancyArrowPatch((0.95, 0.2), (0.95, 0.8), transform=fig.transFigure,
#                                        arrowstyle='<-', mutation_scale=20, color='black'))

# Add a label to the color bar
if USE:
    fig.text(0.97, 0.5, f'{threshold} Threshold [kgSb-eq/kWh]', ha='center', va='center', fontsize=12, rotation=90, transform=fig.transFigure)
else:
    fig.text(0.97, 0.5, f'{threshold} Threshold [kgCO2-eq/kWh]', ha='center', va='center', fontsize=12, rotation=90, transform=fig.transFigure)

# Show the plot
plt.subplots_adjust(top=0.95, bottom=0.15, right=0.82, left=0.1, hspace=0.4, wspace=0.25)

# Save the plot
fig.savefig(f"results/{folder}/{threshold,number_of_runs,step}.png", dpi=300)