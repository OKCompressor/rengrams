#!/usr/bin/env python3
import argparse
import sqlite3

ap = argparse.ArgumentParser()
ap.add_argument("a")
ap.add_argument("b")
args = ap.parse_args()

def load(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    table = "ngram" if "ngram" in tables else "ngrams"
    out = {}
    for ng, ln, cnt in cur.execute(f"SELECT ng,len,cnt FROM {table}"):
        out[(str(ng), int(ln))] = int(cnt)
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
    print("first_only_a", next(iter(only_a)), a[next(iter(only_a))])
if only_b:
    print("first_only_b", next(iter(only_b)), b[next(iter(only_b))])
if diff:
    k = diff[0]
    print("first_diff", k, a[k], b[k])

if only_a or only_b or diff:
    raise SystemExit("COMPARE_FAIL")

print("COMPARE_OK")
