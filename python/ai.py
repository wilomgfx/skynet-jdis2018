"""
This is the file that should be used to code your AI.
"""
import random
from planar import Vec2

from game.models import *


class AI:
    def __init__(self):
        pass

    def step(self, game: Game):
        """
        Given the state of the 'game', decide what your cells ('game.me.cells')
        should do.

        :param game: Game object
        """

        print("Tick #{}".format(game.tick))

        resources = [(1, 0.1, v) for v in game.resources.regular] + [(1, 2, v) for v in game.resources.silver] + [(10, 0, v) for v in game.resources.gold]

        for cell in game.me.cells:

            resources_score_distance_ratio = []

            for resource in resources:
                print(resource[2])
                distance = cell.position.distance_to(resource[2])
                ratio = resource[0] / distance
                resources_score_distance_ratio.append(ratio)

            target_resource_index = resources_score_distance_ratio.index(max(resources_score_distance_ratio))

            print(resources[target_resource_index][2])
            cell.move(resources[target_resource_index][2])
