
import random

__author__ = 'psessford'

# TODO: docstrs
# TODO: logging


class Trainer(object):
    def __init__(self, capacity=2, team_importance=0.5):
        self.capacity = capacity
        self.team_importance = team_importance
        self.individual_importance = 1. - self.team_importance

    def get_train_decision(self, worker_agent):
        assert (0. <= worker_agent.neighbour_training <= 1.)
        assert (0. <= worker_agent.time_at_desk <= 1.)

        worker_importance = (
            self.individual_importance * worker_agent.time_at_desk)
        team_importance = (
            self.team_importance * worker_agent.neighbour_training)

        r = random.random()
        train_decision = ((r < worker_importance) or (r < team_importance))

        return train_decision
