from vectortween.Utils import filter_none

def test_filternone():
    assert filter_none([]) == []
    assert filter_none([None]) == []
    assert filter_none([1, 2, None]) == [1, 2]
    assert filter_none([1, None, 2]) == [1, 2]
    assert filter_none([None, 1, 2]) == [1, 2]
    assert filter_none([[None, 1], [1, None], [1,2]]) == [[1,2]]
