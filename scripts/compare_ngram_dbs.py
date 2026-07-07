#!/usr/bin/env python3
import argparse
import ast
import os
import re
import sqlite3

ap = argparse.ArgumentParser()
ap.add_argument("a")
ap.add_argument("b")
args = ap.parse_args()

def parse_ng(x):
    s = str(x).strip()
    if s.startswith("[") and s.endswith("]"):
        return tuple(int(v) for v in ast.literal_eval(s))
    return tuple(int(v) for v in re.findall(r"-?\d+", s))

def pick_table(cur):
    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )]
    print("tables", tables)
    for name in ("ngram", "ngrams"):
        if name in tables:
            return name
    raise SystemExit("COMPARE_FAIL no ngram/ngrams table found")

def load(db):
    if not os.path.exists(db):
        raise SystemExit(f"COMPARE_FAIL missing db: {db}")
    if os.path.getsize(db) == 0:
        raise SystemExit(f"COMPARE_FAIL empty db: {db}")

    con = sqlite3.connect(db)
    cur = con.cursor()
    table = pick_table(cur)

    out = {}
    for ng, ln, cnt in cur.execute(f"SELECT ng,len,cnt FROM {table}"):
        key = (parse_ng(ng), int(ln))
        out[key] = int(cnt)
    con.close()
    return out

a = load(args.a)
b = load(args.b)

only_a = set(a) - set(b)
only_b = set(b) - set(a)
diff = [k for k in set(a) & set(b) if a[k] != b[k]]

print("a_rows", len(a))
print("b_rows", len(b))
print("only_a", len(only_a))
print("only_b", len(only_b))
print("count_diffs", len(diff))

if only_a:
    k = next(iter(only_a))
    print("first_only_a", k, a[k])
if only_b:
    k = next(iter(only_b))
    print("first_only_b", k, b[k])
if diff:
    k = diff[0]
    print("first_diff", k, a[k], b[k])

if only_a or only_b or diff:
    raise SystemExit("COMPARE_FAIL")

print("COMPARE_OK")
