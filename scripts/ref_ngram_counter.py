#!/usr/bin/env python3
import argparse
import sqlite3
from collections import Counter
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True)
ap.add_argument("--db", required=True)
ap.add_argument("--n-min", type=int, default=4)
ap.add_argument("--n-max", type=int, default=9)
ap.add_argument("--min-freq", type=int, default=3)
args = ap.parse_args()

arr = np.load(args.input, mmap_mode="r")
conn = sqlite3.connect(args.db)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS ngram")
cur.execute("CREATE TABLE ngram(ng TEXT PRIMARY KEY, len INTEGER, cnt INTEGER)")

for n in range(args.n_min, args.n_max + 1):
    c = Counter()
    for i in range(0, len(arr) - n + 1):
        ng = " ".join(map(str, arr[i:i+n]))
        c[ng] += 1

    rows = [(ng, n, cnt) for ng, cnt in c.items() if cnt >= args.min_freq]
    cur.executemany("INSERT INTO ngram(ng,len,cnt) VALUES(?,?,?)", rows)
    conn.commit()
    print("n", n, "rows", len(rows))

conn.execute("VACUUM")
conn.close()
