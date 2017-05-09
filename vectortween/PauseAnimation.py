from vectortween.Animation import Animation


class PauseAnimation(Animation):
    """
    class that keeps returning the same values over and over again
    """

    def __init__(self, frm):
        super().__init__(frm, frm)

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        return self.frm
