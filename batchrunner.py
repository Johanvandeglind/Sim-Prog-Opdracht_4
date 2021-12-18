import random
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.batchrunner import BatchRunner
import numpy as np
import matplotlib.pyplot as plt
from Agent import CarModel, compute_speed
import pandas as pd
import ast

model_params = {
    "car_amount": [1,5,10,15,30,60],
    "speeding_percentage": [1,5,10,15,20,25,30,35,40,45,50,55,60],
    
}

fixed_params = {
    "height": 100,
    "width": 100,
    "brake_prob": 0.1,
    "maximum_speeding": 3,
}

# param_run = BatchRunner(CarModel,model_params,fixed_params, iterations=1, max_steps=500,model_reporters={"datacollector": lambda model: model.datacollector.get_model_vars_dataframe()['Throughput'].to_dict()})

# param_run.run_all()
# df = param_run.get_model_vars_dataframe()
# print(df)
# df.to_csv('./data.csv')
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics
  
# Plot between -10 and 10 with .001 steps.

plt.show()
def plot_list_fd(x):
    x_axis = np.mean
    mean = statistics.mean(x)
    sd = statistics.stdev(x)
    plt.plot(x_axis, norm.pdf(x_axis, mean, sd))

df = pd.read_csv('./data.csv')#, usecols=["","speeding_percentage","car_amount","Run","datacollector","height","width","brake_prob","maximum_speeding"])
df = df.drop(columns=['Unnamed: 0'])

#print(df)#[df['car_amount'] == 11]['datacollector'].values)
df['datacollector'] = df['datacollector'].map(ast.literal_eval)
df['datacollector'] = df['datacollector'].apply(lambda d: list(d.values()))
#df['Zscore'] = df.groupby('datacollector').Run.apply(lambda x: plot_list_fd(x))

# # plt.plot(df[df['car_amount'] == 11]['datacollector'].values)
for i in df[(df['car_amount'] == 5)]['datacollector'].values:
    plot_list_fd(i[:499])
    break
        
# # plt.plot(df[df['car_amount'] == 11]['datacollector'].values[1])
plt.show()