from vectortween.Animation import Animation
from vectortween.Tween import Tween
from vectortween.Mapping import Mapping
from copy import deepcopy
from itertools import tee
import numpy as np


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def normalize(x):
    return x / sum(x)


class SequentialAnimation(Animation):
    def __init__(self, list_of_animations=None, timeweight=None, tween=None):
        super().__init__(None, None)
        if tween is None:
            tween = ['linear']
        if timeweight is None:
            timeweight = []
        if list_of_animations is None:
            list_of_animations = []
        self.ListOfAnimations = []
        self.ListOfAnimationTimeWeight = np.array([])
        self.CumulativeNormalizedTimeWeights = np.array([])
        self.T = Tween(*tween)
        if list_of_animations:
            if not timeweight:
                for a in list_of_animations:
                    self.add(a, 1)
            else:
                for a, t in zip(list_of_animations, timeweight):
                    self.add(a, t)

    def add(self, anim, timeweight=1):
        self.ListOfAnimations.append(deepcopy(anim))
        self.ListOfAnimationTimeWeight = np.append(self.ListOfAnimationTimeWeight, [timeweight])
        self.CumulativeNormalizedTimeWeights = np.cumsum(normalize(self.ListOfAnimationTimeWeight))

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        if birthframe is None:
            birthframe = startframe
        if deathframe is None:
            deathframe = stopframe
        if frame < birthframe:
            return None
        if frame > deathframe:
            return None
        if frame < startframe:
            return self.ListOfAnimations[0].make_frame(frame, birthframe, startframe, stopframe, deathframe)
        if frame > stopframe:
            return self.ListOfAnimations[-1].make_frame(frame, birthframe, startframe, stopframe, deathframe)

        t = self.T.tween2(frame, startframe, stopframe)

        for i, w in enumerate(self.CumulativeNormalizedTimeWeights):
            if t <= w:
                if i == 0:  # reached the end of the cumulative weights
                    relativestartframe = 0
                else:
                    relativestartframe = self.CumulativeNormalizedTimeWeights[i - 1]
                relativestopframe = self.CumulativeNormalizedTimeWeights[i]
                absstartframe = Mapping.linlin(relativestartframe, 0, 1, startframe, stopframe)
                absstopframe = Mapping.linlin(relativestopframe, 0, 1, startframe, stopframe)
                return self.ListOfAnimations[i].make_frame(frame, birthframe, absstartframe, absstopframe, deathframe)