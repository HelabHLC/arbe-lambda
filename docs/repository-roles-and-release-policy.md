# Repository Roles and Release Policy

## Purpose of this repository

`HelabHLC/arbe-lambda` is the scientific and normative reference repository for ARBE λ*.

It contains or may contain:

- the formal definition of ARBE λ*_V2;
- deterministic reference implementations;
- conformance tests and reproducible notebooks;
- scientific documentation, citation guidance and licensing information;
- versioned, immutable release manifests for approved reference datasets.

It is not the application repository for ARBE.org, DesignFit Studio, AtlasFit, MixLock, Spectral Scissor or ARIA. Those application and platform concerns belong in `HelabHLC/designfit-studio`.

## Current status of `masterPKL-v1.0.1`

As audited on 2026-07-14, `masterPKL-v1.0.1` and `main` point to the same commit:

`d1176657728f310dab7838404c4cbbf79da1f65b`

Therefore, `masterPKL-v1.0.1` is currently a historical alias only. It does not represent a separate dataset release and must not be used as a production data source.

## Release rules

A future dataset release must be published only after all of the following are present:

1. an immutable Git tag or GitHub release;
2. a machine-readable manifest;
3. SHA-256 checksums for every released artifact;
4. explicit source, version and licence metadata;
5. a record-count and schema report;
6. confirmation that redistribution rights permit public release;
7. a statement distinguishing source data, derived data and ARBE-computed fields.

## Data publication boundary

Public releases may include only data classified as openly redistributable or ARBE-owned.

Data with unresolved, restrictive or third-party redistribution terms must not be committed to this public repository. This includes derived libraries when their source composition contains restricted records.

## Runtime boundary

`HelabHLC/designfit-studio` must not load pickle files directly in the browser or treat a branch name as a runtime dataset identity. Runtime datasets must be generated through checksum-locked ingestion into a non-executable format and referenced by manifest and content hash.

## Recommended treatment of `masterPKL-v1.0.1`

- keep the ref temporarily for historical continuity;
- do not advertise it as a validated dataset release;
- replace it with a proper immutable tag only after a release manifest and licence audit exist;
- do not delete it until downstream links and citations have been checked.
