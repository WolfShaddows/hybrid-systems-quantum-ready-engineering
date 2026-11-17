# Purpose: lock python (scripts/lock_python.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
from importlib import metadata
from pathlib import Path
from packaging.requirements import Requirement
ROOT=Path(__file__).resolve().parents[1]
roots=["qiskit","qiskit-aer"]
seen={}
def walk(name):
    try: dist=metadata.distribution(name)
    except metadata.PackageNotFoundError: raise SystemExit(f"Missing package: {name}")
    canonical=dist.metadata["Name"]
    if canonical.lower() in seen: return
    seen[canonical.lower()]=f"{canonical}=={dist.version}"
    for item in dist.requires or []:
        req=Requirement(item)
        if req.marker and not req.marker.evaluate(): continue
        walk(req.name)
for root in roots: walk(root)
path=ROOT/"qiskit/requirements.lock"
path.write_text("\n".join(sorted(seen.values(),key=str.lower))+"\n",encoding="utf-8")
print(f"Wrote {len(seen)} pinned packages to {path}")



