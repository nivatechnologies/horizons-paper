# Analysis pipeline status

- Lane 1 | step 1 | 78f147c | 2026-10-07T19:48:13.155270+00:00 | Freeze B pushed; reference scoring and learned inference remain.
- Lane 3 | step 1 | e1aa6bd | 2026-10-07T19:48:13.155270+00:00 | Training freeze pushed; copy inputs to Spark 2, then eight runs and scoring remain.
- Recovery handoff | freeze addendum and inference controller | 160d02a | 2026-10-07T19:54:49.353020+00:00 | Pushed; Stage 19 scoring and inference running, Stage 16 startup in progress.
- Lane 4 | step 1 | 00d812b | 2026-10-07T19:54:49.353020+00:00 | Stage 15 status pushed with this update; A and B implementation ready, C and D remain.
- Lane 1 | step 2 | 0b1666f | 2026-10-07T19:57:00.957114+00:00 | Reference readings complete; C1–C4 and M1–M2 pass, M3 crossover holds; learned readings remain.
- Lane 3 | step 1 startup | 9549092 | 2026-10-07T20:00:14.152862+00:00 | Both Spark queues running; all replication evaluations and per-run readings remain.
