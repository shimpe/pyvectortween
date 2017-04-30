from vectortween.Animation import Animation
from vectortween.ParametricAnimation import ParametricAnimation
from vectortween.ParallelAnimation import ParallelAnimation
from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol, pi, sin, cos

class PolarAnimation(Animation):
    """
    animation of a 2d position (convenience class converting polar equation to two parametric equations)
    """
    def __init__(self, equation="100*sin(5*theta)", tween=None, ytween=None):
        """
        :param equation: polar equation in the form r = f(theta)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        """
        super().__init__(None, None)
        if ytween is None:
            ytween = tween

        self.equation = parse_expr(equation)
        theta = Symbol("theta")
        t = Symbol("t")
        self.equation_timestretched = self.equation.subs(theta, 2*pi*t)
        self.frm = (self.equation_timestretched*sin(2*pi*t)).evalf(subs={t:0})
        self.to = (self.equation_timestretched*cos(2*pi*t)).evalf(subs={t:1})
        self.anim = ParallelAnimation([ParametricAnimation(equation="{}".format(self.equation_timestretched*sin(2*pi*t)), tween=tween),
                                       ParametricAnimation(equation="{}".format(self.equation_timestretched*cos(2*pi*t)), tween=ytween)])

    def delayed_version(self, delay):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t-delay)
        return PolarAnimation(equation="{}".format(new_equation), tween=self.tween)

    def speedup_version(self, factor):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t*factor)
        return PolarAnimation(equation="{}".format(new_equation), tween=self.tween)

    def translated_version(self, amount):
        t = Symbol("t")
        new_equation = self.equation + amount
        return PolarAnimation(equation="{}".format(new_equation), tween=self.tween)

    def scaled_version(self, amount):
        t = Symbol("t")
        new_equation = self.equation*amount
        return PolarAnimation(equation="{}".format(new_equation), tween=self.tween)

    def scaled_translate_version(self, scale, offset):
        t = Symbol("t")
        new_equation = self.equation * scale + offset
        return PolarAnimation(equation="{}".format(new_equation), tween=self.tween)

    def timereversed_version(self):
        t = Symbol("t")
        new_equation = self.equation.subs(t, 1-t)
        return PolarAnimation(equation="{}".format(new_equation), tween=self.tween)

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
