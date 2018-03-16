import time

def primes(n):
    top = int(n**0.5)
    ps = {i for i in range(3, n + 1, 2)}
    ps.add(2)
    for i in range(3, top):
        if i in ps:
            for j in (i*i + x*i for x in range(n)):
                if j > top:
                    break
                ps.discard(j)
    return ps

def factors(n):
    r = n
    fs = {}
    top = n//3
    prim = primes(top)
    p = 0
    for f in prim:
        while r >= f and r % f == 0:
            r = r // f
            p += 1

        if p:
            fs[f] = p
            p = 0

    return [(f,p) for f,p in sorted(fs.items(), key=lambda f: f[0])]

def power_str(fs):
    f,p = fs
    return str(f) + ('^{}'.format(p) if p>1 else '')

def factor_str(fs):
    return ' * '.join([power_str(s) for s in fs])


def main(n):
    return factors(n)


if __name__ == '__main__':
    n = 100276593
    start = time.time()
    factors = main(n)
    end = time.time()
    print("prime factors of {}: {}".format(n, factor_str(factors)))
    print('sive time: {:.3f}\n'.format(end-start))
