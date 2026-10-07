# Release manifest — preparation only

No public archive has been published. Release requires the listed records and a portable copy of the evaluator dependencies. Scoring-only realized outcomes must remain separate from model input histories/forcings. Hidden true states are not inventoried or opened.

Scientific freeze commit: 1f38be370718825196ecf4ff1e5e82138faf44c7. Code addendum: ACD_FREEZE_CODE.md.

Betting settings and implementation: ACD_FREEZE.md, sources/WO_v2.3.md §10, acd_stats.py. The receipt retains file hashes and byte sizes. The independent unit is the case; reliability-bin CP intervals and paired bootstraps are descriptive.

AFD-derived files cannot be released as part of this preparation without separate permission/provenance review. Machine paths require sanitization; possible credential literals require inspection/redaction; files or grouped datasets over the archive size threshold need a suitable storage plan. No checkpoint is copied or uploaded.

| Role | Files | Bytes | Group over 100 MB |
|---|---|---|---|
| CNN-20k checkpoint | 1 | 4003061 | False |
| CNN-F selected checkpoint | 1 | 4008277 | False |
| CPU environment | 1 | 397 | False |
| Tables 2–4 and primary comparison aggregate receipts | 1 | 4264042 | False |
| case provenance and draw policy | 1 | 2928 | False |
| case-level paired endpoint scoring | 1 | 7693 | False |
| confidence / calibration scoring | 1 | 8220 | False |
| cross-model decision records | 1 | 47614 | False |
| decision scoring and CPU step check | 1 | 13981 | False |
| embedded ACD_IDS seed role contract | 1 | 26669 | False |
| external-cost evaluator entry point | 1 | 3982 | False |
| frozen climatological null states | 1 | 2621952 | False |
| frozen scientific protocol | 1 | 26669 | False |
| full precision registry | 1 | 8040096 | False |
| full-grid step-check receipt | 1 | 329785 | False |
| hashed realized case-level outcomes | 200 | 170400 | False |
| inherited evaluator dependency; extract standalone contract/kernel for release | 2 | 6427 | False |
| learned per-case costs; reproduction records | 400 | 298759677 | True |
| null probabilities and decision margin sd | 1 | 2379496 | False |
| observation contract and intervention patterns | 1 | 4557 | False |
| observation/intervention/statistics contract | 1 | 83496 | False |
| observed input panel, outcomes stored separately | 200 | 758000 | False |
| per-case blind-order and hash receipt | 200 | 230773 | False |
| per-case forecast / fit receipt | 200 | 850082 | False |
| post hoc learned-model provenance and readings | 1 | 2594526 | False |
| posterior per-case costs, draws and retained draw ordering | 200 | 390587080 | True |
| pre-confirmation code hash addendum | 1 | 6313 | False |
| question definitions | 1 | 3183 | False |
| question summaries / same-lead scoring | 1 | 15240 | False |
| registry and numeric checker | 1 | 2459 | False |
| registry presentation | 1 | 5533409 | False |
| registry regeneration | 1 | 26287 | False |
| supplied noise-free draw histories H and own forcing F | 200 | 932480022 | True |
| v2.3 betting bounds: frozen grid and settings | 1 | 6102 | False |

