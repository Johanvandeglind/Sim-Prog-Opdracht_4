import random
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.batchrunner import BatchRunner
import numpy as np
import matplotlib.pyplot as plt
from Agent import CarModel, compute_speed
import pandas as pd
import ast
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics

model_params = {
    "car_amount": [10,15,20,25,30,60],
    "speeding_percentage": [1,5,10,15,20,25,30,35,40,45,50,55,60],
}

fixed_params = {
    "height": 100,
    "width": 100,
    "brake_prob": 0.1,
    "maximum_speeding": 3,
}

param_run = BatchRunner(CarModel,model_params,fixed_params, iterations=500, max_steps=200,model_reporters={"datacollector": lambda model: model.datacollector.get_model_vars_dataframe()['Throughput'].to_dict()})

param_run.run_all()
df = param_run.get_model_vars_dataframe()
print(df)
df.to_csv('./data_500x200.csv')