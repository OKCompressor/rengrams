#!/usr/bin/env python3
import argparse
import gzip
import hashlib
import lzma
import os
import sqlite3
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("db")
ap.add_argument("--out-prefix", required=True)
args = ap.parse_args()

db = args.db
out = args.out_prefix

con = sqlite3.connect(db)
cur = con.cursor()

tables = [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
)]

with open(out + "_tables.txt", "w") as f:
    for t in tables:
        f.write(t + "\n")

print("tables:", tables)

target = None
for cand in ["ngram", "ngrams"]:
    if cand in tables:
        target = cand
        break

if target is None:
    raise SystemExit(f"no ngram/ngrams table found; tables={tables}")

schema = "\n".join(r[0] for r in cur.execute(
    "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (target,)
))

with open(out + "_schema.sql", "w") as f:
    f.write(schema + "\n")

summary = list(cur.execute(
    f"SELECT COUNT(*) AS rows, SUM(cnt) AS sum_cnt, MIN(len), MAX(len) FROM {target}"
))[0]

with open(out + "_summary.txt", "w") as f:
    f.write("|".join("" if x is None else str(x) for x in summary) + "\n")

by_len = list(cur.execute(
    f"SELECT len, COUNT(*) AS rows, SUM(cnt) AS sum_cnt FROM {target} GROUP BY len ORDER BY len"
))

with open(out + "_by_len.tsv", "w") as f:
    for row in by_len:
        f.write("\t".join(str(x) for x in row) + "\n")

top50 = list(cur.execute(
    f"SELECT ng, len, cnt FROM {target} ORDER BY cnt DESC, len DESC LIMIT 50"
))

with open(out + "_top50.tsv", "w") as f:
    for row in top50:
        f.write("\t".join(str(x) for x in row) + "\n")

dump_path = out + "_dump.tsv"
with open(dump_path, "w") as f:
    for row in cur.execute(f"SELECT ng, len, cnt FROM {target} ORDER BY ng"):
        f.write("\t".join(str(x) for x in row) + "\n")

con.close()

size = os.path.getsize(db)

h = hashlib.sha256()
with open(db, "rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
        h.update(chunk)

gz_size = len(gzip.compress(open(db, "rb").read(), compresslevel=9))
xz_size = len(lzma.compress(open(db, "rb").read(), preset=9 | lzma.PRESET_EXTREME))

with open(out + "_sizes.txt", "w") as f:
    f.write(f"db_bytes,{size}\n")
    f.write(f"gzip9_bytes,{gz_size}\n")
    f.write(f"xz9e_bytes,{xz_size}\n")
    f.write(f"sha256,{h.hexdigest()}\n")

print("table", target)
print("summary", summary)
print("wrote", out + "_*.txt")
