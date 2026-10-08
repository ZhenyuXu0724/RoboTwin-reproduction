"""Verify publication integrity and paired experimental evidence without GPU/data."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXP=ROOT/'experiments/2026-10-08-policy-comparison'

def load(name):return json.loads((EXP/name).read_text())

def main():
    manifest=load('publication-manifest.json')
    for rel,record in manifest['files'].items():
        path=(ROOT/rel).resolve()
        assert path.is_relative_to(ROOT),rel
        data=path.read_bytes()
        assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],rel
    four=load('four-way-results.json');ablation=load('ablation-results.json')
    assert four['status']==ablation['status']=='completed'
    seeds=four['seeds'];assert len(seeds)==len(set(seeds))==20
    rows=four['rows']+ablation['rows']
    expected=load('export-verification.json')['successes']
    for policy,count in expected.items():
        group=[r for r in rows if r['policy']==policy]
        assert len(group)==20 and sorted(r['seed'] for r in group)==sorted(seeds)
        assert all(r['valid'] and r['complete'] and r['actual_seed']==r['seed'] and r['steps']<=four['steps_limit'] for r in group)
        assert all(not r['actor_truth_for_control'] for r in group)
        assert sum(r['success'] for r in group)==count
        summary=(ablation if policy=='ACT_GRASP_ONLY' else four)['summaries'][policy]
        assert summary['successes']==count and summary['valid_cases']==len(group)
    for seed in seeds:
        group=[r for r in rows if r['seed']==seed]
        assert all(r['initial']==group[0]['initial'] for r in group)
    full={r['seed']:r for r in four['rows'] if r['policy']=='ACT_RGBD'}
    pairs=Counter()
    for r in ablation['rows']:
        assert r['prefix_max_command_difference']==0
        assert not any('release' in event for event in r['guard_event_counts'])
        pairs[f"FULL_{int(full[r['seed']]['success'])}_NO_RELEASE_{int(r['success'])}"]+=1
    assert dict(pairs)==ablation['paired_outcomes']
    assert ablation['baseline_rows']==[r for r in four['rows'] if r['policy']=='ACT_RGBD']
    split=load('split-40-10.json')
    # Split keys follow the archived dataset schema.
    train=split.get('train_episode_ids',split.get('train'));val=split.get('validation_episode_ids',split.get('validation'))
    assert len(train)==40 and len(val)==10 and not set(train)&set(val)
    metrics=[json.loads(s) for s in (EXP/'dp-training-metrics.jsonl').read_text().splitlines()]
    assert [r['epoch'] for r in metrics]==list(range(1,2001))
    assert metrics[-1]['optimizer_steps']==80000
    assert load('dp-training-completion.json')['status']=='completed'
    assert load('dp-diagnosis-completion.json')['status']=='completed'
    assert load('ablation-completion.json')['status']=='completed'
    points=[json.loads(s) for s in (EXP/'dp-expert-points.jsonl').read_text().splitlines()]
    assert len(points)==load('dp-diagnosis-verification.json')['expert_points']==550
    with (EXP/'paired-results.csv').open() as stream:compact=list(csv.DictReader(stream))
    assert len(compact)==len(rows)==100
    assert {(r['policy'],int(r['seed']),r['success']=='True',int(r['steps'])) for r in compact}=={
        (r['policy'],r['seed'],r['success'],r['steps']) for r in rows}
    print(f"Verified {len(manifest['files'])} public files; 100 rollouts, 20 paired scenes, 2000 training epochs, 550 diagnostic points")

if __name__=='__main__':main()
