from functools import lru_cache

from vectortween.Animation import Animation
from vectortween.Mapping import Mapping
from vectortween.Tween import Tween


class NumberAnimation(Animation):
    """
    class to animate the value of a number between startframe and stopframe
    tweening optionally can be applied (default is None, which means linear animation)
    """

    def __init__(self, frm, to, tween=None, noise_fn=None):
        """
        
        :param frm: start value 
        :param to: end value
        :param tween: optional tweening function (default: linear)
        :param noise_fn: optional noise function (default: None)
          noise_fn needs to accept two parameters: a value (frm <= value <= to) and a time (0 <= time <= 1)
          if the noise_fn uses parameter t the noise will be animated in time; by accepting but ignoring t,
          the noise is only spatial
        """
        super().__init__(frm, to)
        if tween is None:
            tween = ['linear']
        self.noise_fn = noise_fn
        self.T = Tween(*tween)

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

        t = self.T.tween2(frame, startframe, stopframe)
        newval = Mapping.linlin(t, 0, 1, self.frm, self.to)
        if self.noise_fn is not None:
            if noiseframe is not None:
                nf = noiseframe
            else:
                nf = t
            noise_val = self.noise_fn(newval, nf)
        else:
            noise_val = 0

        return newval + noise_val
