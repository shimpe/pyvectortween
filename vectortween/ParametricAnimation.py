from functools import lru_cache

from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

from vectortween.Animation import Animation
from vectortween.Tween import Tween


class ParametricAnimation(Animation):
    """
    class to animate the value of a number between startframe and stopframe
    tweening optionally can be applied (default is None, which means linear animation)
    """

    def __init__(self, equation="t", tween=None):
        if tween is None:
            tween = ['linear']
        if not equation:
            equation = "t"
        self.tween = tween
        self.T = Tween(*tween)
        self.equation = parse_expr(equation)
        t = Symbol('t')
        frm = self.equation.evalf(subs={t: 0})
        to = self.equation.evalf(subs={t: 1})
        super().__init__(frm, to)

    def delayed_version(self, delay):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t - delay)
        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween)

    def speedup_version(self, factor):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t * factor)
        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween)

    def translated_version(self, amount):
        new_equation = self.equation + amount
        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween)

    def scaled_version(self, amount):
        new_equation = self.equation * amount
        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween)

    def scaled_translate_version(self, scale, offset):
        new_equation = self.equation * scale + offset
        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween)

    def timereversed_version(self):
        t = Symbol("t")
        new_equation = self.equation.subs(t, 1 - t)
        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween)

    @lru_cache(maxsize=1000)
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        animation happens between startframe and stopframe
        the value is None before aliveframe, and after deathframe
         * if aliveframe is not specified it defaults to startframe
         * if deathframe is not specified it defaults to stopframe

        initial value is held from aliveframe to startframe

        final value is held from stopfrome to deathframe 
        """

        if birthframe is None:
            birthframe = startframe
        if deathframe is None:
            deathframe = stopframe
        if frame < birthframe:
            return None
        if frame > deathframe:
            return None
        if frame < startframe:
            return self.frm
        if frame > stopframe:
            return self.to

        parameter_value = self.T.tween2(frame, startframe, stopframe)
        t = Symbol('t')
        return self.equation.evalf(subs={t: parameter_value})
