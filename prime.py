import time
from functools import reduce
from collections import Counter

def primes(n):
    top = int(n**0.5)
    ps = {i for i in range(2, n + 1)}
    for i in range(2, top):
        if i in ps:
            for j in (i*i + x*i for x in range(n)):
                if j > n:
                    break
                ps.discard(j)
    return ps

def factors(n):
    r = n
    fs = Counter()
    top = int(n**0.5)
    while not r & 1:
        r >>= 1
        fs[2] += 1

    for f in range(3, top, 2):
        while r % f == 0:
            r = r // f
            fs[f] += 1
            if r == 0:
                break

    if r > 1:
        fs[r] = 1
    facts = [(f,p) for f,p in sorted(fs.items(), key=lambda f: f[0])]

    return facts

def power_str(fs):
    f,p = fs
    return str(f) + ('^{}'.format(p) if p>1 else '')

def factor_str(fs):
    return ' * '.join([power_str(s) for s in fs])


def sundaram3(max_n):
    numbers = list(range(3, max_n+1, 2))
    half = max_n // 2
    initial = 4

    for step in range(3, max_n+1, 2):
        for i in range(initial, half, step):
            numbers[i-1] = 0
        initial += 2*(step+1)

        if initial > half:
            return [2] + list(filter(None, numbers))

def main(n):
    start = time.time()
    fs = factors(n)
    end = time.time()
    print("prime factors of {}: {}".format(n, factor_str(fs)))
    print('time: {:.3f}\n'.format(end-start))
    check = reduce(lambda a,b: a*b,[f**p for (f,p) in fs])
    assert check == n


def xtime(f, *args, **kws):
    stime = time.time()
    f(*args, **kws)
    etime = time.time()
    return etime - stime

if __name__ == '__main__':
    #n = 13727732*89345*23244
    #main(n)

    stime = time.time()
    s3=sundaram3(pow(10,3))
    etime = time.time()
    sund = etime - stime
    print('sundaram3: {:f}'.format(sund))

    stime = time.time()
    p=primes(pow(10,3))
    etime = time.time()
    prim = etime - stime
    print('primes: {:f}'.format(prim))
    print('ratio: {:f}'.format(prim/sund))

    print('s3:{}'.format(sorted(s3)))
    print('p :{}'.format(sorted(p)))
