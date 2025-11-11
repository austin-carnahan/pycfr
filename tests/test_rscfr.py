import sys
import os
sys.path.insert(0,os.path.realpath('.'))
from pokerstrategy import *
from pokergames import *
from pokercfr import *

def near(val, expected, distance=0.0001):
    return val >= (expected - distance) and val <= (expected + distance)

print('')
print('')
print('Testing Retrospective Sampling (RS) CFR')
print('')
print('')

print('Computing NE for Leduc poker')
leduc = leduc_rules()

cfr = RetrospectiveSamplingCFR(leduc)

iterations_per_block = 1000
blocks = 10
for block in range(blocks):
    print('Iterations: {0}'.format(block * iterations_per_block))
    cfr.run(iterations_per_block)
    result = cfr.profile.best_response()
    print('Best response EV: {0}'.format(result[1]))
    print('Total exploitability: {0}'.format(sum(result[1])))
print('Done!')
print('')
