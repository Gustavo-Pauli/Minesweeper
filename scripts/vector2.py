'''

'''

# TODO implement this on cell pos
# import pygame
from typing import List, Union


class Vector2Int:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xy = [x, y]

    def __getitem__(self, index):
        return self.xy[index]

    def __str__(self):
        return str(self.xy)

    def __eq__(self, other):
        if len(other) == 2:
            if self.x == other[0] and self.y == other[1]:
                return True
            else:
                return False
        else:
            return False

    def __add__(self, other):
        if type(other) not in [int, float] and len(other) != 1:
            net_vec = list(other)
            net_vec[0] += self.x
            net_vec[1] += self.y
            return net_vec
        else:
            raise Exception("Can't add '" + str(other) + "' to vector")

    def __sub__(self, other):
        net_vec = list(other)
        net_vec[0] -= self.x
        net_vec[1] -= self.y
        return net_vec

    def __mul__(self, other):
        net_vec = self.xy
        net_vec[0] *= other
        net_vec[1] *= other
        return net_vec

    def __div__(self, other):
        net_vec = self.xy
        net_vec[0] /= other
        net_vec[1] /= other
        return net_vec

    # def __new__(cls, *args, **kwargs):
    #     return (cls.x, cls.y)

    # def __call__(self, *args, **kwargs):
    #     return tuple((self.x, self.y))


# def V2ToInt(vector: pygame.Vector2):
#     return round(vector.x), round(vector.y)