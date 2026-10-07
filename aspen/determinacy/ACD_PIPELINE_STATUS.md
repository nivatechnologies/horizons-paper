# Analysis pipeline status

- Lane 1 | step 1 | 78f147c | 2026-10-07T19:48:13.155270+00:00 | Freeze B pushed; reference scoring and learned inference remain.
- Lane 3 | step 1 | e1aa6bd | 2026-10-07T19:48:13.155270+00:00 | Training freeze pushed; copy inputs to Spark 2, then eight runs and scoring remain.
- Recovery handoff | freeze addendum and inference controller | 160d02a | 2026-10-07T19:54:49.353020+00:00 | Pushed; Stage 19 scoring and inference running, Stage 16 startup in progress.
- Lane 4 | step 1 | 00d812b | 2026-10-07T19:54:49.353020+00:00 | Stage 15 status pushed with this update; A and B implementation ready, C and D remain.
- Lane 1 | step 2 | 0b1666f | 2026-10-07T19:57:00.957114+00:00 | Reference readings complete; C1–C4 and M1–M2 pass, M3 crossover holds; learned readings remain.
- Lane 3 | step 1 startup | 9549092 | 2026-10-07T20:00:14.152862+00:00 | Both Spark queues running; all replication evaluations and per-run readings remain.
- Lane 2 | scoring diagnostic addendum | 4613502 | 2026-10-07T20:01:34.643511+00:00 | Additive ties and per-case audit records pushed before learned scoring; inference continues.
- Lane 4 | step 4 | 272bf99 / 3079bf1 | 2026-10-07T20:01:34.643511+00:00 | Response weight control decision scoring and registry complete; Stage 15 and Stage 17 remain running.
- Lane 4 | step 2A | e217097 / 612bc0f | 2026-10-07T20:02:26.790625+00:00 | Forecast matching receipt and ranking definition complete; B presentation, C sampling and D sensitivity remain. Stage 17 B/D unblocked.
- Lane 4 | step 2D | d627109 / 6c3b1fd | 2026-10-07T20:06:33.750461+00:00 | Linearized variance complete; both median ratios first leave the specified range at lead 4 LT. C sampling and corrected A remain.
- Lane 4 | step 3 | 4d2af62 / 36da5c8 | 2026-10-07T20:08:02.354847+00:00 | Stage 17 event scores and transfer diagnostics complete; earlier A/C/E values unchanged. Stage 15C and presentation correction remain.