| Item | Bytes | SHA-256 | Release flags |
|---|---|---|---|
| ACD_FREEZE.md | 26669 | ff04820b81450163db9d815c64f0c9fa5a8192e5b3db8925cc24711e6609a21a | none detected |
| ACD_FREEZE_CODE.md | 6313 | ba3cd480e05f3351dbcbea10a86eb078fe8ac77973f4267c5eb55436fc53bbcc | none detected |
| sources/WO_v2.3.md | 83496 | 77d72c48c8168a3c63dbd45b14a24f9d1c986591f0578a8fa70055f2a3b1f875 | none detected |
| ACD_FREEZE.md | 26669 | ff04820b81450163db9d815c64f0c9fa5a8192e5b3db8925cc24711e6609a21a | none detected |
| acd_protocol.py | 4557 | 160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000 | machine paths: sanitize before release |
| acd_questions.py | 3183 | 5c932b427874ae9108824a528a4ae35b2b5d957c2376a9d71b02369fc5abb698 | none detected |
| acd_stats.py | 6102 | 1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a | none detected |
| acd_evaluate.py | 3982 | f81a042c2c587ca21764b054571ab7698645912fa110feedc1956ad221468b80 | none detected |
| acd_stage13_analysis.py | 13981 | ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b | none detected |
| acd_stage6_analysis.py | 15240 | c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8 | none detected |
| acd_stage9_cnn_metrics.py | 8220 | 471e2363945e25a1f8ee0920c3955bc1a3c41d899de5a164b4369e2299fe859d | none detected |
| acd_stage9_receipts.py | 7693 | 966a21bc72ef4b3c8ede354a1246fb5d01c4b3df440ef19902ec032a688b456c | none detected |
| requirements-cpu.lock | 397 | 795d5b658d49885467763be4a4eab2cf04f4c0a754c5acf8aaa3bf3d7daf9544 | none detected |
| numbers_acd.json | 8040096 | f6d876856f12c461f9ca0c67018d828c79c4d60d1dd98c9a1c5bbe1e46d7b99f | none detected |
| NUMBERS_ACD.md | 5533409 | 91dbe79e90c296492e3e3746181064e0d3328da8be2ca34590940d505353f5e0 | none detected |
| acd_numbers.py | 26287 | 3f345636fb1f69d03ab52623acb58e838b690215f31c0ac55474344b6ae85440 | none detected |
| check_acd.py | 2459 | 7a414f89f4ecfa4264c278bec132165601ae308c33e596067e14031f991efdb1 | none detected |
| receipts/acd_stage2.json | 4264042 | 16b009b1bb3038866f7336a9217a9182b1ae5df27961cab91583760886fbcce1 | none detected |
| receipts/acd_stage2_closeout.json | 2928 | e29197e6be0699aca984a52a0f985c4f04b340743294ee7543c92e7adba9c5d5 | machine paths: sanitize before release |
| receipts/acd_stage9.json | 2594526 | 681011c62c37e265d3e07610802c2d61948a94e42f2657c16389bd2c30215c49 | machine paths: sanitize before release |
| receipts/acd_stage13_decisions.json | 47614 | ebe7e10f13c5d3d7789cbe7d1233b31ef430e5bef1340a49b185cb0e28710b14 | none detected |
| receipts/acd_stage13_dt.json | 329785 | 8421b2179acfadd090f4354a95d260651808b1717b79c01ec2798ba7073ee554 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_000.json | 4256 | 406d7f878eabf7f6ac2bbcfe7878f6b8be8c6fec7958a0942af0b88030706a00 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_000.jsonl | 1145 | c6a97708df1a4f99ef41ab11c3249b77ef7aa487a1da721723b6bd7882d2be6e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_000.npz | 3790 | c5816fefc6749a073fbecf3732247f24f588b0e389d54ccdd5330c70e5db2793 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_000.npz | 905681 | 9f1c8495881652545682b2ff3249648e290243a33e95d2e9b6792722fe354466 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_000.npz | 852 | f1877de46c63805d40a9a189251ff965965d67e27a1da6193a0ab0ee2bd1d185 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/000.npz | 1744844 | e018181044314b3d0c735336498380daf0b7d4947531a020e6dcf25f7b117c81 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/000.npz | 296613 | 3468d88533873717d7f9eb9c41f7275bbc60924a48785fb17d246b025ea786d9 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/000.npz | 296733 | a67aaa3d5a0923f81a84f0becb25664bba875f33a31d438ba8e586f4c4de0932 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_001.json | 4247 | 60336a32f410462062b87de69a0346d47f177c368b0f48c9f2b5ce352b947738 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_001.jsonl | 1145 | 814620c4c96681eb3692c21d771310f7130158e0f8b9718b57c31304fe9ef96a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_001.npz | 3790 | 1f1b500283258225baec140623cb77331a819d97ac54f0e1c3c5dfbd93cb590e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_001.npz | 2726993 | 68bc97b80f156174a3f37314095095e32f64f3b28e0b30c86705d277da795a9f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_001.npz | 852 | 70bfa486afda5bee64efe0182b71594981a4e891d6c7edebc720324cee142ddc | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/001.npz | 6818362 | 3f0bd81268f4e313f1882c32f8aa98b3dbaded24fc87021daed01d868fb5862a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/001.npz | 1080023 | 3c419126b0261f735900d69b050d30dd0d4bc89ab7d002dee2f29b934ee5f200 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/001.npz | 1079565 | c170879116de92ff35ebafa2075c23498118db56a32aa3d025e4d9de4244a938 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_002.json | 4254 | 9d5406a15e68b0e706866d7734bfe5b04b534d5e88a05931a8d9a4dfea35f74e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_002.jsonl | 1148 | 9f313f5e9e4c0fa6ca085b386d770f99806196d6d1ab68477d11f79a6b4631e6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_002.npz | 3790 | 642fe6c985bdd9e10ee9ee6291bfd2b055ea199c528efe0a7aada6bb9a01f73a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_002.npz | 2726993 | 3b2e520e37297aa1031b149470dd99ea0d8aab9934d524c2ab6c6822c873fd81 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_002.npz | 852 | 2d04aaff8e303cf8a5fe0a6a2e846c304dcb163cf5661fcca8051e16737bd9e7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/002.npz | 6817995 | e9571aea4f0df94da7e5452df0e3dab071816b0520b2872f262aa3cdfcfb6ad0 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/002.npz | 1082098 | d3f2ceb3c47359d85df6ba6d7944cbc7237e9cb3dc2b3ba727a9f41c0a9893e2 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/002.npz | 1083102 | ba8c1b7b09cc27fbe483c487c8b1c537ddd6267bfb75b4ee3f4309801efb6a75 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_003.json | 4250 | 751dadc8fd41f4f63159f8dc9d1fd5f3c9fd89d8bda3f24ee60c70725499f7ae | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_003.jsonl | 1148 | 197be167f008b4f2b4fc047f80dd813c23a5f45cf9e501421d077a2b2459436e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_003.npz | 3790 | e8a1130e4a04100d34487d83a73141141ca9ba961c1f70cb8e3d0920d14891f2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_003.npz | 905681 | 9b7ea29133b81da30cf460c20d77b0d9efd23950e23878aa04cafa7c13cd3075 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_003.npz | 852 | a6878d2fc72d64b339dc7e21f52cb6490925f6c0ab85b58acc2cc26b84e9a5b4 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/003.npz | 1745197 | 037752157333ac552d92b319195aff2a0d4f216193563892ab1e52a1ff9e56f6 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/003.npz | 294875 | 69d4dfb02856dcc1fbdd6490810b21ef8d943eecd1b0b3a8e0fe8387073c03ad | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/003.npz | 295225 | 5dd2ad73396bc3db8350ac083832f8b0ec5658dbb568efc6c007dfa7298457e3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_004.json | 4250 | e1d2230719ec17d000f405f517591d3b4f02cc788e87eee2b7a1cac2a22687b6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_004.jsonl | 1148 | 8e4d080219c62c0c800fa0411fb76838b52ead1bdb8ffa91dfb87ae254e3457a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_004.npz | 3790 | 59cc9a9da95b556c422fcbe1932354e4a617ca39d75ba6e2be9c5a13c6b43e24 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_004.npz | 905681 | 03fdfe289aa48a0bd7672b9ebe03ecc00c1774bdd5c655165d3c078d1d8f80a2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_004.npz | 852 | c84fb2180157cd61341abf022ec3df1b9c8ef76291749784de42a9c5c3ca6ac7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/004.npz | 1747437 | 027becf2b0d6eed04326b1d2e2bb91c197fc776705e8ff13f004ca1bc153e45c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/004.npz | 296525 | 9f4a2db20755f018542071c299bd749a6cf0c8a03127b6d58a395e0dd06849e2 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/004.npz | 297164 | f243cd2bafa2d7488bfda5690d12db369fbd1f0a65e61ccb88df2c4c8835e078 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_005.json | 4262 | ad7e7341330ede39020dd6d5607b7afda6d1bd7cbb5518809d43a690b4e51306 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_005.jsonl | 1147 | 09cc3577174b6b3b33e4c8b7a01656d37d533d464d451c8f9812042f0ee04dc6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_005.npz | 3790 | e87355bc9c738de97234f6f25fd7f0c510df5aa2cd6b6189708db15e2516b5d6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_005.npz | 2726993 | aae9784f271668b37b67f5d3906d2e3f39a4f9e46c44a0b42991d1e0d6e36497 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_005.npz | 852 | cc1280a990b359f236ff5a049f591cf82c4e7884c11fc73a1ea963e763d92373 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/005.npz | 6822191 | a6bce3face1c9d0eb2bfe28a8d48538e69a5ee975030dbb739c48720eda9ea14 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/005.npz | 1075121 | 924868cd2049133bf6bcda4d538a3f456427a26c21bd2098303dfb729b722137 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/005.npz | 1074272 | d69083663ec63fd886738b9cda4a95c1ad4e605098245044c1cbdeddeadb54e5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_006.json | 4246 | 3b96d55579e10061f8d6cd6e86f74b9972fe349548cb9afa9b3a2582f4fa6c2a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_006.jsonl | 1148 | dddfa95c010801c9243679733f7721bfbc50ee0a3ea019a7d096a0a71e2231b3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_006.npz | 3790 | 2fe304a828eb6ac28876d3c316d36eeab2c8a81220bc7e42358f58cba57838a5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_006.npz | 905681 | e52769669e87c90afe529b880dff6f5c519b76f3a0eabf3f057726bf1734652f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_006.npz | 852 | 98873b5b80b0c7de418d1859d384c0bbb1bf66c7d3f581ec681ccd9f54dca210 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/006.npz | 1746826 | 626e74547ce4c30066da6c899ef8201df02e24b154727645f1467d9ea6bbbf4c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/006.npz | 299716 | 1a854e1bce27fada669a47294ab1c5df20100feee68c80bafc2f1a48889d1bfc | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/006.npz | 299743 | 4c1008a152d7e1c0d2ce7a2864089089935a850e033651813d73d2d8287772c3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_007.json | 4246 | e1e134778566af33a9d650ade406c21ec8942dfa3833b711fa4766a3124603e2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_007.jsonl | 1148 | 1a2b2b1e27f184e13d28bf78afab750cba64de775752aad1562af71cdd67afc9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_007.npz | 3790 | e54f946572b926f4bf918d16747040ed47d0b693edf4c8467b2a7f77a3967c9e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_007.npz | 2726993 | 2d8ce48531330c31029fb537cc6f361d5267e6ec15adf34d94f78091663f9b8b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_007.npz | 852 | 2c90a80ad83a6dd7b9301d7f44d5290091436b406e842d21ee2d2b9af118cb46 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/007.npz | 6817662 | d3f309011f392a7585e9ad7a8858e55fe9ff0c981955002d14abb9c79dcd3a1a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/007.npz | 1078376 | 861b763c94652a7681e9ea92daedb79766e015773b30cd9f2935c016f61e568c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/007.npz | 1080137 | 2f06373c1d79062c8f67148230d656cb33012bcff61c84bd6e804ba72c46c2d1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_008.json | 4248 | 8f30ca1d301f0717b3a1813fd0eb413982aafcaab4a153c1c490fd43e6bb9885 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_008.jsonl | 1147 | fcdfbf2330e0b25770d3b190f2434c44c76ad3c5c979e4883221ce304bcb3a64 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_008.npz | 3790 | 7cf5c6a2981342ec1596cde1e11a3bad9bca60b9fc9f4789047866dfa42ab5ff | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_008.npz | 2726993 | 57dfaa8ac132aef4e926d0f897f374c9a41d804c9690104da66e31de3592e314 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_008.npz | 852 | 2dabc8b2aac73d03bc9244d1d732b8d751dc8f5b3c839816577d2cd364a60f1f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/008.npz | 6825654 | a79fc75900493a431f5e24339084230535189a97099c28cb0dc298e68d0bfba3 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/008.npz | 1073857 | 581f17e34329bdb1741d3f001932610a0c8749a39f37fb295315f9566342f275 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/008.npz | 1074637 | f16eb77c5371f586170cc402a2754dcdf80c3d61a605cbbfe6661011a2d7061b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_009.json | 4246 | 4d6a610d5326f85243bd038811d169077eebd489fb242ae95b580432741a7d58 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_009.jsonl | 1146 | 70acccac29c228793225278bfd37f7b14f19067d9a1bf706b7c9f58d6a15c3bb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_009.npz | 3790 | 40388f27e97ec0862e5c13e00f8057e784f5093139267a984951a6a6f0031540 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_009.npz | 905681 | 06f6879df91934bebf97434cb13dc90be468b53d97ed9b6ce77733aa99fee7c9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_009.npz | 852 | 8614d5c440d8c7de7afd3261dc75b0fcafefe5a3b036086fe554e448870028b3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/009.npz | 1744080 | 15d0867d1b066f4df6ec9d5f34f0a22c9936392b6644ac7c4acd17868c889ad4 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/009.npz | 295679 | f5b90dd50c0460cb3ec60affe5ff3cec6d655c8815de74a7ac4a28b98849f43f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/009.npz | 295832 | 357f64be75075983e8c64b3df800ce140f0773d16844ba9a5ffd9581cb680cad | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_010.json | 4259 | 3476dab4a192bcd277df77a2087d1efab309c9c0aa06d1876ae264aa37ab8548 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_010.jsonl | 1153 | f0b59029603679f152ecf2e1fe32f76cb385886abf740c509e2fd6fdd690936e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_010.npz | 3790 | 16b571e58536e78b4e7b125b853c8cd262878726d0c955ae9e664f41c24986d2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_010.npz | 2726993 | 45c69e1624827e6354fed53c37a850c6147af2cd7e66f55bb259f72331214396 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_010.npz | 852 | 066e57fa3e4a468b6325d61893a8a278ce68f4b48db89605f7c78d8fa9921805 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/010.npz | 6819299 | 715a3d64bc22296704a830fa32a732ab68fff5727d24f1da6e104612e7f15596 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/010.npz | 1081602 | ad2d87fa68277df37c6f3453e7cd4f04cb6762230a0ef0709f44ae7cf5181c6e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/010.npz | 1082591 | 972b2cff86e791e7bc68c2a5ec8dfa2bee9abd6666d01be62c3b677fa57b9a8d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_011.json | 4249 | e5fd5036dd0713bcd2bd24d14791ab23ba1707cb17af3cb2127519da07f27465 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_011.jsonl | 1149 | c5c7ad220df814fc78ada2a602135336a0cad1613b9dfa953ddb23938b660837 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_011.npz | 3790 | 113dc0fc3b7fafe57da561ff9231457e19f33561077a4e21e6b3405fd1693913 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_011.npz | 905681 | 93f963e19ec6fa3095f6ccfa658792042d95c57290ba48fdc0c6f5a70ff61c5c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_011.npz | 852 | c80612c3abb2e4610bd90d1e04f986aff69bb9cb996e2716ec522930e6bfad84 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/011.npz | 1745713 | 773cedfefa9606290da9c3ca306c2bff1b9279fb81c526042a2213410b7c07c7 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/011.npz | 295071 | 00628262e24e578c3a3de85d34743a5e6ebbf00f4f936b442dacf7cf77af87ad | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/011.npz | 295243 | ab6990178348c4c5100a11eef33bcae157e5cb5ce58a15f530c5addbd4b886f2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_012.json | 4257 | 2997f55a22670a2e9b9c8eda41daaeaf449c1ee8ee1cf47fe6d15f4cdf100ec7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_012.jsonl | 1151 | a609f471c0904d3dd57de5a1e194a7902d93ee2eb0f03ccfbce530ab80f984c8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_012.npz | 3790 | 8349d855274b7e2d3b0f2cd2b26227f79e3cf0ea9bf4ab6c1b5becc509876a3b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_012.npz | 905681 | 4a88c29dbacd0befbef28974157462d4d8d1fbee7411ddd910bd4c7646dbef29 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_012.npz | 852 | 86d212d90ea006dc9fee5cceb759f42a1079baff4b64e26a7d6bfc3451f245f0 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/012.npz | 1748535 | 2d4fdada5d52070b1460de24fdf0cb204b040aa3cfc7a20a9dca844b1df65ce4 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/012.npz | 297127 | b3d34af1b804ceffb16d3ddf0b415592235a5b09bc2315ce647452b2a074c82a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/012.npz | 297162 | b42300b5c589df4ee3648cf690bea5c5e05ddaff739d9a646d83578615101d32 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_013.json | 4249 | 3cb9c45ac16db0834b29c7aae43bdec06c99f9f8429add7c125a3067890b504b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_013.jsonl | 1152 | e691d4220338eb6a7dc5c19a6c2bfdfdc3ca874d400ee61a92dafb2a873798b8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_013.npz | 3790 | 79345dc28de581acad7fe739305838fe14d3c7e8a357406337257a52a53adc13 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_013.npz | 2726993 | 0019b96986bc96b59963b8523fb749d76ea7957d4efe43109c258c0fad054f7d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_013.npz | 852 | a6860c73b3635e821fb284bfb5b3846b05cc9b9678a956b0e2d36c59ca4a1c57 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/013.npz | 6820674 | ea6c70296dbf856eaaec3a31319949f0462738654f4cf8abef47470accad717f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/013.npz | 1080539 | 684b33084c6ae3e2fa969685abf308865fae54dbe4b5fdace1c783bc84dcf51a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/013.npz | 1080283 | 65029c2c9f9c0d60cfbcd37d51455340ff29f1b4376246fcc6ad818ea07b883e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_014.json | 4248 | 67917722b1918e99ddfee5bf9158a22220478029e69916494a7d05e50d7ee998 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_014.jsonl | 1151 | 69c8da3ff4b04017316a4c3bb3e07a820d19bc27f5de9932b18a9b58161be6a2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_014.npz | 3790 | 4cd8c6147f1c0a37257bcd170bc138cfe5a6731accfd16f79962fc3f5a8f979a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_014.npz | 2726993 | f1a92c0c752b30ef6be63279d201901e44732a7509315d4d709d16972d341b67 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_014.npz | 852 | 94fce1def0da8205f0dfd5a2ef7adb46fb11efcf9dd47696f15f1529b2ae1bd9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/014.npz | 6812075 | 9eec7fd25104f72c2cc1f8303f0e94cadb20d0981975b5c2872950f15261526d | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/014.npz | 1077182 | 13f8c18837143485ea1acf6a136fc36126433724893cde341d7ba4132655da91 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/014.npz | 1077155 | 14b645e11d195056c9bf8190d26d002914dacb797e38fc84f6d5735ccb740065 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_015.json | 4250 | dc5f3a0b5df6470ae4d8231c22c1a297cd37415b37cf50c7d49e3bae0493b5de | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_015.jsonl | 1152 | 5f4b328b75aa4f3d27c9ed38c9d14fa30094e5cc74c7b64d1b620b677be2398d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_015.npz | 3790 | d284e7472a1f9d26637c068b93c96d835c42061c2eb057f511d19a98653efe25 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_015.npz | 2726993 | 1eb8d7256bc2e05e86fefa902258e50d6c28da6f8747b08c59f083c0ceb8dfb2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_015.npz | 852 | caa35c48b6261fc977f31b12f2c55f35ba6df0c48eda1f17ac6f336093b630c7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/015.npz | 6804814 | b28cb7d2b151f2d5a10f6cbbcc106dedaeeefd20c4b5d5a91476c03ff61581ac | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/015.npz | 1077344 | 16ec21f6391c5f2b38c2f0909d72749d28d2b3ecbc941c27554993d379d8a4ac | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/015.npz | 1078671 | 4bc18f0a488399a9669fe82fde38239338bde5d3f1696e8e00bbefefdfdfd73e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_016.json | 4253 | fdbdbb49f2ea814e9eea98017f8ea113f20aea4fac90a002048beaadb6c6feee | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_016.jsonl | 1152 | d9520dca811150bcadbef807e7a039f3f8e28b8b53d9d87b3e26193185b57a69 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_016.npz | 3790 | d90999ed73332fd317e808e021b44eb275de11f2f053cbf5199b1e1b1081f62f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_016.npz | 2726993 | 8e9abe5a160a0d3873aaf8929ea127f2fce30bfcca8970b2109e93c6b782f64d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_016.npz | 852 | 15405266b3c079b666a38a259babb2c7f04e456bf01671584d65ad06294b9cd0 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/016.npz | 6834546 | d25c7f5d294e51e8d3953dd93af117035ec2bfe7e07778822accc749efff587a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/016.npz | 1079251 | 71be28e46fe0c8c2c524740a08b1d02bc0e2eb9c44e9a6ebd04db7259c25f034 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/016.npz | 1079875 | 4338e0f36aeaa057dc095b122c872d9262c2faa8d8b7b196bd546d2c7dc8bacf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_017.json | 4256 | 3a6453c3c56bd73af800ef98555246c540a2a7a0101321e4c9c8d7a8d30773e3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_017.jsonl | 1153 | 44ba75258b1287a8f3a29f8d65dd3bd417ab55c50273ecf660c872436231c194 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_017.npz | 3790 | 582fda0fb4a02bf6d82b3207f38539bac3508083d889d329c119ff85a692e3dd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_017.npz | 905681 | b94cfd64c3b1c40a5ee8e0961ade4b1350788ce290a28cda1abc90d8b9a123a6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_017.npz | 852 | 15f5845f4efc232e04d5e7f8446133619c66221474e5c35bbbda0efb6d9815d8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/017.npz | 1747203 | 4561d48a55f2b146dceb2d9d4bf3821858f6442125d58d8af35cabadd79ef26c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/017.npz | 296115 | 2ce079d5236ea3971c486d8cfac47cf1c528d52a2a5aeda613c785176404d7dc | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/017.npz | 296433 | e7d91e5d5158c2306690c08e5d88440171c661ae34519f0a7a79c0d2665aa6ee | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_018.json | 4248 | bb2b9336bac40834237642bffacc72abc92c8b3ee147480fb20e0e202741dd02 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_018.jsonl | 1152 | a43e5e33fce0394b75a16376ba25cffa957615d82ecc4751dc2a2af5ea9dece5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_018.npz | 3790 | 3ef9f118efd3c6cfeba515edd39798e93cc38ef31415b88ed5bbd50243a79e1e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_018.npz | 2726993 | 43da03884546c485a8ff0882b57599a4cf6c202f71017f68d733a5fe68123d55 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_018.npz | 852 | cbb99b0a9720420065076588dfce5884fa840fdd557264f8db886216e7a9fceb | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/018.npz | 6815930 | f80f03ada82f388936d44f4705ab8dfdb4810e58d2da2c3389a4cf5146636feb | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/018.npz | 1081782 | f78257e8e05129c10c6c1f3b42f7d6215e84b8cb6c1fec687e35e184875d9ed2 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/018.npz | 1082071 | 60b7fe756318bf345d5af3f16cef23838f4381df06ab91b7dd1395167ed9efc2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_019.json | 4240 | 2fa4c1920bee84cb80a549b12160ccb1557d867c868dad7c6d42a4553d42319e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_019.jsonl | 1153 | 01a9adae6d7500fc0a30ab2649f7700d4a977dc9b501c147f6e928b8614348a2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_019.npz | 3790 | faf255ba0b1f5110f112d8450afcf70b806502b8ec26ec1e8dc6ff4286466312 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_019.npz | 905681 | 9b4e37ac600faf6f4e468cd8d002676b4d0f8bacf54218f1b8f1e6b9b7afb964 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_019.npz | 852 | 3b13cd2e587df174f338dc4842f80b21321d258da28171bf8aa28ef20c4f1ee2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/019.npz | 1748539 | 5e6e98d9dccd5165c2dfb0b7ccdd59515e3a5614c418221ff5c38281d5581e6f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/019.npz | 296005 | 5d1fd9c15f5093da7d199290a3beef6816b3818352d84532acb9736e5194da2b | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/019.npz | 296261 | 6c8ef505bc13fc71139c75ad174c3503eeb3759274b983d48ffa907b1c9b11b0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_020.json | 4252 | 0b2f027dab71397d0eb6268710b25a4e19ce34f54adc7587d7143a9265e0ce0d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_020.jsonl | 1149 | 81a9b6343f30481e3dbf109da29d23710f80a4dc247f7d37dd077c99e056a057 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_020.npz | 3790 | 6ebc02e68659d2f31564e4203a6ed7fc672aaa45c2191a2ffcc6535cde152aaf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_020.npz | 905681 | 9ff4d20a8d8156bb1ee54a0ad6b0cb20e6ed33d7380f4354cb77e9c6716056f8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_020.npz | 852 | b53a5a72b1b946700c18488dd486a22bacb5c0ed85be9325ec2f78228c068b30 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/020.npz | 1745953 | 4745e306c75f43ab65f58d204acc53f4c319288292766b2fbef5ca765f0d7739 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/020.npz | 298467 | 3a0eecbb347d8bbe17dfe48cec059f00e67d45ecdf3b840a4f8a04d65012e7b3 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/020.npz | 298859 | bcf9f79dbe214d25ba215e7446726dbda251a7582bb3687e554b9569890561a8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_021.json | 4245 | 707d8a4dcffb99edec893d43076c977f69496d479e981e381a931175730794db | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_021.jsonl | 1150 | 0e48c3f76fe9343d213663eb29729bd9050d1927ecee7779be350e68482d4fb0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_021.npz | 3790 | 8e25a661ea09b70c310148f93779343d3252757cdce0dede0644b15b381cd30e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_021.npz | 2726993 | db3e47d84051234aaeb25a2adcc379dbdcc452bc4b8e92ec4d598d1ff493e5a2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_021.npz | 852 | 4b11d6ac5b6dcc8452d2197c64f89f71ec84b20f062d26737026d3098247387f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/021.npz | 6817346 | 0da16bca3059aa37935f3e8ab908543aa6ff50b6e66521b23beaba5602eccede | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/021.npz | 1074824 | aba5d851f2416fa4e73313cb4e02fbcf73b08a2d330bbcf6655e8099cfde39dc | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/021.npz | 1074870 | ff6bda1ae8720e93a1e8b3507717fbfa3e6ca7826c5712361d540fc90ede9ffb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_022.json | 4248 | be512abf4118bd5c7f1d6e4fb9bda16add76846f7741640be20b4f1efc96fbc8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_022.jsonl | 1150 | 1424bf8f693b152d11995028945d182fbde182975eac720200acaac4cc8faa5e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_022.npz | 3790 | 487010e8bd8ae72730116b061ecee5e87d292e264e7e2eb9fd5aaca3f883cad5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_022.npz | 905681 | 7812a8fbceb86fc34006efd1ffa1330037b4ae6694720f25e8057aae08d96a81 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_022.npz | 852 | 7e4e0527e5a285b23fd1194f3a36eeab7c903cc50af40ce0f42df4ac9e4d6532 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/022.npz | 1749314 | 5d8ca2af5ff87401ba71e9f1c5f393c29981228645bb48da8adba0268d100597 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/022.npz | 295628 | 65837a668666f65ba0f323de5ce4f3eac147287cd7216b7ec517072f410c9d3c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/022.npz | 295593 | 28d7f101963e4f6acfc87d87577f14d1d967c3aa65012f1a6fa3f35f4e2b2bf7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_023.json | 4256 | 9af69c3a1fa29decf075ca6a57df43234af5e07f11a0b8770ecfbaab0d6ec4c7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_023.jsonl | 1153 | ede8405873d41ba79d6760a143d85b33191f7686e0bc406c5024c18f0bd3d9c8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_023.npz | 3790 | e9fa755a12c382d20a41af522cebab44fdc227b6ffbc52779a7c5779989b9fcf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_023.npz | 2726993 | 6b438382c262f2ef9065534cf20f7548f9cfecf585ae4caafe8f88b7316cb32a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_023.npz | 852 | cee1096bace4a735ccff559e61da04e851058b6e10bab6bf68e12608d036ecc4 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/023.npz | 6813059 | fc0a8dd7902df4fed240d4726553ef04970ba7bba4b08949c8ae11111824c908 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/023.npz | 1079103 | de94808e16e967070074051637b7f36686b4d067180a11ceb62645b886606e0f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/023.npz | 1078443 | 9d289001f552e4316836c5309987563af9d17bf93dfa3e50abbf1e0e619d93fb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_024.json | 4253 | f3c83204128cad0d93dbe56876d3c830986188caf0143affd6d68c4c565cbd53 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_024.jsonl | 1151 | 6f570df129b2c9433936dc9dee5ba0c735d926a107c55f44a9e2be75d1479822 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_024.npz | 3790 | d5e4af3231f21b7eb501f3195455c7881ac7877d2eff3cb53033880fcd36710e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_024.npz | 2726993 | 78d8c3ecd5aa139770821bc93aaabd2567b67db9f4295963a0007bc5f322ad73 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_024.npz | 852 | 59b9e17dbd2b79383303f3f496eb6e9b329755da8a8741b5a7a9bd8c3e4adaab | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/024.npz | 6806352 | 85d0fb335d433b823048640718099acbc9ae096af553d9b8c6ab233f1e7d733c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/024.npz | 1081195 | 83a3d0f5db26da7549bb1f4af4cc4d0d8650b259feb4ffe6c427dc35c837a3e5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/024.npz | 1082347 | f1c2db4a08f187191e395392ef8b1eaee4a4daa5cf05cd95ba9ad11239272347 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_025.json | 4257 | cfe718a195b25bd078c7b1bea8ad32414479616dbef47f08091fd36aca48d202 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_025.jsonl | 1151 | fd8e43b477a5cc37405a7ed1f1f7cdd23373b941aec3b4f84fe1ea265a029384 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_025.npz | 3790 | bf884d0ad44d6db41bb9ec063f58448f9a06689922752b6fb82c66162a661e01 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_025.npz | 905681 | b576d68affd8274f87fcc8bd35a2f80dcda862deb7ff943ae7d5fe3a9e32937f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_025.npz | 852 | 89f4fb9010d38f394c59f59cc8ff7287e29036ce024f1ce40c380a056a16ed6e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/025.npz | 1747264 | a3008f626eb7063a4c90c20ce71f0600bf0a35889c735005194efe1e8f35971c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/025.npz | 295609 | a33fc6ad6d70e944192e431d56bedb5c22ed32ab05a9af47491171f12d475589 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/025.npz | 295611 | d2b0672fb8547735a83decba6ca4ae41b2323534559599131d59a47634ddff4e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_026.json | 4246 | 6a777a376545870a7876c1513f44a803356b75cba89e8d47b54fb1b99505f571 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_026.jsonl | 1153 | 3df228c9e1c4a5cbf0a57829bb626891a02eb212ce2490dcde1d1637ef0d17fd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_026.npz | 3790 | 5c6a926bf2186a017dd33fcfac8fd5379e82aead14ca7446a6395ecd5949fef3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_026.npz | 2726993 | 2b3818dcda8833fa2759be623772b9c58773bf3e78cafaaeae11280d1978528f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_026.npz | 852 | 5b2ae85d8e476e78e29ea2b51e5f827dfb8f172e853a378aaaae6ef520c0c917 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/026.npz | 6817070 | 5fab0de16acd1e5e38781ab9a587f572c9f34e303cb5229cec791b58d736a249 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/026.npz | 1077603 | 1ee9d27dd874774931bb20571d22458cce20fb284b532e82cd63592c72a7c800 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/026.npz | 1076653 | d660110096cb16e20f4ea6bba1e3c77ab2dd18efdbea7fd90ef9d43367cd8e8f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_027.json | 4255 | 5c9b9bf34726d54a6f84fac189be1dbb2eb2fc7cdf9a7c0b8199e3da8d9cb329 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_027.jsonl | 1152 | 71261877d8ea2f8cfd37ccbe5f657f75a122b85820593bf2bf2ff4c338524dd4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_027.npz | 3790 | c5cfe4123d414cd86dcf6f9008996a9bb41c7bcb2b61b7b16504fa63acc751b0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_027.npz | 2726993 | 7d2e298eb6553b8a0d607bceb3670467bb01b8c873c45aa4a70d81384c69da5f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_027.npz | 852 | 98626a47148fd1804c08c11f4c5439f4940cb08230f61437a9cf2fd873773625 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/027.npz | 6824597 | ce54e95e870d6cb38c9665111e444fea5ecacaa73eebb4ff4c3f515ad6e1d1e8 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/027.npz | 1076250 | 9aadc92c51df7312b76de4492471b851fcce06bbe9c69a85f147f6b060e25a79 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/027.npz | 1075571 | 4c838f2e3e1a75b93832e93365262086a32e7fa55c7f799746a74e34f8cbb75c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_028.json | 4246 | f5923d3fb5de8d057fb1df9432d2c4b2cf902b7e55f1de1727f9442e5955eaa0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_028.jsonl | 1153 | 27e8e0de8d98fef983fac15f24445c136f66066164dec1f1ff4dd4949a2d99fc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_028.npz | 3790 | edf0155f7c947d5a6b3195efe2fbadf866a2363a0a6c0f4e47ba5710755c687c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_028.npz | 905681 | a2fdfd4e032e4938035c6e6f068cebaace3c06ce4adb0ea6cf0fb5368abff9df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_028.npz | 852 | 89e36b5dba6e77bfbc0c9628e0c4a67df984429b8f26978145d14f6a9b76cb60 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/028.npz | 1746191 | c25e3672bcd943f97c7efd47b5ffcbc0dc35703a5134ccdb1eef7bd6ba6ae8b6 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/028.npz | 296823 | 9a9d38e7e537a881c08afe005c0eadc04ca44be0050b70b20f383d00336ba24d | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/028.npz | 296959 | 16b301a3a460951c274167d79b3794585d7b50d3bc60a3ca29be565ed490e575 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_029.json | 4259 | bb233fcabf3fd23b58f4a5f313ef1e6bf415d193745806dfc16f0651d99e5132 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_029.jsonl | 1153 | b96d86ddf3579d1688cc81c719fc6aca0ea20cab59ebbbab760208f4eb5718e8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_029.npz | 3790 | 034034eab922f826376a319c93c4855cca0324daa46b84b89986fe3aa464c44c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_029.npz | 2726993 | 3ca9067236cf585beaebfc7281134fe3a97ac54dc85cf5c5fa6d81d62ca38cdd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_029.npz | 852 | f3ff38377e4a378158d8887a8a34d7a819691b3b9bbc860a4c0e852c3656e10a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/029.npz | 6801923 | b396387e5b17939b528ba68f1fc9b48447a635d99bdfff6ac4b6c31997055415 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/029.npz | 1089729 | 22971c322a527f14cf4f1a746ac95b8d69fe549eff412f412c5d7ea942dc628e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/029.npz | 1089948 | b5161d862ad431d951a5fee889eb5e20fe6e6f573c070e843757a70e0f412b86 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_030.json | 4255 | 10e6f2e8204fa907e09a95733cf5db8878f4a499518f65953b1c97232a371429 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_030.jsonl | 1152 | adba27be8bdd9744fde60b9a1a47f77d31aaa154b8f654e33f870600a4116840 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_030.npz | 3790 | 5b85171ec8666a69865a42abca19e04969ec7bbb616be9da1283a981e011480e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_030.npz | 2726993 | a0ee2227c848434559e4ac57a990fc12f965524a3b72a2428381ef1332061f79 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_030.npz | 852 | f9ffe3c0bfd67d812114d447d0480bc8c08ce4b13d9ea4cf6f731e59859d6750 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/030.npz | 6808947 | c0b64e028b06117932785fa561cfbed0e7ef37f43369c40380d767ecdb0ac27b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/030.npz | 1082616 | 581f48aa2b97401d2273adae201465bd9e06ed29610d356f89a765805230d682 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/030.npz | 1085763 | f96322e3e8a84ef0fcd454e71bc40c83eb54893cf3e490fc0cc8a8a1a6a6e6b0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_031.json | 4251 | 8338a5c022bc51f92c7979728ae0b14b8fdd6d611430a580de9bc7ef6341360c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_031.jsonl | 1151 | 8645fe83161b5dc2c1e08db1453e5b972b2c2612e1dcf9a89941eb58134027d6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_031.npz | 3790 | 1dade8d947c3ae34e1226b97adf1b6dea9676ffc5463a395369b883ae04cc65c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_031.npz | 2726993 | 5a568d337717f7238e352fb76b397cb0ab2a1247c9223e1af2d88682c9ca494a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_031.npz | 852 | 81f4601e08834ce05c0f8f23a0b7ac68fb0c46ed2ac4865e0a68fd47f5b6b301 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/031.npz | 6819667 | 2a55f8c6dad15744e098e7a001e85d8873fb4f714023af834eb6317567f83694 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/031.npz | 1079398 | 8faaa829915e9d09a984dc233518c500406e82cc552c64ab576c1a8a915d1634 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/031.npz | 1079700 | 13554f276c2200e19c833abe252679fea4f17f8b2f4551bbdcf1154c59283dea | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_032.json | 4260 | 308b664ce604bbe517475f4ff860686d39fa1923f882cd276db9ecb623db6991 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_032.jsonl | 1153 | 0c2acaebd034bdf9644194195fd73a907dedc007ea9f818568f9c606941d437b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_032.npz | 3790 | ead1c3f2b9d9d22e633c835c6061d443c870deed215c2771989fb88d5312786c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_032.npz | 2726993 | de3d7a91d892f30953b2702b38af95c377e3d86c98cfe28f2c415c4cc0e2a9bb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_032.npz | 852 | 6ea373667fd27e4b6d9359ceea40c5e4f123dfe6054d878db470a874dce2f414 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/032.npz | 6828667 | 6d15c2c4f8fdf665bca423ccf9a312ea43204f29e60d4ee12673f6931292fc9c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/032.npz | 1087014 | 371acd182b190acdbb7376a33df51e1ce47495573dff35c494a01a119e4c2b2e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/032.npz | 1087532 | 43bc848b5dcbb3cc2be912283e0dd40257b8a8c7430085c8c034479d4eb7cfe8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_033.json | 4250 | e44b0423f532bd5da578069b570245a1772dc2c24057a5efc9dc6b4ff62afc86 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_033.jsonl | 1151 | 353edc85008529e315d737ccf7d4e30249c1c8bda6578215e7ebb4e71e56e544 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_033.npz | 3790 | b4769adb9fe03728a7b9658f142720866c8fc43098ed20cd3f5d93c68a68c5d4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_033.npz | 905681 | a1b4c51f79f41225cc4633a67d3ba69375b216a9c66cec0fd9fe05eeb1cd2aed | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_033.npz | 852 | 55c188c844fdb746ff05b2bcfae02655828f6a21ea9e0b452c24f762ca2477c6 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/033.npz | 1748318 | 44e55c34756283cc4428a9b8e586fd61574c47b9c7739bd07e3321ecf7208327 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/033.npz | 297044 | a0d385d50498ba225dbe4858189da2680e6128381ff89d0f37e1ea4778cd130f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/033.npz | 297361 | 5f7ec0bdb06e4873a4b119c5ab1bcb694d6953686099ac1e18c88bc0a83aee6f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_034.json | 4253 | 9af35260f7f3f0abe37c2a63c6aa93ae38d40c90dd073983fc27dfb68aba4472 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_034.jsonl | 1152 | 935a7e8d8bfea11210a00cf693a29c628265b821664689f2288cb92a82469f8a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_034.npz | 3790 | bb17ffcf87e9477d818d33fc0277d5cf96503899c861d1e46807eb7e31d995e2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_034.npz | 905681 | ec790950c9269f21921a1a5d60b466fdb8b8e0e191be8692a1e4103f48407759 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_034.npz | 852 | d9016d2ef15858335769309350a2cf857a7ee69122a219f959ab9e52e8e88ecc | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/034.npz | 1745650 | 0d9442c14b1dbb62a8c524ee2251fbfe371d4d54bb342a1381ec5eedf0a3eb1c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/034.npz | 295677 | 83aadd1705d9ee42b4c6eb88a59cd90ec2998c162bc22ef910b149743619b3ea | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/034.npz | 296055 | 7fc5d2a9a1ed5a3652766267d5071c6f11dbf4bae0b9dcd30f96a08b85b07abc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_035.json | 4256 | 9ed1d255c873089a639bff0cc479ec4b8104435eefb2e09e9df7668c3c26f84b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_035.jsonl | 1149 | 0323ca914e2a693419e34ce0fed11309d77e242571b776ea20b2b3fffd942baf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_035.npz | 3790 | 3a9c340f5337c3ec14ecc9219656f5d59e4043454309259964eaab31db5fd8ef | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_035.npz | 2726993 | 432fe37e7ce027d49a5873f43b2e2f390df16382608c7735450af51789118d57 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_035.npz | 852 | aa7b8f999cd8bee519a1551d7de95021714c5355eb349f3139cd1c4694eff75d | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/035.npz | 6818861 | 0848733347edc79ad89eca76dc8dc6269dc58648895585af91b0990cd863cd3f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/035.npz | 1080350 | f3dcf13d92e13c403c30c3e6d1c1ee07039d2498e64dd7d82e648fa865986e54 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/035.npz | 1078804 | d4e6eed60804ddf98ec79add4fb0064106fd7ea2b9e6a7a7c87597d318c3a897 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_036.json | 4245 | 18e7ec5fb79a5eee64c996567d71c3f6c1cfb1bdea5245868659b014b51a3d6f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_036.jsonl | 1151 | 41ff59767d0fb8d8735fc24b985c86df21bf05987522677adb121c8b718ae33a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_036.npz | 3790 | f8b2b4c231e697b459efddb24607a58be14adf90b510358a78d6d9dd540e0fac | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_036.npz | 2726993 | 709e51012a25ae02fec5fb74d8cf17e9af7c94279a6ac08bfd5e43b774c7af52 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_036.npz | 852 | 050be08218f3d239c4008e8f787dbd31a08135dab2f4d015d456a2aaaf2796a3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/036.npz | 6814942 | 2f574d701547133a8fa223f84a125d1579b929607ccbf5e0c3505ba5cee2ee86 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/036.npz | 1078316 | c7b42f25a45d7f10ffe10bf583d6cdef5e94a84bfde509a80629909f3adf9ed4 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/036.npz | 1078398 | c8f6020a7f4a3dd666bad9ba818464d5d53e1f3badf045da18e9d41c834db0ef | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_037.json | 4239 | c3d48294e54dae38c70038577fe95bdf7689b8eba4282e7593635617fa8b7c60 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_037.jsonl | 1153 | fecfcd604db39593a3e5352468e44ad853e20d26274797afccdee5949b80790c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_037.npz | 3790 | 92ddcaf9da3f6432621c5ffdb0963245377726f107c6e9dd9ed9d565cf58d852 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_037.npz | 905681 | 4a1495246664323ddf3ff6c05fdbe8120290f07435675b46aa135d64cd00d5d4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_037.npz | 852 | 2e8903ca9b384c5183db25417349ef98d0e6995895aa11c204e89b5e11532c0a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/037.npz | 1745285 | 1f6f327dd5cf92a20eb8cebedc9a673ffe8a24d029fc8b2a25151c7e40f648b3 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/037.npz | 296027 | b12e3abb1a9ea50b67074688b885b532f8408c86ef4f774b9180b9734b562c63 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/037.npz | 295848 | 50203e9334596414820f57575774e281f99112a6a75cec07c6c18f8572c3506d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_038.json | 4239 | b41a6a0f4a45dec2e130d66dc7d88dcb9fe5cc5e9ad647bd9cd74bb0016e7d65 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_038.jsonl | 1151 | 8167a52293475aa829034e4f5e6bcfa02d288e7a52265ff35b0cf20710a8e493 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_038.npz | 3790 | 62374324d4f5c4a362d2f4b9b4269807b22124bd46d907a26cae44ef3faf0606 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_038.npz | 2726993 | f4fa0047920d6e6b7b1bfab93a28e35b4672a627f2abed862a6d4ef4a9f7bf5d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_038.npz | 852 | 0c0d88f47b83ca40a1bdcb2a910562d6fe44eead54bf5a3dfa6d2ddcb39aa242 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/038.npz | 6820532 | c7f982ad7c71f2d4bdcdf1f23f95e67b84ec6705f1baf9465aa26ee483ecf3b1 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/038.npz | 1076378 | 5aa6fa0e9524cd2364ee19fb24de09a595a1e7ff1d159a1f798300b228155ae2 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/038.npz | 1077179 | 234202e1bed3c46bb9b75184ca88f5443ae86d3c146e58437b34f8895bfdd140 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_039.json | 4240 | a154739e9f0491efab7055ff724e1c1313fb152244bd673b3ee16ee9eadd8607 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_039.jsonl | 1152 | e5548dc37b2533be423d0657149cd26e6e22cfade7fb8667be47e805f71a471b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_039.npz | 3790 | e6d643bb894420f39717bdffb59258163e39cfa6ef807e7fa2a82cfba80610bf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_039.npz | 905681 | 073458e4bfb56957d96d668a12176f433771ec95f5bb6a9df03e64288c987e1e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_039.npz | 852 | 56b0ebe2bc4ed7541fc25eb94a86834265bd08498092e34ec3478780daee1683 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/039.npz | 1746613 | f4e4e55fa20a3a2712e2f7ac6e3362c8c0cd67a7012cf030c581886558fba5d1 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/039.npz | 295812 | f81feeabcbfb1aa0904d93227fa73a49b97ed807529fd28933f5a8e4e4e63046 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/039.npz | 296477 | ca18dceda8702db0a908233d2bb6fedb9577c1ca0616023962b029b375140389 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_040.json | 4245 | 0b5d6b78cf2760d257b3afad667588bdf7bfdc0fb99e6b0808f7483ee14520a3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_040.jsonl | 1152 | 893c6c51bd8527e6f4f0aa0eb07770f64b18f8b5aea3f888dc87337d8d36bbc1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_040.npz | 3790 | 241750f749f987ad121aa5d01031fa398b40336d19a81ea65808ef6de0c95e9a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_040.npz | 905681 | 3d53a5941adf4c237c57ea2cdec83e1255f231d9afc9d12991d357635fa5660a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_040.npz | 852 | 1c4f2b1512bcc2b2349a8c46d525bb657c7c312715529640e03ddc38129c72c3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/040.npz | 1748357 | 01018b8e2a1767a00dc5931602ef8e86dc842a3b3aa5c97c5a2aa29b6e4971bf | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/040.npz | 296032 | 0e16181ddff13584330c1b3c2224a1f71ba2a488f3ef73af733187bfc0949286 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/040.npz | 296199 | 7017c35bb9edd64e70299ee721af901c06ea592f74db6d35cd98a518aa86a4b9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_041.json | 4250 | 3886ab0c00a8298de17271f5df8f8352e7757257f4f006f09167502aa1a48056 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_041.jsonl | 1152 | 907cadeb87114d52690d3f91dfb4cc4d255656ac39710c1490cfc557ed8c9898 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_041.npz | 3790 | cedf4492d5b5958bd33949227dafc82f063aec160f352259f83323f2e8f45bbb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_041.npz | 2726993 | cfd0fcad173441adb1a6cbdc908cc46d0c7aff29b39f81a618a38e3941e6ee66 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_041.npz | 852 | e9a130d8dc13e1f21712a975b333596567d500a74469760dc15efd1ffd334af1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/041.npz | 6815150 | e63dd4231328c8ca3eaebf3411fae49be4acf8854aa44d6184a579740d0395c9 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/041.npz | 1088134 | 930e00fe0a95294054ce391a4da5df0e19c7df4d0978a5ad4a19f06cdd654fa6 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/041.npz | 1090063 | dc77cfffefb42d08a2b5315f9b973a7b2c7e6376e995d9e7fd3a71f15fb65de0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_042.json | 4252 | fc1aad0c0959a5eb362667b819b350583b81e7b75b2e04d459b08189da61b00e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_042.jsonl | 1151 | ead03e834f1ac31b6863c260a9dfe0a7598f47153400e2fcc99e030360c990fc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_042.npz | 3790 | 876b1cb40c8e908a404e53f908f35626317b21ab3f00f61603c9d13c6fe4ee91 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_042.npz | 905681 | cbad5d30ded4a327597bab48f7fee7f2f499d2e48c43ffda4887ad912acdb149 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_042.npz | 852 | 24a2a6c6a2d3d0c1aa20ef116243d2ae512a8c0e4c85ea4f8e5919015e6a31c0 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/042.npz | 1746808 | ee9ec06f05ec5b858f2a1c6f0aecda272c9b7d28d0fd177ea98fa8a42f2c518e | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/042.npz | 297542 | d005a9a1ae19b4cbfc9fa0a2785378d547655e7fe4d92bfbc163a7d16698963d | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/042.npz | 297871 | e0937414c5008c207d4ab40c52b04bb2469325adff2828b169c954a7867e09dc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_043.json | 4236 | 2122bffb50369c40da0d767de8c3de464f55d369f50becf9ec7fe52239e7e4cc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_043.jsonl | 1151 | ff490438bbeaa223a931462a09afe21df87257263cd0b0af547c4e1d2b70c830 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_043.npz | 3790 | 8b154a2f27c4b7522381ca3b7dd7c13baecde66da4afc9e2eff3988af3c86b67 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_043.npz | 905681 | f4d0ef8b3e66ef94a8cd225fa65438edabe82f37daa4f3b57d95f71d0b664de4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_043.npz | 852 | 319db6414114e8ca577fc80aa10565f8641ea665ac3e977723d5e8cb27f659a1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/043.npz | 1746416 | f16385a3851b7636076e033cc9d95ac34994900a18d24fa105b509850ad2f179 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/043.npz | 296525 | 6cf1c66a1ea4350a643cbc9b99db18869ac20e476d91adf9ae8ee6bf6e59583c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/043.npz | 296769 | 5ac659db5ccaa25a2c2ce8b972a9f0458ee6793d724479e2aa9dfd9b001524bb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_044.json | 4251 | 403e72398730fd1ce02f0150b5c736ffd62a5fe3aeed164c9f05496acff7838f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_044.jsonl | 1153 | 5abbfe301084907e4550fb5c89d7a70bc50994a6c677fdfeb5edc4ffc42185a7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_044.npz | 3790 | 2561351b016b7327e491e16a0f6f863827b3349a6cb21ff8aea0ecffddf0b754 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_044.npz | 2726993 | 066dde71ce8eeeaea1f80fa43218c8755fe69924a0c993cee0fea20ddde3f844 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_044.npz | 852 | 0f19c6cc04261d0c9cf5c3fb153d76286f449881dde1f429ff92f493668337f2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/044.npz | 6831444 | a69cfa060b0a53f195cceccb0e38beb343f5b30510e4b428f8ba6cc9aa2c8cf9 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/044.npz | 1080825 | 0bc028a31612d630dff18c5ea8d970aac29f7cbccffa40219409dd618fe2b030 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/044.npz | 1081258 | 350f731837de0baf079d6382e168075041131b1f96e3fe2ff931f39a21086320 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_045.json | 4246 | bcffde7d014cb79acb6bfd4660bb749dfa4bb5394e0430f43e406d06f22956e4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_045.jsonl | 1152 | 7d883134131b96aa4b0e8d9728691d021e5be51997b9cbb007f6bfe7bc1e53bd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_045.npz | 3790 | 33a9a9dc71a1d28ebcbbbdbdc630de2fd87ef7f8c4ed185cdcd8c59622878930 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_045.npz | 905681 | e8ee5df61e50c559f04da521a2693c3efb956244295b17c102c2a4f5dd0ef71c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_045.npz | 852 | 447e9ed5050fb4d7381a1d195f2d8701e544875dce50bf53de44a23972d87afe | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/045.npz | 1747483 | 56715cf770373c861388bd9fc2443086ef2d8ca60387b8d3e761206f642f4fe5 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/045.npz | 294568 | 5426b41c43d73579a97d9fc02007780e5f6cba76e6cd9e79afe5dc71d3735d56 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/045.npz | 294752 | c05ef31a43f943f566d179992d6dccafee3b6bba9d8428a0392f0a7628ef0e4e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_046.json | 4255 | 6418cf1ee7d3ae229ecc974cbfeb00316c2f52e43f45976c70829ca47a07b85a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_046.jsonl | 1151 | 0786ec35f5be7e47d4b258d005e1745bc663b8af072843ad956840855b1b828e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_046.npz | 3790 | 5bb23b5b2e276bc80e996de5f14aac57fcbd9a3bf32ffb80ee3e343a060e5ca3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_046.npz | 905681 | 7eda14adb88a11084bbe05d4b0c0dda2af1c6f54fe46997698306b92936f6913 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_046.npz | 852 | b8e1a630cdd83bf108f28e921573465adac9b46f7694ecd9a34b96db314aa64d | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/046.npz | 1740832 | 94d632a210db73fd56203ee3f661249c67fb7ff406d00e88128a9cb0975fae10 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/046.npz | 296131 | 6c9e52a3459a440be1e7a4ca82330ff22fe0a7ba38f2cda41fe1e794b0e19454 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/046.npz | 296381 | a4e844eaa39ba350daf529c52914872b2dd67325cfd5d6842dcbc52691db776c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_047.json | 4254 | ad9e6f0d79e4d3dc3d7bbbdb1246a1d89c97db0894f90ad4081ea8cedad2fd39 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_047.jsonl | 1151 | 139144a92deb77bcfe50a69f7bfc54f9bd3af53f5b4e34daa83e5d70e8fcabb5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_047.npz | 3790 | edb3244894fea31a7e3f6a0001801833cd9326d9188450c1a1fb844248db823a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_047.npz | 905681 | 85d9f90649080247cbc948857fd4ce309a75d95a4f3483bfa0b6a2a572920b94 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_047.npz | 852 | a71f3a5b8518766fba687be15ab24c8858f3e5498fde899b70d5dcb808f00516 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/047.npz | 1745466 | 5ef8721305b0d8a5d2656957bb609fe0f36157973400cb4bc94d020fc8a193a8 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/047.npz | 300027 | 48745592c4944782e78c06798104b8b59df62e0001cf44e81bb7fb2a818453cc | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/047.npz | 300472 | 2493dee1a3721f38a80b8bd45381ca6cba6a4de1bc9144d55b1b4693a04f8d84 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_048.json | 4251 | f8a443677a03e8147e7c91a2a0f0a59127b57e332f554007183c35fe1c3e1d0b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_048.jsonl | 1151 | 88f8f60edb853f89c3080a1faee7d18dc8aa7d6b0f2eac7da1add7fe05cf8f4b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_048.npz | 3790 | 08cac9ac9f60163c85cf95564bfc4ac9b0b6aaf94826d0ec99bfa20b7c4a0c32 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_048.npz | 2726993 | 4b9986869daf29f8a977e58b8f3baa2e12a5170f8e2232a86045fd4db3129281 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_048.npz | 852 | 2695c2af338736e4e60a803d76b0b5e3e6b420bb25624f412251582b92817d66 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/048.npz | 6819652 | 2c25219fe8603af49901b7b465b255019e316e26d256d70530e98fd67a523e33 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/048.npz | 1084201 | 3f7b9d9d66f1856649624b44d0dad8c5c772931537c2a16cbe7991ee1774e9c4 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/048.npz | 1085059 | aef2287d1a40e527fe55609717ddb0d1ff9f018e1b9aab1c93f2c5e0b2d89887 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_049.json | 4250 | 92e4ffe26b35f0b8d7ccfe858f391f5ab8de8be054b3b28963444bdf0d908dae | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_049.jsonl | 1151 | 4ec8f53047e70096de8e23da957171fa03505d05f81ea8651244f71587c25b0e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_049.npz | 3790 | 7fb8dbb13d0be7ef777696aac14cbef162e32663bba116974c08ab8253efb2a0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_049.npz | 905681 | 0b654f9d81989aa579ad26382891cc076a29075598c5361c48ebe996740d4893 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_049.npz | 852 | 8ef82fc361f41fb8d3183e9e99187ee9138eb80980532811324f52fd80ec2488 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/049.npz | 1747803 | 58cad21b401d2d0db18c420a6d0310e28069c532e48a29c8112663e8c49f1341 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/049.npz | 295832 | 5f3a11a501189e7569079b240e41a2a3a8bc40055272601f544a7aa4417188be | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/049.npz | 296132 | bfb3a40fe1d279023b122b4e27edc70396b1bbcfe595819905821cccc36341a1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_050.json | 4255 | a29361d0d5aaec32df5a8f5fee07feb1ab5d54da09035fb5131827cc6a8ed712 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_050.jsonl | 1150 | d96447d980305592906bb8c69a9e44dacd8b3318504da970ebbf4d66afe2da41 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_050.npz | 3790 | eea021c3b65797acea2396bda7f54407ce9f56ba0424a26a6a759c6d5b48ff79 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_050.npz | 2726993 | e9a0e6eab1d9a54cec7c5750c6d70399cda6922ddf10676a72f156965e893c01 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_050.npz | 852 | 034fd854e5ccaba1aeddd41f1c3519e0ad68afa94b6cd616f5dcdbff2d9c17c6 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/050.npz | 6826093 | 091c30430df2f820e33ed91993023443039e9db58c0c52e3a122f217d5cd8eaf | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/050.npz | 1072119 | 5797e61ae235587ae5c319e11eb6481f175dc6c8067e22dd05cba261869fc07d | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/050.npz | 1072810 | f271c34d82fb43e70048afae822a341463937de3bfc518e851475790d2037146 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_051.json | 4247 | 8b386e9aa9eb5001948768e4d575c6c993793eae22f82ceb529a616897a42459 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_051.jsonl | 1152 | c6fc1b3ee25e94063d6ce980d74e2ac707cee72bedb460fdfaeb5fb53571bc27 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_051.npz | 3790 | 1b9ffcdf44e1142406b85d70b919374be7bc5e219dca856320259501b1d9234a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_051.npz | 905681 | 78ab50aabc144746301b256bbc54245ad05d6959a2483c150a23a65160bd2ab0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_051.npz | 852 | 97dcc568f6750ce1b00570ba1c1816d9ecbcb2cd708b092ce61793597a334e2b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/051.npz | 1746649 | 1a96b7ec1a0b6be235108f6789f0fd5e7b025683ca00374c5817651ca37b81c3 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/051.npz | 295414 | f86213d3225ed87c9d98e951d3668e3f32b9ffc4aef45d4d35b8d92a843fa671 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/051.npz | 295233 | 4b80a6a4989745c655eae5bb56ee0e55613ba4e1a075285b712b854a5c4f0196 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_052.json | 4247 | fd05b7d77dcff326370c0074e3b6ff0afdeafa09b0e228918b9cff4c21e05853 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_052.jsonl | 1152 | d8ab0a1ad46ee6721ef80145947352b085efa42a89348a464f47706fd5c20da7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_052.npz | 3790 | a225481073488f6cb74b8c4798be66e57635a866b74a052b9dfa74170b41f14a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_052.npz | 2726993 | f0e137be157a2f530b03689808f46bc58665564d3e9f48d899eac70d4242b5ce | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_052.npz | 852 | 91fde766669af9ee99d1994b2a66796664f8c5b321fbcf3c0f87a0e9b314c0b0 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/052.npz | 6829500 | 66ab12b7cba90b992d675c34367c5bb739902d06f07e967a4f4c1f4d257510af | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/052.npz | 1073955 | c5c6aec531b7894c1b8e9ad2d354429de2f51dc9e1d8a1d82f657b6d827d66f5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/052.npz | 1074091 | 22d3fba4fee6c6ee8d230f9860cda54dc3d618201def372590bcdce4a8af5824 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_053.json | 4241 | 22d6edcb2a456cd7bad5fb89745001d4d07819dffbe6d1712a9b1d784c9c5758 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_053.jsonl | 1151 | da06dae9cd149ac77ad902fdde245ab9b682bad793f67963cb0359f2b588e673 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_053.npz | 3790 | e9d16395b77adf33da2679b4b4d737f7425cc54de457222aa912ca8f6e040f8c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_053.npz | 2726993 | c3e9a5086713a1f973307be2719bfccd096bdd5843b6d8d67da0a66726208d1c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_053.npz | 852 | e25147093f7edf63a7f6e5c492b5b586ae4dcc7179031b00698d46dc824daf1b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/053.npz | 6822875 | 003969380cede2e9cc2a6aae23701c53591100d3d1a4e7030fe1a178e5e93e13 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/053.npz | 1079337 | 6e98dcbb6b735bec9ffd04155d7fc90475f7476d19a24ca2021d6559fe37d099 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/053.npz | 1079181 | d516d21168e940d1c138b832f00a4259ac290c32074fd66ff4653ca3c1e43add | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_054.json | 4247 | e2820f5478e22c6a53d0413e3a5aa9bb53ee2746246e26ccb4229f7796d64d84 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_054.jsonl | 1150 | 16f6854ac1e866d1ce1f0794d79de7b5011a9bcbebd4090b3e723f46e75196f2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_054.npz | 3790 | c6dc8d9144c94f2e8c11a19c1dc279b59aef49c68ed495d5d6c4eea8e183dea3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_054.npz | 2726993 | f9d780664b86354a1e9134db8c59ceee811d22c9d6099a9d087c6738820060d1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_054.npz | 852 | 8cc611c254336aa334a51e493747b4979be048bc1b3dc9ccc9aa810a27730cb6 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/054.npz | 6822226 | c95a9b6e264cbb6d54cb16a806d1e4d9e544885e7361500680d7e73dd37bea0c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/054.npz | 1076756 | a6c844255c5c79b166dac302d65fd943c9584e2956d8751880b110e90a28a2fc | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/054.npz | 1077107 | f0ab9d69d60b8368c47b2e1a2fa0cd8d04486f77b46133a536efc0a516774baa | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_055.json | 4249 | c3bd3c4dd160cc815f3762ac03b3f568f8b81ae76bf810c87e9de19c77cd6ccc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_055.jsonl | 1152 | c6a7a37f28a5a41c099f969724e8101aab682e7b8c99ea0d085acda81eb87567 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_055.npz | 3790 | 5c2affda91306bbd9e19d8f480a1bb9318582bec03ae643d7c0e1070fc209cf3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_055.npz | 905681 | 8c4577d309db3e901a9b987f2bf541312a308d68f9502c8006effd8fc04f0cfa | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_055.npz | 852 | 390535320f8f4c62571c070f1ceb8d93a3f7c5b13edbd77b489cc6a16d66021b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/055.npz | 1746485 | fb67c9f38e556e5b4a575785899bd8a7fb0de160855c9fd8cbf99dcd66f0d22d | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/055.npz | 295996 | bbd8133cd9e9e31d3b22622f275dcb0568f828d3c0afafe1f99ccf94bcdb0fea | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/055.npz | 296382 | c485d0f9b4b8f17bd11a1a77ae68d326cd36be9e4b4c444febbdf6e2c7b936a5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_056.json | 4246 | db9b4897fa769d86ad817f65a2bd3640211c43289092725c53d53df4d5e32644 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_056.jsonl | 1150 | 48d5f2ef6d277410bbb1a3409c410a866fdad6392bf6d55fd924dc06c10d5564 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_056.npz | 3790 | 55ffcc34f7d3567c8c368c6463e1cb99c99c23a0d3ce5b594427ba3a4b2ca875 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_056.npz | 2726993 | 3f4de625ce39d18f29d513889893bef3bb5bcf030d3972c371e489053d65449c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_056.npz | 852 | 9e7e4bc04ac0682bc67bcaf778b7c443fa694ff910c9f9a62106252cbe189d33 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/056.npz | 6814009 | fb5b035a38e31453e3933c1fa3516d482304209c0db895d520abb11fffe7d0bc | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/056.npz | 1079315 | d4cfa7c2816716dc7786c097a45cbfe2678c44ef4a24c64ba9e24f66e674e479 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/056.npz | 1079771 | d324ed078121cc49a48fbf53eb3e4cb0c85ca28f0b27457a1f086564d43031a6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_057.json | 4255 | 674eac394f3b717259cb79efa75e1b40102b5ce9a796f4cfef2fded9568dc342 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_057.jsonl | 1153 | 1356b37523ca2403e00da5fafff5591e03aed4bbb483828fdfbd2d7fb4eb2d46 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_057.npz | 3790 | 7a3d845260773a40f804b320a200882d31b50595cf2780a2f19790c6f69cc9ad | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_057.npz | 2726993 | 966adf70a1999d7f8272b77ee77d48f224b79bcc9232296ee30126c70e1a00d3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_057.npz | 852 | 1cc6b83b3f9be1b340397208c10a2cb23b254dd97ad473c58b401602552eb3d7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/057.npz | 6812591 | 3db0a6524dbee919ad45c1636a8eeb5ef1679472e14f0ab172fb1525d70ee3bb | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/057.npz | 1078850 | 90b920c34c5009653b89c807e2cd254740ea9dfba6e6a3878e5d46be0f16574e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/057.npz | 1079515 | 592aea56bbc52b072fa76693a1070cb8c331b955483dbcc47f30eb023313edb1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_058.json | 4256 | 5e014cb9296e4028744f6c8c08005c35efc89fbc9597fe23a132c86655b4e9c0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_058.jsonl | 1153 | 08615fe56e37e644fecd685691ee5e036849fe4f6ce1259306c55ac6f35f7f2b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_058.npz | 3790 | aded7a424024abcc94145e95a7d64e4b8a2e7a8f96c17d7974cefb9d78938740 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_058.npz | 905681 | 891359c78b7a2db7929e0702afa9eedd15d1aec025d0968a46a36fbbbfdd3ae3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_058.npz | 852 | c21bb7a64dde0b49d6c945c6e3d9a797e7dbba1fb4f5356ac0cce28091b0cbc8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/058.npz | 1743030 | 9ccc35988d68478ac017b9fe50c690b29a6c7e34b49220490dd2f24f38781efa | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/058.npz | 297999 | be300e656dd71a15c65bd6d8955f9274b2907d8b0d07426662bb93c5648bfeaa | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/058.npz | 298159 | 78a7fb0a8dab43eac64db62ec9ed7648c432dc5dd81ee746136ff27622af4d4d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_059.json | 4255 | 2b193df26b801c27c450f4ed1d2ef566e9b1fa209eb6e888b79b351a5c8d7cd3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_059.jsonl | 1151 | 5872a1e38472cee3ac554c70d6669a3329cea089da8e262679b8ec5152f48c02 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_059.npz | 3790 | 063c3f445e604810849b38ae756307fdc5fd73aa88d74b365ec1a4371429d0f4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_059.npz | 2726993 | b80366ed6c5e15e8e568f40cbc1331bd5b546bb324f2263641732c6e1cc6afed | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_059.npz | 852 | 0ae2c9775d880072643f631583c9f56ac25327369554d89f1941430e1b7f9589 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/059.npz | 6810564 | b0ea8f703d890f3b1b1c13cc7b6520170ec8ea22618c5ffd8fcb438ab77f86cc | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/059.npz | 1078268 | b53246f768578017718d5a22eb3404c75b606f3d54339ded0604021b48fc01a7 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/059.npz | 1078829 | 7417f3a90eac34bfa1caafccbe9f9a947c4cea694c6360c858318dda0e149146 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_060.json | 4245 | 812d8035c7863fa18f128845a6e7c263a6662dc64e7c5cc1904e0f87d0950621 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_060.jsonl | 1153 | c7c7fd66c5c4b43880611ba8fb66edf15985bd9be18a8c3ae6426162c2665cb2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_060.npz | 3790 | 9e43b4b9d03a7ab7fb855b5f2428ca3311765ccf2246e0b61a1b253bdece58bb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_060.npz | 905681 | e0d5368e87f2b9236b06d681aad2427ffbcfec795ca1386ccc1675a012f92e89 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_060.npz | 852 | 99efe1fae6142783aba2c2800a23c7555d42032b9778abb881d409201ecba293 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/060.npz | 1745491 | 7cc3f6262fdaa91e8ab7b37cfbc353011cdb131f36de341f7de4fffc6c14bb4a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/060.npz | 293439 | 06a39bfe76c085988288ce6234353fce93da284c56273126734ebaa7aaa4b2fb | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/060.npz | 293416 | c533d4d8f2d8bf322c5a0cec0861196465361067de8c4fb4161ed9feb9930b1f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_061.json | 4253 | 9b69ea4757c78c102ff3ff785680c71c8cb153feab9f0ee3a0f0e6bc22945f00 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_061.jsonl | 1152 | 3ca5731858ea25d5089059b9665c9b422d824832e3b64abc3f8b2a1c4a898477 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_061.npz | 3790 | 2410567bdbd7f667e0b2612594128856846301dc3fc41dcdc9696dca64c1331d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_061.npz | 2726993 | cc33d8a9c81cdbc930f04d3850a6c40e12a79ad09de927e631ab72335db9ee2b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_061.npz | 852 | 06bda7881aec4eb1f5317af7c375ea358835cd6203ace41315780abb00e2bbcc | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/061.npz | 6800708 | bb9a2b18d166233db687ac87e6c617e3f2bdace1b7f2aa4d808965f06f5be84e | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/061.npz | 1081521 | 8a1fd62384ff83bc288bd315b26bfedb8a8ec82bb9b7d9fb1ffb67812e7a9cb3 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/061.npz | 1081938 | 972ed82fbce960cf33da74e25538b5ed5fb1c43d859d4ebd13cc79d776656d9f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_062.json | 4244 | d6871c36a7a65503b2d92f31b798025060c86c62ecb4157758e4484c53ccac44 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_062.jsonl | 1152 | 1198b059fc8577309decb74abb2b3878a0deb2b32e5dcb6c9a1b07edbdb8eda6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_062.npz | 3790 | 7e9236c4088e262f290b5543cb60408aaabb5fc13bd61fa5541816d68ca3c499 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_062.npz | 2726993 | 2dcea0ae3c6685505b42aa3b00fcfcfc10f4baf0c5ad78bc52e3017912fc81eb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_062.npz | 852 | f27b82b04802bedeaeb95da84af2e1ee3561242157d6602e7548825ea079240d | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/062.npz | 6819856 | de3deb9e0f7a89fc3f19b9d496ae42521643e70d101e3e73282ba806b98c78c8 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/062.npz | 1068128 | 78cf2b2f3d3b7829f67b6105fe57a71e3fe5082a52cd322e87a12eac39521b4e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/062.npz | 1071058 | ac1dc398b40f2bdaae597f1bd9fd7b396cf81dceb47123e946b4d64909257346 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_063.json | 4252 | 69157048043e853b773f022b7208dbd449f792099f1e493d71458b7b5560e5df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_063.jsonl | 1149 | 2fd2f0996c4e266050cc68bf51527bde103442f9523b731fb7877ec9c4ef1d66 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_063.npz | 3790 | acbf7380a464ec7d1966c2a4faf3267ea4f420a9a733189a9a8755d9f70d366b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_063.npz | 905681 | 215a8558dbf244c956b8531862b886cd24bf452b0ce524cf05483d1070cbc46a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_063.npz | 852 | 2b45d3b8c1e9245f9bb1d83d1dc031effdc31bd0d9ef3927183dab846b86a3c2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/063.npz | 1748368 | b9d71c512fd26c5d6aecb3d58e84ebc8a1b486643c5cd19a2eef436cde7c8eec | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/063.npz | 296963 | 9d62ff39a031f85272f66db23cccdc448d3845dddf7b9bf87aa5a82cfac22e68 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/063.npz | 297123 | 56267a931e872487ee8abc3ec6bfd20c188322fa4b856e268f0fc9b57f2db412 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_064.json | 4252 | d684d8a608470fd6923fd931416961b278490de4927f5fa7484dcc379d637e4f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_064.jsonl | 1151 | bab5b5e0b470cfeb5b8f2b2cdb4fcdcf4f3da7acb5b7600a3f430cef37a7433e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_064.npz | 3790 | 267ce19664d32279f3b9bf40ec3110a1133b66060aa43fa3059dc555315b8e87 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_064.npz | 905681 | c3063972a99abd4a1cc994d343e4cc9524a0254e23e7044aecd5926d90f3f4a7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_064.npz | 852 | f50a809435c82474c2c33dadbc84bae3914902eb9821b2a4fbcddfd387c5cbf1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/064.npz | 1744562 | 616abe50821a7b339bb856466af904be370a16ad7d19bbd76c84653118e4d040 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/064.npz | 299018 | 368848b35b2028d2e3a0b70ca2a9024e86bd2db5dc66715528e9d0605f4d133a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/064.npz | 298585 | 3311f740afab7d7aba6c1d5e551834844d906d4fc7ad40dc718b98e81db729b4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_065.json | 4251 | 8d1ed781a2c90c65641bb7d1e07e333489424bdb3191c4995640341522a0dd7d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_065.jsonl | 1152 | ff64589bb3b37a9a4e971fa4b62659a15d804863ee601f215fa0646d2d647d2f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_065.npz | 3790 | 8c6b2d06afc6838a264b7860c533d009cd0f11bd4d5a7a6bdb8ebfffed68bec2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_065.npz | 905681 | 7ce9fe6de523bcc571750df56ace7c4c719fa06b51b72289cb0d51921f744968 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_065.npz | 852 | b5676733f5d77e789629d335c058fa8c4e49fce7bbba017536236602143da84a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/065.npz | 1743649 | 900598a62bf82411e9713c12ca4e0d93bccee25b761a69b7ed8b06cf50354aaa | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/065.npz | 295422 | cb090df7b4cc5690d264d60117d0ebe305c4bd37ba84ec8ccd74458d144db58e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/065.npz | 295490 | 37e32c6e82408781d7cc094b32e526000bc7af224a0030fb8077cfd881e0ea3f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_066.json | 4256 | af95d1bd5b7679bf5a01abf77c94972b2de3340e9e26e5675a1f23f44b8f0000 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_066.jsonl | 1152 | 1143f6d96b01f682a751f94f6d88097924bf8ec23374a1b04c5ba2321d71dbd2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_066.npz | 3790 | 741f7e474a7bc8b325b7340a7af9d92b1090ecdf0559ceb00c1bfec258c8a9f7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_066.npz | 2726993 | 593ede9f250c294e82649ec576c9247e03ff88cd892ecbf1c129de505249a951 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_066.npz | 852 | 0e2d0d51e1d15030021202f5c7ecc45e53007b11aa225b3898d8162e6fc2d06c | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/066.npz | 6818536 | 0fb8e295cac4d45edf77b5e2c1f7ed44ab72586cea65a3f385dab7d2f2225a54 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/066.npz | 1077604 | 89654398ea1778929b338c87a2481475d58d96ccb168955b840f4f9f9a3397c1 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/066.npz | 1079477 | 91dc2357e5c88bc7f0b98df183f4521ca8163e52b6ae474e30ff35a12d880c03 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_067.json | 4241 | 6fa341241cf2b705d9a94869c5917de74f04ca9aefa3f441c76e28b2997bc2e0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_067.jsonl | 1152 | c3b50cfff1a962f22cd8ce373f6f9256208237e277e63a3d81797a816eb8f8b2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_067.npz | 3790 | 0ebf8e65ca0dde9acc010cfe30d0924fab3d3d251945c2c241ace7bfb702911c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_067.npz | 905681 | 9a8dfea72134c23926504a877be331e51eb3b055d66106bfd34f9e65720ab615 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_067.npz | 852 | 0d8eeea2624b1b284551827691186e2a79ca64344ec434f4de7c6fd6fc5b801c | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/067.npz | 1743474 | a1aba70770a994a51d42335e64c31f5092e85da7a055a20ee7cf259d0249612a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/067.npz | 298444 | 307e7bc64a3c1f8cb084520a87cbdf489f880fa114e8e454d17128b19aada894 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/067.npz | 298647 | d76841c78e2e695d6a6f1b1951f27f52721d0a249468fff8a11a87570ce9f782 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_068.json | 4247 | dd66c040f131303484062d73bfd38e204581dc033155dea187a2b8d466febf4d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_068.jsonl | 1152 | 1f5fa81ca6aefadf83f721fc6222768a5aab19f7de65653ae4ce001be4149eb8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_068.npz | 3790 | 0ee1d3ee6bf0cd9afe14dc236985c10a09e5974fd8a243712fcafc561bc6dbe3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_068.npz | 2726993 | d2cef1892d2fb03b3b4f41825db37208ace50e37b21328d1fb687ba6b6a39a8b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_068.npz | 852 | a6a3a2482e965d503ef45d63a1bd64ebba606cac7ae05a57c49c6a0d93d39a18 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/068.npz | 6807666 | ad902e532457cc71a3fd2485761608526d9e6c94dc0184a9d6a3108b1f8cbe61 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/068.npz | 1084148 | d8fb9820dcbec5857f05d2e41afc625480aaa690cc75e03c95d0789541a521a8 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/068.npz | 1083930 | 5c3602f612ed1ef728b149be204cfdb8187b6351af66201835d6ef2abf5f4340 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_069.json | 4254 | 1d149d845ee1936458cc000e273c5e8017e1984cb197060fc1c11bb192977b59 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_069.jsonl | 1151 | e62bef4d084adf8db8f65f05dabeb7f3102e96cd113198186f4ceadb9bc8be30 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_069.npz | 3790 | 497b828afa84c79fe43e6c60a3c594acb985ee2f4a5a9d844bd59ed35df59c2f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_069.npz | 2726993 | acee72c13e7aefbfe6aa42c7f03fc5e4907626f548f46858a602d9d2a02df1df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_069.npz | 852 | 298a870211524ec1e621264abc7c3697cd9d4314e8d98d74b483bba68b6b3a03 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/069.npz | 6814612 | 6dec1a2b46ad86930c75d512762290db0929ff6895fbd2b6361023bac1242dc5 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/069.npz | 1076136 | 6e8f60845d97e97d54ecfc4927009244226d072e9ba1fa39d37e4bd3847b2593 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/069.npz | 1077031 | 03fcb43209aef2b7b2b39adf20f56cd1df151ef223fd0ec940176ae2ff69e6bc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_070.json | 4249 | f9657ce4618ef2866810e0d178aa0f4778e8fa4267e33f248666046a3e19559a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_070.jsonl | 1151 | cd5601c3df57512cbe88a4a68b871da0f1dac29e23292992def316d6b34c8df9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_070.npz | 3790 | da35c308f6fcd13b8bf7ddd78fd17d03f1a44f4d27f9a3b95f68189f85bd8525 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_070.npz | 2726993 | 49ac64f74cc05d1cad35047728c7fa9a066c53fb15c63fcb3eba595ae27e3a10 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_070.npz | 852 | b614b7e78e849a8c82505878c08f58c77ff5d5df82c80a77213e44405b505781 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/070.npz | 6816396 | c943b219a3a90a5a419273f8db847c6f64f6633a447405ddeb551980395ca9cf | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/070.npz | 1081696 | b8c83883ee7a0ebac64598bd14a1f8a9323869b7f69563f48d6ed2e4ee69acfd | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/070.npz | 1082403 | 4aaa1fe9ce6dd04b2c9c325aba9c589f1b51f120151e832334fa543448cb47c8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_071.json | 4253 | 001438a28c070c7e4e035981a021284a264fe3b4d6fbf3708cc58766ede4da13 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_071.jsonl | 1152 | 89631826a785f6bb4dbe6d9b6e2d68cefce1c5f851883839721178250c629672 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_071.npz | 3790 | 5ca26ca5d4c7f3d723ac77e2b300eb95510577deb3914a6ff19e475ded4a143b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_071.npz | 2726993 | cff9e4e6bd516e2d5e403386eb0814f99101c2ef7815ce5f56a209a14652baa9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_071.npz | 852 | 9b45da9ce5bae52dc3d4041f64bb92572768ec867b8f6e21769b04fb1a497e39 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/071.npz | 6827492 | 40e8307902446ba7ad864a8327083d18ee8e0f363882e13d9bb01944c863fe53 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/071.npz | 1077397 | 8dd219adc7666707320ef95bef81f641902be611baf14c24d9c35255f0ed5a36 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/071.npz | 1076780 | d76883debd5511c80b687cb1fdd662b199afeedb1759c698c0552c16d9f7403f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_072.json | 4240 | 6b328fb1d6019a26f5fd37cfa281a15eee617b10a73645be8bab026a03b35914 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_072.jsonl | 1152 | 86cfcdd41837c2ab76f528ebca01cd1505de9bb0151f437b25b4cf1998dfe616 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_072.npz | 3790 | 75366166dbfedcf7d21bdd56c0e50686d46b49061024702035c30664de286676 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_072.npz | 2726993 | 5fbbad49b1e72f140df01c110dd4cbf70e664e0175d6f090dc89fc8454ab8aa0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_072.npz | 852 | c3fecb8070d48da6dee8b09bf6ab200871833fd851075eca82f97be380431660 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/072.npz | 6821733 | eaf052311a125c2692b3f4276956fb75692089fdbdb83f08ece034753b55ef2c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/072.npz | 1079509 | 04728a7d1922bf61d2fbbe270b4c9f2f168c2d0337d3363b51454a90fd1b2a2b | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/072.npz | 1081853 | 801a6a5d3c0a86d16b5b06ff2f7add79705780a393f0f45d949f6498258db94c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_073.json | 4258 | ed204f1f1a4949c2e89d3319e90dc9470fcaaa450fee9df6c839c3226376d19d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_073.jsonl | 1153 | 27ae379de5e1027b21547abf61c7111c0a4447fa8a9873ec1a3193828232bc0f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_073.npz | 3790 | fcc2f17c4d529418c61697b3933a513d84314887cb34f4eaaa7eb8c6c523d8d0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_073.npz | 2726993 | 50ff3cedafa6b09b994f5189c8494a288502ebf9ce7cfcca1a408053240ac634 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_073.npz | 852 | 113aa40394974e7df2ee7c4b38da1c39a1a7542816215afa1cefece9f523ee7a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/073.npz | 6817438 | be58e3283e2b0e86781a8bc23105314cf03dd486b38ec9f765f92f7b7ea011e1 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/073.npz | 1082793 | aba91c76c7840c054941b49f9e9f322b6d9ff68b5882ddb3e595dd2170773186 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/073.npz | 1083138 | bf7fb099f5457a65652e7ca044f02f1585217596886a938f5e0f8ab4c95f46d6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_074.json | 4242 | 38207f5f450aa446c0c0aeed644c47143daad71e1d436aa2aea3c8a3a046179b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_074.jsonl | 1152 | 93a7ed9cbf12e410d50c843a13f7c212223954f7bc56a1b18816ccc339ac6bfb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_074.npz | 3790 | f36de1c7c8d7fa54b243aa7a8bd4810aaa83a9882d295951bf9a790550a25439 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_074.npz | 2726993 | ffa3653ea9054bb1cbbade806470fc890712afa11f7779bbc9c359fd2acfa1bc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_074.npz | 852 | bd2987abbe9a7903761519fb168c84e773e40b199a1af01939b659da1052ba94 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/074.npz | 6817021 | c1e88cf661ed7d57d1ff8c9655ac8cdf7e014e8c82341d1e266407447039906b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/074.npz | 1079209 | c658688cdec5561113c97e92ddbe854ee9a309ec2d178b8e100eed8b04bb45c5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/074.npz | 1077362 | 9e523e1afd831f1326fed851395efbc6ed97cc823a659eb0b19d26487b0c09c7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_075.json | 4262 | a209ef8e367999d24fd21b8fbc9614816df635822751ddf43a3f29023eca1870 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_075.jsonl | 1152 | 2acb959aa4eaccd729f1eb1e22b808fb28e08e2128ae92e9c266ce84d563c917 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_075.npz | 3790 | 8e1d55163b82c4ddf46da058fb56fa78f1a7bb2a07ff16a9aadd205d59264079 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_075.npz | 2726993 | a5ef1f3c9c94ea910eb1768b7b26c748acd51c5af35869f88c8268867ce98d32 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_075.npz | 852 | ce413cd6253c7e1f51d985317c567e6258a09cbd9c7d84e327dd2c2bca121ad9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/075.npz | 6812308 | ab5e5d30da50aa0d46b44f41f8023ffbe97c5f42d0b16b867e623a089ab91084 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/075.npz | 1080035 | 3adf8c14dc833e34cd93dbd571417a8b6eff3348c7b60d315ffa0f24168db971 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/075.npz | 1080705 | 0301ddafd01f370746b82566f050119e29cd181a7fa3a6bbb6d079a5fe16dddd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_076.json | 4257 | f0d3e3c915b007fa5a990d155bc6ac568f2257ad653b00605a1862524f4a95f1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_076.jsonl | 1153 | 64ada15e82673e64a08f6b1055cc3f67223b2983be13e40942382850997d1726 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_076.npz | 3790 | 13cea3769db8c54805af45f91c0ae914b168cf884318de3da638e398dc812749 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_076.npz | 2726993 | d84e4c81f2058d8ee7baf07042e9575f4ea61de2f31e0b6c17cfe002cacf9a4f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_076.npz | 852 | bbbdf986c1bf6aa35570926c3624cfcccb651147f59dd6664492d51ed01f965f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/076.npz | 6822605 | cd3a5b3a9e489548da81b396c7be182a5dc3a9a64972d20ed2039a7cf8c49547 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/076.npz | 1084425 | 85dffe916691ad056a827b8228d7ec2b47dfa999b4a67ee1e8e7dbe0502f0826 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/076.npz | 1085866 | 92948558bc7d592404f41f13e10e046bb1f83c407e5c5984b8c78736e96bdfcc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_077.json | 4251 | 59ae3356c14ea36a02454d23f1c77e568133dfdd687b6e7a73fc8d5b5e9396b8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_077.jsonl | 1152 | 8b6537acd319b8dfe71000f96caa80ce7ac5a3088fcca52c969a53fc795163a2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_077.npz | 3790 | 8d4d01700f1e9bc448616912642c8ce1facb142c15ec260e46b0208eda01b9fb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_077.npz | 2726993 | f5dd0762d6b59b30624f01ef695c490824dfbf3d4020197e04e626ba6795bf36 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_077.npz | 852 | f8dcf8f7922487661b8ccd86e0e5ced9a00b59d741bf0892bd89a7bbd1efc5f1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/077.npz | 6815613 | 56e6e8fc3c65fcd0663502bc3a19edc1b85e964462c49dbbcb9039e9f5a7c1c0 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/077.npz | 1076300 | ba284a2d74270fb95968d1ce05a6a0e98c6a08b23a5c4927ada7a2720a7d3e5c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/077.npz | 1077753 | b016af56a0fbfe2ab800044cdb7cb51bfa036bc035de9d08e80d72c7a322ab37 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_078.json | 4247 | 90ff9d5712f760b663d3e486bb17a06c3a5ef668fb471bf4327429808a86b069 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_078.jsonl | 1153 | 55407eff2bf7284a22cceb3a10278e55c50a8d9a455efdd52ff80a29624ea08e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_078.npz | 3790 | d42e1b8cdd1121a82b9b11e137e6bdf34349a50cb9289f51ebca7581e4df7a71 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_078.npz | 2726993 | c38e93df26f7a20798cf4c97ad2d3ffae4871d18f31d190cba3e150b3b92d4d8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_078.npz | 852 | 5d71042213a0fed313122d199b1fefe7cb3e589645f1946f128183fdeebf217b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/078.npz | 6816728 | b7f860ee4869399ada001bc6b49e1114c15719cbd286708bc30dacf82aec0152 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/078.npz | 1090198 | b70b8ae5eb33ed755afa9d82747698304319d6645ed4860d27b43b88318587c6 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/078.npz | 1090780 | 82f69d3203c17259b1687bbd9c0ef3203da32f898efa1bb16b882d7161c9ce93 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_079.json | 4243 | 3d3b0250e309bd4dee270a3055146e0cfc55529497dcb33a345645bdf0611918 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_079.jsonl | 1153 | b3045bdaf7e8f47f07bbcdde3d4b3571f7c8d77a440b74b2aaa9abc32c0961cc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_079.npz | 3790 | b78fa4f30c16fc688a288444dd5d54bb96c64b544a5327e51820bbb05811a92d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_079.npz | 2726993 | f72317b77c1d26e5c7cbe82b22d62cac5856f61839a0aeade4ddcc51560bce57 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_079.npz | 852 | fe56b3ff94c0159c28c4f567f3ffa98ebd851e049017a0efde76383dd022f70b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/079.npz | 6821354 | 3ce434dbcd02a450eab6573d190df661de3a6d89ff30e83aa58f54e703c250d4 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/079.npz | 1083460 | a50df0c1e165022b4390329474c53876dfeabc554f56cbcc38a6582627a6d099 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/079.npz | 1083579 | e3f462d932d1f3f3a53e8f7553f0e09d24a09025399edda41cf7caf6cef102ba | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_080.json | 4236 | 7a2c07618f059ea1c7017fe79ffc7201f4d62226118b4c5580862736579d5c95 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_080.jsonl | 1150 | bbd609ce1272e2784a0cedbfc7db0fed77fff42f96d01da441110bda98552cec | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_080.npz | 3790 | 5e504045db9c6ba900f883e583cb937b3bffd8f4bc646cb04c039862d7bb8f13 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_080.npz | 905681 | 346c04e93254a079f94d390792cac0144e38628aca4612918caaaf13db77f203 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_080.npz | 852 | 49c32734b414da023e3da62cc7fd299e793a51d9d33605eee3fa9e2e9f309e7c | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/080.npz | 1744535 | 7f816bd27884454b262fa33ac06c94d69890f027e77db06d75a1937b61c3cffd | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/080.npz | 294884 | 51d08babcc466d334447a1b2c061e6dda56108c8b8f5ade16590d40dc51429e6 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/080.npz | 295058 | 3232a9ef51eb98f9f39bfaf0541bde96f08259a083edfc2f1c37d0620b15aa67 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_081.json | 4258 | 0838a05219471432e34aa54ad7c26b2751a1d1e375aef6e4eb130cbdf0ddefeb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_081.jsonl | 1153 | ee15f495c5589a835515e4f1f8682cee716aa78561fef735116a0a361d26abcf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_081.npz | 3790 | 0111b94aa762cdaae7dd7a3b4b39af8b87b7767f5b02085dc0fc7ca2a08d6830 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_081.npz | 2726993 | 6b9e0904a822f6b33464280cc414d6888c57cc4a303be25dcb847f46d482e5db | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_081.npz | 852 | 541d5da2eca22cca937762ccfa41a06a16bcb2638ae551a3dd16fd3bc280a549 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/081.npz | 6826197 | 361d567346c45a5913ea3e094f89e2df57ff84d21e29ea59c6df3d39bb37ac9c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/081.npz | 1072404 | 8db120cb02337d59b7e08166a26011a3a9655e0ec2440df61a907f9cb566dba0 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/081.npz | 1074218 | 34fecdb096afd65b8d999020a1671b8abaa828626be7ec1d0fa4a0c54c9127ca | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_082.json | 4255 | da266eab379e28470350249db6b46b6844598f6f823003f15ab9af301143dfba | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_082.jsonl | 1152 | 1cba9b18f3e59f993a768404c64c911aad46064b87e176169f2b12bf882eb8d0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_082.npz | 3790 | bb20bab0491c311faed249f27c804e3b93a0f292074f25f20c714f67ce39812e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_082.npz | 2726993 | 90ff23410c685e626c25aa39843859b35e9a3641da2b5fbd84d7f23c6fa60040 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_082.npz | 852 | 48c32be11f5bad3d565a3ee9d451305c9da52882e733699b21eca0f222339b21 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/082.npz | 6808198 | 8266d69eada47b8062ecd63b2533c8de1ce0d24b989656bb3ed3942339a84817 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/082.npz | 1081674 | 82c5b070f594317e8bb93e55ddfbd7a7c5c704b74b49c5e0c59af79fff2e69a7 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/082.npz | 1082687 | bf609f763cb32ffce94ba046817ed5d58851d846abaea8c104e7e9f2c2d84e89 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_083.json | 4256 | 822a9203b63fb594cfed68ac4a6079c933a5ca2bbd0a3535f03f850bb8a8addb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_083.jsonl | 1151 | 6505e59ea55c9af89aacf415711eb9a5abe04d675d5a467182db72a244ec87a1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_083.npz | 3790 | a6bae8d9fec71be1b2c978920368e4cfae6cc8c11d873738d03b4c826da75f36 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_083.npz | 905681 | 32f6611668f06867e1ff634c07c0082f80a6f85b91ed8e777cd29b895870e997 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_083.npz | 852 | 320dbafe2a46858a713d2261b4952d838ce23ec3afff8af670bd2e963c2a3a6e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/083.npz | 1745858 | 416c967814d765bd3bfa4195811d45ecc2af64ad77f284b94129e20433fa4aa6 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/083.npz | 296631 | a3c185359e86173e46a881872f09920904ca63af804995791a20ea30aff4df8f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/083.npz | 296500 | 51ce0c8359c0751b0f987d42884f93e6d792f1f7e642be699531edc6ca4ca9d3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_084.json | 4250 | 45ae2d1e0b3c079cdca8f0e42808232d08d5118153d84a30852d3aa766033bf9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_084.jsonl | 1152 | c22be1bc60e4c7ca6c268f7691be85f88e905544026b27990523a334b124272c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_084.npz | 3790 | 1921dc6ae85a28f73ae702040795060e24556773d8c0dfb240c43e36b6d5a70c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_084.npz | 905681 | ce48513efc438b4e21b3539cd514517a491feadec2561835f6f34c5f6381eba4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_084.npz | 852 | 852eb834f05ec85f19f2a5c6b245804e84c16ce7d378530ecf246f85c14dc6c3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/084.npz | 1749834 | 84918e01f041c76b5571add24d62f6a59efd34427b2b09d8a26ab73a661b4637 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/084.npz | 297434 | 72612bd2c8190f7c66935235c98533d080edad75b3d74e2dcfd3847e2c9f43e1 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/084.npz | 297369 | c7524de0974d1f3db66443c2d150a33ad675720204e20de57cc5ad3c78f343a0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_085.json | 4246 | 31037fbb2787ee8c53b8e4a0d30bf0211c015129725f4e2266394c4fbf0a6eec | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_085.jsonl | 1150 | 97d9dcb033a30ce5a4c0c246a9c6ddf8e7121b7a189455aa722d89d68b8696b9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_085.npz | 3790 | 220d7a8f5e198d0c032448afe6338a7884485f44b35720818620a201e801d030 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_085.npz | 2726993 | fe636c43b1fc851e8a7b3c62962611a15f3e95e0ab66eeb1760e2191d7e76d91 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_085.npz | 852 | 726fd187084f09455e96cc32a5252cfc15a4bb9b3d4cac7446a82269f63430f2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/085.npz | 6815204 | 6aebc3a81174fe40441b9be58a071f9e9e6770255e2f4da9ce7d4b3123883dc6 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/085.npz | 1076321 | 9182b08b6dffc5da4835e4cb5060026c848e117a59527537bc5e9d8b6cca535a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/085.npz | 1076932 | 0685a24dbc18eea24d24b0d0e830796fa5bdb5ee54be02085060d4f6eb0a1ebf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_086.json | 4253 | ff2a917f27ed287f2894dabae1a436c4482406438e2f1a8b8e88a9578f36507d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_086.jsonl | 1153 | 5f5676015702b9ba6d9feb89ff0464316999efc81d60f02a05c95307066a7e33 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_086.npz | 3790 | a4ff50eb37c4bf13441364ea33868c573921840aa49e36f8f2ebc4b7b85deb07 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_086.npz | 2726993 | 0693f6124c8df74e6588ea9b8b53cc0f9150bc83403f05c99d0ebffab7215b0a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_086.npz | 852 | 5f5d919d04db423daa18c0d40a3d006253ed2f035645cc1f105d09a25961e6a3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/086.npz | 6817651 | a0929d48ed8decfb1e126a41d5018c51054df250454f1f5d10704fd5af5c3258 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/086.npz | 1073261 | 312aa0bd009aca1704548869107c839f8060cb3c101c964fd76675b20fd9734d | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/086.npz | 1072752 | cd6ee32ed326ea025ab4e4d29095ecf8c1ef0cdf2468b3eea1e43a579056869a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_087.json | 4254 | afd810cde5e5494ab2f10e6bbe066e785c35b7d13b4fbde56694af1369a688ff | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_087.jsonl | 1151 | 077f92e24249a0b18333559f92e2e40e41aa3231ad26abbd40703590031b4abe | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_087.npz | 3790 | e9e43fc1be227e5e3afcda9eff9946cc98d4ab31dc9f13c34aa4ab8074886d6b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_087.npz | 905681 | ea17c7b186b741c777290ea382cae9dfa3dd93d78b5b7355b1cdf5aeb7cdcda7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_087.npz | 852 | 229666b2c5857544f3fe77173ffd3fb004ce57e07d864faefbed8dafedb64702 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/087.npz | 1747290 | d00449f629124939b2286af6094cc5a7edb06f34eb64aae90c412c252e54e2b1 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/087.npz | 297468 | 5c854e73913b0dac4d15f9011dd2fd90cdb65bb23c0a9689239b6138f619a281 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/087.npz | 297144 | b583c732e186b7a380fe6bec45401f40839a073355915afe800439c3df865e9b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_088.json | 4249 | 0a98a77dac850e5037c6adc0955d14d1e06d4e7b22013203a16bb2e7dde3fca5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_088.jsonl | 1152 | 7f0721d075a00d8417bb85683b5e6d988cdc3f1a49290c21c74e96c0319b2e68 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_088.npz | 3790 | dd0bed55723124d9a42e4d28a2c1fc1c0a1ce64354676ad99219a1ec96c077bb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_088.npz | 2726993 | c45abd8d5acc1e71651b0b8d5882527c8aad758702e2c66f0eee46fd0dcdba1c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_088.npz | 852 | 90ec4687bd8a4845302ee3cb8d5e11726d8b09b494d7e06b0fcb7334264b03a1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/088.npz | 6805883 | 4794435578436545e8c9bca8d981b13e7049fb7d1f3d49928084d02b4a2d1fab | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/088.npz | 1078082 | 19045a9acf7456cce05a52bf054c4f99fc168a24ec09dbc1eca97b5fa72d2569 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/088.npz | 1079704 | 786385b57ac08974207c8de7689e3d7d23aa0a9a6780c725af3a5d07040bcfe6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_089.json | 4243 | a18cc2ee75f77610a3e111ea1feba3eeb7964012c6af4eea35ebc29f700ec04e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_089.jsonl | 1152 | 6468dbee2fd9e7e4bb5b012fcb0f2a50ff530b4f96350a168582d0846d8a1c24 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_089.npz | 3790 | 42269a941792b06e1a214861028f52293809553f8409274a70f1a6271a0fad85 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_089.npz | 905681 | 9b5e8c78936b9fda39430c5c13ff79dd6b02f631f2a617a4e787ba1c1e660b77 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_089.npz | 852 | 9610fbfcab27a5c98f01913d1c632063064f9f21fe511cd44b9c7205e6eedf51 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/089.npz | 1744556 | 8feca498225d3d7cfb9ec379546e6d58d56f026564322e30333f40c1de689eeb | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/089.npz | 296306 | daba7c13b058dc5570324c246fb8698fe9a80fd0d12ee1f808a119046384e783 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/089.npz | 296258 | c364a9d0cd1c169cace8f474a026ab9f950e135f9cb5e3493911d608f23c066d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_090.json | 4250 | e671a934914a8a9cb76332564abf51eca0e6b72e571eb1df2602d355d3de89fd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_090.jsonl | 1152 | b167660fe62626961341488277dc69daa11d4ef86fe3f986fdd59a81ad98077d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_090.npz | 3790 | 35166b32bfd294044f8c6d8dfb9075d6b4ca69f1b964de5ce4304cc6974a7993 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_090.npz | 2726993 | 487b661644d87c23ed14db6f935b25c963d50566e69a352f6d30918e989f6510 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_090.npz | 852 | e12316bf764035249560ebb8def1b6525592418544ce4f5ff43df9ba87a0d5ab | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/090.npz | 6813801 | ab6c2099ac535fe5fdc840fd36a09faa06fef85609ad25a7109a03a56551456f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/090.npz | 1079949 | 824771aac10f7f40bdb0b26eae253ba4c3b7b6d2eebeb84919a31b6e94d8b210 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/090.npz | 1081912 | 4d0a37431dc4960c47a6b7247808216940a6ab83d693625dd3eaa074922c1020 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_091.json | 4255 | cae1e56a00745e80c6faddfc10dc2605a8f1f16e8e46a676ff2abedc2341a1ab | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_091.jsonl | 1153 | a710ff1f89c0da71baf2b38d1b5eafc28570ad5756710545c6c0a3078c8348e2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_091.npz | 3790 | 18596eb23a49f2595eff2acbcc01e487591e40f429133b4b581ef81f891da667 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_091.npz | 905681 | 4704e141406ccf5d5d54151d24320bd37a4b089745b7c898cf91607c79da0420 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_091.npz | 852 | e133dcb1ce584d7012884d6a1f4409a90f18a197e7c99b57705534953bb654f5 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/091.npz | 1743342 | a29ab4de9fbdf857145c6f5b31605b8dbfa9ee981554931419123009de63621c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/091.npz | 297485 | fbac865a350e794c74919ec5190932a5596cf950629a9c4381ed3789ecb91097 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/091.npz | 297183 | 2560105f96a270d0de91b5588977ae34a8a53e7a731c794622cca4c38ce78119 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_092.json | 4259 | a5be220eaea93594171c691df94ee16ed44ca84f9c4d8e697fb460464dd46643 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_092.jsonl | 1150 | 56cfb68bbefaa3144cc0e1d81dfe2f32f33dc3967f08a2718c53eb91f1cc323d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_092.npz | 3790 | a4b564e0334f6b70cb1df4789f1ff60a0c5a419afd77ca3d18323ca6061c0860 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_092.npz | 905681 | 8d0ae49495f4fa472c8befde331cf1c653da3c54529b0282cfb10c88e241f667 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_092.npz | 852 | e4cf9eec89309afa3c074122c23d11acfe0a024b389a600347f76bfde0302857 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/092.npz | 1745312 | 3b37c061ccfe94b35c6641d9e85f9601f4e66fa99f2c381f4d4c1500f2da11f7 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/092.npz | 294941 | 86ccf568092b3cfd36c0c83d80c80453bed7a6d04dd80f2f9495b4d766c7a5a6 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/092.npz | 294816 | 2d7324ef6312205bbf9dbe7ef917b9033a3d7bb211d12acd050540d4fe56ab5f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_093.json | 4253 | 8a28e0ec28ddd1349d31bb0ebe269a60f7912a73cb6fc4b411f424e5c1374b59 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_093.jsonl | 1150 | 541438700f8917423101b13c17dacb35b7031aad1a0dc8a79c41c8ef5960a5ed | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_093.npz | 3790 | 595621f42fa1e13fa03f2348ac5f1b774b804f9446e971d2ee6a956dc86cf0a0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_093.npz | 2726993 | 11060463e72636403cfb3382ca897b5748ea9047ff690c239336002a36e4d6e9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_093.npz | 852 | f223c7f23cc6149347f585d9350f43a8a5a686ca6be878d13561bbfee5f0084f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/093.npz | 6813534 | 849f47ac77205aef20236a9986f9d75fd7c39e037e3bc5383fe3295d29c49af8 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/093.npz | 1076506 | 21470984b40d6c2ae3b0841fc6fb458379c74705e0453fc02b286692a48dd452 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/093.npz | 1076757 | 9f0629c39d40f9642b7ddc2613fab63c10d2b614dba2f67b7af9aa15a9b06243 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_094.json | 4249 | ea20bf0b152292a8a93707447faae0c0e6ff0229092d9e7bcc3adf3ee45f840d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_094.jsonl | 1151 | 972c8ece05dc53e5e7a1f4448932669bbb031323cb067d7eef6e255342b54d17 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_094.npz | 3790 | 81d3ec94d3fc7f66bc752b49038e51ae2ee807ab6c69c27035f98fa80f2d9a5e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_094.npz | 2726993 | 254429e087eddd776760ea1771d95e9892d708889ba31f19443c052492ee665f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_094.npz | 852 | a5626fe6597bf7e26ff0fb4cb2d5e33c94ce9af4d722e10ccce14da1960c79af | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/094.npz | 6818105 | 90894598e5f0f603a6a6e0befdb5138787a0651e13ff4847bc63fbddc9d476a6 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/094.npz | 1073592 | af0755ac00b8bca023dcd0f10216e1aae87b0053d4f3c494b89ac0d3e72d7e83 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/094.npz | 1074728 | ce322c1ea9f2b7c63d2b5a95543934231092e2605c2fd8049b9d1b4d63db48de | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_095.json | 4247 | 6df90f8fc7370f02fa1a7976f05a8872ec88e84b71fcd1e1ec21c2a7aa44d3d0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_095.jsonl | 1152 | 7fe0bdd86fc485abd821a256ebb9a904a644764b6f2c5399397535cedd5930a7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_095.npz | 3790 | cd1428ed4c450181ede80c7ec726c388b93bd8d9e5df370f23db7b3e5b14ed85 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_095.npz | 905681 | 101ce8e3af0ddfcdd741888387998a89f4d1f2942b911a777cfe778e253cc369 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_095.npz | 852 | 7f4cde3e6439126dc90d4b1b2c04c232a133ba25ed55278a816a4b713d6b4406 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/095.npz | 1746106 | 693eca1c82e85d9408ba4d67e6762cc667b288f34f504d73ac4af6c51b8d5ee0 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/095.npz | 298570 | ef1a1151d4256ae2e9a788d8c8ab4f47953d9e58920bffc25e4c0c8a2fe95086 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/095.npz | 298697 | cb0a364af85f04c9055fa1836461434067966e1723a16154be545bfd6c5d9c05 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_096.json | 4256 | 9294a96a3157f80c1a20780c6305dc3d4d02af5d210dba68db9f35ef5bf6e27b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_096.jsonl | 1152 | 95c7548e574ebc8f7afd51240a64d06881b5cb353ffbccff0c8324f3b1202df0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_096.npz | 3790 | 6c69bf91d4dd750644003f608595e2f71c2670d9e811980fb2448830bce43a71 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_096.npz | 905681 | ab84f4a674a249b4489d032bb49c3e41adf80f14b7d8e5db9df40bcfc0dc07d4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_096.npz | 852 | 20e6f43b3a221d76430bc5817e423147dd78e57321bd16aa1086a9bec9ed3e37 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/096.npz | 1748678 | 15c191331c714b8fd71ebf557b48942487f9a9c2ada74de09b2c7a69ed3cf629 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/096.npz | 296679 | 5ccc8882c4bb54a5fe7d390346240450242793807c93a851609dcadd5156a628 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/096.npz | 296938 | 7f2f7e655c5fa6ab23269d65a3908ef6db35bf38c3ec2ebbef037de2ad7bad2c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_097.json | 4245 | dbb92fa0b72b7dc905fca25aa4aba1d939fa811000337cd236b9fa55164c3d42 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_097.jsonl | 1152 | 3e287862217b8b478550a236d72a6b357f1c25d09c564e9ad818a53c23641ee5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_097.npz | 3790 | 1119b94dccd4c6d4e9a45189875eb3dd530b1cc8fd40b72e797dec0f1b9d101f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_097.npz | 2726993 | f3b536f6f45d507f0578d05f9fc70a69957b9fcc0484211cddb2da20f0ff8740 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_097.npz | 852 | cc22cbcec80cb1e0ded69f4dfe89ac01f0f60b7fa67d426e0432bef8831afbb8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/097.npz | 6820488 | 9ca78bfa0bfd4e25ae99ae65d7deca468a0b518bf1fd5cc29cfb17856372df60 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/097.npz | 1078874 | 768fe68cbd1e8db54f689762a9f4447d64bbd7514bd152ee4ee110fbbdc0ece6 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/097.npz | 1079043 | 0d68a4cc31b6f722b0c25b8d58c4ab7e03e02b8686c8b70e846ab4944b1f9031 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_098.json | 4256 | 308d1a9d3abf5d9536f97d84d3838c37fff167641cb78c24455d306375a293f6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_098.jsonl | 1152 | 66e1204a29ab827f146e4af13bad57912213bbcb6d48d9ea6ef9f5a314f8f3fd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_098.npz | 3790 | 68c7f29de5e3328aaf4b151be4dae9db0d1aafbfca2a9cb65da55eb1e9168baa | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_098.npz | 2726993 | 67219062de344ca03a25a8681b40f1864e0453b6fc775fcb827d9032cdfb566a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_098.npz | 852 | 691de944f6cee66b25a0238e863192552ff78aebb8cfe98c00ccf257c372c105 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/098.npz | 6821010 | 0d7b48c73f4b09511f98c6b67517aaff93a78519025d6df0942da7f5d0beda99 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/098.npz | 1079012 | 606f9061bff21ca5ace95176c42cda196e06a0f3e2f5440ec8da470536870252 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/098.npz | 1080017 | 45f15e62a78e27908baada8a2b3e03394815a241017a35b8b0b7ebcb6d34962c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_099.json | 4246 | ba0d1e0c8df3385002c8d2bad18f0ada6e487c0121110cbf45ea3181e856d401 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_099.jsonl | 1152 | eb3f8722c379b037687cb55429821707a847311a58983b61a6b724d97809f581 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_099.npz | 3790 | 77c44ce7cd80ee1851bb9c32d5f6f51c74008eeb5ebf8204e2458d3988a03c8e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_099.npz | 2726993 | 750aeea169862acefbf12943c27c59c0d23c7b2201126f0e9b75752f2e4a36b0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_099.npz | 852 | 9d5265eb35e2475c57cfc795096cb8e4d6263d04b8d7ecc2d83adbdc9b64e339 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/099.npz | 6814772 | 0a48dd46e450365e404563e77a2f423cad70ba73eadd4914d13cc79806b4aebc | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/099.npz | 1071802 | 9a592f0ad13223f2725179ba94dcf5a2f598d31a0eb72e641e89492264dae46e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/099.npz | 1073096 | 11fa300b9789d087510986b13ebb450fe32b13eb2bc555b455855a7a27bc4902 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_100.json | 4256 | f3a9b6aa5ae3c4c0ac492b13db4d84c004cae04115f6ca4568c546833e0a58df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_100.jsonl | 1158 | 9ee518ab33032da38b831fb9132948437485b8c30be96cc1daedd282ad48f290 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_100.npz | 3790 | 78251f24242203e926e9a9f218372e6e91a09464060c8d4f3555b6641b5cbb8e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_100.npz | 905681 | 3e215ab86faebb7639b51f20492baa714f0ff93ddbf91cddf0efccaaf980cd87 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_100.npz | 852 | f7c6ede6d78ceb38e620230ec17551bca195e130d6e81efc97b6bd33e6196567 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/100.npz | 1745574 | 71d20b1f72b839096c1268ff77117ada1f30ae79053c16c314feccf69ce515f5 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/100.npz | 296070 | c765c1a318435eb7e2e70395da1bd3279f5b907f84b3011f3c55ebb5c89af2f5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/100.npz | 296500 | b7ca3d71c98cc5959d0a24cb26be0a21711239249304c7c24237f8dbb1978e24 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_101.json | 4247 | c2823e5b8349d92029b1c1338d095c6b3778933c0f8f08f6af7511240f485049 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_101.jsonl | 1156 | c7831cca69d81ef7b5e7e0637dda75817b03365e0683c0d223036eb6fdb2fed4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_101.npz | 3790 | 56ea4a8d606cc21a93cee8f0e69317455b2d15661a941af41306c51efc58c381 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_101.npz | 905681 | 6e44a4a3c5d7b744d02f7c0dd87e4123ac4e1b4fc46970a7947988575e6f5caf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_101.npz | 852 | 87db5deb07b38a2517fe6f30a2714f6844e66c4161ee98e89acfcd2088d425c6 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/101.npz | 1743188 | c3064d2daf5fcce203c4ce1fe6f215365a4752a8a93095302620d94c7c720d94 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/101.npz | 294579 | 73398479acefd8411c93a32916add3f9bc2aaf20842534b6974f5f65292e483e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/101.npz | 294938 | 46336946b9ad03ad9f4a7713131e517693ef03d2cd66195e3c02de2b94b04ce5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_102.json | 4249 | cb53bf276ef6de6be5d42bf32d85c6872bdb1217f7aaccc939f51506adf20c40 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_102.jsonl | 1157 | 9c59100e96d5ccd8d40d15de04c6fa94ec2196c24c2cb661b33e970d6571a4f6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_102.npz | 3790 | dc3b026974a1d2ef4fbc7bab3cf910663f23db7a4d8681034c9e2684ae31b708 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_102.npz | 905681 | 7ce4b7312634c49503211c3d6f040c194655d1cc290a5d899a5a5c829b29b0da | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_102.npz | 852 | a5394a7427af4f07c761fe6a425d5173c93326b88cd2b8337db0dc98bc2fa367 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/102.npz | 1745248 | 5fc340789ee03e4cd6043f02e8b8943539ecccec9d1502806c5e0d71ccef4170 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/102.npz | 295307 | ceac282a95057e860e2f0696c571d1f2354f417bd0ecb549c6e855d38796372e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/102.npz | 295381 | 271f61a1852e0fab81e84d092b392c9924eb4378b62c37c6cafe1712094b706a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_103.json | 4249 | a43925cd69576752b133b1252872afe4e18b49e65c9c652ab5113a7575cc2089 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_103.jsonl | 1156 | d2afe52265bf1ffd3f811fae0ca9ca8663fb0d2661a170ecbec4e756364380da | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_103.npz | 3790 | 4ad5bd1a59614be6a8447f51bafd3b5704f28fff2b45bfd08f94f672421969de | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_103.npz | 2726993 | 5911e2f4a3346cb7f73bb361e435a6dd64658c799b974034082e8e93e461cef2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_103.npz | 852 | 41afeb4b74ec0fbfe61658773a4b86272a0bd9bb156d8f42db42e39bfff9c47d | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/103.npz | 6833747 | c0bbeb9aa6b2cb8bfa4e739c9ce605dee71e59cde56d0c8064e55369ee63aa64 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/103.npz | 1086355 | 4ac5c12174aa2ddd4f9988c9d751d478c415dfb32354271c76bd0e8d2799013e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/103.npz | 1088005 | 9a68c4dce31e68ebae2ca6a0faf8a29d799c250a4d61669720c0aeda9c880d0e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_104.json | 4254 | 3c1b767f0756d91b02e480aae49d034f0f350e75c9bddffa543bb220fd041fe4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_104.jsonl | 1156 | a4e7ed411599dbf5b2610caabcf14b355f191aec70e56131a7f4348d619d55df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_104.npz | 3790 | 34ab5dc7c386e1f9912750c87fc232d19a378355a49a95ed2f71cc7166861e3d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_104.npz | 2726993 | 84cd3bf0ad934a5c5a1725a1ca7e095a7e8fe8694b358ab35dafd6697b0309d1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_104.npz | 852 | 4656a3a86bb86b54ef564ec7f2aea7e5acd0fb03f199504d1f0cddb3d91ab651 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/104.npz | 6827311 | acafa97720d4b492875d130be25880de1c04f6d85d00848ae0f2e379570b6c7b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/104.npz | 1080033 | db791284a6c585ded324c847246b4a795f7b85765e1573f769b33365ed5aad6e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/104.npz | 1080782 | 2a8bcfd0cbdc98cf898fbbf73e73cb64cd0bc2d8e4e393adb04d577df8301920 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_105.json | 4251 | 8dd041c38ff7faf877ffc686895f92d8dff7c4c62bcb020bfb255ea6e3ffbbaf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_105.jsonl | 1154 | f9c9f182d757690a84cbbb51bf6cb34381f05e25b1df62e7cb41a0d8851e22b6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_105.npz | 3790 | bda1386618df99de4a3c9a50a5d58987175859f02ea4b57d39ab8c0137cc5117 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_105.npz | 905681 | bfa8c4ccf55646c958f6b6de668a267ff8c391567246eb8f2de01b5762eee405 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_105.npz | 852 | f0c8030b54bf46c09e7c50e3f4b55c5339b65584daf3722ba021cc10766b2da3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/105.npz | 1743767 | 5ee1649cff2a71f0240ebe83eae371148ce81f2a500cfe5b2002f0c9d6488618 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/105.npz | 295617 | 91f7c35c186619d8456690423af4261ed8826e63aa7879b9d9156615ab3c0c66 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/105.npz | 295802 | 50f00b0ef6bb284d2172d8c0f538a3f9bdb592204411f9c45d701791f451ad0f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_106.json | 4251 | aef34e644961ef0d09219bab512b7341d175f2d74787ba2d8b87a535269f5cb4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_106.jsonl | 1156 | b57b1b2b6981f41df487d550d08e6a46296a3e5d12773aa09fbd312a2f982704 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_106.npz | 3790 | 9f0f99aef7b59fd900e51d829afddd27c270816347d4a9a26e0904674dd5583d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_106.npz | 2726993 | b90f20efcc932fcca3c7917ceb06c29e8a373da04ca8e519d2dcbe0aa2087b75 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_106.npz | 852 | 99afd0aaed5c591e6158176aeb46b519cf5151afb8180ba54cb11d102282b3c3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/106.npz | 6810538 | 10349e7174a8918fbc07a733cbfc1dd2166dd3eade8b44645f093cb7735e186b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/106.npz | 1073379 | 0ca92d916c175b0c1d8f4d9d9fcf26aa8c7f502b9718b70796f9ba68b1a19668 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/106.npz | 1073289 | c540af1d0cc789fb942e63f0a0806a6605887835a9ae72c1d3c114fa9e899377 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_107.json | 4251 | da58f21a859211143d10f573adfdb347b02d53ad440fea667f18fde88826e214 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_107.jsonl | 1157 | 3ff41bc9de76d365da972dc434577e3dbd53437b7e3e07c287c0f4e69dbac88f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_107.npz | 3790 | 9a4d4b68d8c7540691848875dc3bca70b6935ffdbb3fe22e76f663d9f455b334 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_107.npz | 905681 | 53e1f3ec7915356f5d0b72a2dd9ee5192ad87536d4535b91d28e9d2bf67853fd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_107.npz | 852 | 923e4c7a88e40a8fbb7715357d73b2635124b3cbd7c31deb8bc151b51f4fa173 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/107.npz | 1749749 | 34d5ab6cd923a19b401600992a9feda80fa715eaaaf537cbd760f1a5aad70967 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/107.npz | 295394 | 6ef10c4261843370eb01e6443d408aa9f325c7979134a4ab673979bc69727c0f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/107.npz | 295484 | 851bb892adeceebcce96e6cf89945c94277a5d6900dc031710567675fdfe2e5f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_108.json | 4245 | 2b614333c002e901af223a94dbfc176b2f0e8e30c7b3a130be68dd113c19c72f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_108.jsonl | 1157 | e97b17d9265ef505b9b25a8403e1c1ed5ee748a7d68e7f06825a747b96d7b753 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_108.npz | 3790 | 9c1f75467469eca71c60af8fbb379c83579e7cee800d0f0c92adbdb233c2cb2f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_108.npz | 905681 | 18ded3b5722e35791b9af1ee303b1a82abffaf4576fc0c42a7f32f0cfed94bf1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_108.npz | 852 | 20a0982f30411876d147ce7990bd8c322750bb4bc1eb09ad79ed02d405831eda | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/108.npz | 1745169 | fc875226989f7ca6c743d4771c220522c4242612df72005738be0384b9ae2e94 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/108.npz | 297545 | d5c35d90759d12ee14ed7340d8e865aa68d3ae5088007ba20d86431a267252f1 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/108.npz | 297615 | caa7429c480ab8178b2ae4effa65d08e2c247e2977da47649bcad2d8b24c14d7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_109.json | 4248 | f90b50c467c8a2ca3b8819820705a3176036f498758fd2f7d5dd9cc5c078882e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_109.jsonl | 1157 | 085a9d92c67ce76d6821ae53398c7005e971062bf395e3bb19a533b8fc120c5d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_109.npz | 3790 | fdb1d08b0f098f882c75c1a17aae84a3750aa5d1eb8b6b53864dded4936de6e3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_109.npz | 2726993 | 920ff712853d998fa73e3b0c3eeffb28b282e2782e99eaef838b2e2daa5b0695 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_109.npz | 852 | a7ff70d99bcbe9efc92e6598b3818b91aec4aadfb33e37eb07ee0ca7d0d4609b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/109.npz | 6828690 | 989d296862a2833d2ceee6901e25b84556ccad8508a63eb8c19a6b5a97602e27 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/109.npz | 1073165 | 63b6ddfc0bb1931fdf466541755833be415a637afcee75fea134789b89f148e9 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/109.npz | 1072845 | e92eb4ab727b5e46acd2445580a50255dfa88c43ef00717e9a5b64230e425767 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_110.json | 4258 | 512602ebd9cc3991803e84e5609d93d06a9a6a054bf3d642aefa5378bb0f108e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_110.jsonl | 1157 | 5582527cdef8d4a31e91f2c5aaddcaf8c36c57688566b62d98d70e2e0b028673 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_110.npz | 3790 | f48e0f74c1ce1d0fedd258cc8961eebeffc7b1285137e606fe115ef8d13cc0d8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_110.npz | 905681 | 053d36ded915c66031c91e724689593a1aad535db50a7992c42830b338629e46 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_110.npz | 852 | c6c598dab86dde471f3c84089747c66bdd09817a2aa11431ed97a681ad165b3e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/110.npz | 1742978 | ca3d289125604db214a54901a3664766dcd351d693de2841ecc4e401b5553fe2 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/110.npz | 298848 | 6ac5ae8b40da1af644bee70ab806c14cad64318bf6541bd79c994f3c8fc87911 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/110.npz | 298956 | 1558a2ecd2ab30f77e2fb2b68d98d58f90f56b0d1634bdc028e339f0432bbac4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_111.json | 4255 | 33db22a68217ab6eee25c1ecf6d5b69173b150f094015401c74be45dd6c955ed | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_111.jsonl | 1157 | 50171f2926cd1b4dc800116f27cf87423ae35444f65e151ffe8db774f56fa730 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_111.npz | 3790 | d553bc1984ce3663c2648d3029ab7fb31b335b1e5e32a5a9281f2893613b6c73 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_111.npz | 2726993 | b5ecfad13e64aa8c570832cc8f798a49c039823debd51ff31abeff4b3b04d3f1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_111.npz | 852 | 6bf17949f34aa2caf7a443de14e57d45a72628a46cbe3bc9392d79bee09f835b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/111.npz | 6835680 | 6eb0726d01940970045afc6cffce69aece465d8fd0ca9042ae1fdc173222dea4 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/111.npz | 1080252 | f2c8351304f4346284bcb6ebf4c75605ce2f6454c4a75293caba34956208ddba | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/111.npz | 1082399 | 3580c707a3a746edc8c4d18572b88a207c954793e8c698f79b44c1a4c634fa99 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_112.json | 4257 | 0917aa4335c191f60524425e2fb11abb40b83657f9215bfd6c852e5b35149043 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_112.jsonl | 1158 | e937c1764fb88e6c30b3095ea56e114cbc47609f8c5c47fd1af10e64c34070ee | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_112.npz | 3790 | 4bbe9e7f858e36d7f02e9352442dd756e3537aab8f22d755046e78c0527b4364 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_112.npz | 2726993 | 3388fd0293ba89196142bcf3287dfec7784948b5c651573a61e1980a4c7fb3cb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_112.npz | 852 | 3f3ad910ad62f1363d596eaa56804ae1537a4d52217bf723d9bb77fc10ddad8e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/112.npz | 6807385 | 3235ab81a670ee86cb04813c36ac987162371bec5872bb8e3b78bf880bc0fd12 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/112.npz | 1081912 | c36d3081e53cb0dd524a5dda47cd010a3d7f2b9108278bcfd7e424e3346dee26 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/112.npz | 1082446 | 753e3f5f9b12cd24de4e80f579d6987f0f8043096d8696905b1d54503445b823 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_113.json | 4251 | afa98086accc3b77cff16f16e85f3335ed5ad0fcc4f8abcffc27c7e1ed475c67 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_113.jsonl | 1155 | c794a1b0093a17fc62fcc84e9da71c664e5791491c1430de793eeee518e131bf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_113.npz | 3790 | e7b3684982b73e257f2b3729f379a9c3871eef063287704633e59c2a14ac73be | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_113.npz | 2726993 | 5e0990a9627ccd48eca1879052d85cf8500cf1ddaa1e1acf095b4c0e446e9871 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_113.npz | 852 | b10308e0f32ba2eaab4d170c90ea17facb44930f9aa2259a53091d3d3ca30457 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/113.npz | 6817192 | d0e883179869a77578b86d88c78b57399aa28e5af7c5b2e284c8bfbece25fa59 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/113.npz | 1080700 | 22fa48652762484ad843be862f598d3356ec108c2545f454b8fb627b4c8522b9 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/113.npz | 1082806 | 3d70acbcee4be34ec78291366049507add105ec04c429caa4371f7a62280b2ce | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_114.json | 4250 | 53238d49f04c2fe7169f4cc7ef3d6e6ce03b1f488f2a1491ee5253be3061a3a7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_114.jsonl | 1156 | b6b8858105c6d3fb8ef4775fdb9a97d526984555d219821f57c06ffef499b9ac | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_114.npz | 3790 | 1a6bda4eda87aac1d9cb2d814d80d66736fb306bdd6797fe6a663d5b14b96a7a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_114.npz | 905681 | bf82384f93dac6f39bc105cdfbb223fd0b781f82542f0bfa2eee818dc56c3cc5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_114.npz | 852 | 84c4a66d38cb2e9c4eaafc6b40687bf9f1390ce45aa4284f519ffca36c14f206 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/114.npz | 1745973 | 845c88781e49716fd68a6a33aa276b1f4f5406b31489a33883e927a86eed7cb9 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/114.npz | 297923 | 9c3ff2c4ae479dcefdd96c3776bb3f27dcbb62baf6662437c61cbdff5f2cd9c7 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/114.npz | 297910 | cc3c46e42ba9ec50abcf40bbe79505e2f577ab9f2217f402b593498f8f828e49 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_115.json | 4261 | bdbef6b2dbb8c728e862588b1f0b3094f5605f66c4bbd2bdd66c03ce3e1ccabe | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_115.jsonl | 1156 | 15bc72211f5506c773f4fe60f9d99531839b56de8e02cebf918e6971e3c87074 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_115.npz | 3790 | e3e9d960bec66f0cf87c3f7b5e38145cee4350b8ad5888110693cd60eb87b48f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_115.npz | 2726993 | 5657ba3c3ed8563de22356654a61fd1b3c3ff0a4333c3491c041255eb102c9c1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_115.npz | 852 | 361685e96fc25aea99143c9683b724eab62fa22a5e8c69d80543de4ce4f2fb96 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/115.npz | 6815874 | 26db4cef189b7aaff37fa9aae26fa976f4b7615374769fb8c535eb8c7ab20035 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/115.npz | 1077266 | 5e8b23d82c5f3c22dc9b1a4822e80c87bfe96ae20ab23c1a9efb899c7fd58339 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/115.npz | 1078727 | f45899138f8a07ad4038c5840f13e65bdcbe4893f2add332146feee1bfeb2e62 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_116.json | 4252 | d94dce3730baa583a2715c5f90edc755f1d0be28a5105cf06ce5686e457ddbad | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_116.jsonl | 1158 | 9b97c04b24d8232a115f11ebb74353213acaa7308dd8c947f75b474df6bd926e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_116.npz | 3790 | 95b8247b022c3d86a03cc57996d51e545b2fd99c03888783c6b9102a98275d9d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_116.npz | 2726993 | 36aee24aa3a2c7499777263399f9d8708d876f72fe09dea94531e76afbe61aa9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_116.npz | 852 | 1e102191d0da27251afbda453879df273213fb1a5e49224bd6487b4a92a60970 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/116.npz | 6811648 | 7aeb11acc68444e68938a9e29526bc65d6f96d5b5426459e91216e982597abe1 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/116.npz | 1079251 | d9e23e54bf51182824eb2ce989bff343820b28ed7c7a24520490dbb716132ec7 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/116.npz | 1080759 | a3732e577590f3f938a05c177118b2e8599dec6d7bfeb76861f6641115eb63cc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_117.json | 4256 | aee43b7050b51984ac4870e5f6491502cf7229c07c9f729aef5481a78cd9aa94 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_117.jsonl | 1157 | 96d9979db9f7aac9da2ac9e35c1544368f7dc013e7b1c59f7a3b62eba5e6f464 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_117.npz | 3790 | 1018d7325a52cf5555079a865a11c95a76595a405f70505b6d9ece3254d9b0cf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_117.npz | 2726993 | 8ced47a48f344c80fba4527419d9bc08582e2fd58f86c12d0ccf17ca590f3584 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_117.npz | 852 | 0585e0e91fc26ff5ea3aa2928cdbd1af619bad60a7b169d76314ff25b47eb6c0 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/117.npz | 6820490 | bbdd812c49065f5c4e09c0236e9cf7c32508477df3fa75c4a6d39232559522f3 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/117.npz | 1084542 | ad938c4c95134f0f6bdc019f1091c18426382061eae4f7e530e0cef0283f9954 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/117.npz | 1085257 | 75351087246cfcd65121d3bece6a992c8d422ed4fcea7838bf94ed1f7af33ffe | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_118.json | 4251 | 55489fd0337b39eaf1c40120acf1afac57106be4c92d6f452f8b404797f80c9e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_118.jsonl | 1155 | d5cd71784801e4286cb9de869228bb654a29c71c5527faa1ce38bea0bab6beb9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_118.npz | 3790 | e0c72fdd495d17169d92bba7399d7e396bbf743bfe2134deb4413a9479b67b33 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_118.npz | 905681 | 6998f8ce8b9ebaf31d0d9b49ce93a0da1c405b93018f3630894ea8cea52dd04c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_118.npz | 852 | 958589b01b32d3307fe73f1975ba551f599be8e404eacb725fe68674ef1c61f9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/118.npz | 1742346 | 928dd4feb805e0466dc4eb45b59ac3e2a402546c9562d5cd73386fd82ad32bfc | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/118.npz | 296403 | b17a56508a4c01161277757dc02de0d7b0e75d655aca7a1b1a07d4101cdaddce | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/118.npz | 296717 | a14423a4e611b9ea65071c314d83fc4babc73a7f8104a54c6125a2eda55d5629 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_119.json | 4249 | 1e7966a3cd610717816b9b203b36f8db18adc2a794a032a1da268b5cef500267 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_119.jsonl | 1157 | 6fb02b3bff58942b6ca5edf6a2f0a5d32f28d55e7847888da5804a4ba1ca6720 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_119.npz | 3790 | aa040672e9859f05c79114ce3223553d056a8501b3694fb3aa6991aaaaa21d4e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_119.npz | 905681 | 3c16bd9c91e561cfd3c0b89a31c78a790d2e527f8954e781fa8491cfad4a4da0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_119.npz | 852 | e770577d864246dfc413a542a674464de210eb69cbee47fcdb9abe3833f3d351 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/119.npz | 1745226 | f2ca830816dd4e8d67d8c6108f2bd09ddf316d2739b69c8aaf1498edcd642e99 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/119.npz | 296205 | 9aac502957f49739562b92dce8a464564f995c94d1859a9efa02184ac1035467 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/119.npz | 296116 | 61181eaad7a5251a8698974097bb41a4e2f5cd2c3897b693623006317a58ba83 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_120.json | 4257 | 464ece9fbb5db7e33a22b98e5ef7f9729e8351bbe39d2bcc088f4134fa39cf2b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_120.jsonl | 1156 | 1e80c6bf1cc7b0998186a0f35f0d73de6212686c4ef5052e722e802e84263687 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_120.npz | 3790 | ddb98f1782064d9e7c571335d6ac037a48744e9da9c1dcb7782dc267d2264e72 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_120.npz | 905681 | e30d807cdddada77e5bdf57b71936ecff283380a58a3b2a324852ca341191ea5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_120.npz | 852 | da3f8486975ffaec81aba3201fc46918352c8ad4ab6832440c5b589fd907ffa9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/120.npz | 1744107 | fb6a8114b86e14d586bc8d2d7407d62aa57fa27fdae62554e27a27c01aa5238b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/120.npz | 297100 | 70e71fc4ef078ad09f0f018f5c91b6c78091d5a0fd9f7243ce718103797c1ff4 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/120.npz | 297057 | 4c119d791191c97e55fc8d16d3a147719367c5d29f5f93b4966a6dc152b3f1c6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_121.json | 4256 | 2fc3591b50fa2f8060f99a72c1296176059e5d0b0f98eea7d94f32c951aa7ce7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_121.jsonl | 1157 | d18499d6b743ca212456e4ccf8c8a9619d2239d4d628e60c1d2e21d5acdf678f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_121.npz | 3790 | 107c34d3029bb0d0ba7061f89bfbe40e4f78a1aaf55e807af561470d27895125 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_121.npz | 905681 | 3bba5d9ed38a198c2f90691aaee8fea79bf8464dd00fdc9782cacb6a5b04c472 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_121.npz | 852 | 5618d15c8e2b7ac857bc94816dce26c04034907a18607e544f0a8f557f3adb48 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/121.npz | 1744466 | cc6a2df0ec4efc594c8217bbd63ad63000626b86cdad02e528c0f61caff754aa | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/121.npz | 295063 | ecaa211b169e5b0c935eb1755d412a5c83a4d8d6b5294da121da96da4d128669 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/121.npz | 294087 | 500bd4f846906d05c47df2d8e9c7fa897a841fb2c51e7af47b379f22369a4bcb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_122.json | 4253 | 1c2a331323e81b9b05a483b4686e080098a8fb93714685c84280077105dbac03 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_122.jsonl | 1158 | 60a6b48e5ff194fbe5fd97f9a58234972869c5f06e346608210014440922c559 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_122.npz | 3790 | 278fe68a6c7935859d5b574c06d16ad588c488e950d09284e560152f38a5832a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_122.npz | 905681 | cdb5250074cd916ca99fa7ee50f54dbe8d43eed1587f98326c91024a0ec9d352 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_122.npz | 852 | 24c50abca8b9b39eab14af7c3d275ea04dff8ff5287ae52d3cf8d161d87f189b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/122.npz | 1744428 | 846cf0bba7de0ee63edbbd6016cc3578e7013a66a8486c02c8b4869f57407b04 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/122.npz | 295929 | e71274c099be5407060fa404da3cb06aaa8e72f0e7ce7b1154e453998328d18d | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/122.npz | 295925 | 64d2ea68ca7536f0cefa4cb633e56a5c5ad3773e21590b5d6b67de10d1e62c81 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_123.json | 4257 | c3eac23fc63aa587a3c2fe3a5103e6b3b02e2fbb076cbbd248cde7f0ae5c0a2a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_123.jsonl | 1153 | 368e01b6abc479857d5732c4ba4a256c7652b363f18dc63643665098537ff9b3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_123.npz | 3790 | 5f2084d416ac0bcc21bd020ac42c810f0c5c7be51713036056f997c46ded1fc9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_123.npz | 2726993 | 87e896f6c3f7a344493b394cc4372a167d2294b4a7cee397050f10685b58a2f0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_123.npz | 852 | 8ffa62769419170d35b44a628ac7a239e8c00f7101cfb48e99fa8503044f18b2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/123.npz | 6822121 | 4ba9cd34d2146daffb41f3cc866090aebc29ceed111733f576b8e5b773d5b69e | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/123.npz | 1076006 | b641656a0e05211a9add6fd28429dff9e49e6815b666c7d6b81c0033fe808463 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/123.npz | 1076473 | b22c93d9a6e94ea427a2da129f2d1dfa7ef78660d30975042e01b05a7dbb8481 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_124.json | 4249 | f49821d7607fc3d5f5c9ff8c02db361f65d3e989cb269bc98c02cf9f52ca84e6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_124.jsonl | 1157 | f9c2ff29b54dd1f9d70bdf2d9ba5c3a1f77e88e49b07e2b31785447688638bde | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_124.npz | 3790 | 86244ef2f2cb4a59e98937ab2b92156fe624ca384a7b16ac7d2ac6f0d55e60f9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_124.npz | 905681 | baf1cafb207d06642f24fe9fea0fcaa8822375236a3b519be8602f9cff17ad39 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_124.npz | 852 | a3a58ed85fcaabfb9ec57791f601d5688bb084b3c644f942e5b1726517234202 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/124.npz | 1742629 | 5700ba0c58be0cf748aa9d9eef5e5565f93bf4cbadaee3e18321f43ff46ddb2d | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/124.npz | 296198 | 6ccb04e38afeefd3266d69b335fc2f737e4ed956849d36989bf9d93900b36861 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/124.npz | 296487 | 4ee9efd94a07c51115f95379b65491f7a358f24a2053fb49c5c538e11d0d2353 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_125.json | 4250 | 791df7b32572a19d1db3896a518f4f4d651c00c4efc4447e436eb2e1e6634c89 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_125.jsonl | 1157 | 46ca32873e737fb5e2a0d91c21b42f48083d493df26d9e5f94f90f49f8e21d60 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_125.npz | 3790 | 7f991cf4ca9e333fea5540f40faf19eae02da6ddba748a51f543ff48dd4f4a84 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_125.npz | 2726993 | f01bb96a6f85455a38baed20144bdfa1991ac598b02dd7af347df65cdbce9fe8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_125.npz | 852 | 97c802069431a131df561079115d9a6039ceeff33e9666c70dbd9b3a54b90842 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/125.npz | 6810756 | f9286c183c7e130d699273cd9aad6c5a3c167d0ea00009ce682bcf6b0464ec53 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/125.npz | 1070851 | 7225a4e7066299a64fcff053289bfa6a8378bd8a76653a0ed4d21b643b85ff99 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/125.npz | 1071256 | 524b8ccc9709a5efc67fff323175b1f8801ea7741d485a0559cc9f0244835078 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_126.json | 4247 | 31ea00ecb2b01c2d6524deb238d6bae279c0d96ad8b2e5951d3b58b0c9accdd8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_126.jsonl | 1157 | 3ab3baf7980b47ab1bb40816ff687832acbacb8f8385fae5c5f0e8683edea891 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_126.npz | 3790 | 585bf52002cd8e78d3dfc6e7b4f5098c05d825394cfa5855471334d9485bf914 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_126.npz | 905681 | 27eabadd9caa87ecd0ac2cf01bcb8e0883ebcaaf15d46468bddb2c11bc730eba | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_126.npz | 852 | 402872b48392c9e3c027c7e3539aa17f23430d8fd8e3a1c97c03dace41180079 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/126.npz | 1742098 | 09a81403c49a1bfd045f348301348ab1591b84f0735330b714329a05ec4740f9 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/126.npz | 295577 | 7d5815cba0842d2daf76097365b668207f805c8b9de6a5ebe49635407a026363 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/126.npz | 295968 | 3c3e6a5ca0161a6a1dbe28bde1c2f4ede68db0e5aceeff1d5769f4b36d35b5c3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_127.json | 4247 | 9c01966e6e407048ac9c2d2d159f778eec537938ca6f8652ba7f9ba731e82783 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_127.jsonl | 1157 | e4a34f36b4e1c38eab16c6968578f1404566479b6ad156d85eca3ca96f509b4c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_127.npz | 3790 | f76d9dd4d342259e1488fb4e443e420c088601c26aa698c16f8d87dea4c7454d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_127.npz | 2726993 | 1332054ca22c1f5b91a5b7d9d6f1a7060f4fcaa3f1e5041ca6fb3627fceb68c0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_127.npz | 852 | 88d6a63c1376f2fefee00f77199c6e052dc83be40ac054a360ddf43ac653b058 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/127.npz | 6827322 | 4e539a482d484fc4753535c4bff205c829c94fe2a695329550d4154b2357b842 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/127.npz | 1071437 | 2bf44ecaa7e5b5fe8eded0dfddad2c0be3d1d194c289d90546c829d3a4571c04 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/127.npz | 1073922 | 7e92f43ae50402be9674e4112bd2a1dffff3bcc599fd8110ce4113a7fc7efc6f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_128.json | 4252 | 0fa9a69367e3746dd03127ed852ad4f0cada29c22ece4099e1a983c39a08b0c8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_128.jsonl | 1156 | 75e16ddc4b4685fd89b591ed3a224abad51054acdba47cd68648b24ae2f7c0f3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_128.npz | 3790 | 46b43d5e6d0646637eb9cc1d74ce6a0bf210da1a9d3e1b577028bd19f84966ad | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_128.npz | 2726993 | 53c59846d0d9195169da821529c23ff0f6e7342044d2dca715eeb8c8d73c418e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_128.npz | 852 | 1736fea9711fbbea0b5c5660902acc4918fe2dbd8bff8b83ac27dbbf080f3362 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/128.npz | 6817862 | 331a513a60f7532c9e643683e636341d6a4c1baeaacabdb5749c3a20348609b5 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/128.npz | 1079109 | 7463b732b666e79404fe2f18f4f64cd3a12726948883fc3546411373eb6be8d5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/128.npz | 1079003 | 73e49d7387e21c75ebc100cc7eb47e27ad8fc5d4f4ded9b8b97247af2374a82f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_129.json | 4248 | b0dfe8c4a147510994a5056d0f8647a7b02addb3815859be0f1ca3d60c19252e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_129.jsonl | 1157 | 11959df4b4cbe1885567efabe2168fd5d1a1f5e1212667ff5321e86a7934f002 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_129.npz | 3790 | 979e604534a0cbd893fe8e145d5aa7a7a7ef7ddf43b83d35629eded231be6701 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_129.npz | 2726993 | 4940f8f05a298d0a72e65b9ccceae20a28a16f23ece83a04cd0e6723937afd94 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_129.npz | 852 | fb23b31882039a7fe7e0a06104567412469276c5b1d7190f061d8a5278161aca | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/129.npz | 6815167 | 60be2987b9e129ac634d08cd7f48bbd8cc129c112712f3a603367076155d329f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/129.npz | 1078918 | 6ae070c047a6f859b7c8141e008a6e14fb85d30d3bead7900cd7fb7a040bd6f9 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/129.npz | 1078823 | 444ad98febe1a11588db91c6dfc6c9eb8959f4611ddcf6746129aecb5086ffd0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_130.json | 4253 | 208501e1b587d887f30ecae791f352615fdc17e8b5343d6a328919f6ae71975c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_130.jsonl | 1156 | 8c511b49da5fae28a411a3b2fc394cc0b7ee82958d5e79c0ad19fac3b611d565 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_130.npz | 3790 | 55db1971c4a52b484c8b65916e071331de2d26d553eaee82f6597ada2ac5ca0d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_130.npz | 905681 | aef6b4940738f5a49886882df2c604f40801cf36e1ef1f6f4b2fa04814a48d68 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_130.npz | 852 | 42b35c118d126b846027b22646518dacd5e2236f0129e6a17f29a36b4f59ed76 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/130.npz | 1744827 | 669fdf726fe738ce6dacaf1d49cd77e0607e91e0f74a3c9fbb2b7cb05c225c50 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/130.npz | 296109 | e193c679ace50299a8059ab350452ed202ad36f48229513013519375eb2fdb59 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/130.npz | 296428 | dcdbad5a9b842647167725dcb5ac786893c8ded80ad407109a793db772b00637 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_131.json | 4250 | 60306912b2ee20df968be62a6cdbce5fde6b316a001bc41175cf90877104ad80 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_131.jsonl | 1157 | 73467771803e67493d8db67ed5254d524c24761357f4ae8c8cc6ab6490eb0e91 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_131.npz | 3790 | e513d979d41cf23ac6f56d463f2c27c6040530aeb6b0f17ec35e15a4925876da | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_131.npz | 905681 | 181a3708c242df55c6f9d8d16105e4b5e56d009640578cbd76bd07b9292bde82 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_131.npz | 852 | 07f70ba68d645c0a1cfd2f771eff18083ed47938487423d5e77b8981e5ac7176 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/131.npz | 1747303 | c0c4c0cf8e82a94ab479d41601a13954e3526111d44c151985c8285bf238c938 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/131.npz | 297988 | 755a31ce74f41f0f6efae80f06081e5219974236e3050ba7dfa6751b2b477270 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/131.npz | 297918 | 61a29c17fb1ad98043c11805c852b7320e8bc18886d4c5f7384f170fe16f6e6d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_132.json | 4254 | d8d6d02784938c2bfddd7b356204d2773ec87340a3c9ea984d2cdd7a15044014 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_132.jsonl | 1156 | 093e3a3c80b63870f2b615f02ed0d70b675ab2178a038b10bbcd62e8546231f5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_132.npz | 3790 | 8592a6afbcd46617a0f8787de9371a161561f2a20b9768678872468d2769e3d2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_132.npz | 2726993 | 71b0afe142a845b8bbe745b34db6a818db91027bb16812adf0890264f2d133b4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_132.npz | 852 | 155f1abd6302797c878accc124636d30755330672b16316516879a7553783680 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/132.npz | 6809155 | c3857be7d0de752910703085db1c78cfe21ce735de2f941feaad1ac123e9788c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/132.npz | 1088153 | 50264f961276c292f57f18247089a7b01fa98a4cb06f02abcf8750144cff14f1 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/132.npz | 1088656 | 8e3af523ef72b84aa06826691019353cbbfb62fb31a2172db59a4e3c02a9aeac | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_133.json | 4253 | b8014725e1338eec1bc09b16299b278f7cef2f8f8d5b7c42f68ee757ba816d4e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_133.jsonl | 1154 | 31c97439b396c59e7538f1032249c9a3db0bcc847ced2d3c88e90056a7c89347 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_133.npz | 3790 | 9da0a6fa76097b184c975c406a66140bd6f5ec1cc21678c860a25bb91e450029 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_133.npz | 2726993 | 2fe2c45f2bb2cfd9792ead9dfeedd2cff8c9cd8570a003a9faedba1ced6a2d93 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_133.npz | 852 | 5c398276f953b2d7ca0730cf7ed56399bb40c6f169fb45c7ad1386d5c1b404d7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/133.npz | 6829615 | ee2b2c0644c8c592f40fffa599d72fe02ac23d0be754586589f6c25840b9e5be | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/133.npz | 1083615 | ee2ce069e3b73abe0506c8c664f3f6dc7f5ca1240f95059500b826f98f2de5ef | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/133.npz | 1084995 | 71ccb2678fc9c47248118cc1cbf2ce1acd93741acf18886f92b9d2189a57c53e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_134.json | 4257 | 4cbb60fcb2c33c001de4add66c32dfdf5e1af8817b46dc3cdd0bb105d2df43b4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_134.jsonl | 1157 | 7c01e7c12ae5a9ec8f6e097d370ec71bd82fb88ba9eaf63d56d96fd52128da17 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_134.npz | 3790 | 3c054b40c35512f2a48e861fbc9cc159e0a1f57f2a9e0c771f4cada7a6f56df5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_134.npz | 905681 | f418473aa7bb142b94a45cfbe8304036638e7135881a011f4cdd366f61dd26ea | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_134.npz | 852 | 1449de454da955706b501430294e7b46e32f5c80b2464807786a75a6239dcfd9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/134.npz | 1745533 | eaf7492f8a2b1997c11728ae8d7f5a217062890cb7fb9f84a5dffc4cd8c40fbf | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/134.npz | 296395 | e7cd58ca351cd0d60780bc3bd803f9f502f161c7150dcbbb4203700549ee628f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/134.npz | 296897 | f25aaedbc43fa28e53b2e54bd6c963501485f9d387a255f4328610e6b510262d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_135.json | 4246 | 051b5108491d0fc9373fc5f1da1390b9098004c403c6bfac62bfdda4ff9ab0ed | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_135.jsonl | 1154 | d407c0ca60b19714f982a2c548408f9151455964dd9d23153001141469fe1180 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_135.npz | 3790 | 915a0b25d3cb2fc66c6001e31420e0c7447b99626ac4d54c78189f0d7a29910b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_135.npz | 2726993 | 0488573dfa5fa7768ae01e3d4d5b5617e5516584e595c847df2bbf0677a21df1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_135.npz | 852 | 666694f9338c6ed703ba485bab213739e164984229cacd4efac3662e6793eb9e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/135.npz | 6809469 | 85464cdbb70462a8e1d8cd611a76bd0d9b6848b092f5d4fbda765d7362d96adf | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/135.npz | 1078015 | cf02f32aa12f100d7e92bd79f066f41c5c72ef6fd140edf5a8bc581b2a2df61c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/135.npz | 1077472 | 9e91e4197422daffd12c653163faa035d8cfcb17b2f44891c75320543c6f2113 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_136.json | 4253 | cfd8a514adc4a7ceab06a340c97b5fcf431ab58092cf06e855f95b3d9c042cd3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_136.jsonl | 1156 | b6a7554d2e8b00b9fc9e4b6d814e872aaf84cea61cceb70197d3e39383652bf1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_136.npz | 3790 | ff9a33d711a5ce836e2970173b5a8e03f446c1f1517a2e88162069f4237259de | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_136.npz | 2726993 | d3e57a5a0e339fd02860ab1a53c194bd3eb91945b4dd512b34c91cb3906adbef | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_136.npz | 852 | ab25f295a93604d7dfab1bf3cd9da95e1f2a45a845ea19997363f9e697f5a4f1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/136.npz | 6820971 | c04c60c9142a4133a51eaf40b589213687a8e84bf6506885ba782df6d7849a6f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/136.npz | 1078541 | 7de28cf161f03f634231b2695e2ed3c2935ddd1d094bbf58ad2d5d0061822e28 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/136.npz | 1080036 | 79e39c94aa02e9fab0c083de9ebdfbbb6e61958ad283e8c41bbba0ac32436f36 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_137.json | 4247 | e976188da26d10946279272191c88e540b7d7aac040df768b3db079a143a0ab6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_137.jsonl | 1154 | dfff65a33d382b12e3e8e643d742d007a4a7f34dd2050e9c535af5da34dd1aa0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_137.npz | 3790 | ac61cb174a130b5ddc03fd57a282ecaea8c828273047df93227a07893119dfea | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_137.npz | 2726993 | fc7d55a18c7c65935e8bff46aef5ef819a97d5a5a59a44b8f335bdd9a05db3bf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_137.npz | 852 | 7933eb0abc7efc95c34ca547c978b7c0e75da71e3be40343ea49499c4d645533 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/137.npz | 6810109 | 91216252a400440e4889e18558c013cd6dcfd524395164b8204b4ce88e494d5b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/137.npz | 1073967 | 5e3d8f133a63aeb98500ab7f3c83fcad47e03dd371ddb181ca9e2e03a6e9f311 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/137.npz | 1075223 | a9051076fa360c55f6bc2e4d90a0235117d42bc75d1815a0150ab303ebd28da3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_138.json | 4249 | 038e39e24e7957c28bb0aa6723e2731e1eb188a9f36630fdcc12ef5cc4a5cf26 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_138.jsonl | 1157 | 8587c8a943a0991cfc44af1b776b9fb1481a65426ec47b8eee8539a6e4e2c433 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_138.npz | 3790 | 8394bef9375b020e5c5a119180bf35e64713595167bd8b4d0eef52652391734a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_138.npz | 2726993 | a7304c11ed7c0d5aecf3bd2f4cc03ca5568b9e5d08ae30a86b462923c8cedf01 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_138.npz | 852 | 2948d909c61191b1eb67b4382a8be4df74c424c5408fdcaec9bbe5e68c06e81a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/138.npz | 6826202 | 1639ee21007f15231873f2b2b95ce9c5f29ca73cc73cd104f81b7134d517f30e | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/138.npz | 1075813 | f5c7bec8625d38a763aee57478a22167c23a3f4b58fa9f159713667b34d73aeb | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/138.npz | 1078932 | dcfdf6a43f8e6cd016577e86a085e54e2cfe9361f91bc0a58f54c54d287918c7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_139.json | 4249 | 43bff51fd167cb7d1287fa6831238e24f5c3a064724c19cbb857f96693f218bd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_139.jsonl | 1158 | 153b5a680b262aa724818aac97beb7f6952c4b637034d38a9eeea0fa795d87e1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_139.npz | 3790 | 95a488049826e30051a975d08077c3899c431d0fdbb3b13e62a33efe8a83879b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_139.npz | 2726993 | dabb57530b693b9ec30ce22e583591d2b7a1c8cc4a080065bb1e25cace12dfcb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_139.npz | 852 | 0a0552a299050440ea7d54988c8ccfed624324669b3f9f539be72493e6e45d65 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/139.npz | 6815053 | 15517454e4bcc1ac7c2cfe040a49c1f23bd7a79d66b7b8ef6c05c9204f147906 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/139.npz | 1090892 | 26ef36e62b33980d1c3c4884dd722a941a545085f51f218fe75d09a2c4f78909 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/139.npz | 1092266 | a0201978e7e0d076c43766a801e10978f3c0b509cde10986a248a032d9a86302 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_140.json | 4252 | dc7e5424134d350eda29bc3b40fd4ea364b7418ef9a3d94e5d669ae1f0f9028b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_140.jsonl | 1155 | 8ca78866f029f2a3c584169c22f08137aca3922f1049c6b5a4310c66ebb7d48e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_140.npz | 3790 | 556ea85d3653f5eb86aac32db4114bf3fd7a60f904c8a683e2bd7760640251dc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_140.npz | 905681 | 29d939a1617069fb26d2b2502f79619558e86bd2a71cf9938782d81a9a739465 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_140.npz | 852 | 59a2232b4844bb9a1c7742cd01cbd17c143a03f61e7cd7bc5394ff5db631af71 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/140.npz | 1746816 | b53d7849e5d8dbd37b22b3d8550c5afc3b36e9b8580244ade5db4f1f27303a6d | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/140.npz | 293749 | d646dfa655dadc666279f4350286568a1cf84398f3d6d5346695271681843d7f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/140.npz | 293582 | ce72f1eef45a1cba0642a57a03b4f23c8ccbe8d613e91b8fc694d71ea1ddaee9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_141.json | 4251 | 7cec2b3f0eb71771d4e1936b4d763753771dc8a3ad5ae320bb730a1109303a2d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_141.jsonl | 1158 | eee143fe16c7d93f8a536e6ff402344edac6f5582cc9f5932e746a7944108622 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_141.npz | 3790 | e614dbe50bae99419278967d791167995211de65d3478558a18f17038224c8fa | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_141.npz | 2726993 | 54860022edfa828acc53d8ecb75e841c87cfe90b15e8459e9923685cd149a30b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_141.npz | 852 | 29e8c9f9fa1648df2cd5d45b2285ce9d4babd120a5470b971377780a238362c8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/141.npz | 6811022 | 8b771c370afaa47bff3e218097f85e9507225f9578956bd05c436f031790e7c8 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/141.npz | 1078717 | 9db555ddd86842c2ab8409686c24a853c21cc4a25f154a5a88e3ea2204136810 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/141.npz | 1079488 | 63b560bbc716da843cdafe1caf65d19dd5d76ae0ca66d662ac460bb809bddb32 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_142.json | 4243 | 08676f233c2ac5dab3ef0cc093570c461ce61fce8ff837ee30126f92d335d6c6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_142.jsonl | 1158 | a1eaa573b7f781a9beb67f5bc5e9e43262d45b509baba4709e925bae90d06176 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_142.npz | 3790 | 731ac20d21200de6ed59eb3c68e70f42da5b6d6947ad654f7f8fb1fd2c6a032e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_142.npz | 2726993 | c59eba980e044b336fdc2e564f28fe2b71db364ff66d6dd7b18969f154a5f515 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_142.npz | 852 | bf26b7847b9089e498c8077ab51065033b2796434a7d94f0558a8542ac6ec70b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/142.npz | 6819411 | f260e4932b45c6af89934d50e62235d7fee1283e1da1863a9e4a4d068fd3de4e | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/142.npz | 1083709 | ad413773dfecd34c5dd6462e84442bdeaffad8c23ddff12813215739bd4850b3 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/142.npz | 1083447 | 290e7e9c1a6850a0e12433a4a50564ce0992a2ecc19834b69ab087d809cbc520 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_143.json | 4252 | 1e9dbf7a90986859bb1c6aca2735d01a843ae85f1b782c0497d8d724b892bfeb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_143.jsonl | 1155 | 191dd963c464ff7bae11007684b99135aaa8bee2f1fb348d4eafe29145356a2b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_143.npz | 3790 | fbc741b7580b96f79c0fb5e1594609407c8e8323057cfe54f743291346e40139 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_143.npz | 905681 | 9f4f3861f0a7b9f4807fe7bed5a98d15ec30a5a389c84693c6a236fee8f25fa5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_143.npz | 852 | 9eb5a51082477f3c244bac7e5021451e598f03e1f9702df5e45b901dc4cfc420 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/143.npz | 1745263 | 1032664b22ee0f0d5dab474fbe070bff50b9e3235aa63bc8cc2e6ec12b794e1a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/143.npz | 295850 | 5e584551bb532316fb68504cf6f7d808e61e2af70627dc275d813549b1af7357 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/143.npz | 295964 | a71de266a6e800567855e8d510797333905460803b83de86704bb43d90e3dc4a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_144.json | 4249 | b545f8b894c5a985c3bcbe14af755f87b0ff0828c5c73cf9e4cb5b9250eae7fe | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_144.jsonl | 1153 | 02f3466fb8793bb1d0589116d754f6154cc4e663f468c7c81459084d8ec1e3c2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_144.npz | 3790 | 26e4be49172ff3c987dc3597b15a401b19c0a2c716858e724309473cbcce8055 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_144.npz | 2726993 | d4f12e9ca62889972b551ec83f00890db64973363a2a4673033b1c23e603afa9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_144.npz | 852 | 02ed937537de3a21e70cd21c612248fd5a443e0cefb30bff2d29e89e0a61176b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/144.npz | 6815107 | 9255c1609c8760ea3e533ed62e9a8ce3035298df4c6efb113f3894b2c0e1753f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/144.npz | 1073902 | 3ff968a42f84f511f60c32c09f9b60df0324ad02f379757dd953645c9de5da81 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/144.npz | 1072291 | 2cd3225f3352e8581eb3441cf0a89843c8cc517d27cccdad51c9078b396e9aee | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_145.json | 4241 | f924f0df100ffb8ba22650db04ed07656d5429344c73d42fccb6d2f6ba0872c3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_145.jsonl | 1158 | d921205c39d1fd4572ef8aef83e4ab0a6f8910a5c60a668142684cc3fac10e2b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_145.npz | 3790 | 8508e7a2e76d91114ac8846a01c4954759fea5f1dde6fbb148949e2f3acd37e6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_145.npz | 2726993 | dca028948333bd37b21a2ef4db019aaef0c56f006d54c34917e5b42bf6b950e9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_145.npz | 852 | 2198984c3181eb7150a1f7f7478aa4ae79470842106afd63a2d96ca8dbb9bf8a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/145.npz | 6817601 | eba207319f6c20ece88cf11f1b6334737b65323231e2e430cc3772733d78f3b6 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/145.npz | 1082145 | 71bea5fb7a20b53b74113c6c5cd12fc6387e8fa5154b4a2a9ce5c087e6f55bcb | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/145.npz | 1082933 | 8413e25f3d76a80a6e0bd9e93d81a01f195e79aee96abe28b7a8235c20654d82 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_146.json | 4255 | 2f0a64533a7fb3d00bf0f38d259a4823a01f12615296aecf629bee49c3b08085 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_146.jsonl | 1157 | 14fac09078868d32fc0cdb9f316fff6f231d8139685e44002bc66a8bce20438b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_146.npz | 3790 | 3348bb144eed4ade34a152a814d3cd570c56723f7c18286203a2a1b8ed038320 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_146.npz | 905681 | 8b85932e52e692d58bf4ae4468d4d701a75fef485a72a18a5f65bd44560cc218 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_146.npz | 852 | d3949428bc0ae5333ed6268b603792a0e6813e83e85d3216934da7fc09ea2463 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/146.npz | 1747690 | 34e30a0fa361ea29643451b7c63abbf610e66e2e23de8462469bee648ea77fe9 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/146.npz | 296925 | f7f3137cb869c7997a11b6a5841b5af56337fcdc94dacf4d6fb2eac03f40ceba | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/146.npz | 297032 | 81aa1cac2e67432c1e44453229ac071b31007657da3127f71bf76b840d749a37 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_147.json | 4256 | e0da2cd423f9dd10256f72f9705a1116548d733379bbdeee0efc2a92034337c6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_147.jsonl | 1156 | 73388089529e76b957db446098997db933bde096bbff7a621d659aac0a692dfb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_147.npz | 3790 | bd6139d593be89e0b9612201bcae785fa8a01bc3dbf7cb5ca0a97f8faac61b8d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_147.npz | 905681 | 4d4f02a97e94ddd39b3429ada3922ad7dd868a0400b34c930ccb2cad4c2800bb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_147.npz | 852 | 688894cdb4cb3f9dd68855d8660a1a21120fe43524d5da3b4024ee4d989547e8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/147.npz | 1747373 | 3dd4bcabd06abe417d1836492c4dd0e9348bbb4fb8596edc29029b6e47b2aa33 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/147.npz | 295049 | 9530211af46d81ad9d1d620a18b77cb4465b3c061fa0dcc9a71bc3f2a3f1a823 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/147.npz | 295089 | 9d448c6ef29510471eb43ba216fa21156d1fb3196761f75fdacca2467f91eee6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_148.json | 4247 | 522f50cbeae6b70ff9430a6152eabb1738527331c5599ac794a3a5afd54750c0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_148.jsonl | 1157 | 7e63dc3a7895f8d97782934416700fc402566283f8fadcdd4300bb4246765133 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_148.npz | 3790 | 1522201dc681eec4bd56237c1a14cff4952a2618f3cfcfe09e8b2538a0e07bf2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_148.npz | 905681 | 4563ab847592249c18af79259140c2b4d5609cdabd0b960a4406321e02277175 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_148.npz | 852 | a303a71fac0751ccd2e48ad1f64148b6c25ce1c392440aaba3cb8f5e66df3868 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/148.npz | 1746168 | ad111cd7d6ff9af1a11891a1afc152c3cbbbc75f7849162129edcc5659088d97 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/148.npz | 295382 | 67fad56c150ccfba10a6acdb0a63de72e8f1f05d19f56e9ea7b77f8fec55f62a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/148.npz | 295700 | 03680aa3246bb45005469b7981a1c0a561f7892ed5b2f7929a4d4e9559c3bce7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_149.json | 4257 | 19535f5464155a491bf803a96663e4f2efe081bc11ad3bdb052bff0eb7c87194 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_149.jsonl | 1157 | d4799ce812ac9e790427957c291f71c04894e42e2b196b84d37d1a63f7fd0e14 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_149.npz | 3790 | 87afa72eaa5bc984c83e40630816ce33bc772bbf2043c59cb5d304deb97a2e2f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_149.npz | 2726993 | 954cf8999abc223e6784a6c91df2b6e953dca199755a27a794888a40b54f7674 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_149.npz | 852 | 6281e364cba09872d48d76211c19698f8c885854e402ad75a090940ac84de2c6 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/149.npz | 6812987 | fe9e695c8cdbbaa7f063199afd99c817a939d6de8d1108a32d23d7ec4f6f9522 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/149.npz | 1076740 | efdfd4156b2309b30eddee3cc2430dfa9087f9090da89d2053341e89354f830f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/149.npz | 1076674 | a81f9f172cdf175ec18fcf5eba473c7a5da28f1b25a96cbad0da6abe4fdac04e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_150.json | 4245 | 6d124ec556e2a7c9ac5bb8391a65c76c0d409db09894ee0649f5ae28ce03f0ca | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_150.jsonl | 1158 | cb9fc76a5033a962ec36c2ef58220b7d5e127ac7845c4727b34d252874a5408c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_150.npz | 3790 | a9caa07bcd8c8d8e6fc5f51a9c613bbb80283c2f7f333551ca0ffff904648405 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_150.npz | 2726993 | 510c7b855641c5bff86fe52cf846e1cfee0819f482d25948a44121e17e169942 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_150.npz | 852 | 3255003ef9f36c93ca1cd90fa6617a68119a54337b0ac4f43066200b1db7c9bc | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/150.npz | 6819305 | 6eb9052a2f116cb7838064b77aa3031e1ec7ef2f8081721bd7318c43a56b4896 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/150.npz | 1069891 | c569f91f8e610aafdf332197c9ede9c66a6c29a4f316388d77b2b887c5d1e9ac | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/150.npz | 1070625 | 3a1096daba1f32d3490944546adc2817e3df1698015000b50e938e78cff1a5a6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_151.json | 4256 | d753589a94f955f5d6d4b056502e0f02a1cbee584207d327074d07d9908da7c0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_151.jsonl | 1157 | f5f1833cae7a70989ba247bbb28d78803fc1cd7fc4fc115178d511314108091e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_151.npz | 3790 | f7556ee4a08635d6033346cc8b5ec82fa6249e5cf5d365160ab1efcdc378b095 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_151.npz | 2726993 | 5a88be76efc4221ffa987c92746f8a7f26752ccb7f561ff3de74d090f05da29e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_151.npz | 852 | 922edfa713e727ae353fbf8d9ab40fb1ddf073d78ce90c4b90b8b6ac36fd0262 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/151.npz | 6822088 | a798a8baa49f17ea4a5603ec52655f16d6753ead1d0aea6afd716c2dcf872176 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/151.npz | 1082662 | fdb25ee19d0eded8a5086e842e543d582d3b87fa8be63f9cc247a9e64be78b15 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/151.npz | 1082225 | 2e2923d5127216b912813cb9f705a00ece7aeee6882c293ea589ec8de932616d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_152.json | 4252 | b1ac53c692d64dae52d5890a7c54b28ad1a4a74fc4931e3ea360f1e4da5ea030 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_152.jsonl | 1157 | a957c1e2d8e5d859a5a78b6056f02405b451cbb8be2d88a34efd7dc0c987ebaf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_152.npz | 3790 | c3e6a1f517dab1acb425725f5a148f24cf9650360f21ce7f9c0cdf3950f5f314 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_152.npz | 2726993 | 381dbfd11fb29bf4fd3fe7b60754b38642c7cd6fc41ab8eafae4cb61167f15d0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_152.npz | 852 | 1b8a5b70f552d4f771f9217657da1368a83ee901deda61370cf9ea81b0d8fcdc | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/152.npz | 6818971 | c579d0ea520fb6de153d0925ba0f4da1e053f2fec5a6513ae960d8aa32201912 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/152.npz | 1081616 | 090efa507bc664957f86726af1ef1e72087d69c92e75756bd4ecd171ccdd0be8 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/152.npz | 1081352 | 8aef9cd6c802ff92a70a189b81b43ad7880cc79afa256b9b61b7ae3f4ba53a78 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_153.json | 4250 | d42c0cceefa60f26276894cd0cab4d0bd6f2668ba6b0f5b6d3dbd3f4ff3bb09b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_153.jsonl | 1157 | cd168be713542b916150668fc516455b8ac959f03a8569aeff68de078376687d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_153.npz | 3790 | ee0b65e57869535996c4513d20ffe066f7b71388f871b7dc740a35e072e3c8db | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_153.npz | 2726993 | 3b4280e059b9feb8a5c0fafd925b2549896c21bf7826f5c54043619eadf45206 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_153.npz | 852 | 251c138010df742a7806868a5c9cb22d7782807d608cb1f9fd38a5378451d193 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/153.npz | 6818769 | 1adeb5ce9a13890c35abbd13ad98e602379b1e0ea20e0fc69cad1f792753305a | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/153.npz | 1081346 | 4657e5854b204c3e77e12ae39521b261373f5983b7caae34b4db47abb401f229 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/153.npz | 1081996 | 76561e3058efcdd9468d31199a9739bb585b8cde33baa9cc5911cf799a6fbf61 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_154.json | 4245 | 64adc07a88db2e4425e74043d1579a863ade04ac377bc7de7a331bb725a7d2fd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_154.jsonl | 1157 | 788cfd9ae62feb47e7a5ee375c89e6b79d2a9d341e7c3317cc085c859340244d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_154.npz | 3790 | 951d8e8a6b245a841c842e794b7cc7edb4fa96262258fdb1c9deb65bbe3a41de | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_154.npz | 2726993 | 02152b0c5d2855d5128942f7a0b01f8d2834efc254fb93c6eb9b759ac34dc9e0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_154.npz | 852 | 0df56056507dc6f654ef8e542711c0c2dafa43185abc1e613ed54654845ebff1 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/154.npz | 6817546 | b1a242a0c89eaeb15b3a4612ae703becc345683373f01b45f10d5bcd4188adbf | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/154.npz | 1081228 | 5e3d03906b9761487cf9cb84362b0b169f919654fd17fb638eb19300ac3b6aa0 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/154.npz | 1080397 | 9bbe2079c38110ef01a2ea2411a38f94a5edc2dfb90ca24d07d9374d06184c0b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_155.json | 4254 | 15140ea725e023b374b36b59f3e0e2b4f529f217149894a4056b119c89e51873 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_155.jsonl | 1155 | c8681b26973ddd71b3b354a8a40406c87779da6034adb92d6e7e09e86805e8f9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_155.npz | 3790 | 9a08f8309a2d615035c3e73316b8a8755c09e6494419fd97a5ec5dd79f127e2d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_155.npz | 905681 | dfb96e2d00ded29cc3e6539e15d3e2e44e1de918d348c96e0061e89bc8855391 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_155.npz | 852 | 9087fb05e284d60dc68af6994e3a2a0f8da40bc50bffb6802c6e068996786c8b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/155.npz | 1745807 | 52717228584204f49922ae70cee1cbb9888ad80c0965b0cb286606ee4227c898 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/155.npz | 295721 | 38bce71e2a720be66f2ff897c459a7309687a49f263fa2468b60b61c6d8d7ce5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/155.npz | 295600 | f99c85702332d6c5e849f46435d66ad886186ca249795aee0b14b40170328143 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_156.json | 4250 | eefcdfd77e713e8c53a8d149e337c7d720bdc504935e247a74068caf35c285f5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_156.jsonl | 1158 | 1a3f27ec810191c8cdfcfd2bcd08e4fb8f9f91030ce64a8cfe23340b3d5bb3c7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_156.npz | 3790 | 7d0fa76ce05bcd638ddfccc41ad9534e0c8d32d1499c0cc1861e8383aa55d468 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_156.npz | 2726993 | 990cd5c9b3709c33907507fdf939492c2ef540dc3f6fa8e2ab7207a90f679568 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_156.npz | 852 | e4ebdd0fad29022fee4504f5c81498580ed93cbe2506716b577e7ce1798df1ed | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/156.npz | 6819407 | 22787a7ba8d59b60f45f5cdcaa90fe397bee77766ab58db9e31301a59cd333f2 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/156.npz | 1083670 | eaccfb6e3fb3b94298a89275a88bb59e9b47606106c8a07ebdcf6737fb99eddf | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/156.npz | 1083691 | 45e12033b167162dc26c26ec3ab4645bda90ee5a0d5efab3451a985c9807980c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_157.json | 4252 | 32a531db991e64ad73c9a3e3fa5300ce10d216fee1fb882e0e24bbbf6cf101ba | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_157.jsonl | 1156 | 3b543510bee1efbbf9583ec9f4b975b5e30ed027852a08cba5f60e6f68628892 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_157.npz | 3790 | 5121073b2c74768a1d205ee11a7b95e367b29773590adfe1efd80b0f58b24b03 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_157.npz | 905681 | e85a7ecf078a50d1ef074031a167ceef8d0dafe877fe6caee911e49601e798f9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_157.npz | 852 | 45b422dc5781f723f78de1d8541f880ef6f4890df7d54616fe31dd62d3da9998 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/157.npz | 1747219 | 4a5b883516ce84661dc59dc2e18ec155d97a1ac2207dd954a599237dc6fc86a3 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/157.npz | 296536 | a2829630ac4c8f3c22b96171fe006143e6d0ea458ebb74480dfd0c16413e4fbb | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/157.npz | 296535 | 94948c48489108f0ee245760117624235ad400e5336cfb7ce13fdac8b441fde8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_158.json | 4254 | 26b79ceb09c492feeb363274c88a2dac20e0e08e72831ce10b368c0e3901ef4f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_158.jsonl | 1157 | 8df99274db4920fb00040787efbf4231fdba366e9c503aa83fe3c2d058cb708b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_158.npz | 3790 | 8189f2dc588e04c32eef00ff537b20a688a4e0e428ed3e63791ca630036d55df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_158.npz | 2726993 | ef636343e61819f8a883f55296cbe2dc82601c7a6c9b015be3252ea2c1c7184a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_158.npz | 852 | fb0f2ab5df357edaf1164da658b851909b464b75aa0c35e011f33ca65bec6693 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/158.npz | 6822965 | 22e9dd72fe507e5863f5378f205254afbd5e843de756cca748201b9709ff1259 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/158.npz | 1081001 | 8ee9293358ea18e5ef61a0206b1f6d836137cd9421fd286cb2e2679b92db8de8 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/158.npz | 1080616 | 59d4ca3a498170610c786b5b7cb7461aa5c5fdfb8dc30b01d361d823afcbcb4a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_159.json | 4253 | c2301655ae3de7fe662b7eaea511a8531b2deba7d8bfa0e6dfd4e6d586429fde | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_159.jsonl | 1157 | 5c13ea9bb59f875e55f790eaa5c1abafac8a379f102cb6aabba52a064090d825 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_159.npz | 3790 | 520ae9298784baa774d9f09db2211a6600c66a7d8282c042c2494aad49371e8e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_159.npz | 905681 | e2a93667783885fbaeab5bd3dda382ab4a82e440d850de11ef2b3a15f769c182 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_159.npz | 852 | e291ef6c4b8c278683370b18ef5ce43aa1b0439b4e67583751cb213cab3952ad | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/159.npz | 1747601 | a59a0c93fd8d7b56a4647c41a4cac33aaddd3aa24897a136f5d397ab690d3d19 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/159.npz | 295915 | b66ae7d3cb938088965f9d12104ec405d1509f18b9b323f799573094eab08f51 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/159.npz | 296254 | 96662fb580e6b06db5e1596125a39f93ec4695f87bcb8c9cf6e718bdf36e8564 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_160.json | 4251 | c0b8b41aeadb7d2c7177ccae3e9ef40ce5db5b9ec62dcf957134cb78e0089d81 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_160.jsonl | 1157 | 773597110503e9fce67c5c9979814e82cc4ef0fe8fdf1eaf40db51fa7373a24c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_160.npz | 3790 | 0b9b33edc415778c8ea2c10a7c72331622b7eedca8f7daf6e22a88105667d9c8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_160.npz | 2726993 | e43d2f03389e68e30918b6c5e2e98292389e48b89f57409a4e5e3fb5e5387d76 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_160.npz | 852 | 8a2c37cb4b57ea7406af16bd54c0dba26220ead24c158f668851fa5cab5663c2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/160.npz | 6827753 | 85252e56ed0a8153a33ffed1448405bbefd2131b272d8244c6d46f3573a48250 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/160.npz | 1083464 | 8e6187952087856ea9e48d0626d2721ee09ed2f3a7a7c87e83ca4480bf7d3a5a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/160.npz | 1083940 | 4a5664621df3050f590f1da7fdd3a21849d2b36d94a7f2d4b5fd864076f5d7c8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_161.json | 4248 | 868b77120356e71cede5512bb45425c1b6eb0e0127e66175f66eb1090739824e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_161.jsonl | 1156 | d63fd15e4b54d6a411028bd4ba0d83fb6916220639ab44e83ed783bf2eeb91d5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_161.npz | 3790 | 1105f28cfcdaa29d0978ce5346391d897fd63e2e0c94534b1963e34ee3086f1e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_161.npz | 905681 | a45470e7e3904a39c5ea95925062eeebcf273ecae9aa0e7875241c11469878c1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_161.npz | 852 | 36ab10b8194016af89e3bac123c4e710a2dac5ba01b49845212f4cdb62aeba1f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/161.npz | 1749873 | d94fab742c171d70b27b9f08baf26bd580989cac817e02f89b39d9ffbbc86492 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/161.npz | 295844 | 1726c4238d42ad429df8eb580913c03c40cacc8be7d828831c26680605aa118e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/161.npz | 296107 | 50cb9e96ccf5fe30c31c7eb4db2cd9489b3ae6f89e4f85028510ca331e33cf34 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_162.json | 4248 | b8ff79b4563bafd771d42ce776c94b53f56809dc58b1209d3fcf340185d99636 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_162.jsonl | 1156 | 3293749b1bef19b4cf85858df431f166900f2b6d4b538c0caadf9c61d4ffea9a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_162.npz | 3790 | aae2e513e3d81a8ccba635dcfbb7192ec63a8339f677d7d2b39e57381aaa447e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_162.npz | 905681 | 6ab60dc29d1793a2579b4faffb7967bc0f5d21b472a14a096787114b91bd9106 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_162.npz | 852 | f99e13be08be80cd1110f887fb971bf356999d059bb5880d079aa0bf518c9a6b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/162.npz | 1747868 | e1aeb38d6cf57ed890b61f976b5545b34f7dded74f3ccd15d8cd4e1de7b472d9 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/162.npz | 295426 | cdde208253db26216d27c26a5de6eb812392660061fcbc4ecce2ea90c682862e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/162.npz | 295364 | 85afe74acde9c14d66d262e4d9d6411a0c345c2d854dbd72cb583209ec280484 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_163.json | 4247 | 5448a5a73d2e8d805cdb315feab6d5ed170a087893efe5d9d51049f1d688ab19 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_163.jsonl | 1157 | cc6174a16054590cd55412122ea84d0d5d254696d8ca9ca0b957274c1f55377c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_163.npz | 3790 | ea59998dd5e0244eb47a931bad7302e751f2d460787686483f48de2f4cf719e4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_163.npz | 2726993 | eed07400597170eb4eca39a30aefab6a851cf291f9d30e989240ca463c033135 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_163.npz | 852 | 0c5dcea0cc132ff8b4757a62657bb9ac60e8bfc66ad20233ed3d47b1aa3c6a3f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/163.npz | 6808267 | 4961c3668ef268fe53415e73760c184331e24a3584d2e72aaa0287c3342651ab | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/163.npz | 1077988 | 591810219dc3f4922622003c98f3f9c14ca39f53ebfa7a7c726a1e98055cb05c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/163.npz | 1078291 | 090e7bc5749d8fb6049147e5800a8d07b1f16dbe11e5ed44d225c3e93e9b6e25 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_164.json | 4256 | e565b56e9c523ddec3251d2fa0c7ae4c5058ac6b8088ba25cf0db39afc52557a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_164.jsonl | 1155 | 480c10aad8523a421913c96aabf93813de2535c7221a57edec9cbfede0b87aa3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_164.npz | 3790 | 0a3088947ae6e42c427884238922c8b8e2eb8b09a0c44500b32df2bbf39256e6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_164.npz | 905681 | d016f431a8a13037fbb0280b829b91f9ae8ac0c7ea85a91ca1ba5468e7039cd3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_164.npz | 852 | 78c997bede235439a278812b69bed7b3455d563023d348581af3ab9484d5e17b | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/164.npz | 1744207 | e6aacae92daa542d1b58689748c13a8ef2434b0f78e47349b2f6bf3c31d8fcbb | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/164.npz | 298179 | 1be851a13c1519c75a19ba5dc011f1a11009c3b8f47423f0bc0f9844f13f169a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/164.npz | 298068 | 4f7100149dcd4cb0046bd381d2d5249fab31b6c99e5853f46b8e8431294c6d29 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_165.json | 4250 | dd49287c396a5f5825e8c0f3fefcfdf9d27cb1eb91559af95e047f6197a26412 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_165.jsonl | 1157 | bd36d1d847e7fbeef326b726abbd7f0eddd819b834e30dd94887be14afab27da | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_165.npz | 3790 | 50564464ff358230e6ccc40f1a8f356f2aaa28f1d70015a59c2c0820e96e6d10 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_165.npz | 2726993 | d34b5842e755d93f373f164cd9a200ffe2685916a7fc9c59acbe3424f0013b64 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_165.npz | 852 | f4a34384217209fe7ef7a6cf33ac062216642f866be855d182626fbd16fe820c | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/165.npz | 6824922 | 5f7ca02f302df50c9ee57e40fe7ca409dd7f8493e9b78ef83e14d63c6dedf466 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/165.npz | 1071894 | e9ff902297863a60c795759735d843f8afe335a10f97259a15dfbeaf98edc62a | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/165.npz | 1074374 | 90782ee031b87f2e736513dae8d72061a779291afb00a8569c8ff10e39928743 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_166.json | 4245 | 729673dd29258f89ca0023b3f2f327bc88284ce03951fbfa4ecc414569d7e45b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_166.jsonl | 1156 | 81724b98897cf337c270d70bf8e5ccd47253d5a69d843b3fb14f6e7a9bdbc231 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_166.npz | 3790 | dee0e199448b6b400bb2e6dfdbc8481de62217a34dcc7967641ec012f4455dc9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_166.npz | 2726993 | 679b56eeb3a2d4b242b366efb709fc5339bb333e1c8aac2eacb1935bf6947705 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_166.npz | 852 | 420dc02d14d9a4ef7e4ca61ec374f8190bc535d2aca3431306d7a15003f8f8a9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/166.npz | 6825044 | 4d6621a03ec9a56ff8f883c00ea0d43bf1f2a09767be0b5a4ea5925ea5f39eee | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/166.npz | 1076810 | 907c4383ad7fc433fc9cb5727dd6bb15e0f31828b92a4bf692c8d6b36f7586c2 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/166.npz | 1078218 | 79db3e93e844862e4a1e43de94a8a6d66de9a2b10e7e0e921530ed9c5e66b0ef | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_167.json | 4251 | 9bbad25bc75494b526ea7f0d146c2f5d9b585af0474f8917d1187eadbc1d2411 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_167.jsonl | 1156 | 426804181a94c1278615ab85e05154101b9927e576ba03836204fa1ee2099107 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_167.npz | 3790 | 55bb05dea9d46793d736557622f563f97f46b0d76d532ec3aeb761ca1457d99e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_167.npz | 905681 | f237f680a12d429620865a8b7bcf6a3369914ec6877913ebf0a2b45f7267b9ad | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_167.npz | 852 | 4846d6092c9bde16d2241760ed7899d19a5643782ecf675517c394838b396241 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/167.npz | 1747251 | 081833ea9d6e262f927afbca2a0dac92665fd0b2d342f3a3fd830ddded418dd4 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/167.npz | 296200 | 0ff11d266769d1a45082b13d8ce47aae131fd3000d2c73e49e2f6663589b6266 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/167.npz | 296338 | 4e7ea669db41cd884ad803eeac3c54c384e5d2c306835092e2186b1eb1aecc00 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_168.json | 4241 | f2345d6cdc8293435a98c593b7579d45ef0e7d219a772981a4a5bc785af13cc2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_168.jsonl | 1158 | 36a08de9175feb6ae6708d35218c235190d77dbc63dcc01c91fa7648111c6912 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_168.npz | 3790 | 1d661c596349edae643832188da4f9da13ebd9b7e1d957ae378c9a55fafc78b6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_168.npz | 2726993 | cb154ddb679fd16a0a17851c46c7479d3a1bc10f85f4dfa1cd70ec2bf4552b7d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_168.npz | 852 | 86653b9f70fb1b6805df6494149b97797e9a59a3e35ea57f2965e59b9b65bff2 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/168.npz | 6817460 | 34d9307d7727426f7bb9130471f0d7dba006113891384d3d533552b6953a70f4 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/168.npz | 1081949 | ceab7a5b9118fdccea1b85e3b1b3de90251089e6417dc8ca74b688bb876ca9fc | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/168.npz | 1081509 | 33a8aaf5859a83919d5ce8be55b8b0e185c364b4880f64d045475162659cbb67 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_169.json | 4243 | bf5b3e49ca8109f318327bce54ce7245209fcac82e91808f2e05b1e99f66544a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_169.jsonl | 1157 | fdfbcac838c26dba8e623141f6bc4c3b0ec49e6ad73a8b23de82b8d1408d94e6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_169.npz | 3790 | 6951182ed1088fa3f25aa13f09562b7e964e4ce33c3f6f0531c23453936dd651 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_169.npz | 2726993 | 5ea8ba99a1b987d9cba92759639d3ae6bce9d6509dbfe54e3b254c9e9720c677 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_169.npz | 852 | d3a135d48786f0c818ffd60ddf33d1b89a1927e21d877eb528ee211b86f2ea9e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/169.npz | 6805719 | 77f7f9f1bc13c9910507c111ebaada8112a82aec3f479d88e237663909151b8f | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/169.npz | 1088689 | 408d4203dd56cbabf233930567570f640577b46bb508819eb2ff77e5379733b4 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/169.npz | 1087330 | 86a701e287f3dee45b2bc15f1c1ecc5f06166f541539e876d287e5ac295864eb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_170.json | 4247 | 76967b4c07c57fa78baccc5dd5b3c8d08a4bc96f5946b897c5c0facb29701d48 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_170.jsonl | 1158 | 71aac9bfdb44c758397f861d82764522491a4498a172bafc802304b8a87b0b4b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_170.npz | 3790 | dc8d064ab3a9abb9246ac133d5d0d894ded034f82c63a46754d6b4445c4d179f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_170.npz | 905681 | cfc260e731b9454198e2c90e0b4cc548c859053317fb7eb92859da37787d3824 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_170.npz | 852 | 65473ec759a919aa6c7b403be7fa6bda3fb3bdfb140c374b6a7855ef5bece83f | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/170.npz | 1743750 | 2ed7b3314b59d768a674349a4edb129256c63a2fd7674966bfb0640613d38865 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/170.npz | 296704 | 02946094cf35414acda8e827ea1330bb3795f5e28a788940ff1c402f8512b9e4 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/170.npz | 297247 | cbf0863df0878e4cedf5b93a0789fd26edbde87162d3414f7d988d94b1fb29f8 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_171.json | 4247 | 233e29c14087da4b15773fd678c3329fea646a1bb933ae86ce4a2c84c1aa47eb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_171.jsonl | 1156 | 4d7ef5d35c96ff55fcf5a4ecc908ee1e9d0e5a52f3e78b6996f1123f3b42043f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_171.npz | 3790 | d616c1e8d45a55d65c815bf588d3c01bf691adce2afe57aa60384da6b259d07d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_171.npz | 905681 | 478367bc53920785ae8e3a8658bb783b4ae2a96c2d423640a5d9b2071a3836d2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_171.npz | 852 | 399e5215714e49d30211cea4bcc0dffa95097b0ad350dfaf9e872a69a43bccbe | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/171.npz | 1748175 | dc48856cccaac9d481393eb4154be61fc458b710e59175f78cd206bfc24ef017 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/171.npz | 296793 | 259f572cc81cdc242118e3ef0cf977bb61144ee65e7d7b14608dcdb54824cd53 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/171.npz | 297242 | 34c0531907d87e44d3158aa15e23ca583269dad52642cc664dc7bf881cbd8ddf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_172.json | 4248 | 0aa05f3d7f689b0a124a13c975daf0be2ef2e2c0fe65f58256bd456c46ea0343 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_172.jsonl | 1157 | 074e99f1057ef6fe3c0ac90896603b4bc854a987bbae19201c13184a9e137f78 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_172.npz | 3790 | c80f2344ea7d4b1a8f673a059dcfd699c8810c1cb56741f0a1bf6705e338249b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_172.npz | 2726993 | 147f2450778d31e7a74e9305cc997902eb6d398f2b96f15dbfb1e83b551982d1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_172.npz | 852 | 9e6cfc4b688010ea6936807c6a87d6f5f4ecb639f19841266aabf195fb1a2830 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/172.npz | 6817715 | afd08a085f98d58ba0887a5617153eee0739100bf9343b93f945325602f66fb0 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/172.npz | 1088598 | fd39ca8dbfa16b41aef64e31d31c31398441bfcc8123cd7e789e9b37726184d1 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/172.npz | 1088415 | 4f0339db6917ee24fa05a49ea8bad9b704c335e593b2da270a3ed5008218becf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_173.json | 4249 | 90d0fe6d48f278ee4495f25b4be269127f65ca8cc93d752d9b6648d40057d3ef | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_173.jsonl | 1158 | 44f700d9fd02c82d6b72bb25fb04c43d103590854d85abbf73cb3a5b22b7a35b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_173.npz | 3790 | 6a1c3ae8fc735c562677e678f96e35e00cad98cbdde6c27bbc031b025fcda717 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_173.npz | 905681 | 9e24f91c19470ba84575a08c4236a0725887959205a7852412aa2aed6c558d3d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_173.npz | 852 | c6bdb3e71cef4f8914a8ee6731215c3406f5be1aba66c5a0076a1cdf9fd9ffa9 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/173.npz | 1746643 | 84ad180062f78febafe9f653611d58acbbb1f2f505183ed4a017baf9a840aa2c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/173.npz | 295171 | 2bc50db569c0dbc7a349e2b439707b39e6779f4b04687f097fe7a7cf333f63ab | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/173.npz | 295253 | 72652147e4a65dcdf1ca92d6a24fd9e7447ff2ec4e3335d1c64800324e534446 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_174.json | 4254 | 828445642584cd28bbd8aae5ce62352e4a275b3c45361ffa747613f889e3ba92 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_174.jsonl | 1156 | 331ef4d102294ae9e4630db16e54a2e18767c011cddf70fe89012274db7c55c4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_174.npz | 3790 | b0c4279630bef962534becba7c41cd92bc292708e9de5596dedcc1d23be0165c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_174.npz | 905681 | 75769e275a93775e4f97746e2eadb962d1a28d2d2453cbf98592019e90584ca5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_174.npz | 852 | e381546e5e0d85581842c4b896cbe55b09361411f7493f09f0c24ba93a286c9d | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/174.npz | 1746677 | 443b610df8671d408b14f7a5994baac0c1ad8b62c1088b1510436cf58cfbadfa | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/174.npz | 296505 | 6663e07d96a1fbabfa653137467878dc0f465316790e9a08c9cda4e54c06101f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/174.npz | 296564 | 207e6b1f9219a8cb2a31781df90fdb1be27e69c1c87c5325176451bfa922c5f7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_175.json | 4262 | a6c32438cb680f805aed7e7d8aaeddb9e229de0be260e8fcec5b68fb7310eeca | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_175.jsonl | 1158 | ee39d0c711d0187b38451f4cd7b905f3ce44eaa3db240e9b3ffe6e6415947f20 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_175.npz | 3790 | 30ce98a8c00f8691c380c178e6767a2f8f45d0ddef99993a38d049019ff344b4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_175.npz | 905681 | d319393a287ab7fc4da8459c92e840f61e20d290250decdbcc78ee29dc2e1d14 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_175.npz | 852 | a8299ad3a09d11d4d97383259e1e30eb82be6f7d9bbe9fbc9d90fa4b1ab4dde4 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/175.npz | 1746241 | 2c8572a0e1a298dc9eba88c2555cb66f2a503bd95c670699e4c55823a0f49847 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/175.npz | 295242 | 922969dc1fb2acaefa40fac369a60093fa83fc81e9f61ea93d164e284b0cd59f | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/175.npz | 295395 | e25a80dbdc10d47576184f4314224b4efc484660d2f7efb2a216c46ce16439bf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_176.json | 4249 | ce5aeeac3298501ccc3946a4e1f7bc17fe4c01233897ef745a50b396fd039780 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_176.jsonl | 1158 | 9e86251c6182f9e90c84281f434b4e3e8024a5603d08956ae3f566429c399f9b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_176.npz | 3790 | cd9aa81381a36fb8b79933ea68340bb21d7731e5d43c30dd3509f6f3e3f24401 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_176.npz | 905681 | 7919f921728813bd42bfc86e35bd2f83408be7518da50cc7774e0959cd387c56 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_176.npz | 852 | 10be25b5edd24aed2e6c607d55bf150700b05a556a2947a2473e8661ea4538c6 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/176.npz | 1746823 | 75fa2735d66200f71162aaa84bc87ac664e21ca2aba561923159dda03cefe173 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/176.npz | 297960 | 5058ae97d45e237afb08e989f59edc9b65be258e3dfdb1829b246dedc8a5c555 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/176.npz | 297879 | d5c732dbcc823fb225f14e9109b95994c45b5effe51115209227d195c4da0453 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_177.json | 4253 | 3e8f84e4e3130ad0b664a0dbfb478974b0a21976b62819273065120a22811ce0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_177.jsonl | 1153 | e6ec8df9b7d548339fe008f29b7c1b2e5fce5fb2cb2eb2259e4c3f7e060c063e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_177.npz | 3790 | 098b9822533c61ac0576fb426821f8dd13b6ac71d9fcca560ac72cc752965f19 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_177.npz | 2726993 | fee2434e64872ab1b97dd8505cd8487df6d88a9c44bae187210c3bc1e247472f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_177.npz | 852 | 1c724378ee521e13ba9fc4a601db6c8af592d288fbf0ecd1efa7bc50b3e866b8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/177.npz | 6813935 | f17dd1016179458017a9e5b697c11de24c5c8fe32e442be58c4ee5e98e407a40 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/177.npz | 1077423 | 6c3eb02ec57acb4a10e5f29de7ab62cb9f22e5d637acceefc8292355a529691e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/177.npz | 1078591 | ce1d327847bc9cba50bfa51fb60daf8ee254129a023a784bf3ee9d8c14b40b9a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_178.json | 4254 | 0f9e21259f74cdf4cb73168bf61e540efe3f0efa197dee9dadacad513c69a0c0 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_178.jsonl | 1156 | 1fa7b211ee4ed0bd2abae6854d80edff152628f531bd6811c857e171d65909a3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_178.npz | 3790 | f55dcaa22d7091b7732de4a6e87a7a3d216aec42cbcf6f1f4116069321e257f5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_178.npz | 905681 | e8142263742d90748f028891363b26e620b98cb1b335380c5141809d2127cb92 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_178.npz | 852 | b64951e91380bc3da5604b01c84e1abf1ecb29c999ff02e52cc88fa8d4b97e0a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/178.npz | 1748090 | 7926c8f1775a3ba080db17cce57887c5798c7d7f6c81afb084b1126f7ae00d27 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/178.npz | 296279 | 33e001e2c2abacc9b0286a20b6d25a2848df34970c2d10233663236406716ef8 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/178.npz | 296277 | 874859323d3aeb8802919f70c8e040c19eafa54d44a9b21aeac3ce817ee98548 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_179.json | 4250 | c703a9b6431b4699708d62b6b30bb70b73aca92f6b6c2f863959953346087a16 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_179.jsonl | 1158 | e84f76af641afafe161244546f07030424e7a536f4d8a89bbf7b0dbdedad96cc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_179.npz | 3790 | 0c8403559e9eb7372f845dfcf5ddf2ffc0077d181a4ff621fe2666c437039dd7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_179.npz | 2726993 | bec95b3f5c92b6703705c89a34d5bc4996ecf1c7f32228b45f9d7839ac152774 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_179.npz | 852 | eb2d9b98ffdf61d967fabdad8379e29a045063f889fce1bfd59a59ca0b219d3a | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/179.npz | 6824114 | b33a1691634316530499a27131f5e03b2177eb629f2f224edb38fc4193ae6a05 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/179.npz | 1082574 | 733e03405481b5bf74552ca680f1876f8ebddbf28aa13b938c910ffd592b364e | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/179.npz | 1083318 | c285b0f0dedc942fd35ff633badb614b6b4a55b42a9bc329490c175f02dc693a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_180.json | 4251 | 92d216b887c32eda10af7c803963ff94a0048167c703d3c56c1d07521c301f28 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_180.jsonl | 1158 | 4f8f5d8d2732e2db5f1086ce736be4849f0e7a48d83d2f31711cdb743111b739 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_180.npz | 3790 | eed87eaeb63da19a254c8fbdbe7233d3b3762e2ff6757d2f9d0a7e52eec3b45f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_180.npz | 2726993 | 434735d88fe840d6e46b34a074871be19cf2ee67467a8a41f9b167f49c3207df | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_180.npz | 852 | 6920b5179b2b06cab6db38d3c17e7396632314a44648b87f54b920abb6d64ffd | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/180.npz | 6826540 | d69f095f0d239feba321640aa2429f90490a53b842c57433bb75f0c9c3c808ca | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/180.npz | 1079733 | 095b94fb4949cf6678a549b71d53f51afa7144d84964e6cab8de396bd5942a76 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/180.npz | 1078953 | 5db2844b3f1b427783972a4d3cabaa879147b4caf73c3ff9c83d10bf5b65eae7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_181.json | 4243 | 8387181f99cb587160e87d50cd842129058d980e48d3bf1e2edbb497ee80c1dc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_181.jsonl | 1158 | 9baa22282e43fca1286933cd074fedfe9355eeab0d0c9c015ab4028e52913fdb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_181.npz | 3790 | 7c1448235f8b5290312d00ff84e15d0e015952d9b528e32f5d7fdcadf620d0cf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_181.npz | 905681 | 936f99a64e90a77831ff32a44402e499590262eac42113928a6dafcbe9dd07d3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_181.npz | 852 | ecccb43fbfcc0ee8edcec4ef34f6e3988ce385217a08cff49ab344570e80fc47 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/181.npz | 1746458 | e859cb9ca9d5ae4bbbc995b97d0d59cef9702d965f273cfdc271e1e36af0ad3b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/181.npz | 294482 | e970763b245bab9d8b403f7a822edfa03ed91febf7d00e459d94b60b656d7b8d | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/181.npz | 294399 | 040059fbcee789d85648ae1fe0d69a835e78ad222b534cf2257a1780c39c42e7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_182.json | 4242 | 78a532a17facb547736cc3e50013d42536d5c028265504e155f0a0ac6e3afb8b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_182.jsonl | 1157 | aff391b05d27471e6ab37c27473ab281717b989673c3311889f53ef8266ea6f9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_182.npz | 3790 | 0b0529095c377e9900676292914bba1256f05650f6d35e27c38b60c49a20fe8e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_182.npz | 2726993 | 6687d467737ccf7301f96812777b3f1beca6ca574b2c6a39319bcd894cbdc9be | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_182.npz | 852 | 4f3b9e484dbc6feb11f3bb4b2feedff2997f9472b281013e02bb575f86c4815d | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/182.npz | 6821934 | e66fa1368c011f17aeb31f5b29b90b9a9a4fa9c183d95564e005709fd0ba017d | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/182.npz | 1086335 | 97d0866e69d89737ff74cd24d0c15c154144febb5195f6ce1fdac49b2c443d64 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/182.npz | 1087921 | 19848e8ef06eceb65352bc8b11275b29207f1c6ba1d2758f38c61495a757bb1a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_183.json | 4245 | f690e9edf2d456a406fae80e125ff5c639426f68f52f4ccbf4e61da1b4a5284b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_183.jsonl | 1157 | 08f76726a619423b3050ef2a937214ebb77fcb56e8d9c6dc42a0b12e7fa890a4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_183.npz | 3790 | 4ddb207e25837461c123069bb3138d8354da3ea61f1fcf4d12b0626b618aef03 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_183.npz | 905681 | af622c6da39c5a5f9b5b7859050050f2a04d8957057b6112514478ccd2ffb0c5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_183.npz | 852 | 9d3e333a923766b87b227079d78464a173deaef5d159685f0bbaaca2aefb1be4 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/183.npz | 1743491 | 01b3e4932bf56baffa0c22d36f9feb5a62ec2b9b815423b3a03782fbf8f62af2 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/183.npz | 296717 | b677216bec52bbf9c6903b030239cf0e0b461f6acdbbe0996c40d8eb9513f1a5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/183.npz | 296875 | da16112671de9a3c45fb56659cdd81d9a2c26a956c4ef0a3fff4bc5aff8eda59 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_184.json | 4249 | 46d9dfaa2abc7aac7a7efda1077cafd03ac69b964da74cab3869c9084580b6fb | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_184.jsonl | 1157 | 8ab43267911244f86d5a6a0b49d62b0183b856e9cb825468f4ca588ba24f245e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_184.npz | 3790 | 4db4357a658af053f78a609fd59e4b98d78a6fe7e26542c90fb93ea320b9b143 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_184.npz | 2726993 | 5df9335bc5e3f1f19fbb1b6705312b9ec0337b8355fe9bea9e3ec7e4402ab833 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_184.npz | 852 | 423a771c2b6358d7e2b99b33b012350f4c9db5e1f0cac5ee2748df0176191aa8 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/184.npz | 6826727 | 287754bc86333e21a2175d189881772b6bd6042329b19b985f33f392c852226d | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/184.npz | 1076859 | 355f76e4a095ef3b3ed02c62316b6b3c4ad165838f9122e4588c4e23c7b2cc5c | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/184.npz | 1077568 | 3237cf49198c8759afbd274189737488c80de98c6b6eac1a1d6694a4dd8b1b1f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_185.json | 4250 | e5eb4df9923ca94b140a804d87c19106388f1d5cca7de955824661e6bbc0d2f4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_185.jsonl | 1158 | 0db84e85c1a97efedbb54754b38b99c078e7694d57e3ee4bd645e7fa7198882b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_185.npz | 3790 | 77c474a831a7c7219a10e6558ab732bbde116b58edcc7c51db75dd1dac0e261e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_185.npz | 2726993 | b16b87bbb43d4268b56097e775988683b502b9e5af0be450bb875483b2cafa15 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_185.npz | 852 | d954d93cde34021c31d2456f6aaff4324ee74e8f49c2b938f34d413b00dd2698 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/185.npz | 6825267 | 45c77a0a24aa2aed7738f3e8dd78089486837009eb80a156a97140dbd1616c97 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/185.npz | 1080211 | 4234ec42646ca0ff8c4c78e47c5ac21a60c96bec231a586ffc8bc96836e1c093 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/185.npz | 1080373 | 977a5a435125d96ce0b58c6a51dd30d06a6ed7e5dbe9733403e32850ccc3be73 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_186.json | 4245 | 7119d57bbb3b43e95259a874302e81779ee66022be84f3a8f12526bfb2b2b452 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_186.jsonl | 1156 | 43d7f54c52b23ba81cb3a54863ec4854aafedf16c36a7222ce1af7c9319603e9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_186.npz | 3790 | c6c055702fd0b982fb9410f2b01ade6110dbc7f477b654286c4c00321d17a8c2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_186.npz | 2726993 | 0d0556710387877cbac12e4ddcdf79f82ce49137a2d1c64a8c0a88a318320ec7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_186.npz | 852 | 032b5e2fa2f4d23277d5737b763e03e9e1d5a78a185824f8088acfe91ce1614e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/186.npz | 6825487 | a23d0bb5d9d88ea02176b7f87a2ed347e063fd6a7a8b09f24bdf6103e34002ae | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/186.npz | 1077599 | 9a201868b7ee27b08e6c46b3b59b65949f5de264cfac66c0411714d2e079ea23 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/186.npz | 1078823 | b019e24481c1c9d4e32eb8e12ee389d5b747513a2135c348084b297d591fbd34 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_187.json | 4247 | 7d5b0c4b4e592459bdbb54a3edcb631e8232d2170f361f6b043d0a09eacd3d68 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_187.jsonl | 1158 | e6e7c4d402e713ef341f9d305031c13209a06db98e284bf08cf8132e87cbc54a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_187.npz | 3790 | ec0c4c65f6421946f14046118cfe479c0b5a5b043d2ad6cc242eaebdefe15cfa | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_187.npz | 2726993 | 88f65ccde9dd9310511a1767c38577f2f8e49ad1d9a7fbf76e8fc89eed2fc04d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_187.npz | 852 | de3215aa7114f47f437183831cb78d68136a09e28f67b832c8526ec549e74488 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/187.npz | 6807781 | 5a634fe20e9a82a79d38b9ca5670256cf9df8a477b9173e90f3a751727aa0273 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/187.npz | 1075822 | 77c28c349689364d5ac947110a4f370199814e2f46ba1e644bd85422cf9afa33 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/187.npz | 1074509 | 29f9186061c81826313c8ad988cc4158eb631355a2da7c32bf6a4c3df32dd734 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_188.json | 4250 | 4eac66a7a1c3f0ecab73832892bb44a37f898d29a066939e766aca303f289c19 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_188.jsonl | 1155 | c3d9341bcf087673e6ee06382a19fc25090d088fa199731bf9ad2d544033ddf5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_188.npz | 3790 | bb516c64e59cbcb19dcb9aa196ad39aaa09b8aebc32cd9f4a7eca3fe133ebc9e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_188.npz | 2726993 | cd43800021dab5df5972597d2f9851e64b72b4c0fd838ebc93e2b664f29852d7 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_188.npz | 852 | 70c64400bb4bab473efa758a280a5677c7bdaf1c93e04975e44552845a35f17e | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/188.npz | 6821407 | 64c504efc7fcb8bf9259aaea5c48545b5d2b8cd1a9f684df1c8d0317314b9042 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/188.npz | 1085943 | 6b78e42979b062eb9c5948667723eefb991abce8ab4d889ee9196e286edaad47 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/188.npz | 1087371 | 618b8ef56c60a9202dcef863b626f2692a3f2f67502f3f8be11cd96ac3b5743b | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_189.json | 4252 | 68968e192dbefb6604fa8393c62dfd8e80902916426f0302b5e1bb35fe4b302d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_189.jsonl | 1156 | c7c86abe42ee7391a276e7c73e05cbc2d2f2d2f6a7daba305c5aa62b977ac1b4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_189.npz | 3790 | d1d6d6a5df749fde37f91c6de2294a8a3c097f3e5aa40485c20895df468a4c63 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_189.npz | 2726993 | 5f419b635bc3ff53d5d5c0ccf10ed2f414d38080f270e83c96c41a6647b3490f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_189.npz | 852 | c03971e3fce045e6d3f2b47f47304fce17ff35a6c53a7de4e8f0877798d955ea | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/189.npz | 6817334 | 03ec6fb40a807440d7839c8e60598382f29e3079063437ce77c76c0393e78b3b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/189.npz | 1079878 | d6b6e0ea318714052b0882a95bc7c67d190b9e09b69018941abc1f325f383b23 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/189.npz | 1079767 | 8d47e51968e4dd18ea9355416498eb4be99707af6ec33ff8722139b5ffc59fdd | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_190.json | 4257 | d20b9bbfcb687d0532b7bd4d227e76bab96f172332b09be176a499e2022cd2b6 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_190.jsonl | 1157 | a366d97233ae3a3f0387886e527e721d80b812355b93d11005056bf5ae600cea | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_190.npz | 3790 | 6df1a1d0272efeddf0f5a787a0b932c41215d3f7a0684eb17ce92ef46d3e9e51 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_190.npz | 2726993 | fa944bdffa83b2fdcc2c7b6ddf56f274d7457d93aac8745262cec145a12d3c2f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_190.npz | 852 | f34f63d5811a1bb8d02e83ba434537751523933772775ef08421e22fa72856b7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/190.npz | 6808005 | ae2c6fe5888cbef762d55575fb7397c4090a3b30bd51358f9f656f6e849ccc4c | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/190.npz | 1078070 | e1961e0494f5b210110cb5d8b292d98ba51503a311202a1c9171908e7782be35 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/190.npz | 1079699 | 07def79b1c4cbf5dc81a6e6f760fbca62945f71d0ddf2b098b11effc0ccb86f3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_191.json | 4254 | 12ab15103a4823e8c460f65a1742017d81422ddced2a58fd46e932f8db49556d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_191.jsonl | 1155 | 1206cba66b7bf73aa1620e8135a07a04dcc68dafd5212cfa086c623b8f7988ce | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_191.npz | 3790 | 726cc9b174b44bd345343ee74474ef558e561e34b7fa00727942cbfe529b975d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_191.npz | 905681 | 7e061a57d28a0e0b179deee309aa7585e59fdd39980cecf472ef94e106c1530d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_191.npz | 852 | 58635c5f60f7938b91162b924d90b781efa113eceffb429a6801ef78084447a3 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/191.npz | 1747278 | f736474783ccab2c1cd444d68fa8d6b5c7d43f1b603e2ba55044e8d05e275449 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/191.npz | 297129 | 472d6e6c360ff284001aa42643b5338bce3953c5c9133524e40a7a6582c16907 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/191.npz | 297450 | b06fa2a3a99ed7b30ef51577a35e1c5a3598e130697c86661cd2baeb62754cc9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_192.json | 4249 | 3123175a3e493929070e1e977a13d6ba25d48bd3be03b6735155344bbfa84276 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_192.jsonl | 1157 | adfc511487c74c724fe46ca3abf7b2cf2aa601a56b466a2e3a89243cd5cc5822 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_192.npz | 3790 | 0d102e295aad832632346c2d3c711408919a836829170024952e59463992ae81 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_192.npz | 2726993 | a9248f127e4e69f9169ce0bb5877f94bead849936d7e5766ef7997e36fbe48a5 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_192.npz | 852 | f3dd43596e15c9e6a1ad78ee31644fc13ac1c12eb884966dc336aa6484a83d69 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/192.npz | 6807072 | a3d190b6a33865dc651eac0a9955246c9aa1e852e281ff51eb2e34dead9db07e | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/192.npz | 1083347 | 6db37736ceaa00b3654caa196d95c4918463227de07ea3ba732a4f2a8d869002 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/192.npz | 1084449 | 91792b8facc3366b7bf1aa75e195f479247dbff71660da4e5e0f45b5c79df641 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_193.json | 4245 | 93390ee773c6e4aedef6bb4a55c6efcf35e23edbe09a668c66ffaf232177e0be | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_193.jsonl | 1158 | 080e592a05fb9cbc3a04a91e640e21f6cae764d79f90d23b24d424f35068d0a9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_193.npz | 3790 | 1813e625d6d188c8feaf92fe1e5e12ed3a573eec657cc17fd68b6c5d3b8430bf | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_193.npz | 905681 | e35e79720af4d990763f78ddc21640a161e157af751912406f667bea2fcc74d2 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_193.npz | 852 | 79ea458ede9e2305c1f8fca1924137b2403a1cdb5ab63deb1b1e5a87d9cb9be4 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/193.npz | 1743019 | 36febac6c457cb4278d2b2b8fb13b1d208ee87cca775b090e18cab21b226a6f7 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/193.npz | 296165 | 3cf970a827b3c3b6135614e50f5efa0fa52f40e98afa2a316121757aac0207f5 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/193.npz | 296345 | 71ada545511d408f5e4aef411713d7f370d05abe5eec7352f3dbbba054b4985d | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_194.json | 4248 | ce30982f8df436b18383e4dedb609f2f0e19eb15ed0c5701dddd98c8927d0cc3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_194.jsonl | 1156 | 749da7ba71d5dda839cfdcf45563115d0f9bcb55be37e5f204f70495f4b2b590 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_194.npz | 3790 | edadf4ddcb1d29c344c752cd8f675db4e3f06335c88f3ce2bf61f38cb360f5da | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_194.npz | 905681 | 56bc82f3ecaa057bfa10fca6e7aff45fb7d5f31cdb3cac919979bae1c408d749 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_194.npz | 852 | 96016a8ea7de5bc989ce86bc6a0862747c59a245ccf39bbf855824968a20bfdc | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/194.npz | 1744788 | 8b222fa7c4fe25f11a0fd4240fe7d1071fb02c5cfdd993306890758645d272db | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/194.npz | 297208 | 215dd795c08902855c792873b5a75cb337d3c8e53beda444c5191b2a3ba24569 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/194.npz | 297486 | 052de41ec15f328741accf9bcd8d34d39ca4a4a08165384df9c16f571f23f59a | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_195.json | 4251 | d837982f698f407ddfd762a982fbe6333e23c36c5b3acbe15e227f2ebdb33305 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_195.jsonl | 1157 | d530f18c7d9d95b813ae03e276e04217529d8f7b614a872f3457b2dbec763f85 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_195.npz | 3790 | a4fc28294dc82f710eacc5713ccf62e6e68aa0e108af9fab4fc3148ef51dda2e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_195.npz | 905681 | 2cd106b79eba8733e620490c286621e3590886d6069114d596f098c28489ec06 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_195.npz | 852 | 1bedce40cc17da0e35f21a819a4d79bf4fa5d24096b33426349d33934eb01c66 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/195.npz | 1745814 | 12ec647c471ca03ff94461588e81a07078778f213cc9459b8e9526f658b8d720 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/195.npz | 294774 | 312785cfeb87f3b90bf7aca70449e530721c72afbc8c07d4e19ca324f4477220 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/195.npz | 294923 | 5d78fbe96cd207b41aebb1affaa63d5f105cc61d62e0789d86256bddc26903bc | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_196.json | 4247 | cfdd0a6e1ad5fff425e45e3d7155ea873aef2f88a3d7a95e78f3d4c00b405c61 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_196.jsonl | 1154 | efe15cd21e6990caa2be3b1571e64a6e97b291847da01f4f03ce9b57436ad145 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_196.npz | 3790 | a563dc4fc9527c2f62e76e8cf81566f6e887831d4bdccccb18f7002230a38125 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_196.npz | 2726993 | f4fb771fb6d0930671dc541b41863e8debab8a4de5ef91567faa8cb0294bacb9 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_196.npz | 852 | 411a6aa9dab581115316211739f16c9dfaaa8a4a4c3c030237a72623eb6b85b7 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/196.npz | 6825213 | 12b1d2bafb6a8241834ead540e352f8eb0dcfa7675a6d8ae2d39eae895c8011b | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/196.npz | 1085593 | acf3db8acc29791a129ef77be31ac1167e404fbfbc23ea4ff30d1f96b9efc1ae | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/196.npz | 1090211 | 59c6d5f068df1ba37d2ec2517962f578efc68c2e43b7406c2a8f0161e5ecd342 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_197.json | 4255 | 24d7ecae44a45b107052c1d0e5244b29fa84936d6be31049516a3d3d69ea6ec3 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_197.jsonl | 1157 | fbcb3a5fb78dff4419cb700148377fe39b237cdcefbdbc630024809004253c63 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_197.npz | 3790 | ec3584e05fa29849ca3b5f70a5cd04a7ae35de50566cbbc96d001aa9dc75e502 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_197.npz | 2726993 | 7e42b59490116bba0e64fd138093c11a334d0c7669bca28cc2383fbfc23abb3e | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_197.npz | 852 | 9795d303f453777fa750bd6c71c19e6954a4d194a531b718581e573b8f329c67 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/197.npz | 6811419 | f42f0f8057a37d6e73383e6d33a48087e40b0e8809013d29f095089435a80a87 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/197.npz | 1078862 | 849b4c5f6ebc4956eb7fbb43900f009d1b8c4965e40e9b550da9f3f2ddf135e0 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/197.npz | 1080012 | 32dd95c86dbfdfbc34f8f98f76e4c65d43faadbfe184e346cda69d282a14eab4 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_198.json | 4257 | 0ccefbedf32acbf05069f8ab25965077b390006a4bc83c4982d60747e110bcc1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_198.jsonl | 1156 | 05f0e8cdf82168dd669a3054c3cd577335aaba7c17ead77e2a65f231b92c9a05 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_198.npz | 3790 | 16b6b4edb796d65515bbb0823e1c6a998a156b931ef422c2cfc1480e97573805 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_198.npz | 905681 | 9b48c521ff0dabb00e1f211b0b1217f1b59a104801efddb9f8bf550d4633a64f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_198.npz | 852 | 565bb3d4abd2f8a0853a978e222e212524864ef236628f3d8b0e11ed75e74340 | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/198.npz | 1747078 | b0511af278049ebdb194f31c225c6ec906858df8d4e4aa6b264d01b34191d1b7 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/198.npz | 295976 | 8b2d7ad0f04e06c59b3d97c1b3bf125ab4bd11731e1e8844f21f86a44b0c3778 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/198.npz | 296459 | e75a9ff26c14ab9c1d861b719a6401790f69c496512beaaae9dfe8f73b0e4a0c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_199.json | 4250 | 105641786f8609fd16df63b5008062d66aa03b5dc92a0511c2feae4bed2dcb1c | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/order_199.jsonl | 1158 | a47335746d47008b2af2d51a2406e0575c48d2ea337f32c7f7158652d59db55f | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/input_199.npz | 3790 | 7b8b57b2265395e9c311f34207e4bea01bb1956e2640a61751ad7fdb0d830907 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/case_199.npz | 2726993 | ce77d8f1f6d293cda5ee1486f75b231d3c5099c4ad4fe1b663aa77d1b673b6a1 | none detected |
| /home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf/score_199.npz | 852 | f73d64de8b4cdbeb9013ac94247b3ab47b747732a006b2fa26932db35380b5bd | scoring-only outcomes: release separately from model inputs |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/evaluation_inputs/199.npz | 6817777 | 3d508336a80af3592b6f786a9e11d88c0d6107202bcbf55bab38a721f97338f3 | none detected |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-20k/199.npz | 1084378 | 6fb51d7eb4e58e5dda3516833ec6838af8bb9b64e8934bcf5dae68c915b96a77 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9/inference/CNN-F/199.npz | 1086173 | 5eceac74b979d599cc7bb2c12705afbffcdde30c8a0ed5a4fd5897afe92810af | none detected |
| runs/stage4b_null/states.npz | 2621952 | 0d7db6b75fc1f1a279e884a1c63205ba278a58726d676e41cb58d2aba5160b4d | none detected |
| runs/stage4b_null/null_0.16.npz | 2379496 | 3eee6184746483dcc4e2a9f4efb8d155521700b7f11fb49fd3b90548c9fab729 | none detected |
| /home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision/inputs/CNN-20k.pt | 4003061 | 3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9_training/CNN-F/selected.pt | 4008277 | f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b | none detected |
| /home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision/physics.py | 3037 | 13ef98834e47bd667f53cce50af3e7d573a1bc4eb9c38987f389a05b1f2fc5d7 | AFD-derived: permission/provenance review before release |
| /home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision/protocol.py | 3390 | e6d002264a8000ac88d15db41b76cd69bf17c5472de04b29f51b56408841412d | AFD-derived: permission/provenance review before release |
