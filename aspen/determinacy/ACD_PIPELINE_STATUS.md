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

Lane 3 | Stage16 CNN-noF-seed1 confirmation scoring | 2e673e8504003473b0a1edfc91133b3d454a0056 | 2026-10-08T05:07:36.449137+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 3 | Stage16 CNN-F-seed2 confirmation scoring | 94496c818f86d0d6502e832282efdb36ae3e5de5 | 2026-10-08T05:08:06.483480+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 3 | Stage16 CNN-noF-seed2 confirmation scoring | 5ff999879ebfc294c47da8df8538e84bfc8a2088 | 2026-10-08T05:08:35.483696+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 3 | Stage16 CNN-F-seed3 confirmation scoring | 679d2c18b8e2f248c5f3b9eab96ea86f4f72985d | 2026-10-08T05:09:04.960802+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 3 | Stage16 CNN-noF-seed3 confirmation scoring | 99802e69db1d5c1054fc051bdcd5d94c73d3e6c0 | 2026-10-08T05:09:33.159928+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 3 | Stage16 CNN-F-seed4 confirmation scoring | 9b229f99f44ed3c5fbdbb44a8c7f087c9d2dafbc | 2026-10-08T05:10:00.622048+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 3 | Stage16 CNN-noF-seed4 confirmation scoring | 20ab23d99e87bc7a54df09095f2c504edbff7aec | 2026-10-08T05:10:28.154954+00:00 | Run and selected checkpoint recorded; registry PASS, prior values unchanged; fresh L3 inference remains to run.

Lane 2 | Stage19 L3 inference adapter | a13fbae832034f39916d6d161b90ef9ea48bddd1 | 2026-10-08T05:13:18.689267+00:00 | Committed seed checkpoint adapter prepared; unchanged Part2 inference; launch only after push, outcomes and scoring withheld until all inference complete.

Lane 2 | Stage19 L3 startup synchronization | 30688447bcbf4202e13f6e62c502834aac4ad20f | 2026-10-08T05:16:03.830040+00:00 | Fresh inference active; initial concurrent FETCH_HEAD gate failures recorded, stable-ref and serialized-gate fix prepared; retry failed launches after active lanes, no outcome access or scoring.

Lane 2 | Stage18 A scored information diagnostics | af17da68d5efc5968c146c896b11e8a00854df33 | 2026-10-08T05:30:48.935350+00:00 | Four arms reported; registry PASS and prior values unchanged. B publication next; D and C remain queued.

Lane 2 | Stage18 B scored context pipelines | 626e43cd10f19490265ac509336528e2903dd4f2 | 2026-10-08T05:31:39.960112+00:00 | All retained-model estimator pipelines reported; registry PASS, prior values unchanged. D and C remain queued; matched Stage16 CNN-F/E0 follow-up remains.

Lane 2 | Stage19 Part3b Freeze D | 473372ac252acb64c934b139e138cba20f49e1ab | 2026-10-08T06:09:33.224698+00:00 | Inventory found no Stage18 fresh pipeline output; freeze and adapters complete, registry PASS. Inference queued behind L3 and existing jobs; B1/B2/B3 scoring follows hashed outputs.

Lane 2 | Stage19 Freeze D implementation amendment | b5642c583382bcbbdddd0dc343605a82b8c9252b | 2026-10-08T06:12:19.506199+00:00 | First-panel CNN-noF decisions sourced from their separate receipt; criteria unchanged; no fresh repair inference yet. Queued scorer and receipt publisher prepared.

Stage20 | A | 5af2c1b919ec612363404e848a2d64bec1426b4a | 2026-10-08T06:34:27.622347+00:00 | All-lead saved-output scoring pushed; B and C Spark inference remain.

Stage20 | B/C setup | 5b6fe6d | 2026-10-08T06:45:35.024643+00:00 | B physics-floor inference running on Spark1; C awaits Spark2 connectivity, retrying after sixty seconds.

Stage20 | transfer/scoring setup | 1606c37 | 2026-10-08T06:48:58.904919+00:00 | B runs on Spark1; controller retries Spark2 every sixty seconds and will score/publish B and C independently.

Stage20 | completion controller | 8493336 | 2026-10-08T06:49:22.330542+00:00 | Spark2 connectivity restored; C deployment starts. B running on Spark1; independent result publication queued.

Stage20 | Spark2 recovery | 52bb56a | 2026-10-08T06:52:57.698971+00:00 | B and C inference both running; C first fixed pipeline has written hashed original-panel outputs.

