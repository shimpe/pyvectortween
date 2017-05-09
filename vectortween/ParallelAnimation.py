from copy import deepcopy

from vectortween.Animation import Animation


class ParallelAnimation(Animation):
    def __init__(self, list_of_animations=None):
        super().__init__(None, None)
        if list_of_animations is None:
            list_of_animations = []
        self.ListOfAnimations = []
        if list_of_animations:
            for a in list_of_animations:
                self.add(a)

    def add(self, anim):
        self.ListOfAnimations.append(deepcopy(anim))

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        if birthframe is None:
            birthframe = startframe
        if deathframe is None:
            deathframe = stopframe
        if frame < birthframe:
            return None
        if frame > deathframe:
            return None
        if frame < startframe:
            return [a.make_frame(startframe, birthframe, startframe, stopframe, deathframe, noiseframe) for a in
                    self.ListOfAnimations]
        if frame > stopframe:
            return [a.make_frame(stopframe, birthframe, startframe, stopframe, deathframe, noiseframe) for a in
                    self.ListOfAnimations]

        return [a.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe) for a in self.ListOfAnimations]
