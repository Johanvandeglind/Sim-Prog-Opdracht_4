from random import random

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import BaseScheduler

class CarModel(Model):
    def __init__(self, height, width, brake_prob, car_amount):
        super().__init__()
        self.height = height
        self.width = width
        self.brake_prob = brake_prob
        self.car_amount = car_amount

        self.schedule = BaseScheduler(self)
        self.grid = SingleGrid(height, width, torus=True)

        self.place_agents()

        self.running = True

    def place_agents(self):
        for i in range(self.car_amount):
            while True:
                try:
                    r = random()
                    agent = CarAgent((int(r*100), 5), self, 10)
                    self.grid.position_agent(agent, int(r*100), 5)
                    self.schedule.add(agent)
                    break
                except Exception:
                    continue

    def step(self):
        self.schedule.step()


class CarAgent(Agent):
    def __init__(self, pos, model: CarModel, max_speed):
        """
        Create a new car agent.
        """

        super().__init__(pos, model)
        self.model = model
        self.pos = pos
        self.max_speed = max_speed
        self.speed = 1

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
            self.speed -= 1
        
        # Move the agent
        self.move()
        print(self.pos)

    def move(self):
        """
        Move the agent one step forward in the direction it is facing.
        """
        if self.model.grid.is_cell_empty(self.model.grid.torus_adj((self.pos[0]+self.speed, self.pos[1]))):
            self.model.grid.move_agent(self,
                                       self.model.grid.torus_adj(
                                           (self.pos[0]+self.speed, self.pos[1]))
                                       )

model = CarModel(100, 100, 0.1, 100)
for x in range(100):
    model.step()