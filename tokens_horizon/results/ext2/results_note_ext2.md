
## EXT2: learned-tokenizer kill test (WO 2026-09-25)

Generated from result files by `ext2/scripts/ext2_results_note.py`; NUMBERS.md section K3 holds the full tables. Freeze commit `9f12064` (ext2/EXT2_FREEZE.md, ext2_freeze.yaml), made before any training beyond a 300-step timing pilot. Gate report: ext2/EXT2_GATE.md. Kolmogorov Re 40, 64², the 1,000 KKE3 confirmation states; W = 27. Labels: bound / reference / learned / estimate. **T_pt is perfect next-token prediction (reference); it is not a bound.**

### Tokenizers (FSQ autoencoders, one seed each)

| Config | Levels | Codes/token | Bits/frame | Params enc / dec | Train time (min) | Best step | Held-out rel. RMS | Held-out within 0.1 | Code utilization | Level usage |
|---|---|---|---|---|---|---|---|---|---|---|
| L8-b10 | [8, 5, 5, 5] | 1000 | 637.8 | 4220292 / 4219905 | 80.2 | 30000 | 0.0461 | 0.948 | 1.0000 (1000) | 8/8 5/5 5/5 5/5 |
| L8-b12 | [7, 5, 5, 5, 5] | 4375 | 774.1 | 4222597 / 4222209 | 60.3 | 30000 | 0.0434 | 0.958 | 1.0000 (4375) | 7/7 5/5 5/5 5/5 5/5 |
| L8-b16 | [8, 8, 8, 5, 5, 5] | 64000 | 1021.8 | 4224902 / 4224513 | 77.9 | 30000 | 0.0356 | 0.986 | 0.9914 (63448) | 8/8 8/8 8/8 5/5 5/5 5/5 |
| L16-b10 | [8, 5, 5, 5] | 1000 | 2551.2 | 3481348 / 3480961 | 59.5 | 30000 | 0.0244 | 1.000 | 1.0000 (1000) | 8/8 5/5 5/5 5/5 |
| L16-b12 | [7, 5, 5, 5, 5] | 4375 | 3096.3 | 3483653 / 3483265 | 76.2 | 30000 | 0.0228 | 1.000 | 0.9833 (4302) | 7/7 5/5 5/5 5/5 5/5 |

Held-out = calibration held-out split (51200 states, 64 trajectories). Null reconstruction (calibration mean): relative RMS 0.999; zero field 1.049. Quantizer parameters: 0 (FSQ). Label: learned.

*Source: `results/ext2/k3_tokenizers.csv`*

### M1 reconstruction at t = 0 (confirmation states)

| Config | Rel. RMS | Median | Within 0.1 | Within 0.3 | Within 0.5 |
|---|---|---|---|---|---|
| L8-b10 | 0.0462 | 0.0312 | 0.950 | 1.000 | 1.000 |
| L8-b12 | 0.0436 | 0.0296 | 0.958 | 1.000 | 1.000 |
| L8-b16 | 0.0355 | 0.0244 | 0.986 | 1.000 | 1.000 |
| L16-b10 | 0.0245 | 0.0187 | 1.000 | 1.000 | 1.000 |
| L16-b12 | 0.0227 | 0.0175 | 1.000 | 1.000 | 1.000 |

*Source: `results/ext2/k3_recon.csv`*

### M2-M5 at Δ = 0.35 (primary score: future frames; secondary: from t = 0)

d = decode-and-integrate − T_pt, paired over trajectories. R1 = vocabulary binds (d ≥ 0.25, 95% > 0); R2 = does not bind (90% within ±0.10, or T_pt above DI).

| Config | ε | T_pt | DI | Persistence | d [95%] | Outlast | Reading (primary) | Reading (from t = 0) |
|---|---|---|---|---|---|---|---|---|
| L8-b10 | 0.1 | 14.053 | 1.318 | 0.061 | -12.735 [-13.342, -12.154] | 0.011 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b10 | 0.3 | 27.000 | 2.518 | 0.162 | -24.482 [-24.562, -24.398] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b10 | 0.5 | 27.000 | 3.187 | 0.364 | -23.813 [-23.905, -23.716] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b12 | 0.1 | 14.564 | 1.370 | 0.060 | -13.194 [-13.800, -12.606] | 0.006 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b12 | 0.3 | 27.000 | 2.594 | 0.162 | -24.406 [-24.485, -24.323] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b12 | 0.5 | 27.000 | 3.250 | 0.363 | -23.750 [-23.842, -23.655] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b16 | 0.1 | 17.305 | 1.515 | 0.061 | -15.790 [-16.382, -15.216] | 0.005 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b16 | 0.3 | 27.000 | 2.752 | 0.162 | -24.248 [-24.332, -24.157] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L8-b16 | 0.5 | 27.000 | 3.403 | 0.364 | -23.597 [-23.692, -23.499] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L16-b10 | 0.1 | 27.000 | 1.831 | 0.061 | -25.169 [-25.234, -25.101] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L16-b10 | 0.3 | 27.000 | 3.040 | 0.162 | -23.960 [-24.045, -23.868] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L16-b10 | 0.5 | 27.000 | 3.707 | 0.364 | -23.293 [-23.391, -23.190] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L16-b12 | 0.1 | 27.000 | 1.840 | 0.061 | -25.160 [-25.220, -25.096] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L16-b12 | 0.3 | 27.000 | 3.054 | 0.162 | -23.946 [-24.030, -23.858] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |
| L16-b12 | 0.5 | 27.000 | 3.732 | 0.364 | -23.268 [-23.360, -23.164] | 0.000 | R2 (T_pt above decode-and-integrate) | R2 (T_pt above decode-and-integrate) |

