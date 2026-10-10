# Stage22 case-count execution reading

R-other: criteria unchanged. Stage21 files remain untouched. Parameterized copies replace only assigned-case-count literals, including the balanced half-count expressed as N//2. The adapter supplies N before executing those copies. The line-level diff is in ACD_STAGE22_PARAMETERIZATION.diff and is embedded in Freeze F.

The N=200 replay used Stage21 namespaces and committed inference outputs on sulaco CPU. Every JSON value, including provenance fields and all descriptive entries, reproduced exactly for the receipts listed below. No Stage22 observation or outcome was generated. The existing realized cache was opened only inside the frozen score_actual function; each access was logged with its hash and caller. Hash-manifest coverage, realized score-array coverage and receipt coverage were asserted against N. Retained/excluded populations and forcing subgroups keep their original definitions.

- acd_stage21_R12_recovery.json: exact=True; differing values=0; assigned cases=200; SHA-256 d268819d30b774450a2ba516f6320fcd78956ecfe144b72496ad63c19fa38bdf.
- acd_stage21_R34.json: exact=True; differing values=0; assigned cases=200; SHA-256 5499288b63ed14def18c4206c9a084ccaebd635ff5ee4b353b2d95824d3f2877.
- acd_stage21_descriptive.json: exact=True; differing values=0; assigned cases=200; SHA-256 7241c5874fa0bb60e3aee4d2742a61f84d29b2891b617a6c3b652ee0d2f536e3.

The empty diff JSON files and outcome-access log accompany this execution reading. Stage22 sampling remains gated on the pushed Freeze F and panel contract. The same parameterization applies to Stage23 scoring on this panel.

## Remaining literal 200 inventory

The inventory follows local ACD imports transitively, including legacy entry points in imported modules. Mathematical coefficients and earlier-panel leaf enumeration are preserved. The new assigned-panel loop and output checks use N in the parameterized copies. Remaining legacy entry points are listed explicitly for review; importing a module does not execute these functions.

