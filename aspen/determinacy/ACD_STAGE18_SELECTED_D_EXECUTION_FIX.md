# Selected response-control derivative execution-path repair

Stage18 C is published at 0b637e71b78913454995b955f7f5fb2599338a24. The derivative launcher failed before GPU work: its import order selected acd_stage18_controller.py from the Stage19 L3 publication checkout, whose runs/stage18 log directory is absent. No derivative output was created and no score was computed. The first traceback is saved in runs/stage18/D_selected_launcher_failure.log.

Fix: import the publication helper first, then put the actual Stage18 scientific checkout first for controller and derivative-report imports; assert the controller module path and OUT directory. Gate dispatch on this pushed execution note. Record task return codes, block scoring on failure or absent complete.json, and commit the task log alongside its JSON. Frozen training, inference, derivative and scoring code and hashes remain unchanged; criteria unchanged.

Previous launcher SHA-256: c4f7209c803ce011d961798d3d78640ba5687e2d24fb26143e5a2f9cf6b17753

Corrected launcher SHA-256: 921517e03aa497404eb2fef84bd634b131d6a3d61340b7c2da08aa6ca432aba3
