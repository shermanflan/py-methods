#!/bin/python3

import math
import os
import random
import re
import sys
from operator import *
from collections import Counter

s = 'qwertyuiopasdfghjklzxcvbnm' #input()
print(Counter(s))

top3 = Counter(s).items() #.most_common(3)
print(top3)

byGradeAsc = sorted(top3, key=lambda x: x[0])
print(byGradeAsc)

byFreqDesc = sorted(byGradeAsc, key=lambda x: x[1], reverse=True)[:3]
print(byFreqDesc)

print('\n'.join(['{0} {1}'.format(l, n) for l, n in byFreqDesc]))
