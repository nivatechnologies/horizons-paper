# Stage18 execution handoff

## Execution handoff for unattended D/C continuation

Execution only; criteria unchanged. The legacy D coordinator would regenerate already committed C data after D publication. After all initial D outputs and scoring receipts are complete, the handoff watcher stops only that finished coordinator. No derivative or training worker is interrupted. The persistent supervisor publishes D and starts the unchanged C response controller using the verified committed data manifest. The watcher is itself resumed by the supervisor after a restart. The durable coordinator also skips generation when the committed manifest verifies.

The publication helper retains supplemental registries for the post hoc decision keys, preventing those keys from enlarging the core registry beyond the remote file-size limit. Every prior key value must still pass the publisher verification.

Execution file SHA-256s:

- `/mnt/niva-array/work/aspen-deadline-20261008/acd_stage18_safe_handoff.py`: `2efc50b1601f7cc6b3b66ba13d39027fed995741c1e64ccab0cc3c920d74f69b`
- `/mnt/niva-array/work/aspen-deadline-20261008/acd_deadline_supervisor.py`: `3abbde067e6c2dc5b86e5038fb70b50d596c1800e8560ca8ec7a22e592442dea`
- `/mnt/niva-array/work/aspen-deadline-20261008/acd_stage18_after_B.py`: `f52a2761fbcdaf35826a359fdc594838c7e343b0231f2b3cf6c9dc1d8ecbec33`
- `/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy/acd_guarded_publish.py`: `017e488b0d4dfda861989eeabc87e328d6ecdb24cdbbded14505d4e452eacc63`
