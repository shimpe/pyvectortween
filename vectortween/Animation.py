from abc import ABCMeta, abstractmethod


class AbstractAnimation(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        
        :param frame: current frame 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None
        :return: tweened value
        """
        pass


class Animation(AbstractAnimation):
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to


