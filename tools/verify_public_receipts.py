#!/usr/bin/env python3
import json, pathlib, re, sys
problems=[]
for p in pathlib.Path('receipts/public').glob('*.json'):
    try: data=json.loads(p.read_text())
    except Exception as e: problems.append(f'{p}: invalid json {e}'); continue
    text=json.dumps(data,sort_keys=True)
    for marker in ['/say-signed/','/set-signed/','ghp_','github_pat_','SIGN_SEED=','BEGIN PRIVATE KEY','BEGIN OPENSSH PRIVATE KEY']:
        if marker in text: problems.append(f'{p}: secret marker {marker} present')
    if re.search(r'\"(?:token|password|private_key|seed|cookie|signed_url)\"\s*:', text, re.I):
        problems.append(f'{p}: forbidden secret-like key present')
print(json.dumps({'ok':not problems,'problems':problems},indent=2))
sys.exit(1 if problems else 0)
