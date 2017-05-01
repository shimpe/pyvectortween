from sympy import Symbol, pi, sin, cos
from sympy.parsing.sympy_parser import parse_expr

from vectortween.Animation import Animation
from vectortween.ParallelAnimation import ParallelAnimation
from vectortween.ParametricAnimation import ParametricAnimation
from functools import lru_cache

class PolarAnimation(Animation):
    """
    animation of a 2d position (convenience class converting polar equation to two parametric equations)
    """

    def __init__(self, equation="100*sin(5*theta)", offset=None, scale=None, tween=None, ytween=None):
        """
        :param equation: polar equation in the form r = f(theta)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        """
        super().__init__(None, None)
        if scale is None:
            scale = [1, 1]
        if offset is None:
            offset = [0, 0]
        if ytween is None:
            ytween = tween

        self.tween = tween
        self.ytween = ytween
        self.equation = parse_expr(equation)
        self.offset = offset
        self.scale = scale
        theta = Symbol("theta")
        t = Symbol("t")
        self.equation_timestretched = self.equation.subs(theta, 2 * pi * t)
        self.frm = (scale[0] * self.equation_timestretched * sin(2 * pi * t) + offset[0]).evalf(subs={t: 0})
        self.to = (scale[1] * self.equation_timestretched * cos(2 * pi * t) + offset[1]).evalf(subs={t: 1})
        self.anim = ParallelAnimation([ParametricAnimation(equation="{}".format(
                                        scale[0] * self.equation_timestretched * sin(2 * pi * t) + offset[0]),
                                        tween=tween),
                                       ParametricAnimation(equation="{}".format(
                                        scale[1] * self.equation_timestretched * cos(2 * pi * t) + offset[1]),
                                        tween=ytween)])

    def delayed_version(self, delay):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t - delay)
        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=self.scale, tween=self.tween, ytween=self.ytween)

    def speedup_version(self, factor):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t * factor)
        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=self.scale, tween=self.tween, ytween=self.ytween)

    def translated_version(self, offset):
        new_equation = self.equation
        new_offset = [self.offset[0] + offset[0], self.offset[1]+offset[1]]
        return PolarAnimation(equation="{}".format(new_equation),
                              offset=new_offset, scale=self.scale, tween=self.tween, ytween=self.ytween)

    def scaled_version(self, scale):
        new_equation = self.equation
        new_scale = [self.scale[0]*scale[0], self.scale[1]*scale[1]]
        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=new_scale, tween=self.tween, ytween=self.ytween)

    def scaled_translate_version(self, scale, offset):
        new_equation = self.equation
        new_offset = [self.offset[0] + offset[0], self.offset[1] + offset[1]]
        new_scale = [self.scale[0] * scale[0], self.scale[1] * scale[1]]
        return PolarAnimation(equation="{}".format(new_equation),
                              offset=new_offset, scale=new_scale, tween=self.tween, ytween=self.ytween)

    def timereversed_version(self):
        t = Symbol("t")
        new_equation = self.equation.subs(t, 1 - t)
        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=self.scale, tween=self.tween, ytween=self.ytween)

    @lru_cache(maxsize=1000)
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        :param frame: current frame 
        :param birthframe: frame where this animation starts returning something other than None
        :param startframe: frame where animation starts to evolve
        :param stopframe: frame where animation is completed
        :param deathframe: frame where animation starts to return None
        :return: 
        """
        return self.anim.make_frame(frame, birthframe, startframe, stopframe, deathframe)
