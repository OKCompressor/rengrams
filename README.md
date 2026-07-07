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

## enwik7 proof results

Input:

    enwik7.ids.npy

Produced by OKC IDStream from a canonical Redumb/Rare1-compatible ASCII ID stream.

### Short sweep

Parameters:

    n_min=4
    n_max=9
    min_freq=3

Results:

- rows: 766,561
- SUM(cnt): 8,464,889
- DB bytes: 59,453,440
- gzip -9 DB bytes: 20,860,436
- xz -9e DB bytes: 13,777,804
- wall time: 24.30s
- max RSS: 663,680 KB

### Long sweep

Parameters:

    n_min=3
    n_max=77
    min_freq=3

Results:

- rows: 1,561,352
- SUM(cnt): 16,917,643
- DB bytes: 239,591,424
- gzip -9 DB bytes: 51,747,948
- xz -9e DB bytes: 30,510,152
- wall time: 9:19.94
- max RSS: 3,265,900 KB

## Correctness check

A 100k-token prefix was counted with an independent Python Counter reference and with the Rengrams binary.

Both produced:

- rows: 12,806
- SUM(cnt): 147,394
- min len: 4
- max len: 9

The Rust binary stores n-grams as list-like strings, while the Python reference stores space-separated strings. Comparisons normalize n-gram serialization before equality checks.

## Comparator notes

Rengrams is adjacent to KenLM/SRILM and suffix-array dedup systems, but it is not the same task.

Rengrams produces deterministic repeated-symbolic-structure receipts over OKC integer streams for downstream reversible transforms.

It is not itself a restore encoding.

## Why this matters

Rengrams is built for repeated symbolic structure, not generic text decoration.

It scans OKC integer streams and emits deterministic SQLite receipts that can be inspected, hashed, compressed, and fed into downstream reversible macro/sideband encoders.

The public enwik7 proof shows two useful operating modes:

- short repeated-structure scout: n=4..9, min_freq=3, 24.30s wall time
- long-span structure sweep: n=3..77, min_freq=3, 9:19.94 wall time

This makes Rengrams useful as a corpus-structure microscope: fast enough for iteration, explicit enough for receipts, and long-range enough to expose repeated symbolic material that normal tokenizer views can leave tangled.

## Comparators

Rengrams is adjacent to several known tool families, but it is not identical to them.

- KenLM / SRILM: classic n-gram language-model build/count workflows.
- suffix-array / LCP dedup tools: repeated substring discovery and dataset deduplication.
- Python Counter: small-prefix correctness reference.
- SQLite insert baselines: storage/write-path comparison.

Current public proof compares against an independent Python Counter reference on a 100k-token prefix.

Full external comparator runs are TODO. Pull requests with receipts are welcome.

## Pull request rule

PRs are welcome if they preserve the receipts-first discipline.

A useful PR should include:

- exact command
- input description
- parameters
- output hashes
- timing receipt
- machine notes
- restore/verification story where applicable

No receipt, no claim.
