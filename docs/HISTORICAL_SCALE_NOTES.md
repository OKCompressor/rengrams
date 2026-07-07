# Historical Rengrams Scale Notes

These are historical OKCompressor v3.7 / Bench workspace Rengrams notes.

They are useful for context and roadmap planning, but the current public proof pack should cite only receipts that are present in this repository.

## Current public proof in this repo

enwik7, n=4..9, min_freq=3:

- rows: 766,561
- SUM(cnt): 8,464,889
- DB bytes: 59,453,440
- gzip -9 DB bytes: 20,860,436
- xz -9e DB bytes: 13,777,804
- wall time: 24.30s
- max RSS: 663,680 KB

enwik7, n=3..77, min_freq=3:

- rows: 1,561,352
- SUM(cnt): 16,917,643
- DB bytes: 239,591,424
- gzip -9 DB bytes: 51,747,948
- xz -9e DB bytes: 30,510,152
- wall time: 9:19.94
- max RSS: 3,265,900 KB

## Historical v3.7 scale notes

Older workspace notes include larger-scale Rengrams runs:

enwik8, n=3..77, min_freq=3:

- rows: about 16.28M
- DB size: about 2.65 GB
- gzip -9 DB: about 611 MB
- wall time: about 6,724s
- max RSS: about 27.5 GB

enwik9 chunked run, n=3..77, min_freq=3:

- 419 shards
- merged master rows: about 81.62M
- SUM(cnt): about 2.89B
- merged DB size: about 23.4 GB
- gzip -9 DB: about 3.16 GB
- shard generation: about 16h
- merge: about 2h17m

## Caveat

These historical notes should not be treated as current public-release claims unless their receipts, hashes, commands, and machine notes are copied into this repository.

Current public claims should reference `results/` in this repo.

## FlashText / trie replacer relation

FlashText is useful related work for the replacement side of the pipeline: it builds a trie of known keywords, scans input in one pass, prefers longest matches, and replaces known terms efficiently.

Rengrams addresses the earlier discovery problem over OKC integer streams: which repeated symbolic sequences should become candidates?

Sentinel Lite then demonstrates the reversible replacement/restoration contract over ID streams.

So the public bridge is:

    Rengrams discovers candidates.
    Sentinel Lite replaces candidates.
    Restore verifies exact recovery.
