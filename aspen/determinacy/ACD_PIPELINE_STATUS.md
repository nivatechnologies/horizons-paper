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
- Lane 4 | step 2A correction | 843a116 / a87e48a | 2026-10-07T20:10:19.478771+00:00 | Exact coverage count corrected; earlier registry values preserved in superseded precheck receipt.
- Lane 4 | step 2B | 71d092c | 2026-10-07T20:10:19.478771+00:00 | Control and matching paper figures rendered; C final results integration remains.
- Lane 4 | step 2C | 8be3ca9 / deb52eb / 764b76d | 2026-10-07T20:13:58.160227+00:00 | Known-forcing panel complete: all case outputs hashed, one exclusion after retry; Stage 15 A–D complete.
- Lane 3 | evaluation addendum | db1bf7e / 9692b19 | 2026-10-07T20:14:50.751701+00:00 | Matched coverage adapter uses corrected ranking; persistent observer isolates failures. Training unchanged and continuing.
- Registry maintenance | serialization | 80a295e | 2026-10-07T20:17:15.228535+00:00 | Compact JSON serialization preserves all values and provenance; registry passes. GPU lanes remain running.
- Lane 2 | Stage18 freeze | 2ee06a7 | 2026-10-07T20:28:45.022350+00:00 | Independently reviewed freeze pushed; A/B waits for Stage19 learned readings push.
- Lane 3 | retained baseline reports and observer | 315a99c / 804a3eb / 4c6e485 | 2026-10-07T20:28:45.022350+00:00 | Baselines and registry pushed; eight new runs continue, per-run reporting enabled.
- Lane 2 | steps 1–2 | fa9969c | 2026-10-07T20:31:55.135854+00:00 | All three fresh-panel inference manifests and learned readings pushed; L1/L2 pass; L3 waits for Stage16. Stage18 waiter unblocked.
- Lane 1 | Part3a Step0 | 8d6ab56 | 2026-10-07T20:54:44.689580+00:00 | Known-forcing implementation byte comparison passes; Freeze C and scoring remain.

Lane 1 | Stage 19 Part 3a Freeze C | b2289a5 | 2026-10-07T21:01:28.568733+00:00 | Implementation comparison passed; timing, case-list commitment and scoring remain.

Lane 1 | Stage 19 Part 3a variance timing | 5674349 | 2026-10-07T21:02:08.173671+00:00 | Projection 236.49535055737942 seconds; all 200 main instances frozen; ratios and scoring remain.

Lane 1 | Stage 19 Part 3a scoring | 8a8370a | 2026-10-07T21:08:54.792400+00:00 | K1-K4 and V1-V2 PASS; paired endpoint -0.40536315536315537 interval [-0.5720000000000001, -0.268]; registry 355653 to 368351 prior values unchanged; Part 3b repairs remain deferred.

Lane 1 | Stage 19 Freeze B L3 addendum | 0e8451c | 2026-10-07T21:34:36.942882+00:00 | Confirmation inference already partial for CNN-F seed1 and seed3; no new-seed fresh evaluation found. L3 scoring awaits every new Stage16 run commit; training and queues untouched.

Lane 1 | Stage 19 L3 execution-gate amendment | c02be50 | 2026-10-07T21:40:14.968987+00:00 | Per-run fresh inference permitted after selected checkpoint commit without preempting Stage16 or Stage18; outcome access and L3 scoring await every new run commit and complete inference; criteria unchanged.

Lane 3 | Stage16 CNN-F-seed1 confirmation scoring | ad6437e4da9e2092b67887685d0ba1df95b82987 | 2026-10-08T05:07:07.956992+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.
