"""Operational guard tests, without hosts, jobs, samples or realized outcomes."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import acd_stage22_watchdog as w

class RecoveryGuards(unittest.TestCase):
    def test_computing_worker_is_never_stale(self):
        previous=dict(workers=[dict(pid=7,cpu_ticks=10)])
        current=dict(workers=[dict(pid=7,cpu_ticks=11)],utc=5000,last_output_mtime=0)
        self.assertFalse(w.stale_decision(previous,current,1200))

    def test_integrity_failure_blocks_every_launch(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);out=root/'runs/stage22';out.mkdir(parents=True)
            (root/'receipts').mkdir();(root/'receipts/acd_stage22_freeze_f.json').write_text(json.dumps(dict(N=1000)))
            (out/'FAILED.json').write_text(json.dumps(dict(reason='hash mismatch')))
            probe=dict(utc=1,workers=[],cases_done=1000,status='blind_sampling_complete')
            response=type('Result',(),dict(returncode=0,stdout=json.dumps(probe),stderr=''))()
            with patch.object(w,'ROOT',root),patch.object(w,'OUT',out),patch.object(w,'remote',return_value=response),patch.object(w,'publication') as publish,patch.object(w,'start_cpu') as cpu,patch.object(w,'start_local') as gpu:
                state=w.tick({})
                self.assertEqual(state['phase'],'FAILED');cpu.assert_not_called();gpu.assert_not_called();publish.assert_called_once_with('failure')

    def test_dead_cpu_controller_resumes_only_after_passed_gate(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);out=root/'runs/stage22';out.mkdir(parents=True)
            (root/'receipts').mkdir();(root/'receipts/acd_stage22_freeze_f.json').write_text(json.dumps(dict(N=1000)))
            probe=dict(utc=1,workers=[],cases_done=5,status='timing_passed',timing=dict(passed=True),failed_logs={},last_output_mtime=1)
            response=type('Result',(),dict(returncode=0,stdout=json.dumps(probe),stderr=''))()
            with patch.object(w,'ROOT',root),patch.object(w,'OUT',out),patch.object(w,'remote',return_value=response),patch.object(w,'start_cpu') as cpu,patch.object(w,'start_local') as gpu:
                state=w.tick({});cpu.assert_called_once_with('aspen-stage22-resume','resume');gpu.assert_not_called();self.assertEqual(state['cpu_restarts'],1)

if __name__=='__main__':unittest.main()
