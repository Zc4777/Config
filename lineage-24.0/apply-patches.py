#!/usr/bin/env python3
"""Apply the recorded upstream-source patches after syncing manifest.xml."""
from pathlib import Path
import argparse,hashlib,json,subprocess
p=argparse.ArgumentParser();p.add_argument('source_root',type=Path);p.add_argument('--check',action='store_true');args=p.parse_args()
root=args.source_root.resolve();here=Path(__file__).resolve().parent
if not (root/'.repo').is_dir():p.error('source_root must be the root of a repo checkout')
items=json.loads((here/'sources.json').read_text())['sources'];pending=[]
for item in items:
 if not item.get('apply_after_sync'):continue
 patch=here/item['patch'];assert hashlib.sha256(patch.read_bytes()).hexdigest()==item['sha256']
 project=root/item['path'];cmd=['git','-C',str(project),'apply']
 if subprocess.run(cmd+['--reverse','--check',str(patch)],capture_output=True).returncode==0:
  print('Already applied:',item['path']);continue
 head=subprocess.check_output(['git','-C',str(project),'rev-parse','HEAD'],text=True).strip()
 if head!=item['base']:raise SystemExit('Wrong source revision: '+item['path'])
 subprocess.run(cmd+['--check',str(patch)],check=True);pending.append((item,cmd,patch))
for item,cmd,patch in pending:
 if not args.check:subprocess.run(cmd+[str(patch)],check=True)
 print(('Checked: ' if args.check else 'Applied: ')+item['path'])
