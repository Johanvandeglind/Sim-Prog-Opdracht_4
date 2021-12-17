import random
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.batchrunner import BatchRunner
import numpy as np
import matplotlib.pyplot as plt
from Agent import CarModel, compute_speed
import pandas as pd

model_params = {
    "speeding_percentage": np.linspace(0,100,20, dtype=int)[1:],
    "car_amount": np.linspace(0,50,10, dtype=int)[1:],
}

fixed_params = {
    "height": 100,
    "width": 100,
    "brake_prob": 0.1,
    "maximum_speeding": 3,
}

param_run = BatchRunner(CarModel,model_params,fixed_params, iterations=5, max_steps=500,model_reporters={"datacollector": lambda model: (model.datacollector.get_model_vars_dataframe()['Throughput'].to_list())[5:]})

param_run.run_all()
df = param_run.get_model_vars_dataframe()
#print(df)
#df.to_csv('./data.csv')
#df = pd.read_csv('./data.csv')#, usecols=["episode","speeding_percentage","car_amount","Run","datacollector","height","width","brake_prob","maximum_speeding"])
#print(df[df['car_amount'] == 11]['datacollector'].values[0])
print(len(df[(df['car_amount'] == 11) & (df['speeding_percentage']==5)]['datacollector'].values))

# plt.plot(df[df['car_amount'] == 11]['datacollector'].values)
for i in df[(df['car_amount'] == 11)& (df['speeding_percentage']==5)]['datacollector'].values:
    plt.plot(i)
# plt.plot(df[df['car_amount'] == 11]['datacollector'].values[1])
plt.show()