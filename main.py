from time import perf_counter
from json import dump, load
from os.path import exists
from sys import getrecursionlimit

name = "Python Fibonacci"
author = "Kacper Chołody"
group = "Grupa 1.1"
        
def fibonacci(n: int, cache: dict = {}) -> int:
    if n == 0 or n == 1:
        return n
    
    limit = getrecursionlimit() - 3
    
    if n <= (limit):
        try:
            return cache[n]
        except KeyError:
            result = fibonacci(n-1, cache) + fibonacci(n-2, cache)
            cache[n] = result
            return result
    else:
        a = fibonacci(limit - 1, cache)
        b = fibonacci(limit, cache)
        
        iters = n - limit + 1
        
        for _ in range(iters):
            a, b = b, a + b
        return a
        
        
    

def main():
    print(getrecursionlimit())
    print(f"{name=}\n{author=}\n{group=}\n")
    N = int(input("Please input element number you want to calculate: "))
    
    
    if exists('cache.json'):
        with open('cache.json', 'r') as f:
            cache = load(f)
    else:
        cache = {}
        
    start_t = perf_counter()
    
    try:
        result = fibonacci(N, cache)
    except RecursionError:
        print("Calculation crashed, probably input value is too large")
        exit(-1)
    
    print(f"Value of {N} element {result= }")
    print(f"Calculation time: {(perf_counter() - start_t):.3f} s")
    
    with open('cache.json', 'w') as f:
        dump(cache, f)
    

if __name__ == "__main__":
    main()
        