from __future__ import annotations

import marshal
import os
import sys
from pathlib import Path


_REQUIRED = (3, 12)
_PYTHON_312 = Path(r"C:\Users\edebe\anaconda3\python.exe")


def _ensure_python_312() -> None:
    if sys.version_info[:2] == _REQUIRED:
        return
    if _PYTHON_312.exists():
        os.execv(str(_PYTHON_312), [str(_PYTHON_312), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise RuntimeError(
        f"trade_viewer_api.py requires Python {_REQUIRED[0]}.{_REQUIRED[1]} "
        f"to run the preserved fs bytecode; current runtime is "
        f"{sys.version_info.major}.{sys.version_info.minor}"
    )


def _cached_bytecode_path() -> Path:
    _ensure_python_312()
    current = Path(__file__).resolve()
    pyc_path = current.with_name("__pycache__") / f"{current.stem}.cpython-312.pyc"
    if not pyc_path.exists():
        raise FileNotFoundError(f"No Python 3.12 cached bytecode found for {current.name}")
    return pyc_path


def _run_cached_api() -> None:
    pyc_path = _cached_bytecode_path()
    with pyc_path.open("rb") as handle:
        handle.read(16)
        code = marshal.load(handle)

    globals()["__cached__"] = str(pyc_path)
    exec(code, globals())


_run_cached_api()
