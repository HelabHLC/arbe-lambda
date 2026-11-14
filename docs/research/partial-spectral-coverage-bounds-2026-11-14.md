# Partial-coverage ARBE: mathematically guaranteed bounds (research protocol)

**Status:** Proposed research protocol, 2026-11-14. Not an amendment to ARBE Formal Specification 1.0, not a validated coating-ageing test, and not a Brent-conformant executable implementation. Full-range ARBE remains 380–730 nm.

## Assumptions and provenance
Measured spectral reflectance R(lambda) is dimensionless in [0,1]. The available instrument covers 400–700 nm; 380–400 nm and 700–730 nm are unmeasured. Both wavelengths and numerical quadrature/interpolation conventions for the observed bands must be recorded; boundaries are not treated as acquired outside that interval. Bounds below are conditional on exact observed-area integrals and physical 0..1 limits; measurement error, stray light, calibration and 10-nm quadrature error must be treated separately. Do not substitute invented endpoints, zeros, or extrapolated values for original measurements. A 400–700 nm-only index is not full-range ARBE.

Let a=380, b=730, O=[400,700], U=[380,400) union (700,730]. Denote the measured integral A=integral_O R(lambda) dlambda, and missing-area B=integral_U R(lambda) dlambda. Thus 0<=B<=50 nm.

## Bound for lambda*_V2
The unchanged formal definition gives lambda*_V2 = 380 nm + A + B. Therefore:
- lower = 380 nm + A;
- upper = 430 nm + A.
No statistical confidence is implied. Given two observations with A1 and A2, temporal V2 difference (NOT the ARBE descriptor Delta lambda*) belongs to [A2-A1-50, A2-A1+50] nm. A guaranteed increase requires A2-A1>50 nm, and a guaranteed decrease A2-A1<-50 nm, without additional constraints. At the endpoints equality allows zero change: the sign is not proven strict. These generic bounds can be tightened if additional measured constraints are justified.

## EE and ARBE Delta lambda* with missing bands
For total positive reflectance integral, lambda*_EE=(integral_380^730 lambda R(lambda) dlambda)/(A+B), and the formal descriptor Delta lambda*=lambda*_V2-lambda*_EE. Define M=integral_400^700 lambda R(lambda) dlambda. Unknown endpoint contributions B and C=integral_U lambda R(lambda) dlambda must come from *one and the same* admissible completion R_U in [0,1]. For any completion:
- lambda*_EE=(M+C)/(A+B);
- Delta lambda*=380+A+B-(M+C)/(A+B).

To obtain guaranteed and (up to discretization) sharp endpoint bounds for EE and Delta lambda*, optimize each expression over the same admissible R_U; do NOT subtract separately optimized V2 and EE bounds and call that sharp. If total area can be zero, the centroid and Delta lambda* are undefined for that completion and an interval cannot be reported without an additional positive-area assumption. Numerical optimization methods and discretization convergence must be published before reporting tight numeric intervals.

## Decisions and ageing interpretation
- Report guaranteed increase, guaranteed decrease, or indeterminate sign for each *temporal change* only where intervals allow the corresponding conclusion. A feasible zero difference must remain indeterminate; absence of proof does not prove stability.
- To claim a direction reversal over time, both adjacent temporal changes must have opposite *guaranteed* signs, with comparable sample identity and conditions.
- Recorded coating sample identity, exposure duration, reference controls, geometry, surface and colour, calibration and repeat measurements determine whether change can be interpreted as ageing. Two unrelated 'new'/'weathered' specimens are not paired temporal observations.
- Reflectance gaps do not establish corrosion, causality, predictive utility, a damage threshold, or superiority to the unweighted mean reflectance. V2 is an exact affine transform of the full-range unweighted mean; any incremental utility of the joint V2/EE/Delta display must be independently assessed.
- Report rounding, interpolation model, uncertainty and sample-specific missingness. The theoretical +/-50 nm temporal V2 uncertainty shown above is from *unobserved bandwidth*, not instrument uncertainty.

## Illustrative example (not study data)
If A1=100 nm and A2=160 nm, V2 intervals are [480,530] and [540,590] nm, yielding a guaranteed increase of 10..110 nm. Do not attribute these numbers to Fraunhofer, Leone or KLUM.

## External data status and proposed next validation
A coating-weathering study using 400–700 nm spectrophotometry has been discussed, but **no suitable Fraunhofer raw spectral time series have been acquired or assessed in this protocol**. Request full 380–730 nm spectra when available, or documented 400–700 nm raw values and repeat/uncertainty data for interval analysis. Independently evaluate Leone polymer spectra with documented grouping and provenance: unrelated specimens and multiple scans of the same sample are not longitudinal ageing by themselves.

## References
- ARBE definitions and sign: https://github.com/HelabHLC/arbe-lambda/blob/main/README.md
- Formal definition DOI: https://doi.org/10.5281/zenodo.18644381

This document defines a *conditional analysis protocol*, not an ARBE standard amendment or a validated industrial performance claim.
