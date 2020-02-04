
import logging
import random
from mesa import Agent

__author__ = 'psessford'

logging.basicConfig(level=logging.INFO)

# TODO: docstrs


class OfficeWorker(Agent):
    def __init__(self, pos, model, time_at_desk):
        super().__init__(pos, model)
        self.pos = pos
        self.time_at_desk = time_at_desk

        self.logger = logging.getLogger(__name__)

        # initialise useful attributes
        self.is_trained = False
        self.neighbour_training = 0

        # initialise helpers for properties
        self._collaboration = None

    @property
    def max_n_neighbours(self):
        return 8

    @property
    def neighbour_training_scalar(self):
        return 0.1

    @property
    def collaboration(self):
        if self._collaboration is None:
            self._collaboration = self._get_worker_collaboration()

        return self._collaboration

    def step(self):
        self._set_neighbour_training()
        self._update_is_trained_by_neighbour()

    def _get_worker_collaboration(self):
        return sum(self.model.grid.neighbor_iter(self.pos))

    def _set_neighbour_training(self):
        self.neighbour_training = (
            sum(neighbour.is_trained
                for neighbour in self.model.grid.neighbor_iter(self.pos)) /
            float(self.max_n_neighbours))

    def _update_is_trained_by_neighbour(self):
        if not self.is_trained:
            for neighbour in self.model.grid.neighbor_iter(self.pos):
                if not neighbour.is_trained:
                    continue

                r = (random.random() * self.time_at_desk *
                     self.neighbour_training_scalar)
                # self.logger.info(
                #     f"random value to determine training from neighbour: {r}")
                is_training_received = ((1. - neighbour.time_at_desk) < r)
                if is_training_received:
                    self.logger.info(
                        f"neighbour training rubbed off on office worker at "
                        f"location ({neighbour.pos[0]}, {neighbour.pos[1]})")
                    self.is_trained = True
                    break