S(τ) for T_pt and DI, and all Δ, are in K3D. Labels: T_pt, DI, persistence reference; d estimate.

Secondary Δ (reading counts over configurations × ε): Δ 0.14 from_t0: R2 (T_pt above decode-and-integrate) 15; Δ 0.14 future: R2 (T_pt above decode-and-integrate) 15; Δ 0.7 from_t0: R2 (T_pt above decode-and-integrate) 15; Δ 0.7 future: R2 (T_pt above decode-and-integrate) 15.

*Source: `results/ext2/k3_paired.csv`*

### M6 beside k-means patch codebooks (Δ = 0.35, future frames; descriptive, no reading)

| Config (bits) | k-means (bits) | ε | FSQ T_pt | FSQ DI | k-means ceiling (bound) | k-means p₀ | k-means DI |
|---|---|---|---|---|---|---|---|
| L8-b10 (637.8) | 8x8 b10 (640) | 0.1 | 14.053 | 1.318 | 0.044 [0.0444, 0.0444] | 1.000 | 0.049 |
| L8-b10 (637.8) | 8x8 b10 (640) | 0.3 | 27.000 | 2.518 | 12.001 [11.4261, 12.5975] | 0.082 | 1.122 |
| L8-b12 (774.1) | 8x8 b12 (768) | 0.1 | 14.564 | 1.370 | 0.044 [0.0444, 0.0444] | 1.000 | 0.251 |
| L8-b12 (774.1) | 8x8 b12 (768) | 0.3 | 27.000 | 2.594 | 13.965 [13.3674, 14.5719] | 0.048 | 1.456 |
| L8-b16 (1021.8) | 8x8 b16 (1024) | 0.1 | 17.305 | 1.515 | 1.133 [1.0396, 1.2334] | 0.370 | 0.782 |
| L8-b16 (1021.8) | 8x8 b16 (1024) | 0.3 | 27.000 | 2.752 | 19.033 [18.4564, 19.6121] | 0.007 | 2.029 |
| L16-b10 (2551.2) | 16x16 b10 (2560) | 0.1 | 27.000 | 1.831 | 0.045 [0.0444, 0.0449] | 1.000 | 1.056 |
| L16-b10 (2551.2) | 16x16 b10 (2560) | 0.3 | 27.000 | 3.040 | 26.908 [26.8211, 26.9753] | 0.000 | 2.288 |
| L16-b12 (3096.3) | 16x16 b12 (3072) | 0.1 | 27.000 | 1.840 | 2.555 [2.3705, 2.7493] | 0.217 | 1.433 |
| L16-b12 (3096.3) | 16x16 b12 (3072) | 0.3 | 27.000 | 3.054 | 27.000 [27.0000, 27.0000] | 0.000 | 2.662 |

*Source: `results/ext2/k3_kmeans.csv`*

### Kill criterion: R1 at ε = 0.1 (Δ = 0.35, future frames)

| Config | Codes/token | Literal set | R1 | Reading | d [95%] | Reading from t = 0 |
|---|---|---|---|---|---|---|
| L8-b10 | 1000 | False | False | R2 (T_pt above decode-and-integrate) | -12.735 [-13.3424, -12.1540] | R2 (T_pt above decode-and-integrate) |
| L8-b12 | 4375 | True | False | R2 (T_pt above decode-and-integrate) | -13.194 [-13.7999, -12.6061] | R2 (T_pt above decode-and-integrate) |
| L8-b16 | 64000 | True | False | R2 (T_pt above decode-and-integrate) | -15.790 [-16.3822, -15.2161] | R2 (T_pt above decode-and-integrate) |
| L16-b10 | 1000 | False | False | R2 (T_pt above decode-and-integrate) | -25.169 [-25.2344, -25.1014] | R2 (T_pt above decode-and-integrate) |
| L16-b12 | 4375 | True | False | R2 (T_pt above decode-and-integrate) | -25.160 [-25.2200, -25.0964] | R2 (T_pt above decode-and-integrate) |

- literal (>= 1,024 codes per token): R1 in any member = **False** (members measured: 3/3).
- nominal (all five; b10 = FSQ ~2^10): R1 in any member = **False** (members measured: 5/5).

The WO's kill criterion fires if R1 fails at ε = 0.1 for every configuration with at least 2^10 codes per token. The gate found the eligible set unpinned (the b10 FSQ level set has 1,000 < 1,024 codes), so the executor does not issue the verdict; both sets are shown. **Both candidate sets give the same outcome: R1 fails for every member, so the WO's kill condition is met under either referent.** **Decision: Todd.**

*Source: `results/ext2/k3_kill.csv`*

