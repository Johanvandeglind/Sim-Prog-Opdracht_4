import random
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement

from mesa.visualization.TextVisualization import (
    TextData, TextGrid, TextVisualization
)

from Agent import CarModel

def car_draw(agent):
    '''
    Portrayal Method for canvas with random color
    '''
    if not agent.color:
        color = '#00FF00' 
        agent.color = color
    return {"Shape": "rect", "w": 0.5,"h": 1, "Filled": "true", "Layer": f"Speed: {agent.speed}", "Color": agent.color, "stroke_color": "#00FF00"}

canvas_element = CanvasGrid(car_draw, 100, 10, 1000, 100)

chart = ChartModule([{"Label": "Throughput", "Color": "#0000FF"}], data_collector_name='datacollector', canvas_width=1000, canvas_height=1000)


model_params = {
    "height": 100,
    "width": 100,
    "brake_prob": UserSettableParameter("slider", "Brake Probability", 0.1, 0, 1, 0.05),
    "speeding_percentage": UserSettableParameter("slider", "Percentage of Cars that are speeding", 10, 0, 100.00 , 0.05),
    "maximum_speeding": UserSettableParameter("slider", "Maximum speeding limit", 1, 1, 10, 1),
    "car_amount": UserSettableParameter("slider", "Number of Cars", 10, 1, 100 , 1),

}

server = ModularServer(CarModel,
                       [canvas_element, chart],
                       "Nagel-Schreckenberg", model_params)