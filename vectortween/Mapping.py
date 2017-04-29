import math


class Mapping(object):
    """
    class to map numbers from one range to another range
    """

    def _init__(self):
        pass

    @staticmethod
    def clip_value(value, minimum, maximum):
        if minimum > maximum:
            minimum, maximum = maximum, minimum
        if value < minimum:
            return minimum
        elif value > maximum:
            return maximum
        else:
            return value

    @staticmethod
    def linlin(value, in_min, in_max, out_min, out_max, clip=True):
        """
        maps value \in [in_min,in_max] linearly to the corresponding value \in [out_min, out_max]
        (extrapolating if needed)
        e.g. linlin(0.3,0,1,10,20) = 13
            
        :param value: value to be mapped 
        :param in_min: input range minimum
        :param in_max: input range maximum
        :param out_min: what input range minimum is mapped to
        :param out_max: what input range maximum is mapped to
        :param clip: if True, the output value is clipped to range [out_min, out_max] 
        :return: linear mapping from value in input range to value in output range (extrapolating if needed)
         
         example: linlin(0.2, 0, 1, 10, 20) = 13
        """
        if in_min == in_max:
            if value == in_min and out_min == out_max:
                return out_min
            return None

        output = ((out_min + out_max) + (out_max - out_min) * (
            (2 * value - (in_min + in_max)) / float(in_max - in_min))) / 2.0
        if clip:
            output = Mapping.clip_value(output, out_min, out_max)
        return output

    @staticmethod
    def linexp(value, in_min, in_max, out_min, out_max, clip=True):
        """
        maps value \in linear range [in_min,in_max] corresponding value \in exponential range [out_min, out_max]
        (extrapolating if needed)

        :param value: value to be mapped 
        :param in_min: input range minimum
        :param in_max: input range maximum
        :param out_min: what input range minimum is mapped to
        :param out_max: what input range maximum is mapped to
        :param clip: if True, the output value is clipped to range [out_min, out_max]        
        :return: mapping from value in linear input range to value in exponential output range (extrapolating if needed)
        """
        if out_min == 0:
            return None
        if in_min == in_max:
            if value == in_min and out_min == out_max:
                return out_min
            return None

        output = math.pow(out_max / out_min, (value - in_min) / (in_max - in_min)) * out_min
        if clip:
            output = Mapping.clip_value(output, out_min, out_max)
        return output

    @staticmethod
    def explin(value, in_min, in_max, out_min, out_max, clip=True):
        """
        maps value \in exponential range [in_min,in_max] corresponding value \in linear range [out_min, out_max]
        (extrapolating if possible)

        :param value: value to be mapped 
        :param in_min: input range minimum
        :param in_max: input range maximum
        :param out_min: what input range minimum is mapped to
        :param out_max: what input range maximum is mapped to
        :param clip: if True, the output value is clipped to range [out_min, out_max]        
        :return: mapping from value in  exponential input range to value in linear output range 
        (extrapolating if possible)
        """
        if in_min == 0:
            return None
        if (value / in_min) <= 0:
            return None
        if (in_max / in_min) <= 0:
            return None

        output = math.log(value / in_min) / math.log(in_max / in_min) * (out_max - out_min) + out_min
        if clip:
            output = Mapping.clip_value(output, out_min, out_max)
        return output

    @staticmethod
    def expexp(value, in_min, in_max, out_min, out_max, clip=True):
        """
        maps value \in exponential range [in_min,in_max] corresponding value \in exponential range [out_min, out_max]
        (extrapolating if possible)

        :param value: value to be mapped 
        :param in_min: input range minimum
        :param in_max: input range maximum
        :param out_min: what input range minimum is mapped to
        :param out_max: what input range maximum is mapped to
        :param clip: if True, the output value is clipped to range [out_min, out_max]           
        :return: mapping from value in  exponential input range to value in exponential output range 
        (extrapolating if possible)
        """
        if out_min:
            return None
        if value == 0:
            return None
        if value / in_min <= 0:
            return None
        if in_min == 0:
            return None
        if (in_max - in_min) <= 0:
            return None

        output = math.pow(out_max / out_min, math.log(value / in_min) / math.log(in_max / in_min)) * out_min
        if clip:
            output = Mapping.clip_value(output, out_min, out_max)
        return output
