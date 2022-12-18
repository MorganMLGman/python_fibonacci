from time import perf_counter
from pickle import load, dump
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
        try:
            return cache[n]
        except KeyError:            
            a = fibonacci(limit - 1, cache)
            b = fibonacci(limit, cache)
                        
            for i in range(limit, n+1):
                a, b = b, a + b
                if(i <= 100000):
                    cache[i] = a
            return a

def main():
    print(f"{name=}\n{author=}\n{group=}\n")
    
    if exists('cache.pkl'):
        with open('cache.pkl', 'rb') as f:
            cache = load(f)
    else:
        cache = {}
        
    while True:
        N = int(input("Please input element number you want to calculate, enter -1 to exit: "))
        
        if(N >= 0):
            start_t = perf_counter()
        
            try:
                result = fibonacci(N, cache)
            except RecursionError:
                print("Calculation crashed, probably input value is too large")
                continue
            
            end_t = perf_counter()
            
            print(f"Value of {N} element {result= }")
            print(f"Calculation time: {(end_t - start_t):.6f} s")
        
        elif N == -1:
            break
        else:
            continue
    
    with open('cache.pkl', 'wb') as f:
        dump(cache, f)

if __name__ == "__main__":
    main()
