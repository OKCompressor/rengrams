#!/usr/bin/env python3
import argparse
import ast
import json
import re
import sqlite3

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--limit", type=int, default=256)
ap.add_argument("--macro-base", type=int, default=1000000000)
ap.add_argument("--min-len", type=int, default=4)
ap.add_argument("--max-len", type=int, default=9)
args = ap.parse_args()

def parse_ng(s):
    s = str(s).strip()
    if s.startswith("[") and s.endswith("]"):
        return [int(x) for x in ast.literal_eval(s)]
    return [int(x) for x in re.findall(r"-?\d+", s)]

con = sqlite3.connect(args.db)
cur = con.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
table = "ngram" if "ngram" in tables else "ngrams"

rows = list(cur.execute(
    f"""
    SELECT ng, len, cnt
    FROM {table}
    WHERE len >= ? AND len <= ?
    ORDER BY cnt DESC, len DESC, ng ASC
    LIMIT ?
    """,
    (args.min_len, args.max_len, args.limit),
))

macros = []
for i, (ng, ln, cnt) in enumerate(rows):
    seq = parse_ng(ng)
    macros.append({
        "id": i,
        "seq": seq,
        "len": int(ln),
        "cnt": int(cnt)
    })

out = {
    "macro_base": args.macro_base,
    "source": args.db,
    "selection": {
        "limit": args.limit,
        "min_len": args.min_len,
        "max_len": args.max_len,
        "order": "cnt DESC, len DESC, ng ASC"
    },
    "macros": macros
}

with open(args.out, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("GRAMMAR_OK", args.out, "macros", len(macros))
