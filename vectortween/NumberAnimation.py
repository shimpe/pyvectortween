from vectortween.Animation import Animation
from vectortween.Tween import Tween
from vectortween.Mapping import Mapping
from functools import lru_cache

class NumberAnimation(Animation):
    """
    class to animate the value of a number between startframe and stopframe
    tweening optionally can be applied (default is None, which means linear animation)
    """
    def __init__(self, frm, to, tween=None):
        super().__init__(frm, to)
        if tween is None:
            tween = ['linear']

        self.T = Tween(*tween)

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

        newval = Mapping.linlin(self.T.tween2(frame, startframe, stopframe), 0, 1, self.frm, self.to)

        return newval

