from vectortween.Tween import Tween
from vectortween.Mapping import Mapping

class NumberAnimation(object):
    """
    class to animate the value of a number between startframe and stopframe

    animation happens between startframe and stopframe
    tweening optionally can be applied (default is None, which means linear animation)
    
    the value is None before aliveframe, and after deathframe
     * if aliveframe is not specified it defaults to startframe
     * if deathframe is not specified it defaults to stopframe
     
    initial value is held from aliveframe to startframe
    
    final value is held from stopfrome to deathframe 
    """
    def __init__(self, startframe, stopframe, frm, to, tween=None, birthframe=None, deathframe=None):
        self.startframe = startframe
        self.stopframe = stopframe

        if birthframe is None:
            self.birthframe = self.startframe
        else:
            self.birthframe = birthframe

        if deathframe is None:
            self.deathframe = self.stopframe
        else:
            self.deathframe = deathframe

        self.frm = frm
        self.to = to

        if tween is None:
            tween = ['linear']

        self.T = Tween(*tween)
        self.M = Mapping()

    def make_frame(self, frame):
        if (frame < self.birthframe):
            return None
        if (frame > self.deathframe):
            return None
        if (frame < self.startframe):
            return frm
        if (frame > self.stopframe):
            return to

        newval = self.M.linlin(self.T.tween2(frame, self.startframe, self.stopframe), 0, 1, self.frm, self.to)
        return newval

