from __future__ import print_function

from random import random as rand
from random import uniform, gauss

def rand_vals(count=256):
    '''Return values chosen randomly from interval [0,1).

    ARGUMENT
    count -- number of values to return.

    RETURNS
    A tuple of lists (x,y).  The y values are the computed random variates,
    and the x values are sequentially numbered from 1.
    '''

    x = []
    y = []
    for n in range(1, count + 1):
        x.append(n)
        y.append(rand())

    return (x,y)

def uniform_vals(a=-0.5, b=0.5, count=256):
    '''Return values chosen randomly from interval [min, max].

    ARGUMENTS
    a -- minimum value to return
    b -- maximum value to return
    count -- number of values to return.

    RETURNS
    A tuple of lists (x,y).  The y values are the computed random variates,
    and the x values are sequentially numbered from 1.
    '''

    x = []
    y = []
    for n in range(1, count + 1):
        x.append(n)
        y.append(uniform(a,b))

    return (x,y)

def gaussian_vals(mu=0.0, sigma=1.0, count=256):
    '''Return values chosen randomly from gaussian distribution having
    specified mean and standard deviation].

    ARGUMENTS
    mu -- distribution mean
    sigma -- distribution standard deviation
    count -- number of values to return.

    RETURNS
    A tuple of lists (x,y).  The y values are the computed random variates,
    and the x values are sequentially numbered from 1.
    '''

    x = []
    y = []
    for n in range(1, count + 1):
        x.append(n)
        y.append(gauss(mu, sigma))

    return (x,y)


if __name__ == '__main__':
    def print_vals(vals):
        x,y  = vals
        _vals = ['%s %0.3f' % (x[i], y[i]) for i in range(len(x))]
        print('\n'.join(_vals))

    print ('rand_vals')
    print_vals(rand_vals(20))
    print()

    print('uniform_vals')
    print_vals(uniform_vals(0,1,20))
    print()

    print ('gaussian_vals')
    print_vals(gaussian_vals(1,.5,20))
