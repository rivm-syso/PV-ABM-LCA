import pandas as pd

#Import Sobol sensitivity indices from excell file
#For resource depletion
sobol_indices_RD = pd.read_csv("results/Supporting_information/Metamodel_RD/test3b_SensIndHDMR.csv")
#Name first column parameter and second column RD sensitivity index
sobol_indices_RD.columns = ["Parameter", "Mineral resource depletion"]

#For climate change
sobol_indices_CC = pd.read_csv("results/Supporting_information/Metamodel_CC/test3b_SensIndHDMR.csv")
#Name first column parameter and second column CC sensitivity index
sobol_indices_CC.columns = ["Parameter", "Climate change"]

#Combine in dataframe based on parameter in first column
sobol_indices = pd.merge(sobol_indices_RD, sobol_indices_CC, on="Parameter")

# Modify the Parameter column
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('_', ' ')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('LT', 'lifetime')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('rec', 'recovery')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('Elec', 'Electricity use')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('Siem', 'Siemens process')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('PR', 'Performance ratio')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('Eff', 'Efficiency')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('CZ', 'Czochralski process')
sobol_indices['Parameter'] = sobol_indices['Parameter'].str.replace('Zeol scrub', 'Hazardous gas abatement')

#Plot in heatmap
import seaborn as sns
import matplotlib.pyplot as plt
# Set the style of seaborn
blue=sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)

# Plot in heatmap using the custom color palette
plt.figure(figsize=(10, 8))
sns.heatmap(sobol_indices.set_index("Parameter"), annot=False, cmap=blue, linewidths=.5, linecolor=None)
plt.subplots_adjust(left=0.3, right=0.9)  # Adjust the left margin to add space
# plt.show()


inputoutput_RD = pd.read_csv("results/Supporting_information/Metamodel_RD/InputOutputDataTest.csv")
inputoutput_CC = pd.read_csv("results/Supporting_information/Metamodel_CC/InputOutputDataTest.csv") 


# Set the style using seaborn
color1 = blue(0.3)  # Example: Get a color from the palette
color2 = blue(0.9)


# # Plot LCA output vs metamodel predicted output for resource depletion
# plt.figure(figsize=(10, 8))

# # Customize the scatter plot color and marker style
# plt.scatter(inputoutput_RD["LCA output"], inputoutput_RD["Metamodel predicted output"], color=color1, s=100, marker="o")

# # Calculate the correlation coefficient
# correlation_RD = inputoutput_RD["LCA output"].corr(inputoutput_RD["Metamodel predicted output"])

# # Calculate the R2 and use as title
# R2_RD = correlation_RD**2
# plt.title(f"Resource depletion: R-squared = {R2_RD:.2f}", fontsize=16)

# # Add a line to show the perfect correlation on top of the scatter plot and scale to data
# plt.plot([0, 1], [0, 1], color=color2, linestyle="--", linewidth=2, transform=plt.gca().transAxes)

# plt.xlabel("LCA output", fontsize=14)
# plt.ylabel("Metamodel output", fontsize=14)

# # Show the plot
# plt.show()

color3 = blue(0.5)
color4 = blue(0.7)

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Plot LCA output vs metamodel predicted output for resource depletion
axes[0].scatter(inputoutput_RD["LCA output"], inputoutput_RD["Metamodel predicted output"], color=color1, s=100, marker="o")
correlation_RD = inputoutput_RD["LCA output"].corr(inputoutput_RD["Metamodel predicted output"])
R2_RD = correlation_RD**2
axes[0].plot([0, 1], [0, 1], color=color2, linestyle="--", linewidth=2, transform=axes[0].transAxes)
axes[0].set_title("Resource depletion [kgSb-eq/kWh]", fontsize=16)
axes[0].set_xlabel("LCA output", fontsize=14)
axes[0].set_ylabel("Metamodel output", fontsize=14)
axes[0].legend(title=f"R-squared = {R2_RD:.2f}", frameon=False)

# Plot LCA output vs metamodel predicted output for climate change
axes[1].scatter(inputoutput_CC["LCA output"], inputoutput_CC["Metamodel predicted output"], color=color1, s=100, marker="o")
correlation_CC = inputoutput_CC["LCA output"].corr(inputoutput_CC["Metamodel predicted output"])
R2_CC = correlation_CC**2
axes[1].plot([0, 1], [0, 1], color=color2, linestyle="--", linewidth=2, transform=axes[1].transAxes)
axes[1].set_title("Climate change [kgCO2-eq/kWh]", fontsize=16)
axes[1].set_xlabel("LCA output", fontsize=14)
axes[1].legend(title=f"R-squared = {R2_CC:.2f}", frameon=False)


# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()