Stage20 | reporting setup | 340432f | 2026-10-08T06:54:24.397647+00:00 | Both Spark jobs active; registry PASS; B and C scoring and separate publication remain queued.

Stage21 | contract | 1f90ea740a0c5312d44364e7da04160fb83091ef | 2026-10-08T07:05:19Z | No realized-outcome access; Freeze E and emulator/scoring work remain.

Stage21 | timing | e5c0c2f3d6cb3d1fa2118ad8bb3d94ca8b5b240b | 2026-10-08T07:07:08Z | No realized-outcome access; Freeze E and emulator/scoring work remain.

Stage21 | climatology | 7a1c69513f0fd4b28d5cc9cf65c75fcfa3c68914 | 2026-10-08T07:08:11Z | No realized-outcome access; Freeze E and emulator/scoring work remain.

Stage21 | panel | 9055ef80b4bdec70507f8e253fa454e3229328b8 | 2026-10-08T07:47:28Z | No realized-outcome access; Freeze E and emulator/scoring work remain.

Stage21 | execution and blind-step registry | 9bddc054bd22b744383ac98ec448bfa2a0a5f7c4 | 2026-10-08T07:55:41Z | See Stage21 receipts; prior queues remain unchanged.

Stage21 | Freeze E | 61e040638970cec3198351a8e7dca81256e84b03 | 2026-10-08T07:55:55Z | See Stage21 receipts; prior queues remain unchanged.

Stage19 | Freeze D amendment | 0edb9b4daf9520e62bf2285773d89046dc0427ef | 2026-10-08T08:02:18Z | No governed output exists; seven-pattern criterion unchanged; all-eight criterion and uniform/seven diagnostics added.

Stage21 | Freeze E amendment | b30b16787781a3278016d02b1ff10680070b85f2 | 2026-10-08T08:02:45Z | No governed output exists; seven-pattern criterion unchanged; all-eight criterion and uniform/seven diagnostics added.

Stage20 | B uniform amendment | f0787ebf37ba02fc47aec2f1f4a30bfcaa044c99 | 2026-10-08T08:09:07Z | Extension output inventory empty; queued behind both B and C; no fresh-panel or outcome access.

Stage21 | Todd execution reorder | 3593f1f599694181da4140b1d023bb9a4478e260 | 2026-10-08T08:31:16Z | G1/G2 CPU now; after L3/Part3b, R1/R2 on 170HX, R3/R4 together on freed Spark, descriptive arms last; Stage18 D/C after Stage21 inference. All criteria unchanged.

Stage21 | Todd execution reorder | 3b9a7cf29d5862ffe67ec906b3d457eda609d813 | 2026-10-08T08:35:25Z | G1/G2 CPU now; after L3/Part3b, R1/R2 on 170HX, R3/R4 together on freed Spark, descriptive arms last; Stage18 D/C after Stage21 inference. All criteria unchanged.

Stage21 | reference | 83f427684de7aaff7712d22128f34dbf42cf18ee | 2026-10-08T08:36:09Z | See Stage21 receipts; prior queues remain unchanged.
Stage20 | B failure | pending | 2026-10-08T09:38:25Z | subprocess.CalledProcessError: Command '['/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python', '/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy/acd_stage20_readability.py', '--outputs', '/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/runs/stage20/B', '--inputs', '/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/runs/stage18/confirmation_inputs', '--receipt', '/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy/receipts/acd_stage20_B.json', '--reading', '/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy/ACD_STAGE20_READING.md', '--figures', '/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy/figures']' returned non-zero exit status 1.

Stage20 | B | fc36eb73f599f2c186c6db3d3c1038b87cc64764 | 2026-10-08T10:09:59Z | Scored and pushed; other Stage20 part continues independently.

Stage19 | L3 scoring | 3f52f5313a14ed0f67615fb306319aa2dffbda32 | 2026-10-08T10:52:22Z | Frozen L3a/L3b and every seed reported; registry PASS; prior values unchanged; CPU handoff omission repaired.

