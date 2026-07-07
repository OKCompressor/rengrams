# OKC Rengrams

Rengrams is a scalable n-gram counting stage for OKCompressor integer ID streams.

It emits deterministic SQLite analysis artifacts for repeated sequence structure.

Rengrams is not, by itself, a lossless restore encoding of the original stream. It is an analysis/statistics source for downstream reversible encoder stages such as Sentinel.

## Input

NumPy integer ID stream:

    enwik7.ids.npy

Produced by OKC IDStream from a canonical ASCII ID stream.

## Output

SQLite database:

    ngram(ng TEXT PRIMARY KEY, len INTEGER, cnt INTEGER)

## Proof target

- deterministic command
- row count
- SUM(cnt)
- DB size
- gzip/xz DB size
- sha256
- wall time
- max RSS

## Public boundary

This repository publishes Rengrams benchmark/proof artifacts and, where available, Linux research binaries.

It does not publish private Sentinel macro strategy, proprietary encoder details, or final OKC compressor internals.
