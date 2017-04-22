from vectortween.NumberAnimation import NumberAnimation

class PointAnimation(object):
    """
    animation of a 2d position (convenience class composing two number animations)
    """
    def __init__(self, frm, to, tween=None,ytween=None):
        """
        :param frm: a list/tuple containing an (x, y) number (starting point; floats) 
        :param to: a list/tuple containing an (x, y) number (end point; floats)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        """
        if ytween is None:
            ytween = tween
        self.anim_x = NumberAnimation(frm[0], to[0], tween)
        self.anim_y = NumberAnimation(frm[1], to[1], ytween)


    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        :param frame: current frame 
        :param birthframe: frame where this animation starts returning something other than None
        :param startframe: frame where animation starts to evolve
        :param stopframe: frame where animation is completed
        :param deathframe: frame where animation starts to return None
        :return: 
        """
        newx = self.anim_x.make_frame(frame, birthframe, startframe, stopframe, deathframe)
        newy = self.anim_y.make_frame(frame, birthframe, startframe, stopframe, deathframe)
        return (newx, newy)
