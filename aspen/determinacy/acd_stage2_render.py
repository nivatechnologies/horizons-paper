"""Fill §11 sentences and ledger from confirmation numbers only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def pct(v):return 'not evaluable' if v is None else f'{100*v:.2f}%'
def num(v):return 'not evaluable' if v is None else f'{v:.6f}'

def render(d):
    cal=d['R0'];m=d['R1m'];r5=d['R5'];rules=sorted(set(r['rule'] for r in d['resolutions']))
    lines=['# Aspen counterfactual determinacy — confirmation (v2.3)','',
           f"**§11 status: {d['gate']}.** Independent confirmation panel: 200 cases, acd-observation-conf, indices 0–199.",'',
           'All posterior/crude/CNN outputs were written and hashed before realized outcomes for each case; blind-order verification is in `ACD_STAGE2_ARTIFACTS.json`.',
           '',f"Truth coverage: {d['coverage']['covered']}/200 ({pct(d['coverage']['share'])}); Wilson 95% [{pct(d['coverage']['wilson95'][0])}, {pct(d['coverage']['wilson95'][1])}]. Diagnostic exclusions: {d['excluded']}/200. Goodness-of-fit flags: {d['fit_flags']}/200.",
           '', 'Frozen computation: sulaco CPU, dt .01, float64, four NUTS chains, 1000 warmup and 500 draws/chain; required all-draw and 2000-warmup retries retained. R5: first60 qualifying cases at2LT, Q/F/V/R only. CNN-20k: sulaco GPU inference only.',
           '', 'Cuts: '+', '.join(d['settings']['cuts'])+'. RML-conf and all-site ceiling not run; no R5/CNN at3LT. P/B are reported only at2/3LT.',
           '', '| Lead (LT) | R0 | Case accuracy [95% one-sided L,U] | Answer accuracy / answers / cases | Included-excluded R0 | R0-F accuracy [L,U] / status |',
           '|---|---|---|---|---|---|']
    for row in cal:
        r=row['R0'];f=row['R0_F'];i=r['included_excluded']
        lines.append(f"| {row['lead']:g} | {r['status']} | {num(r['case_accuracy'])} [{num(r['case_lower'])}, {num(r['case_upper'])}] | {num(r['answer_accuracy'])} / {r['answers']} / {r['cases']} | {i['status']}; {num(i['case_accuracy'])} [{num(i['case_lower'])}, {num(i['case_upper'])}] | {num(f['accuracy'])} [{num(f['lower'])}, {num(f['upper'])}] / {f['status']} |")
    lines+=['','R0 uses the worse primary/included-excluded status. Bounds use the frozen v2.3 betting procedure; R0-F uses exact Clopper–Pearson. Case-index ordering and all count floors remain fixed.','',
            '| Lead (LT) | All-confident S | Observation-confident S | Confident Fc | Median correlation | Median cancellation |',
            '|---|---|---|---|---|---|']
    for t in [3,5]:
        r=m['lead_relationship'][t]
        lines.append(f"| {r['lead']:g} | {pct(r['confident_S_share'])} | {pct(r['observation_S_share'])} | {pct(r['confident_Fc_share'])} | {num(r['median_rho'])} | {num(r['median_cancellation'])} |")
    lines+=['','## Publish routes','']
    for r in d['R2a']:lines.append(f"R2a {r['lead']:g} LT: **{r['status']}**; Δ {num(r['point'])}, 99% interval [{num(r['lower'])}, {num(r['upper'])}]; prerequisites met: {r['prerequisite']}.")
    b=d['R2b'];lines+=['',f"R2b: **{b['status']}**; Δ_loss {num(b['point'])}, 99% interval [{num(b['lower'])}, {num(b['upper'])}], {b['cases']} eligible cases and {b['actions']} eligible actions; prerequisites met: {b['prerequisite']}. Case-averaged loss shares: "+', '.join(f'{k} {pct(v)}' for k,v in b['pair_shares'].items())+'.',
                              '',f"R5 2 LT: **{r5['status']}**; common population {r5['population']}, margin {num(r5['margin'])}.",'',
                              '| Arm | Confident-correct / population | Confident-wrong | Accuracy lower95 | Truth coverage | Failed refits |',
                              '|---|---|---|---|---|---|']
    for arm,r in r5['arms'].items():lines.append(f"| {arm} | {r['correct']} / {r['population']} | {r['wrong']} | {num(r['accuracy_lower'])} | {pct(r['coverage'])} | {r['failed']} |")
    lines+=['','Exact one-sided McNemar: '+('; '.join(f"Q vs {a}: {r['q_only']} vs {r['other_only']} discordant; p={r['p']:.10g}" for a,r in r5['McNemar'].items()) or 'not evaluable')+'.','',
            '## Comparators and horizon rule','',
            '| Comparator | Lead (LT) | Confident S | Observation-confident S | Case accuracy [L,U] | R0 | Cohen kappa S |',
            '|---|---|---|---|---|---|---|']
    for t in [3,5]:
        a=d['R3'];r=a['calibration'][t]['R0'];share=next(v for v in a['confidence_shares'] if v['type']=='S' and v['lead']==cal[t]['lead'])
        lines.append(f"| Crude | {cal[t]['lead']:g} | {pct(share['all'])} | {pct(share['observation'])} | {num(r['case_accuracy'])} [{num(r['case_lower'])}, {num(r['case_upper'])}] | {r['status']} | {num(a['kappa_S'][t])} |")
    cnn=d['R6']
    if cnn['status']=='COMPLETE':
        r=cnn['calibration']['R0'];share=next(v for v in cnn['confidence_shares'] if v['type']=='S')
        lines.append(f"| CNN-20k | 2 | {pct(share['all'])} | {pct(share['observation'])} | {num(r['case_accuracy'])} [{num(r['case_lower'])}, {num(r['case_upper'])}] | {r['status']} | {num(cnn['kappa_S'])} |")
        p=cnn['posterior_not_confident'];lines+=['',f"R6 among posterior-not-confident S: {p['cnn_confident']}/{p['questions']} CNN-confident ({pct(p['X'])}); {p['correct']} correct ({pct(p['Y'])}). Surviving paired members: min {min(cnn['members'])}, max {max(cnn['members'])}; zero-member cases {cnn['zero_member_cases']}."]
    else:lines+=['',f"R6: {cnn['status']}; no CNN claim licensed."]
    lines+=['',f"R2c forecast-horizon rule: {d['R2c']['horizon']} LT.",'',
            '| Lead (LT) | Rule answers? | Answered not confident | Refused confident | Exception accuracy |',
            '|---|---|---|---|---|']
    for r in d['R2c']['readings']:lines.append(f"| {r['lead']:g} | {r['answers']} | {pct(r['answered_not_confident_share'])} | {pct(r['refused_confident_share'])} | {pct(r['exception_accuracy'])} |")
    lines+=['','## Licensed sentences (§11)','', 'Setup: known one-scale Lorenz-96 law, N=40; inferred F uniform on [6,10], initial-state prior N(0,(10·SIGMA)²); true F=8; 11 noisy full-state snapshots over .84 LT, Gaussian noise .02·SIGMA; eight persistent forcing patterns of amplitude .16; energy averaged over the inherited [T,T+1] LT windows. Confidence means modal posterior probability at least .95 under that model and prior.','']
    licensed=[]
    def add(label,condition,sentence):
        licensed.append(dict(label=label,condition_met=bool(condition),sentence=sentence if condition else None))
        lines.append(f"**{label}.** "+(sentence if condition else 'Condition not met; no sentence licensed.'))
        lines.append('')
    for t in [3,5]:
        r=cal[t]['R0'];f=cal[t]['R0_F'];lead=cal[t]['lead'];s=m['lead_relationship'][t]
        add(f'L1 ({lead:g} LT)',r['status']=='PASS' and f['status']=='PASS',
            f"With 11 noisy snapshots spanning 0.84 Lyapunov times, the posterior under the known law answers the sign of a small intervention’s effect on window energy with at least 95% probability for {pct(s['confident_S_share'])} of case–action questions at {lead:g} LT ({pct(s['observation_S_share'])} beyond what climatology alone gives), against {pct(s['confident_Fc_share'])} for the sign of the unforced window-energy anomaly.")
        i=r['included_excluded']
        add(f'L2 ({lead:g} LT)',r['status']=='PASS',
            f"Averaged over cases, confident intervention-sign answers that climatology alone does not give are right {pct(r['case_accuracy'])} of the time at {lead:g} LT (one-sided 95% lower bound {num(r['case_lower'])}); over all such answers, {pct(r['answer_accuracy'])}. Including excluded cases: case accuracy {pct(i['case_accuracy'])}, lower bound {num(i['case_lower'])}, answer accuracy {pct(i['answer_accuracy'])}.")
        a=next(v for v in d['R2a'] if v['lead']==lead)
        phrase='differ by' if a['status']=='DIFFERS' else 'are within 0.10 of each other, with difference' if a['status']=='EQUIVALENT' else 'have difference'
        suffix=', which establishes neither a difference nor equivalence' if a['status']=='INCONCLUSIVE' else ''
        add(f'L3a ({lead:g} LT)',a['status'] in ['DIFFERS','EQUIVALENT','INCONCLUSIVE'],
            f"At {lead:g} LT the observation-confident S share and the confident share for the sign of the unforced window-energy anomaly {phrase} {num(a['point'])} (99% interval [{num(a['lower'])}, {num(a['upper'])}]){suffix}.")
        add(f'L4 ({lead:g} LT)',r['status']=='PASS',f"At {lead:g} LT, the posterior correlation between factual and counterfactual window energies is {num(s['median_rho'])} (median), so the difference carries {num(s['median_cancellation'])} of their summed uncertainty.")
        climate=(s['confident_S_share']-s['observation_S_share'])/s['confident_S_share'] if s['confident_S_share'] else None
        add(f'L5 ({lead:g} LT)',r['status']=='PASS',f"Of the confident sign answers at {lead:g} LT, {pct(climate)} are given by climatology at the true forcing; the rest depend on the observations.")
    p=b['pair_shares'];condition=b['prerequisite'] and b['cases']>=30
    if b['status'] in ['OUTLIVES','PRECEDES']:
        phrase='outlasts' if b['status']=='OUTLIVES' else 'is lost before'
        sentence=f"Paired by case, confidence in an intervention’s sign {phrase} confidence in the sign of the unforced window-energy anomaly: it is lost later in {pct(p['later'])} and earlier in {pct(p['earlier'])} of a case’s eligible actions, averaged over cases (99% interval for the difference [{num(b['lower'])}, {num(b['upper'])}])."
    elif b['status']=='NO DIRECTIONAL PREFERENCE':sentence=f"Paired by case, confidence in an intervention’s sign shows no directional preference between earlier and later loss relative to the sign of the unforced window-energy anomaly (Δ_loss {num(b['point'])}, 99% interval [{num(b['lower'])}, {num(b['upper'])}] within ±0.10)."
    else:sentence=f"Paired loss difference {num(b['point'])}, 99% interval [{num(b['lower'])}, {num(b['upper'])}]; no ordering word is licensed."
    add('L3b',condition,sentence)
    arms=r5['arms'];complete=all(a in arms for a in ['Q','F','V','R'])
    if complete:
        if r5['status']=='Q-BEATS':sentence=f"Four precise measurements targeted at the decision question turn {pct(arms['Q']['C'])} of open decision questions at 2 LT into confident, correct answers, against {pct(max(arms[a]['C'] for a in ['F','V','R']))} for the best of spread-targeted, forecast-targeted and random measurements."
        else:sentence=f"Question-, forecast-, spread-targeted and random measurements turned {pct(arms['Q']['C'])}, {pct(arms['F']['C'])}, {pct(arms['V']['C'])} and {pct(arms['R']['C'])} of open decision questions at 2 LT into confident, correct answers; question targeting did not reliably beat the best alternative."
    else:sentence='Measurement population not evaluable.'
    add('L6 (2 LT)',complete and r5['population']>=40,sentence)
    lines+=['The all-40-site clause is omitted because R5-A was cut before confirmation; no ceiling is inferred.','']
    crude=d['R3']['calibration'][3]['R0'];strong=crude['case_accuracy'] is not None and crude['case_accuracy']<.85 and crude['case_upper']<.90
    add('L7 (crude)',crude['case_accuracy'] is not None,(f"An ensemble built from perturbed last frames gives confident answers that are right only {pct(crude['case_accuracy'])} of the time." if strong else f"An ensemble built from perturbed last frames gives observation-confident intervention-sign answers with case-averaged accuracy {pct(crude['case_accuracy'])} and answer-level accuracy {pct(crude['answer_accuracy'])} at 2 LT (one-sided 95% upper bound {num(crude['case_upper'])})."))
    add('L7 (RML)',False,'')
    if cnn['status']=='COMPLETE':
        p=cnn['posterior_not_confident'];r=cnn['calibration']['R0']
        sentence=f"On sign questions where the posterior is not confident at 2 LT, a deterministic CNN emulator’s ensemble is confident on {pct(p['X'])} and right on {pct(p['Y'])} of those."
        if r['case_accuracy'] is not None and r['case_accuracy']<.85 and r['case_upper']<.90:sentence+=f" The ensemble is overconfident: case-averaged observation-confident accuracy {pct(r['case_accuracy'])}, one-sided 95% upper bound {num(r['case_upper'])}."
        add('L8 (2 LT)',cal[3]['R0']['status']=='PASS' and p['X'] is not None and p['Y'] is not None,sentence)
    else:add('L8 (2 LT)',False,'')
    rows=d['R2c']['readings'];answered=[r for r in rows if r['answers']];refused=[r for r in rows if not r['answers']]
    U=sum(r['answered_not_confident_share'] for r in answered)/len(answered) if answered else None
    D=sum(r['refused_confident_share'] for r in refused)/len(refused) if refused else None
    denominator=sum(r['answered_not_confident_share'] for r in answered)
    V=sum(r['answered_not_confident_share']*(r['exception_accuracy'] or 0) for r in answered)/denominator if denominator else None
    add('L9',U is not None and V is not None and D is not None,
        f"Answering every question up to the lead at which the sign of the unforced window-energy anomaly is confident for half the cases, and none beyond, would answer {pct(U)} of sign questions the posterior is not confident on (right {pct(V)}) and refuse {pct(D)} that it is confident on. Fractions are within the answered and refused lead ranges respectively.")
    add('L10',False,'')
    lines+=['## Resolutions and scope','', 'Rules fired: '+', '.join(rules)+'.','']
    for r in d['resolutions']:lines.append(f"- **{r['rule']}** — {r['trigger']}: {json.dumps(r['detail'],ensure_ascii=False)}")
    lines+=['','All bootstrap share/mechanism/comparator intervals are approximate and descriptive; they do not gate publication or license comparison words. Betting, exact Clopper–Pearson and exact McNemar determine the route statuses. Null probabilities are reused unchanged; climate classification uses the sampler’s modal answer. Wilks coverage is measured and approximate.',
            '', 'The full receipt contains R1 maps, R1m covariance/divergence, R2c per-lead errors/refusals, R3/R6 calibration and reliability, R5 site/refit records, rank histograms, fit flags and diagnostic uncertainty: `receipts/acd_stage2.json`. Omitted readings supply no claim. This is a confirmation reading, not an abstract submission.',
            '', 'Related: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], [[L_Aspen-Counterfactual-Determinacy-Claim-Ledger-2026-10]].']
    text='\n'.join(lines)+'\n';(ROOT/'ACD_STAGE2_READING.md').write_text(text)
    target=ROOT/'vault/04-Results/R_Aspen-Counterfactual-Determinacy-Confirmation-2026-10.md';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    (ROOT/'runs/audit/acd_licensed_sentences.json').write_text(json.dumps(licensed,indent=2)+'\n')
    old=(ROOT/'sources/Ledger_pre_stage2.md').read_text()
    q=arms.get('Q',{});best=max((arms[a]['C'] for a in ['F','V','R'] if a in arms),default=None)
    ledger=old+'\n## Confirmation update — 2026-10-05\n\n'+f"§11 status **{d['gate']}**. Independent 200-case confirmation at the frozen noise, actions, law and compute settings. R0 at2LT {cal[3]['R0']['status']}, at3LT {cal[5]['R0']['status']}; truth coverage {d['coverage']['covered']}/200. R2a statuses: "+', '.join(f"{v['lead']:g}LT {v['status']}" for v in d['R2a'])+f". R2b {b['status']}, Δ_loss {num(b['point'])}. R5 {r5['status']}: Q {pct(q.get('C'))}, best alternative {pct(best)}, margin {num(r5['margin'])}.\n\n"
    ledger+='The historical development-only risks above describe Stage1. Confirmation numbers now determine publication licensing under §11; every licensed or unavailable sentence is enumerated in the confirmation reading. Scope remains this one-scale perfect-model Lorenz-96 setting; no broader system claim is licensed. Resolution rules: '+', '.join(rules)+'.\n\n'
    ledger+='[Confirmation reading](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_STAGE2_READING.md). Related: [[R_Aspen-Counterfactual-Determinacy-Confirmation-2026-10]].\n'
    (ROOT/'CLAIM_LEDGER.md').write_text(ledger)
    (ROOT/'vault/04-Results/L_Aspen-Counterfactual-Determinacy-Claim-Ledger-2026-10.md').write_text(ledger)
