class Mapping(object):
    """
    class to map numbers from one range to another range
    """
    def _init__(self):
        pass

    def linlin(self, value, a, b, c, d):
        """
            maps value \in [a,b] linearly to the corresponding value \in [c, d]
            e.g. linlin(0.3,0,1,10,20) = 13
        """
        if (a == b):
            if (value == a and c==d):
                return c
            return None

        return ((c + d) + (d - c) * ((2 * value - (a + b)) / float(b - a))) / 2.0
