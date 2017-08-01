from functools import lru_cache

from scipy.special import binom

from vectortween.Animation import Animation
from vectortween.ParallelAnimation import ParallelAnimation
from vectortween.ParametricAnimation import ParametricAnimation


class BezierCurveAnimation(Animation):
    """
    animation of a 2d position (convenience class converting polar equation to two parametric equations)
    """

    def __init__(self, controlpoints=None, tween=None, ytween=None, noise_fn=None, y_noise_fn=None):
        """
        :param equation: polar equation in the form r = f(theta)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        :param noise_fn: optional noise function mapping (x, t) -> value
        :param y_noise_fn: optional noise function mapping (y, t) -> value
        """
        super().__init__(None, None)
        if controlpoints is None:
            controlpoints = []
        if tween is None:
            tween = ['linear']
        if ytween is None:
            ytween = tween

        self.tween = tween
        self.ytween = ytween
        self.noise_fn = noise_fn
        self.y_noise_fn = y_noise_fn
        self.controlpoints = controlpoints

        order = len(controlpoints) - 1
        x_terms = []
        y_terms = []
        for i, c in enumerate(controlpoints):
            x_terms.append("{0}*((1-t)**({1}-{2}))*(t**{2})*{3}".format(binom(order, i), order, i, c[0]))
            y_terms.append("{0}*((1-t)**({1}-{2}))*(t**{2})*{3}".format(binom(order, i), order, i, c[1]))
        # print ("+".join(x_terms))
        # print ("+".join(y_terms))
        self.anim = ParallelAnimation(
            [ParametricAnimation(equation="{}".format("+".join(x_terms)), tween=tween, noise_fn=self.noise_fn),
             ParametricAnimation(equation="{}".format("+".join(y_terms)), tween=ytween, noise_fn=self.y_noise_fn)])
        self.frm = self.anim.make_frame(0, 0, 0, 1, 1)
        self.to = self.anim.make_frame(1, 0, 0, 1, 1)

    #@lru_cache(maxsize=1000)
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        """
        :param frame: current frame 
        :param birthframe: frame where this animation starts returning something other than None
        :param startframe: frame where animation starts to evolve
        :param stopframe: frame where animation is completed
        :param deathframe: frame where animation starts to return None
        :return: 
        """
        return self.anim.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe)
