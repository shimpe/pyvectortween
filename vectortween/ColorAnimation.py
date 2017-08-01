from functools import lru_cache

from vectortween.Animation import Animation
from vectortween.NumberAnimation import NumberAnimation


class ColorAnimation(Animation):
    """
    class to animate a color
    
    colors are specified as tuples (r,g,b) where for each color component c 0<=c<=1
    """

    def __init__(self, frm, to, tween=None, tweengreen=None, tweenblue=None, tweenalpha=None):
        """
        :param frm: start color, e.g. (1,0,0) for red (optionally also specify an alpha component)
        :param to: stop color, e.g. (0,1,0) for green (optionally also specify an alpha component)
        :param tween: tween method for red color component (defaults to linear if not specified)
        :param tweengreen: tween method for green color component (defaults to same as red if not specified)
        :param tweenblue: tween method for blue color component (defaults to same as red if not specified)
        :param tweenalpha: tween method for alpha color component (defaults to Linear if not specified)
 
        Note: output will contain alpha if input contains alpha
        """
        super().__init__(frm, to)
        try:
            dummy = frm[3]
            self.use_alpha = True
        except IndexError:
            self.use_alpha = False
            pass

        if tweenalpha is None:
            tweenalpha = ['linear']

        self.anim_red = NumberAnimation(self.frm[0], self.to[0], tween)
        self.anim_green = NumberAnimation(self.frm[1], self.to[1], tweengreen)
        self.anim_blue = NumberAnimation(self.frm[2], self.to[2], tweenblue)
        if self.use_alpha:
            self.anim_alpha = NumberAnimation(self.frm[3], self.to[3], tweenalpha)
        else:
            self.anim_alpha = NumberAnimation(1, 1, tweenalpha)

    @staticmethod
    def __clip(val, minimum, maximum):
        """
        
        :param val: input value 
        :param minimum: min value
        :param maximum: max value
        :return: val clipped to range [minimum, maximum]
        """
        if val is None or minimum is None or maximum is None:
            return None
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    #@lru_cache(maxsize=1000)
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        """
        :param frame: current frame 
        :param birthframe: frame where animation starts to return something other than None
        :param startframe: frame where animation starts to evolve
        :param stopframe: frame where animation stops evolving
        :param deathframe: frame where animation starts to return None
        :return: 
        """
        if self.use_alpha:
            return (self.__clip(self.anim_red.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1),
                    self.__clip(self.anim_green.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1),
                    self.__clip(self.anim_blue.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1))
        else:
            return (self.__clip(self.anim_red.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1),
                    self.__clip(self.anim_green.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1),
                    self.__clip(self.anim_blue.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1),
                    self.__clip(self.anim_alpha.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe), 0, 1))
