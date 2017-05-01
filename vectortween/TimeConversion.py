class TimeConversion(object):
    """
    class offering some convenience methods for conversion of time to frame number
    """

    def __init__(self):
        pass

    @staticmethod
    def sec2frame(sec, fps):
        """
        :param sec: seconds (float) 
        :param fps: frame rate (float)
        :return: frame number (integer)
        """
        return int(sec * fps)

    @staticmethod
    def hms2frame(hms, fps):
        """
        :param hms: a string, e.g. "01:23:15" for one hour, 23 minutes 15 seconds 
        :param fps: framerate 
        :return: frame number
        """
        import time
        t = time.strptime(hms, "%H:%M:%S")
        return (t.tm_hour * 60 * 60 + t.tm_min * 60 + t.tm_sec) * fps
