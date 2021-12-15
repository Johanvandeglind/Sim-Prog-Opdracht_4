from random import randint, random

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector

def compute_speed(model):
    """
    Compute the average speed of all cars.
    """
    cars = model.schedule.agents
    total_speed = 0
    for c in cars:
        total_speed += c.get_speed()
    avg_speed = total_speed / len(cars)
    return avg_speed

class CarModel(Model):
    
    def __init__(self, height, width, brake_prob, car_amount, speeding_percentage, maximum_speeding):
        super().__init__()
        self.maximum_speed = 5
        self.height = height
        self.width = width
        self.brake_prob = brake_prob
        self.car_amount = car_amount
        self.agents = []

        self.speeding_percentage = speeding_percentage
        self.maximum_speeding = maximum_speeding

        self.schedule = BaseScheduler(self)
        self.grid = SingleGrid(height, width, torus=True)

        self.place_agents()

        self.running = True

        self.datacollector = DataCollector(
            model_reporters={"Throughput": compute_speed})

    def place_agents(self):
        speeding_amount = int(self.car_amount * self.speeding_percentage) / 100
        for i in range(self.car_amount):
            while True:
                try:
                    if i < speeding_amount:
                        random_speeding = self.maximum_speed + randint(1, self.maximum_speeding)
                        speeding_color = "#FF0000"
                    else:
                        random_speeding = self.maximum_speed
                        speeding_color = None


                    r = random()
                    agent = CarAgent((int(r*100), 5), self, random_speeding, speeding_color)
                    self.agents.append(agent)
                    self.grid.position_agent(agent, int(r*100), 5)
                    self.schedule.add(agent)
                    break
                except Exception as e:
                    continue

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

class CarAgent(Agent):
    color = None
    def __init__(self, pos, model: CarModel, max_speed, color=None):
        """
        Create a new car agent.
        """

        super().__init__(pos, model)
        self.model = model
        self.pos = pos
        self.max_speed = max_speed
        self.speed = 1

        if color:
            self.color = color

    def step(self):
        """
        Car agents move according to the model.
        """

        if self.speed < self.max_speed:
            self.speed += 1

        tmpX = self.pos[0] + 1
        while True:
            # If the cell is not empty, brake
            if not self.model.grid.is_cell_empty(self.model.grid.torus_adj((tmpX, self.pos[1]))):
                break
            tmpX += 1

        # Check if the cells in front are empty.
        if tmpX - self.pos[0] < self.speed:
            self.speed = tmpX - self.pos[0]

        # Random brake
        if random() < self.model.brake_prob:
            if self.speed > 0:
                self.speed -= 1
        
        # Move the agent
        self.move()

    def move(self):
        """
        Move the agent one step forward in the direction it is facing.
        """
        if self.model.grid.is_cell_empty(self.model.grid.torus_adj((self.pos[0]+self.speed, self.pos[1]))):
            self.model.grid.move_agent(self,
                                       self.model.grid.torus_adj(
                                           (self.pos[0]+self.speed, self.pos[1]))
                                       )

    def get_speed(self):
        return self.speed