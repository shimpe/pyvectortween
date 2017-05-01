import pytweening

from vectortween.Mapping import Mapping


class Tween(object):
    """
        wrapper around pytweening
    """

    def __init__(self, method, param1=0, param2=0):
        """
        :param method: one of the methods supported by pytweening
         ['linear', 
          'easeInQuad', 'easeOutQuad', 'easeInOutQuad',
          'easeInCubic', 'easeOutCubic', 'easeInOutCubic',
          'easeInQuart', 'easeOutQuart', 'easeInOutQuart',
          'easeInQuint', 'easeOutQuint', 'easeInOutQuint',
          'easeInSine', 'easeOutSine', 'easeInOutSine',
          'easeInExpo', 'easeOutExpo', 'easeInOutExpo',
          'easeInCirc', 'easeOutCirc', 'easeInOutCirc',
          'easeInBounce', 'easeOutBounce', 'easeInOutBounce',
          'easeInElastic', 'easeOutElastic', 'easeInOutElastic',
          'easeInBack', 'easeOutBack', 'easeInOutBack']
          
        :param param1: used by "Back" (how much to retract) and "Elastic" (amplitude) tweeners 
        :param param2: used by "Elastic" tweeners (damping)
        """
        self.method = method
        self.param1 = param1
        self.param2 = param2
        self.method_to_tween = {
            'linear': pytweening.linear,
            'easeInQuad': pytweening.easeInQuad,
            'easeOutQuad': pytweening.easeOutQuad,
            'easeInOutQuad': pytweening.easeInOutQuad,
            'easeInCubic': pytweening.easeInCubic,
            'easeOutCubic': pytweening.easeOutCubic,
            'easeInOutCubic': pytweening.easeInOutCubic,
            'easeInQuart': pytweening.easeInQuart,
            'easeOutQuart': pytweening.easeOutQuart,
            'easeInOutQuart': pytweening.easeInOutQuart,
            'easeInQuint': pytweening.easeInQuint,
            'easeOutQuint': pytweening.easeOutQuint,
            'easeInOutQuint': pytweening.easeInOutQuint,
            'easeInSine': pytweening.easeInSine,
            'easeOutSine': pytweening.easeOutSine,
            'easeInOutSine': pytweening.easeInOutSine,
            'easeInExpo': pytweening.easeInExpo,
            'easeOutExpo': pytweening.easeOutExpo,
            'easeInOutExpo': pytweening.easeInOutExpo,
            'easeInCirc': pytweening.easeInCirc,
            'easeOutCirc': pytweening.easeOutCirc,
            'easeInOutCirc': pytweening.easeOutCirc,
            'easeInBounce': pytweening.easeInBounce,
            'easeOutBounce': pytweening.easeOutBounce,
            'easeInOutBounce': pytweening.easeInOutBounce
        }

        self.method_2param = {
            'easeInElastic': pytweening.easeInElastic,
            'easeOutElastic': pytweening.easeOutElastic,
            'easeInOutElastic': pytweening.easeInOutElastic,
        }

        self.method_1param = {
            'easeInBack': pytweening.easeInBack,
            'easeOutBack': pytweening.easeOutBack,
            'easeInOutBack': pytweening.easeInOutBack,
        }

    def tween(self, t):
        """
        t is number between 0 and 1 to indicate how far the tween has progressed
        """
        if t is None:
            return None

        if self.method in self.method_to_tween:
            return self.method_to_tween[self.method](t)
        elif self.method in self.method_1param:
            return self.method_1param[self.method](t, self.param1)
        elif self.method in self.method_2param:
            return self.method_2param[self.method](t, self.param1, self.param2)
        else:
            raise Exception("Unsupported tween method {0}".format(self.method))

    def tween2(self, val, frm, to):
        """
        linearly maps val between frm and to to a number between 0 and 1 
        """
        return self.tween(Mapping.linlin(val, frm, to, 0, 1))
