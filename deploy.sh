set -e
[ -d venv ] || virtualenv venv
. venv/bin/activate
pip install build tox
tox
python -m build
ssh pi@blunderboard.igloo.icmp.camp rm -f 'blunderboard-*.whl'
scp dist/blunderboard-*.whl pi@blunderboard.igloo.icmp.camp:
ssh pi@blunderboard.igloo.icmp.camp blunderboard/venv/bin/pip uninstall -y blunderboard
ssh pi@blunderboard.igloo.icmp.camp blunderboard/venv/bin/pip install 'blunderboard-*.whl'
