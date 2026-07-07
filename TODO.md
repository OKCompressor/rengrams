# Rengrams TODO

## P0

- Keep binary archive hash pinned.
- Keep extracted ELF hash pinned.
- Keep UPX hash separate and non-canonical.
- Keep generated DBs out of git.
- Keep 100k Python-reference comparator receipt.

## P1

- Add one-command reproduction script for:
  - 100k prefix
  - 1M prefix
  - enwik7 n4..9
  - enwik7 n3..77

- Add machine info receipt.
- Add release checksum manifest.

## P2 Comparator runs

Rengrams should be compared against adjacent tools, not falsely framed as the same task.

Candidate comparators:

- Python Counter on small prefixes
- SQLite insert baseline
- KenLM / SRILM for classic n-gram workflows
- suffix-array / LCP dedup tools for repeated-substring discovery

Required for comparator PRs:

- exact commands
- same input stream where possible
- same n range / threshold where meaningful
- timing
- memory
- output summary
- hashes

## P3 Downstream

- Sentinel RFC
- macro candidate export
- sideband accounting
- restore-bundle proof
- Rust/API cleanup if needed

## Not claims

Rengrams is not a compressor by itself.

Rengrams is not a universal replacement for language-model n-gram toolkits.

Rengrams is a repeated-symbolic-structure receipt generator for OKC integer streams.
