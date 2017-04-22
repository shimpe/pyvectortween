from vectortween.NumberAnimation import NumberAnimation

class PointAnimation(object):
    """
    animation of a 2d position (convenience class composing two number animations)
    """
    def __init__(self, startframe, stopframe, frm, to,
                 tween=None,ytween=None,birthframe=None,deathframe=None):
        """
        
        :param startframe: start of animation 
        :param stopframe: stop of animation
        :param frm: a list/tuple containing an (x, y) number (starting point; floats) 
        :param to: a list/tuple containing an (x, y) number (end point; floats)
        :param tween: tween method for the x coordinate (defaults to linear if not specified)
        :param ytween: tween method for the y coordinate (defaults to same as that for x coordinate)
        :param birthframe: time of appearance (defaults to startframe)
        :param deathframe: time of disappearance (defaults to stopframe)
        """
        if ytween is None:
            ytween = tween
        if birthframe is None:
            birthframe = startframe
        if deathframe is None:
            deathframe = stopframe
        self.anim_x = NumberAnimation(startframe, stopframe, frm[0], to[0], tween, birthframe, deathframe)
        self.anim_y = NumberAnimation(startframe, stopframe, frm[1], to[1], ytween, birthframe, deathframe)

    def make_frame(self, frame):
        """
        :param frame: current frame 
        :return: tuple containing the tweened values
        """
        newx = self.anim_x.make_frame(frame)
        newy = self.anim_y.make_frame(frame)
        return (newx, newy)