Pipeline | stage18-execution | e5ec4cc0a715f77f18d1920a985a2e867f69f838 | 2026-10-08T11:06:51Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage19-unattended-operations | f7f17d36c52d61ee41815774c50cea9d99fd6bb3 | 2026-10-08T11:09:12Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage19-continuation-completion | 000a8628c83c5683933e02b94581f9843ac96ccb | 2026-10-08T11:11:28Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage19-scoring-resume | 3e592108bbbbe9ceb45cb9b133a57feaf934d9f4 | 2026-10-08T11:12:56Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-R12_inference | 34814262c823577a63528bf7b7ab710f7fe0e9f9 | 2026-10-08T17:43:55Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-R12 | befe01b89bb6738384afee79fe99e87b00b0deb7 | 2026-10-08T17:45:04Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage20-C | 913da4880d27f5616b97865fc3f3943ea54b3283 | 2026-10-08T17:58:01Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage19-part3b | 465a772eb0ba7f1b7d1b3ef14e05fd83be0de27a | 2026-10-08T21:12:08Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage20-uniform | bc9b69972b173a22f2d68e2dd1ed8facb3fb2477 | 2026-10-08T21:14:11Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage19-continuation-recovery | 297fd0a5ce360df71070d350cc067fd122bee766 | 2026-10-08T21:14:56Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-R12-execution-correction | 24245c50e5c42acde884a1b69da98d2fcf54bed8 | 2026-10-08T21:30:52Z | CORRECTION: original R12 FAILED at import: ModuleNotFoundError: No module named numba. Earlier completion line remains unchanged. Offline dependency repaired; criteria unchanged; recovery results pending.

Pipeline | stage20-B-step-times | 29cb70c7cec9c912d2c1d9b6077be5ea6e5085fb | 2026-10-08T21:34:55Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-Spark-log-gate | b0b2ae9830e7eb598402a326d568db8295b3e662 | 2026-10-08T21:37:45Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-execution-handoff | 06a90ae056b735decb4aa4b5b52db642af04f2c6 | 2026-10-08T21:40:40Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-multispark-execution | d614d83f5501a637b51dba6e1c841fb179fe1ed3 | 2026-10-08T23:06:24Z | Execution amendment: matched E1 seed pairs split across three authorized local GB10 GPUs; criteria unchanged. R34 waits for successful R12 publication.

Pipeline | stage21-R12_recovery_inference-recovery | a51648f4fc0df5fc2fc130666d3ddca4b3ed647b | 2026-10-08T23:08:37Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-R12-recovery | 81942ab802872a70c097fb6b21bdb46d8b46b6a3 | 2026-10-08T23:10:22Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage21-execution-host-followup | 36b6d0ca1c19b7faf9e466f39da9a4898a130896 | 2026-10-08T23:12:54Z | Criteria unchanged; matched R34 seeds use three GB10 GPUs, subsequent CPU scoring uses sulaco. Reused outputs retain actual process exit-status evidence.

Pipeline | stage21-multispark-resume | 10ca46f51809c4e8c32c054a28311f2dadf42199 | 2026-10-08T23:17:23Z | Three GB10 queues run without preemption; controller resumes attach to live queues and retain actual exit-code records. Criteria unchanged.

Pipeline | stage21-parallel-capacity | 6673addb71f3f92bc42dc3a17cd5c6a699724924 | 2026-10-08T23:42:14Z | R34 retains priority on Sparks; independent descriptive GPU inference and sulaco CPU preparation run in parallel; Stage16 aggregate publishes without GPU wait. Criteria unchanged.

Pipeline | stage16-combined | 6d7655a9ba2c4347684a2c86d301a8f9e3670ce2 | 2026-10-08T23:43:11Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage18-C-data-execution | abe6fc13e0681682a1fe9d1561f2af339c42134c | 2026-10-08T23:44:49Z | CPU preparation first attempt FAILED before generation: missing staged freeze marker. Existing marker copied, frozen hash guards PASS; retry on sulaco. Criteria unchanged.

Pipeline | stage18-C-float64-execution | 34bd9d2391fd088d4862572ac6aabc663c57e22a | 2026-10-08T23:45:37Z | Stage18 C validation generation FAILED on mixed dtype; launcher promotes inputs to float64 at unchanged physics boundary, with existing data reused. Criteria unchanged.

Pipeline | stage18-C-data | 278d85d831d46c011b9e74d5e67d093d9e75ac56 | 2026-10-08T23:48:17Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.

Pipeline | stage18-D-free-card-execution | cfc2205e20d7b78320bc92c801cf6cb7a48efdfa | 2026-10-09T02:07:11Z | Use released Baccus card for frozen CNN-noF derivatives alongside remaining Stage21 inference; wait for occupied cards, never preempt. Criteria unchanged.

Pipeline | stage21-descriptive_inference | 3f3bc9fb529589c2503e61ed0e6901b1e648cd74 | 2026-10-09T02:12:23Z | Completed, registry PASS, every prior value unchanged; downstream controllers continue.
