
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from agentbasedmodelspractice.office_training.model import TrainingCoverage


class TrainingCoverageElement(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''

    def __init__(self):
        super().__init__()

    def render(self, model):
        return "Number of staff trained agents: " + str(model.is_trained)


def draw_training_coverage(agent):
    '''
    Portrayal Method for canvas
    '''
    if agent is None:
        return None

    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.is_trained == 0:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"

    return portrayal


training_element = TrainingCoverageElement()
canvas_element = CanvasGrid(
    draw_training_coverage, grid_width=20, grid_height=20, canvas_width=500,
    canvas_height=500)
training_chart = ChartModule([{"Label": "is_trained", "Color": "Black"}])

model_params = {
    "height": 20,
    "width": 20,
    "density": UserSettableParameter(
        "slider", "Agent density", value=0.65, min_value=0.1, max_value=1.0,
        step=0.05),
    "n_steps": 100,
}

server = ModularServer(TrainingCoverage,
                       [canvas_element, training_element, training_chart],
                       "Schelling", model_params)
