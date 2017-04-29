from vectortween.Mapping import Mapping

def test_linlin():
    clip = True
    noclip = False

    table = (
        # inputs, expected output
        ([0, 0, 0, 0, 0], 0),
        ([0, 0, 0, 0, 0, clip], 0),
        ([1, 0, 0, 0, 0], None),
        ([1, 0, 0, 0, 0, noclip], None),
        ([1, 0, 2, 0, 100], 50),
        ([-1, 0, -2, 0, 100], 50),
        ([-2, 0, -2, 0, 100], 100),
        ([6, 5, 10, 50, 100], 60),
        ([2, 0, 1, 0, 100, noclip], 200),
        ([2, 0, 1, 0, 100, clip], 100),
        ([-2, 0, -1, 0, -100, noclip], -200),
        ([2, 0, 1, 0, -100, clip], -100),
        ([2, 1, 10, 1, 100], 12),
        ([2, 10, 1, 1, 100], 89),
        ([2, 10, 1, 100, 1], 12),
        ([2, 1, 10, 100, 1], 89),
        ([-2, -1, -10, 1, 100], 12),
        ([-2, -10, -1, 1, 100], 89),
        ([-2, -10, -1, 100, 1], 12),
        ([-2, -1, -10, 100, 1], 89),
        ([2, 1, 10, -1, -100], -12),
        ([2, 10, 1, -1, -100], -89),
        ([2, 10, 1, -100, -1], -12),
        ([2, 1, 10, -100, -1], -89),
    )

    for test in table:
        assert Mapping.linlin(*test[0]) == test[1]

def test_linexp():
    clip = True
    noclip = False

    table = (
        # inputs, expected output
        ([0, 0, 0, 0, 0], None),
        ([0, 0, 0, 0, 0, clip], None),
        ([1, 0, 0, 0, 0], None),
        ([1, 0, 0, 0, 0, noclip], None),
        ([1, 0, 2, 0, 100], None),
        ([1, 1, 10, 1, 100], 1),
        ([2, 1, 10, 1, 100], 1.6681005372000588),
        ([8, 1, 10, 1, 100], 35.938136638046274),
        ([8, 1, 10, -1, -100], -35.938136638046274),
        ([11, 1, 10, -1, -100], -100),
        ([11, 1, 10, -1, -100, noclip], -166.81005372000593),
        ([-2, -1, -10, -1, -100], -1.6681005372000588),
        ([-2, -10, -1, -1, -100], -59.94842503189409),
        ([-2, -10, -1, -100, -1], -1.6681005372000592),
        ([-2, -1, -10, -100, -1], -59.948425031894104),
        ([2, 1, 10, 1, 100], 1.6681005372000588),
        ([2, 10, 1, 1, 100], 59.94842503189409),
        ([2, 10, 1, 100, 1], 1.6681005372000592),
        ([2, 1, 10, 100, 1], 59.948425031894104),
        ([-2, -1, -10, 1, 100], 1.6681005372000588),
        ([-2, -10, -1, 1, 100], 59.94842503189409),
        ([-2, -10, -1, 100, 1], 1.6681005372000592),
        ([-2, -1, -10, 100, 1], 59.948425031894104),
        ([2, 1, 10, -1, -100], -1.6681005372000588),
        ([2, 10, 1, -1, -100], -59.94842503189409),
        ([2, 10, 1, -100, -1], -1.6681005372000592),
        ([2, 1, 10, -100, -1], -59.948425031894104),
    )

    for test in table:
        assert Mapping.linexp(*test[0]) == test[1]