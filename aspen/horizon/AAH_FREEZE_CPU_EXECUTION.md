# Kolmogorov CPU execution addendum — 2026-10-04

Recorded before any Kolmogorov test data or learned training, and before any completed Kolmogorov calibration amplitude. No scoring, member counts, seeds, cases, thresholds, action formulas, precision or time step changes.

The initial sulaco layout (16 case workers, one CPU thread each, chunks64) is impractically slow. Synthetic-state measurements found about0.55seconds/step for384states on one thread; an alternative SciPy FFT implementation passed numerical reference and convergence checks but did not improve throughput sufficiently and is NOT adopted for scientific execution.

Use the unchanged Torch World D solver, with independent processes over single ensemble members and128workers. Each worker evaluates all6actions from the exact original member input; assembly restores the full6x256 paired calibration matrix before the unchanged2000-replicate bootstrap. All20cases are retained at every tested amplitude. Calibration still stops at the smallest passing amplitude. CPU threading is1 per worker.

Each member's input recreates the original256-member Gaussian array and slices the same index. No data-dependent sampling, early statistical stopping, or action selection is introduced. Shards are immutable and resumable; complete sources/provenance retained. The prior slow job is interrupted solely for scheduling/layout and its raw log retained. It had produced no completed case/amplitude scores at the change.

The SciPy prototype's synthetic one-time-unit reference error was5.304198058357111e-16 and dt-halving convergence ratio16.183044667245593. These are verification readings, not paper findings. Original Torch backend remains the scientific solver. Execution batch/profiling choices are authored by the executor, independently of scientific scores.
