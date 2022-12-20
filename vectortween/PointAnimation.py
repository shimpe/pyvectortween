from functools import lru_cache

from vectortween.Animation import Animation
from vectortween.NumberAnimation import NumberAnimation
from vectortween.Tween import Tween


class PointAnimation(Animation):
    """
    animation of a 2d position (convenience class composing two number animations)
    """

    def __init__(self, frm, to, tween=None, ytween=None, noise_fn=None, y_noise_fn=None, xy_noise_fn=None):
        """
        :param frm: a list/tuple containing an (x, y) number (starting point; floats) 
        :param to: a list/tuple containing an (x, y) number (end point; floats)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        :param noise_fn: optional noise function for x,t coordinates, returning single value
        :param y_noise_fn: optional noise function for y,t coordinates, returning single value
        :param xy_noise_fn: optional noise function for x,y,t coordinates, returning two values
        """
        super().__init__(frm, to)
        if ytween is None:
            ytween = tween

        self.xy_noise_fn = xy_noise_fn
        self.anim_x = NumberAnimation(self.frm[0], self.to[0], tween, noise_fn)
        self.anim_y = NumberAnimation(self.frm[1], self.to[1], ytween, y_noise_fn)

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
        newx = self.anim_x.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe)
        newy = self.anim_y.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe)

        if self.xy_noise_fn is not None:
            if noiseframe is not None:
                t = noiseframe
            else:
                t = Tween.tween2(frame, startframe, stopframe)
            addx, addy = self.xy_noise_fn(newx, newy, t)
        else:
            addx, addy = 0, 0
        final_x = newx + addx if (newx is not None and addx is not None) else None
        final_y = newy + addy if (newy is not None and addy is not None) else None
        return final_x, final_y
