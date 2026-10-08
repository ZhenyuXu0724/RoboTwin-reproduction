"""Restore archived patches into a clean, locked RoboTwin checkout."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE = '30954692d06ba7e89f7a6b76064f4062c488fa81'
XBASE = 'a9ccf8dbc34ad047534a14b7ee0503bddf0e54b5'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()

def patches(root):
    old = REPO/'experiments/2026-10-07-stack-blocks-rgbd'
    new = REPO/'experiments/2026-10-08-policy-comparison'
    return [(root, old/'robotwin-workspace.patch'),
            (root/'XPolicyLab', old/'xpolicylab-act-repaired.patch'),
            (root, old/'training-and-controller.patch'),
            (root, new/'dp-workflow.patch')]

def apply(root, path_root, temporary):
    for index, (destination, source) in enumerate(patches(root)):
        content = source.read_text().replace('${ROBOTWIN_ROOT}', str(path_root)).replace('${USER_HOME}', str(Path.home()))
        path = temporary/f'{index}.patch';path.write_text(content)
        git(destination, 'apply', '--check', str(path))
        git(destination, 'apply', str(path))
    snapshot=json.loads((REPO/'experiments/2026-10-08-policy-comparison/source-snapshot.json').read_text())
    import hashlib
    for rel, record in snapshot['files'].items():
        path=root/rel
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],rel
        compile(path.read_text(), str(path), 'exec')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args=parser.parse_args();root=args.root.resolve()
    if any(c in str(root) for c in ['\n','\r','"','\\']):
        raise ValueError('Choose a root without quotes, backslashes or newlines for historical text substitution')
    assert git(root,'rev-parse','HEAD')==BASE,'RoboTwin baseline mismatch'
    assert git(root/'XPolicyLab','rev-parse','HEAD')==XBASE,'XPolicyLab baseline mismatch'
    # The separately locked XPolicyLab commit can differ from RoboTwin's gitlink.
    assert not git(root,'status','--porcelain','--ignore-submodules=all'),'Use a clean RoboTwin checkout'
    assert not git(root/'XPolicyLab','status','--porcelain'),'Use a clean XPolicyLab checkout'
    with tempfile.TemporaryDirectory(prefix='robotwin-materials-') as tmp:
        temporary=Path(tmp);scratch=temporary/'checkout'
        subprocess.run(['git','clone','--shared','--no-checkout',str(root),str(scratch)],check=True,capture_output=True)
        git(scratch,'checkout','--detach',BASE)
        subprocess.run(['git','clone','--shared','--no-checkout',str(root/'XPolicyLab'),str(scratch/'XPolicyLab')],check=True,capture_output=True)
        git(scratch/'XPolicyLab','checkout','--detach',XBASE)
        apply(scratch, root, temporary)
        if args.apply:apply(root, root, temporary)
    print('Four patches and 24 source snapshots verified; '+('applied to target' if args.apply else 'target unchanged'))

if __name__=='__main__':main()
