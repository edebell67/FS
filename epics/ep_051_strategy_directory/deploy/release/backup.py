"""Create and verify an explicit EP051 release backup. Version 1.0.0."""
from __future__ import annotations
import argparse, hashlib, json, tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ("decomposition_manifest.json", "solution/database", "verification")

def create(destination: Path) -> dict:
    destination = destination.resolve()
    if ROOT == destination or ROOT in destination.parents:
        raise ValueError("backup destination must be outside the epic source tree")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(destination, "w:gz") as archive:
        for rel in SOURCES: archive.add(ROOT / rel, arcname=rel)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    metadata = {"archive": str(destination), "sha256": digest, "sources": list(SOURCES)}
    destination.with_suffix(destination.suffix + ".sha256.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata

def verify(archive: Path, digest: str) -> bool:
    archive = archive.resolve()
    if hashlib.sha256(archive.read_bytes()).hexdigest() != digest: return False
    with tarfile.open(archive, "r:gz") as bundle:
        names = bundle.getnames()
        if any(Path(name).is_absolute() or ".." in Path(name).parts for name in names): return False
        return all(any(name == source or name.startswith(source + "/") for name in names) for source in SOURCES)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("destination", type=Path); args=parser.parse_args()
    print(json.dumps(create(args.destination), indent=2))
