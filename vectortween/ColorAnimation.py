from vectortween.NumberAnimation import NumberAnimation

class ColorAnimation(object):
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
 
        Note: output will contain alpha if input contains alpha. You can force adding/removing alpha by setting use_alpha=True/False in the 
        ColorAnimation instance.
        """
        self.startred = frm[0]
        self.stopred = to[0]
        self.startgreen = frm[1]
        self.stopgreen = to[1]
        self.startblue = frm[2]
        self.stopblue = to[2]
        self.startalpha = 1
        self.stopalpha = 1
        try:
            self.startalpha = frm[3]
            self.stopalpha = to[3]
            self.use_alpha = True
        except:
            self.use_alpha = False
            pass

        if tweenalpha is None:
            tweenalpha = ['linear']

        self.anim_red = NumberAnimation(self.startred, self.stopred, tween)
        self.anim_green = NumberAnimation(self.startgreen, self.stopgreen, tweengreen)
        self.anim_blue = NumberAnimation(self.startblue, self.stopblue, tweenblue)
        self.anim_alpha = NumberAnimation(self.startalpha, self.stopalpha, tweenalpha)

    def __clip(self, val, minimum, maximum):
        """
        
        :param val: input value 
        :param minimum: min value
        :param maximum: max value
        :return: val clipped to range [minimum, maximum]
        """
        if (val is None or minimum is None or maximum is None):
            return None
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        :param frame: current frame 
        :param birthframe: frame where animation starts to return something other than None
        :param startframe: frame where animation starts to evolve
        :param stopframe: frame where animation stops evolving
        :param deathframe: frame where animation starts to return None
        :return: 
        """
        if self.use_alpha:
            return (self.__clip(self.anim_red.make_frame(frame, birthframe, startframe, stopframe, deathframe),0,1),
                    self.__clip(self.anim_green.make_frame(frame, birthframe, startframe, stopframe, deathframe),0,1),
                    self.__clip(self.anim_blue.make_frame(frame, birthframe, startframe, stopframe, deathframe),0,1))
        else:
            return (self.__clip(self.anim_red.make_frame(frame, birthframe, startframe, stopframe, deathframe), 0, 1),
                    self.__clip(self.anim_green.make_frame(frame, birthframe, startframe, stopframe, deathframe), 0, 1),
                    self.__clip(self.anim_blue.make_frame(frame, birthframe, startframe, stopframe, deathframe), 0, 1),
                    self.__clip(self.anim_alpha.make_frame(frame, birthframe, startframe, stopframe, deathframe), 0, 1))
