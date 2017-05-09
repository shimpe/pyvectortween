from abc import ABCMeta, abstractmethod

from vectortween.Utils import filter_none


class AbstractAnimation(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        """
        returns a single frame 
        :param frame: current frame 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None
        :param noiseframe: frame in which time varying noise function is evaluated
        :return: tweened value
        """
        return None

    @abstractmethod
    def curve_points(self, beginframe, endframe, framestep, birthframe, startframe, stopframe, deathframe,
                     filternone=False, noiseframe=None):
        """
        returns a list of frames from startframe to stopframe, in steps of framestep
        :param beginframe: first frame to include in list of points
        :param endframe: last frame to include in list of points
        :param framestep: framestep, e.g. 0.01 means that the points will be calculated in timesteps of 0.01
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None 
        :param filternone: removes all "None" values from the list of curve_points. The reply can still be None if no curve_points
        can be calculated.
        :param noiseframe: for time varying noise, this frame represents the current time for which the noise 
        must be evaluated
        :return: list of tweened values
        """
        return None


class Animation(AbstractAnimation):
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        """
        returns a single frame
        :param frame: current frame 
        :param birthframe: frame before which animation always returns None
        :param startframe: frame from which animation starts to evolve 
        :param stopframe: frame in which animation completed
        :param deathframe: frame in which animation starts returning None
        :param noiseframe: frame in which a time varying noise function is evaluated
        :return: tweened value
        """
        return None

    def curve_points(self, beginframe, endframe, framestep, birthframe, startframe, stopframe, deathframe,
                     filternone=True, noiseframe=None):
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
        :param filternone: automatically remove None entries
        :param noiseframe: for time varying noise, this represents the time for which the noise should be evaluated
        :return: list of tweened values
        """
        if endframe < beginframe and framestep > 0:
            assert False, "infinite loop: beginframe = {0}, endframe = {1}, framestep = {2}".format(beginframe,
                                                                                                    endframe, framestep)
        if endframe > beginframe and framestep < 0:
            assert False, "infinite loop: beginframe = {0}, endframe = {1}, framestep = {2}".format(beginframe,
                                                                                                    endframe, framestep)

        i = beginframe
        result = [self.make_frame(i, birthframe, startframe, stopframe, deathframe, noiseframe)]
        while i < endframe:
            i += framestep
            if i <= endframe:
                result.append(self.make_frame(i, birthframe, startframe, stopframe, deathframe, noiseframe))
        if filternone:
            return filter_none(result)
        else:
            return result
