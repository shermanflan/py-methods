from algolib.apply.strings.knuth_morris_pratt import kmp

def test_kmp():
    t = 'atcdamalgamatexyz'
    p = 'amalgamate'

    assert kmp(t, p, 4) == 4
