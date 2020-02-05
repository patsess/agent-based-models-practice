
import logging
import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agentbasedmodelspractice.office_training.trainer import Trainer
from agentbasedmodelspractice.office_training.office_worker_agent import (
    OfficeWorker)

__author__ = 'psessford'

logging.basicConfig(level=logging.INFO)

# TODO: docstrs
# TODO: more logging

# TODO: RANDOMISE LOOP THROUGH WORKERS FROM THE TRAINER!!!


class TrainingCoverage(Model):
    def __init__(self, height=20, width=20, density=0.65, n_steps=100):
        super().__init__()
        self.height = height
        self.width = width
        self.density = density
        self.n_steps = n_steps

        self.logger = logging.getLogger(__name__)

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=False)

        self.is_trained = 0
        self.datacollector = DataCollector({'is_trained': 'is_trained'})

        self.trainer = Trainer()

        self._set_up_agents()

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.is_trained = 0  # reset counter of trained agents
        self.schedule.step()
        self.datacollector.collect(self)  # update tracker of trained agents

        self._update_worker_training()

        if self.n_steps < self.schedule.steps:
            self.running = False  # run for specified number of steps

    def _set_up_agents(self):
        for cell in self.grid.coord_iter():
            x = cell[1]  # grid coordinate
            y = cell[2]
            if self.random.random() < self.density:
                time_at_desk = random.random()
                agent = OfficeWorker(
                    pos=(x, y), model=self, time_at_desk=time_at_desk)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

    def _update_worker_training(self):
        n_workers_trained = 0
        for cell in self.grid.coord_iter():
            if self.trainer.capacity <= n_workers_trained:
                break  # no more trainer capacity for this step

            agent = cell[0]
            if agent is None:
                continue

            train_decision = self.trainer.get_train_decision(
                worker_agent=agent)
            if train_decision:
                self.logger.info(f"trainer is training office worker at "
                                 f"location ({cell[1]}, {cell[2]})")
                agent.is_trained = True
                n_workers_trained += 1
