'''

'''

# Created on 4 Jan 2021
#
# .. codeauthor::  jhkwakkel

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from enum import Enum

class Color(Enum):
    RED = 1 # minority color
    BLUE = 2 # majority color

def count_happy(model):
    happy = 0
    for agent in model.schedule.agents:
        if agent.happy:
            happy += 1
    return happy

class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    
    Parameters
    ----------
    height : int
             height of grid
    width : int
            height of width
    density : float
            fraction of grid cells occupied
    minority_fraction : float
            fraction of agent of minority color
    tolerance_threshold : int
    
    Attributes
    ----------
    height : int
    width : int
    density : float
    minority_fraction : float
    schedule : RandomActivation instance
    grid : SingleGrid instance
    
    """

    def __init__(self, height=20, width=20, density=0.8, minority_fraction=0.2,
                 tolerance_threshold=4, seed=None):
        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.density = density
        self.minority_fraction = minority_fraction

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)
        self.datacollector = DataCollector(model_reporters={'happy':count_happy})

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_fraction:
                    agent_color = Color.RED
                else:
                    agent_color = Color.BLUE

                agent = SchellingAgent((x, y), self, agent_color, tolerance_threshold)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

    def step(self):
        """
        Run one step of the model.
        """
        self.schedule.step()
        self.datacollector.collect(self)


class SchellingAgent(Agent):
    """
    Schelling segregation agent
    
    Parameters
    ----------
    pos : tuple of 2 ints
          the x,y coordinates in the grid
    model : Model instance
    color : {Color.RED, Color.BLUE}
    tolerance_threshold : float
    
    """

    def __init__(self, pos, model, color, tolerance_threshold):
        super().__init__(pos, model)
        self.pos = pos
        self.color = color
        self.tolerance_threshold = tolerance_threshold
        self.happy = True

    def step(self):
        '''execute one step of the agent'''

        different = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos, moore=True):
            if neighbor.color != self.color:
                different += 1
        
        meets_threshold = different <= self.tolerance_threshold
        
        if not meets_threshold:
            self.model.grid.move_to_empty(self)
            self.happy = False
        else:
            self.happy = True
            
            
if __name__ == '__main__':
    model = Schelling()
    for _ in range(10):
        model.step()