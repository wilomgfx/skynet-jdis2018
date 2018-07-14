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

        resources = [(0.1, 1, v) for v in game.resources.regular] + [(1, 2, v) for v in game.resources.silver] + [(10, 0, v) for v in game.resources.gold]

        for cell in game.me.cells:
            target_index, target = self.get_target(cell, resources)
            del resources[target_index]

            if cell.mass >= 0:
                viruses  = game.viruses

                while True:
                    print('t')
                    is_colision = False
                    for virus in viruses:
                        if colision2(target, cell, virus):
                            print('colision: ' +str(target) + str(cell.position) + str(virus.position))

                            if len(resources) == 1:
                                target = resources[0]
                                break
                            else:
                                target_index, target = self.get_target(cell, resources)
                                del resources[target_index]

                            is_colision = True
                            break
                    if not is_colision:
                        break


            cell.move(target)

    def colision(self, target, cell1, cell2):
        u = target - cell1.position
        v =  cell2.position - cell1.position
        proj_uv = u.project(v)
        theta = u.angle_to(v)
        norm_proj_uv = math.sqrt(proj_uv[0] ** 2 + proj_uv[1] ** 2)
        norm_u = math.sqrt(u[0] ** 2 + u[1] ** 2)

        return norm_u > norm_proj_uv and math.tan(theta * 2 * math.pi / 360) * norm_proj_uv > cell1.radius + cell2.radius

    def get_target(self, cell, resources):
        resources_score_distance_ratio = []

        for resource in resources:
            distance = cell.position.distance_to(resource[2])
            ratio = resource[0] / distance
            resources_score_distance_ratio.append(ratio)

        target_resource_index = resources_score_distance_ratio.index(max(resources_score_distance_ratio))

        return target_resource_index,resources[target_resource_index][2]

def colision2(target, A, B):
    u = (target-A.position).normalized()
    print(u)
    AB = B.position - A.position
    distance = abs(AB.cross(u)) / u.length

    return distance < A.radius + B.radius

def colision3(target, A, B, radius1, radius2):
    u = (target-A).normalized()
    print(u)
    AB = B - A
    distance = abs(AB.cross(u)) / u.length

    return distance < radius1 + radius2

def colision(target, cell1_pos, cell2_pos, radius1, radius2):
    u = target - cell1_pos
    v =  cell2_pos - cell1_pos
    proj_uv = u.project(v)
    theta = u.angle_to(v)
    norm_proj_uv = math.sqrt(proj_uv[0] ** 2 + proj_uv[1] ** 2)
    norm_u = math.sqrt(u[0] ** 2 + u[1] ** 2)
    return norm_u > norm_proj_uv and math.tan(theta * 2 * math.pi / 360) * norm_proj_uv < radius1 + radius2

from planar import Vec2

if __name__ == '__main__':
    direction = Vec2(2,2)
    cell1_pos = Vec2(1,1)
    cell2_pos = Vec2(5,5)
    print(colision3(direction, cell1_pos, cell2_pos, 1, 1 ))
