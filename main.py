from time import perf_counter
from pickle import load, dump
from os.path import exists
from sys import getrecursionlimit
import redis

name = "Python Fibonacci"
author = "Kacper Chołody"
group = "Grupa 1.1"
        
def fibonacci_local(n: int, cache: dict = {}) -> int:
    if n == 0 or n == 1:
        return n
    
    limit = getrecursionlimit() - 3
    
    if n <= (limit):
        try:
            return cache[n]
        except KeyError:
            result = fibonacci_local(n-1, cache) + fibonacci_local(n-2, cache)
            cache[n] = result
            return result
    else:
        try:
            return cache[n]
        except KeyError:            
            a = fibonacci_local(limit - 1, cache)
            b = fibonacci_local(limit, cache)
                        
            for i in range(limit, n+1):
                a, b = b, a + b
                if(i <= 100000):
                    cache[i] = a
            return a
        
def fibonacci_redis(n: int, r: redis) -> int:
    if n == 0 or n == 1:
        return n
    
    limit = getrecursionlimit() - 3
    cache = {}
    
    if n <= (limit):        
        if r.exists(str(n)):
            return int(r.get(str(n)))
        else:
            result = fibonacci_local(n-1, cache) + fibonacci_local(n-2, cache)
            str_cache = {str(k): v for k, v in cache.items()}            
            r.mset(str_cache)  
            r.setnx(str(n), result)
            return result
    else:
        if r.exists(str(n)):
            return int(r.get(str(n)))
        else:            
            a = fibonacci_local(limit - 1, cache)
            b = fibonacci_local(limit, cache)
                        
            for i in range(limit, n+1):
                a, b = b, a + b
                if(i <= 10000):
                    cache[i] = a
            
            str_cache = {str(k): v for k, v in cache.items()}            
            r.mset(str_cache)            
            return a

def main():
    print(f"{name=}\n{author=}\n{group=}\n")
    
    r_available = False
    r = redis.Redis(host='localhost', port=6379)
    
    try:
        if r.ping():
            r_available = True
    except Exception:
        pass
        
    if not r_available:
        print("Redis is not available, fallback to local cache")
        if exists('cache.pkl'):
            with open('cache.pkl', 'rb') as f:
                cache = load(f)
        else:
            cache = {}
        
    while True:
        N = int(input("Please input element number you want to calculate, enter -1 to exit: "))
        
        if(N >= 0):
            start_t = perf_counter()
        
            if r_available:
                    result = fibonacci_redis(N, r)
            else:
                result = fibonacci_local(N, cache)
            
            end_t = perf_counter()
            
            print(f"Value of {N} element {result= }")
            print(f"Calculation time: {(end_t - start_t):.6f} s")
        
        elif N == -1:
            break
        else:
            continue
    
    if not r_available:
        with open('cache.pkl', 'wb') as f:
            dump(cache, f)

if __name__ == "__main__":
    main()