- acd_stage19_score.py:18 (score_actual): `for c in range(200):`
- acd_stage19_score.py:50 (run): `for c in range(200):`
- acd_stage6_analysis.py:76 (score_saved_A): `for c in range(200):`
- acd_stage6_analysis.py:111 (a_receipts): `for c in range(200):`
- acd_stage6_analysis.py:159 (mechanism): `for c in range(200):`
- acd_stage6_analysis.py:205 (score_forward): `for c in range(200):`
- acd_stage6_analysis.py:225 (b_readings): `for c in range(200):`
- acd_stage6_analysis.py:194 (score_forward): `for c in range(200):`
- acd_stage6_analysis.py:89 (score_saved_A): `selected=np.full(200,8,dtype=int);probabilities=[]`
- acd_stage6_forward.py:105 (run): `for c in range(200):case(panel,c,amp)`
- acd_protocol.py:59 (assert_leaves): `for c in range(200):`
- acd_fits.py:37 (objective): `val+=100*np.sum(diff*diff)/440;adj+=200*diff/440`
- acd_stage19_part2_gate.py:44 (part1_ready): `if receipt['status'] != 'blind_sampling_complete' or len(receipt['cases']) != 200:`
- acd_stage13_analysis.py:25 (loadcosts): `for c in range(200):`
- acd_stage13_analysis.py:139 (forward_dt): `for c in range(200):`
- acd_stage13_analysis.py:154 (score_dt): `for c in range(200):`
- acd_stage13_analysis.py:68 (score_decisions): `actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])`
- acd_stage13_analysis.py:100 (score_withheld_instance): `actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])`
- acd_confirmation_analysis.py:79 (cnn_reading): `for c in range(200):`
- acd_confirmation_analysis.py:123 (run): `for c in range(200):`
- acd_confirmation_analysis.py:196 (run): `for c in range(200):`
- acd_confirmation_analysis.py:210 (run): `output=dict(null=dict(jbar=jbar,F=8.,states=4096,Fc_above_shares=null[37,:,1].tolist(),question_probabilities=null.tolist()),version='2.3',panel='confirmation',cases=200,gate=decision,dt=dt(),settings=settings(),R0=cal,R1=shares,R1m=mechan,R2a=R2a,R2b=R2b,R2c=dict(horizon=float(LEADS[horizon]) if horizon>=0 else None,readings=R2c),R3=dict(calibration=cal_c,reliability=reliability(sc,truth,keep)),R3b=dict(status='NOT RUN: RML-conf cut'),R5=measure,coverage=dict(covered=covered,total=200,share=covered/200,descriptive=boot(np.array([r['coverage']['covered'] for r in reports]),sub=7),wilson95=[wilson_center-wilson_radius,wilson_center+wilson_radius]),excluded=int((~keep).sum()),fit_flags=sum(r['minimum']>467.6 for r in reports),reliability=reliability(s,truth,keep),threshold_uncertain=s['uncertain'][keep].mean((0,1)).tolist(),split_instability=s['split_unstable'][keep].mean((0,1)).tolist(),true_F_rank=dict(histogram=np.histogram(forcing_ranks,bins=np.linspace(0,1,11))[0].tolist(),uniformity_KS=dict(statistic=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').statistic),p=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').pvalue)),case_values=forcing_ranks),exact_zero_answers=zeros,rank_histogram=np.histogram(np.asarray(ranks)[keep],bins=np.linspace(0,1,11))[0].tolist(),extra_selector_readings=extras,resolutions=resolutions,source_hashes={p.name:digest(p) for p in sorted(list(ROOT.glob('acd_*.py'))+[ROOT/'check_acd.py'])},seconds=time.perf_counter()-start)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_confirmation_analysis.py:202 (run): `kill=covered/200<.85 or (cal[3]['R0']['status']=='FAIL' and cal[5]['R0']['status']=='FAIL')`
- acd_confirmation_analysis.py:210 (run): `output=dict(null=dict(jbar=jbar,F=8.,states=4096,Fc_above_shares=null[37,:,1].tolist(),question_probabilities=null.tolist()),version='2.3',panel='confirmation',cases=200,gate=decision,dt=dt(),settings=settings(),R0=cal,R1=shares,R1m=mechan,R2a=R2a,R2b=R2b,R2c=dict(horizon=float(LEADS[horizon]) if horizon>=0 else None,readings=R2c),R3=dict(calibration=cal_c,reliability=reliability(sc,truth,keep)),R3b=dict(status='NOT RUN: RML-conf cut'),R5=measure,coverage=dict(covered=covered,total=200,share=covered/200,descriptive=boot(np.array([r['coverage']['covered'] for r in reports]),sub=7),wilson95=[wilson_center-wilson_radius,wilson_center+wilson_radius]),excluded=int((~keep).sum()),fit_flags=sum(r['minimum']>467.6 for r in reports),reliability=reliability(s,truth,keep),threshold_uncertain=s['uncertain'][keep].mean((0,1)).tolist(),split_instability=s['split_unstable'][keep].mean((0,1)).tolist(),true_F_rank=dict(histogram=np.histogram(forcing_ranks,bins=np.linspace(0,1,11))[0].tolist(),uniformity_KS=dict(statistic=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').statistic),p=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').pvalue)),case_values=forcing_ranks),exact_zero_answers=zeros,rank_histogram=np.histogram(np.asarray(ranks)[keep],bins=np.linspace(0,1,11))[0].tolist(),extra_selector_readings=extras,resolutions=resolutions,source_hashes={p.name:digest(p) for p in sorted(list(ROOT.glob('acd_*.py'))+[ROOT/'check_acd.py'])},seconds=time.perf_counter()-start)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_confirmation_analysis.py:210 (run): `output=dict(null=dict(jbar=jbar,F=8.,states=4096,Fc_above_shares=null[37,:,1].tolist(),question_probabilities=null.tolist()),version='2.3',panel='confirmation',cases=200,gate=decision,dt=dt(),settings=settings(),R0=cal,R1=shares,R1m=mechan,R2a=R2a,R2b=R2b,R2c=dict(horizon=float(LEADS[horizon]) if horizon>=0 else None,readings=R2c),R3=dict(calibration=cal_c,reliability=reliability(sc,truth,keep)),R3b=dict(status='NOT RUN: RML-conf cut'),R5=measure,coverage=dict(covered=covered,total=200,share=covered/200,descriptive=boot(np.array([r['coverage']['covered'] for r in reports]),sub=7),wilson95=[wilson_center-wilson_radius,wilson_center+wilson_radius]),excluded=int((~keep).sum()),fit_flags=sum(r['minimum']>467.6 for r in reports),reliability=reliability(s,truth,keep),threshold_uncertain=s['uncertain'][keep].mean((0,1)).tolist(),split_instability=s['split_unstable'][keep].mean((0,1)).tolist(),true_F_rank=dict(histogram=np.histogram(forcing_ranks,bins=np.linspace(0,1,11))[0].tolist(),uniformity_KS=dict(statistic=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').statistic),p=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').pvalue)),case_values=forcing_ranks),exact_zero_answers=zeros,rank_histogram=np.histogram(np.asarray(ranks)[keep],bins=np.linspace(0,1,11))[0].tolist(),extra_selector_readings=extras,resolutions=resolutions,source_hashes={p.name:digest(p) for p in sorted(list(ROOT.glob('acd_*.py'))+[ROOT/'check_acd.py'])},seconds=time.perf_counter()-start)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_confirmation_analysis.py:139 (run): `wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)`
- acd_measure.py:68 (population): `for c in range(200):`
- acd_stage9_receipts.py:31 (score): `for c in range(200):`
- acd_stage9_receipts.py:61 (run): `for c in range(200):`
- acd_stage9_receipts.py:93 (run): `for c in range(200):`
- acd_stage9_receipts.py:40 (score): `answer=np.broadcast_to(keep[:,None,None],(200,8,6));right=s['modal'][:,:8,:6]==truth[:,:8,:6]`
- acd_stage9_receipts.py:46 (score): `choices={'E':choice,'no_action':np.full(200,8),'always_uniform_decrease':np.zeros(200,dtype=int)}`
- acd_stage9_receipts.py:46 (score): `choices={'E':choice,'no_action':np.full(200,8),'always_uniform_decrease':np.zeros(200,dtype=int)}`
- acd_stage9_receipts.py:48 (score): `selected=np.full(200,8,dtype=int)`
- acd_stage9_forward.py:60 (run): `for c in range(200):`
