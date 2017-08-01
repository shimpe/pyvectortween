from functools import lru_cache

from sympy import Symbol, pi, sin, cos
from sympy.parsing.sympy_parser import parse_expr

from vectortween.Animation import Animation
from vectortween.ParallelAnimation import ParallelAnimation
from vectortween.ParametricAnimation import ParametricAnimation


class PolarAnimation(Animation):
    """
    animation of a 2d position (convenience class converting polar equation to two parametric equations)
    """

    def __init__(self, equation="100*sin(5*theta)", offset=None, scale=None, tween=None, ytween=None, noise_fn=None,
                 y_noise_fn=None):
        """
        :param equation: polar equation in the form r = f(theta)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        :param noise_fun: optional noise function (defaults to None) for the x coordinate. Maps (x,t) -> value
        :param y_noise_fun: optional noise function (defaults to None) for the y coordinate. Maps (y,t) -> value
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
        self.noise_fn = noise_fn
        self.y_noise_fn = y_noise_fn

        def new_noise_fn(value, t):
            return self.noise_fn(value, 2 * pi * t)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value, 2 * pi * t)

        self.equation_timestretched = self.equation.subs(theta, 2 * pi * t)
        self.frm = (scale[0] * self.equation_timestretched * sin(2 * pi * t) + offset[0]).evalf(subs={t: 0})
        self.to = (scale[1] * self.equation_timestretched * cos(2 * pi * t) + offset[1]).evalf(subs={t: 1})
        self.anim = ParallelAnimation([ParametricAnimation(equation="{}".format(
            scale[0] * self.equation_timestretched * sin(2 * pi * t) + offset[0]),
            tween=tween, noise_fn=new_noise_fn if self.noise_fn else None),
            ParametricAnimation(equation="{}".format(
                scale[1] * self.equation_timestretched * cos(2 * pi * t) + offset[1]),
                tween=ytween, noise_fn=new_y_noise_fn if self.y_noise_fn else None)])

    def delayed_version(self, delay):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t - delay)

        def new_noise_fn(value, t):
            return self.noise_fn(value, t - delay)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value, t - delay)

        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=self.scale, tween=self.tween, ytween=self.ytween,
                              noise_fn=new_noise_fn if self.noise_fn else None,
                              y_noise_fn=new_y_noise_fn if self.y_noise_fn else None)

    def speedup_version(self, factor):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t * factor)

        def new_noise_fn(value, t):
            return self.noise_fn(value, t * factor)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value, t * factor)

        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=self.scale, tween=self.tween, ytween=self.ytween,
                              noise_fn=new_noise_fn if self.noise_fn else None,
                              y_noise_fn=new_y_noise_fn if self.y_noise_fn else None)

    def translated_version(self, offset):
        new_equation = self.equation
        new_offset = [self.offset[0] + offset[0], self.offset[1] + offset[1]]

        def new_noise_fn(value, t):
            return self.noise_fn(value + offset[0], t)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value + offset[1], t)

        return PolarAnimation(equation="{}".format(new_equation),
                              offset=new_offset, scale=self.scale, tween=self.tween, ytween=self.ytween,
                              noise_fn=new_noise_fn if self.noise_fn else None,
                              y_noise_fn=new_y_noise_fn if self.y_noise_fn else None)

    def scaled_version(self, scale):
        new_equation = self.equation
        new_scale = [self.scale[0] * scale[0], self.scale[1] * scale[1]]

        def new_noise_fn(value, t):
            return self.noise_fn(value * scale[0], t)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value * scale[1], t)

        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=new_scale, tween=self.tween, ytween=self.ytween,
                              noise_fn=new_noise_fn if self.noise_fn else None,
                              y_noise_fn=new_y_noise_fn if self.y_noise_fn else None)

    def scaled_translate_version(self, scale, offset):
        new_equation = self.equation
        new_offset = [self.offset[0] + offset[0], self.offset[1] + offset[1]]
        new_scale = [self.scale[0] * scale[0], self.scale[1] * scale[1]]

        def new_noise_fn(value, t):
            return self.noise_fn(value * scale[0] + offset[0], t)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value * scale[1] + offset[1], t)

        return PolarAnimation(equation="{}".format(new_equation),
                              offset=new_offset, scale=new_scale, tween=self.tween, ytween=self.ytween,
                              noise_fn=new_noise_fn if self.noise_fn else None,
                              y_noise_fn=new_y_noise_fn if self.y_noise_fn else None)

    def timereversed_version(self):
        t = Symbol("t")
        new_equation = self.equation.subs(t, 1 - t)

        def new_noise_fn(value, t):
            return self.noise_fn(value, 1 - t)

        def new_y_noise_fn(value, t):
            return self.y_noise_fn(value, 1 - t)

        return PolarAnimation(equation="{}".format(new_equation),
                              offset=self.offset, scale=self.scale, tween=self.tween, ytween=self.ytween,
                              noise_fn=new_noise_fn if self.noise_fn else None,
                              y_noise_fn=new_y_noise_fn if self.y_noise_fn else None)

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
