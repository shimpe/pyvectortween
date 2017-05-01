from abc import ABCMeta, abstractmethod
from vectortween.Utils import filter_none

class AbstractAnimation(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        returns a single frame 
        :param frame: current frame 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None
        :return: tweened value
        """
        return None

    @abstractmethod
    def curve_points(self, beginframe, endframe, framestep, birthframe, startframe, stopframe, deathframe):
        """
        returns a list of frames from startframe to stopframe, in steps of framestep
        :param beginframe: first frame to include in list of points
        :param endframe: last frame to include in list of points
        :param framestep: framestep 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None 
        :return: list of tweened values
        """
        return None


class Animation(AbstractAnimation):
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe):
        """
        returns a single frame
        :param frame: current frame 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None
        :return: tweened value
        """
        return None

    def curve_points(self, beginframe, endframe, framestep, birthframe, startframe, stopframe, deathframe, filternone=True):
        """
        returns a list of frames from startframe to stopframe, in steps of framestepj
        warning: the list of points may include "None" elements 
        :param beginframe: first frame to include in list of points
        :param endframe: last frame to include in list of points
        :param framestep: framestep 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None 
        :return: list of tweened values
        """
        if endframe < beginframe and framestep > 0:
            assert False, "infinite loop: beginframe = {0}, endframe = {1}, framestep = {2}".format(beginframe,
                                                                                                    endframe, framestep)
        if endframe > beginframe and framestep < 0:
            assert False, "infinite loop: beginframe = {0}, endframe = {1}, framestep = {2}".format(beginframe,
                                                                                                    endframe, framestep)

        i = beginframe
        result = [self.make_frame(i, birthframe, startframe, stopframe, deathframe)]
        while i < endframe:
            i += framestep
            if i <= endframe:
                result.append(self.make_frame(i, birthframe, startframe, stopframe, deathframe))
        if filternone:
            return filter_none(result)
        else:
            return result