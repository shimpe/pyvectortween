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

    def __init__(self, equation="t", tween=None, noise_fn=None):
        """
        
        :param equation: parametric equation written as a string, expressed in terms of parameter "t". 
        :param tween: optional tweening specification
        :param noise_fn: 2d function accepting a value ( equation(0) <= value <= equation(1)) and a time (0 <= t <= 1).
         By accepting and using t, the noise is animated in time. By accepting but ignoring t, the noise is only spatial.
        """
        if tween is None:
            tween = ['linear']
        if not equation:
            equation = "t"
        self.tween = tween
        self.T = Tween(*tween)
        self.noise_fn = noise_fn
        self.equation = parse_expr(equation)
        t = Symbol('t')
        frm = self.equation.evalf(subs={t: 0})
        to = self.equation.evalf(subs={t: 1})
        super().__init__(frm, to)

    def delayed_version(self, delay):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t - delay)

        def new_noise_fn(value, t):
            return self.noise_fn(value, t - delay)

        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween,
                                   noise_fn=new_noise_fn if self.noise_fn else None)

    def speedup_version(self, factor):
        t = Symbol("t")
        new_equation = self.equation.subs(t, t * factor)

        def new_noise_fn(value, t):
            return self.noise_fn(value, t * factor)

        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween,
                                   noise_fn=new_noise_fn if self.noise_fn else None)

    def translated_version(self, amount):
        new_equation = self.equation + amount

        def new_noise_fn(value, t):
            return self.noise_fn(value + amount, t)

        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween,
                                   noise_fn=new_noise_fn if self.noise_fn else None)

    def scaled_version(self, amount):
        new_equation = self.equation * amount

        def new_noise_fn(value, t):
            return self.noise_fn(value * amount, t)

        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween,
                                   noise_fn=new_noise_fn if self.noise_fn else None)

    def scaled_translate_version(self, scale, offset):
        new_equation = self.equation * scale + offset

        def new_noise_fn(value, t):
            return self.noise_fn(value * scale + offset, t)

        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween,
                                   noise_fn=new_noise_fn if self.noise_fn else None)

    def timereversed_version(self):
        t = Symbol("t")
        new_equation = self.equation.subs(t, 1 - t)

        def new_noise_fn(value, t):
            return self.noise_fn(value, 1 - t)

        return ParametricAnimation(equation="{}".format(new_equation), tween=self.tween,
                                   noise_fn=new_noise_fn if self.noise_fn else None)

    #@lru_cache(maxsize=1000)
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
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
        if self.noise_fn is not None:
            if noiseframe is not None:
                nf = noiseframe
            else:
                nf = parameter_value
            noise_value = self.noise_fn(frame, nf)
        else:
            noise_value = 0
        return self.equation.evalf(subs={t: parameter_value}) + noise_value
