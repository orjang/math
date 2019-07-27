import unittest
from pymath import prime


def is_prime(n):
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return n > 1


class TestPrimes(unittest.TestCase):

    def test_primes_returns_only_prime_numbers(self):
        for n in range(100):
            ps = prime.primes(n)
            composites = list(filter(lambda d: not is_prime(d), ps))
            self.assertFalse(composites, 'non prime numbers found in return from primes({})'.format(composites))

    def test_one_is_not_a_prime_number(self):
        ps = prime.primes(1)
        self.assertFalse(ps, 'one it not a prime number')
