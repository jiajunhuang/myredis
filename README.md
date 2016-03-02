# myredis

## deprecated

fake redis implement in python3.

usage:

```bash
git clone https://github.com/gansteed/myredis
sudo pip3 install hiredis 
sudo pip3 install rdbtools3
cd myredis && python3 main.py
```

Here is result of benchmark by `redis-benchmark -t lpush,lpop`:

```bash
====== LPUSH ======
100000 requests completed in 10.84 seconds
50 parallel clients
3 bytes payload
keep alive: 1

0.00% <= 1 milliseconds
0.01% <= 2 milliseconds
0.05% <= 3 milliseconds
0.18% <= 4 milliseconds
6.87% <= 5 milliseconds
73.04% <= 6 milliseconds
99.95% <= 8 milliseconds
99.96% <= 9 milliseconds
99.96% <= 10 milliseconds
99.96% <= 11 milliseconds
99.96% <= 13 milliseconds
99.96% <= 16 milliseconds
99.96% <= 19 milliseconds
99.96% <= 23 milliseconds
99.96% <= 26 milliseconds
99.96% <= 30 milliseconds
99.96% <= 34 milliseconds
99.97% <= 37 milliseconds
99.97% <= 41 milliseconds
99.97% <= 45 milliseconds
99.97% <= 50 milliseconds
99.97% <= 54 milliseconds
99.97% <= 58 milliseconds
99.97% <= 63 milliseconds
99.97% <= 67 milliseconds
99.97% <= 72 milliseconds
99.97% <= 77 milliseconds
99.98% <= 81 milliseconds
99.98% <= 86 milliseconds
99.98% <= 91 milliseconds
99.98% <= 96 milliseconds
99.98% <= 101 milliseconds
99.98% <= 105 milliseconds
99.98% <= 109 milliseconds
99.98% <= 113 milliseconds
99.98% <= 118 milliseconds
99.99% <= 122 milliseconds
99.99% <= 127 milliseconds
99.99% <= 131 milliseconds
99.99% <= 136 milliseconds
99.99% <= 141 milliseconds
99.99% <= 146 milliseconds
99.99% <= 151 milliseconds
99.99% <= 156 milliseconds
99.99% <= 162 milliseconds
99.99% <= 167 milliseconds
100.00% <= 173 milliseconds
100.00% <= 179 milliseconds
100.00% <= 185 milliseconds
100.00% <= 191 milliseconds
100.00% <= 197 milliseconds
100.00% <= 203 milliseconds
9224.24 requests per second

====== LPOP ======
100000 requests completed in 10.67 seconds
50 parallel clients
3 bytes payload
keep alive: 1

0.06% <= 1 milliseconds
0.28% <= 2 milliseconds
0.36% <= 3 milliseconds
0.54% <= 4 milliseconds
39.66% <= 5 milliseconds
97.92% <= 6 milliseconds
99.69% <= 7 milliseconds
99.78% <= 8 milliseconds
99.86% <= 9 milliseconds
99.90% <= 10 milliseconds
99.93% <= 11 milliseconds
99.96% <= 12 milliseconds
99.97% <= 14 milliseconds
99.97% <= 16 milliseconds
99.97% <= 18 milliseconds
99.97% <= 20 milliseconds
99.97% <= 22 milliseconds
99.97% <= 24 milliseconds
99.97% <= 32 milliseconds
99.99% <= 39 milliseconds
99.99% <= 44 milliseconds
99.99% <= 49 milliseconds
99.99% <= 54 milliseconds
99.99% <= 60 milliseconds
99.99% <= 65 milliseconds
99.99% <= 70 milliseconds
100.00% <= 76 milliseconds
100.00% <= 81 milliseconds
100.00% <= 87 milliseconds
100.00% <= 93 milliseconds
100.00% <= 99 milliseconds
100.00% <= 105 milliseconds
9374.71 requests per second
```

Note: list in `myredis` implement in deque.
