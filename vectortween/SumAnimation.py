from vectortween.Animation import Animation


class SumAnimation(Animation):
    """
    animation to return the sum of two or more numberanimations or pointanimations
    """

    def __init__(self, list_of_animations=None):
        super().__init__(None, None)
        self.list_of_animations = list_of_animations

    def _my_sum(self, list_of_el):
        if any((el is None) for el in list_of_el):
            return None
        return sum(list_of_el)

    def make_frame(self, frame, birthframe, startframe, stopframe, deathframe, noiseframe=None):
        all_frames = [f.make_frame(frame, birthframe, startframe, stopframe, deathframe, noiseframe) for f in
                      self.list_of_animations]

        if not all_frames:
            return None

        if isinstance(all_frames[0], (int, float)):
            valid = all(isinstance(f, (int, float)) for f in all_frames)
            if valid:
                return self._my_sum(all_frames)
            return None
        elif isinstance(all_frames[0], (tuple,)):
            valid = all(isinstance(f, (tuple,)) for f in all_frames)
            if valid:
                result = []
                for i in range(len(all_frames)):
                    result.append(self._my_sum([el[i] for el in all_frames]))
                return tuple(result)
            return None
        return None
