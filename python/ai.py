"""
This is the file that should be used to code your AI.
"""
import random
import math
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

        resources = [(1, 0.1, v) for v in game.resources.regular] + [(25, 2, v) for v in game.resources.silver] + [(10, 0, v) for v in game.resources.gold]

        for cell in game.me.cells:
            target_index, target = self.get_target(cell, resources)
            del resources[target_index]

            if cell.mass == 100:
                target = self.shoopdawoop(game.viruses, cell)
                print(target)
                cell.move(target)
                if (target.position - cell.position) == 0:
                    cell.trade(80)
                else:
                    cell.move(target)

            if cell.mass >= 110:
                viruses  = game.viruses

                while True:
                    is_colision = False
                    for virus in viruses:
                        if self.colision(target, cell, virus):
                            # print('colision: ' +str(target) + str(cell.position) + str(virus.position))
                            target_index, target = self.get_target(cell, resources)
                            del resources[target_index]
                            is_colision = True
                            break
                    if not is_colision:
                        break


            cell.move(target)

    def colision(self, target, cell1, cell2):
        u = target
        v =  cell2.position - cell1.position
        proj_uv = u.project(v)
        theta = u.angle_to(v)
        norm_proj_uv = math.sqrt(proj_uv[0] ** 2 + proj_uv[1] ** 2)
        norm_u = math.sqrt(u[0] ** 2 + u[1] ** 2)

        return norm_u > norm_proj_uv and math.tan(theta) * norm_proj_uv > cell1.radius + cell2.radius

    def get_target(self, cell, resources):
        resources_score_distance_ratio = []
        # print(resources)
        for resource in resources:
            distance = cell.position.distance_to(resource[2])
            ratio = resource[0] / distance
            resources_score_distance_ratio.append(ratio)

        target_resource_index = resources_score_distance_ratio.index(max(resources_score_distance_ratio))

        return target_resource_index,resources[target_resource_index][2]

    def shoopdawoop(self, viruses: List[Virus], cell: Cell):
        virus_distances = []
        for virus in viruses:
            distance = cell.position.distance_to(virus.position)
            virus_distances.append(distance)
        target_virus_index = virus_distances.index(min(virus_distances))
        return viruses[target_virus_index]

