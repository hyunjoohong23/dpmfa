# -*- coding: utf-8 -*-
"""

Created on 19.11.2018
@author: sram
Tire Wear Flow Model for Switzerland 1988 - 2018

"""

###############################################################################

import Test_Model
from dpmfa import simulator as sc
import numpy as np
import os

###############################################################################

# define model
model = Test_Model.model

# check validity
model.checkModelValidity()

# print out the model content for verification by the experimenter
model.statusModel()

###############################################################################

# starting year in period considered
startYear = 1988

# number of periods modelled (must be compatible with the inflow and TC data)
Tperiods = 5

# defined period for printing a summary of the flows
Speriod = 0

# number of runs, determines the precision of the results
RUNS = 10

###############################################################################

# set up the simulator instance (2250 is the seed)
simulator = sc.Simulator(RUNS, Tperiods, 2250, True, True)

# define what model needs to be run
simulator.setModel(model)

# run the model
simulator.runSimulation()

###############################################################################

# find out the sinks and the stocks of the system
sinks = simulator.getSinks()
stocks = simulator.getStocks()

###############################################################################

# compartment with loggedInflows
loggedInflows = simulator.getLoggedInflows()
# compartment with loggedOutflows
loggedOutflows = simulator.getLoggedOutflows()

###############################################################################

## display mean ± std for each flow
print("")
print("-----------------------")
print("Logged Outflows:")
print("-----------------------")
print("")
# loop over the list of compartments with loggedoutflows
for Comp in loggedOutflows:
    print("Flows from " + Comp.name + ":")
    # in this case name is the key, value is the matrix(data), in this case .items is needed
    for Target_name, value in Comp.outflowRecord.items():
        print(
            " --> "
            + str(Target_name)
            + ": Mean = "
            + str(round(np.mean(value[:, Speriod]), 0))
            + " ± "
            + str(round(np.std(value[:, Speriod]), 0))
        )
    print("")
print("-----------------------")
print("")

###############################################################################

import csv

# export all outflows to csv
for Comp in loggedOutflows:
    # loggedOutflows is the compartment list of compartmensts with loggedoutflows
    for (Target_name, value) in Comp.outflowRecord.items():
        # in this case name is the key, value is the matrix(data), in this case .items is needed
        with open(
            os.path.join(
                "experiment_output",
                "loggedOutflows_" + Comp.name + "_to_" + Target_name + ".csv",
            ),
            "w",
            newline="",
        ) as RM:
            a = csv.writer(RM)
            data = np.asarray(value)
            a.writerows(data)

# export all inflows to csv
for Comp in loggedInflows:
    # loggedOutflows is the compartment list of compartmensts with loggedoutflows
    with open(
        os.path.join("experiment_output", "loggedInflows_" + Comp.name + ".csv"),
        "w",
        newline="",
    ) as RM:
        a = csv.writer(RM)
        data = np.asarray(loggedInflows[Comp])
        a.writerows(data)