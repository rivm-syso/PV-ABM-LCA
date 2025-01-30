# -*- coding:utf-8 -*-
"""
Created on Wed Nov 21 12:43 2019

@author Julien Walzberg - Julien.Walzberg@nrel.gov
Modified December 2024 by Agnese Fuortes

Run - one or several simulations with all states of outputs

"""
from Integrated_ABM.ABM_CE_PV_Model import *
import matplotlib.pyplot as plt
import time
import os

##CHANGE TRIGGERS HERE
number_run = 1  # Set the number of runs
# USE = False  # Set to False to use climate change labels
if USE:
    folder = "Resources"
else:
    folder = "ClimateChange"

# Ensure the output directory exists
output_dir = f"results/{folder}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def run_model(number_run, number_steps):
    """
    Run model several times and collect outputs at each time steps. Creates
    a new file for each run. Use a new seed for random generation at each
    run.
    """
    for j in range(
        # 10,15):
        number_run):
        # Reinitialize model
        t0 = time.time()

        # if j < 20:
            # model = ABM_CE_PV(
                # seed=1, threshold_concern=0.3821-j*(0.38208*0.05), threshold_indifference=0, positive_feedback = 1, negative_feedback = 0, calibration_n_sensitivity =0.544)
        if j < 20:
            model = ABM_CE_PV(
                seed=1, threshold_concern=0, threshold_indifference=0, positive_feedback = 1, negative_feedback = -0.5, calibration_n_sensitivity =0.544)

                # seed=1, threshold_concern=2.276e-5-j*(2.2756e-5*0.05), threshold_indifference=0, positive_feedback = 1, negative_feedback = -0.5, calibration_n_sensitivity =0.544)
        else:
            model = ABM_CE_PV(
                seed=1,threshold_concern=1.2e-5, threshold_indifference=(1e-5)+(j*1e-6), positive_feedback = 1, negative_feedback = -0.5, calibration_n_sensitivity =0.544)
        # Run model
        for i in range(number_steps):
            model.step()
        # Get results in a pandas DataFrame
        results_model = model.datacollector.get_model_vars_dataframe()
        results_agents = model.datacollector.get_agent_vars_dataframe()
        results_model.to_csv(f"{output_dir}/Results_model_run{j}.csv")
        results_agents.to_csv(f"{output_dir}/Results_agents.csv")
        # Draw figures
        draw_graphs(False, True, model, results_agents, results_model)
        print("Run", j+1, "out of", number_run)
        t1 = time.time()
        print(t1 - t0)


def color_agents(step, column, condition1, condition2, model, results_agents):
    """
    Color figure of the network.
    """
    color_map = []
    for node in model.H1:
        agents_df = results_agents.loc[step, column]
        if agents_df[node] == condition1:
            color_map.append('green')
        elif agents_df[node] == condition2:
            color_map.append('red')
        else:
            color_map.append('grey')
    return color_map


def draw_graphs(network, figures, model, results_agents, results_model):
    """
    Draw different figures.
    """
    if network:
        fig, ax = plt.subplots(figsize=(12, 12))
        # plt.figure(figsize=(12, 12))
        nx.draw_networkx(model.H1, node_color=color_agents(
            1, "Recycling", "recycle", "landfill", model, results_agents),
                node_size=5, with_labels=False, ax=ax)
        # Draw other networks:
        # nx.draw(model.H1, node_color="lightskyblue")
        # nx.draw(model.H2, node_color="purple")
        # nx.draw(model.H3, node_color="chocolate", edge_color="white")
        # nx.draw(model.G, with_labels=False)
    if figures:
        results_model[results_model.columns[2:7]].plot()
        results_model[results_model.columns[16:21]].plot()
        plt.text(0.6, 0.7, 'Landfilling').set_color("red")
        plt.text(0.6, 0.8, 'Recycling').set_color("green")
        plt.text(0.6, 0.9, 'Other behavior').set_color("grey")
#    if network or figures:
#        plt.show()  # draw graph as desired and plot outputs

### Run the model, change number of runs and steps as desired
run_model(number_run, 30)
