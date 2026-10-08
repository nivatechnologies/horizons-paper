# Parallel capacity execution note

Todd requested that available CPUs and GPUs run independent work while keeping R3/R4 highest priority.

R3/R4 continues on its existing Spark queues without interruption. Stage21 descriptive inference runs on the available Baccus cards through the existing GPU lease and unchanged inference path. Stage18 D/C follows on those cards after descriptive inference and its publication, while R3/R4 can continue on the Sparks. Stage18 C data generation runs independently on sulaco using the unchanged frozen generator; training remains behind D. The combined Stage16 saved-output report has no compute dependency and publishes independently. Stage22 remains behind completion and publication of the entire current queue.

Concurrent descriptive dispatchers use a lock to prevent duplicate inference; CPU scoring and publication use a lock to protect the shared reading. The fail-loud gates remain in force. Criteria unchanged.

Launcher SHA-256s:

- `acd_stage21_ops_parallel_acd_deadline_stage21.py`: `5ff0cef495d1c66790643156df46b5a4fcd0c0aa175c704d1d8f2c781e8d9d33`
- `acd_stage21_ops_parallel_acd_deadline_supervisor.py`: `a525cd0fb539dfa6dcced2c168d4305bff827fee67651a342c04059402b7d13a`
- `acd_stage21_ops_parallel_acd_deadline_stage21_sulaco_score.py`: `db3dccec076409681c850929473294bade698b794813a50f4ff0ea1475e5f94c`
- `acd_stage21_ops_parallel_acd_deadline_stage18_data_parallel.py`: `ced059408855ac1d835aa22aaed1c654b432c065c7b4aa152492f54dfe042c32`
- `acd_stage21_ops_parallel_publish_stage16_aggregate.py`: `366d745fad292a6571e620f059a9fc78f87bbf96851cfd346bc6ca58e29d4a08`
