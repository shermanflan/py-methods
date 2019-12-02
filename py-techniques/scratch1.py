def compress(s):
    """AABBCC|AAABCCDDDD"""
    import re

    nn2 = r"""(?P<twoplus>(?P<single>[a-zA-Z])(?P=single){1,})"""
    re_nn2 = re.compile(nn2, flags=0)
    compressed = re_nn2.sub(lambda m: m.group("single")+str(len(m.group("twoplus"))), s)

    return compressed if len(compressed) < len(s) else s

if __name__ == "__main__":

    t3 = 'AABBCC'
    arr = compress(t3)
    assert arr == 'AABBCC'

    t4 = 'AAABCCDDDD'
    arr = compress(t4)
    assert arr == 'A3BC2D4'

