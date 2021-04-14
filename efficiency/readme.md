

python -m memory_profiler memory_profiler.py

```
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
     1   39.863 MiB   39.863 MiB           1   @profile
     2                                         def my_func():
     3   47.496 MiB    7.633 MiB           1       a = [1] * (10 ** 6)
     4  200.086 MiB  152.590 MiB           1       b = [2] * (2 * 10 ** 7)
     5   47.496 MiB -152.590 MiB           1       del b
     6   47.496 MiB    0.000 MiB           1       return a
```


## reference
https://scikit-learn.org/dev/developers/performance.html#memory-usage-profiling
https://zhuanlan.zhihu.com/p/121003986