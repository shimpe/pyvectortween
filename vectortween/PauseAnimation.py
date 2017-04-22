from vectortween.Animation import Animation


class PauseAnimation(Animation):
    """
    class that keeps returning the same values over and over again
    """
    def __init__(self, frm):
        self.frm = frm

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        return self.frm
