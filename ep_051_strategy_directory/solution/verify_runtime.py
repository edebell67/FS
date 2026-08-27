"""EP051 deterministic runtime verification. Version 1.0.0 (2026-08-23)."""
import json,platform,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"decomposition_manifest.json").read_text(encoding="utf-8"))
assert sys.version_info >= (3,11),"Python 3.11+ required"
assert len(manifest["original_task_list"])==44
assert (ROOT/"workstreams").is_dir() and (ROOT/"verification").is_dir()
print(json.dumps({"status":"ready","python":platform.python_version(),"nodes":44,"root":str(ROOT)},sort_keys=True))

