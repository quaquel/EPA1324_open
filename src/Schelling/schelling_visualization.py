'''

'''
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from schelling import Schelling, Color  # @UnresolvedImport


def agent_portrayal(agent):
    if agent is None:
        return
    
    if agent.color == Color.RED:
        color = 'red'
    else:
        color = 'blue' 
    
    portrayal = {"Shape": "circle",
                 "Color": color,
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal


chart = ChartModule([{"Label": "happy",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

width = 20
height = 20
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)


server = ModularServer(Schelling,
                       [grid, chart],
                       "Schelling Model",
                       { "width":width, "height":height})
server.port = 8521 # The default
server.launch()