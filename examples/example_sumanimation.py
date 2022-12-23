from vectortween.NumberAnimation import NumberAnimation
from vectortween.PointAnimation import PointAnimation
from vectortween.SumAnimation import SumAnimation

if __name__ == "__main__":
    p = NumberAnimation(0, 10, ['linear'])
    q = NumberAnimation(5, 20, ['linear'])
    s = SumAnimation([p, q])
    assert(s.make_frame(0, 0, 0, 1, 1) == 5)
    assert(s.make_frame(1, 0, 0, 1, 1) == 30)

    p2 = PointAnimation([0,0], [5,10], ['linear'], ['linear'])
    q2 = PointAnimation([0,0], [-10,-30], ['linear'], ['linear'])
    s2 = SumAnimation([p2, q2])
    assert(s2.make_frame(0, 0, 0, 1, 1) == (0, 0))
    assert(s2.make_frame(1, 0, 0, 1, 1) == (-5, -20))

    p3 = NumberAnimation(0, 10, ['linear'])
    q3 = PointAnimation([0, 0], [-5, -20], ['linear'], ['linear'])
    s3 = SumAnimation([p3, q3])
    assert(s3.make_frame(0, 0, 0, 1, 1) == None)
    assert(s3.make_frame(1, 0, 0, 1, 1) == None)

