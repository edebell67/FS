# VERSION HISTORY v1.1.1 · 2026-09-11 · Make source-tree launches independent of editable package installation.
# v1.1.0 · 2026-09-11 · Expose local Arena on all interfaces with explicit trusted hosts.
# v1.0.1 · 2026-09-10 · Accept a BOM-prefixed local pgpass entry.
# v1.0.0 · 2026-09-10 · Launch local EP052 against the existing PostgreSQL database without exposing credentials.
import os
from pathlib import Path
import sys

import uvicorn


def database_url():
    path = Path(os.environ['APPDATA']) / 'postgresql' / 'pgpass.conf'
    for line in path.read_text(encoding='utf-8').splitlines():
        fields = line.lstrip('\ufeff').strip().split(':', 4)
        if len(fields) == 5 and fields[:4] == ['localhost', '5432', 'tradedb', 'postgres']:
            return 'postgresql://postgres:' + fields[4] + '@localhost:5432/tradedb'
    raise RuntimeError('Local tradedb credential entry not found')


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
    os.environ['EP052_DATABASE_URL'] = database_url()
    # EP057 strategy intelligence provider (scenario_engine_v2/start_runner.bat); EP052_INTELLIGENCE_URL set beforehand wins.
    os.environ.setdefault('EP052_INTELLIGENCE_URL', 'http://127.0.0.1:8766/v1/queries')
    _token = Path(__file__).resolve().parents[1] / '.credentials' / 'ep057_intelligence_token.txt'
    if _token.exists():
        os.environ.setdefault('EP052_INTELLIGENCE_TOKEN', _token.read_text(encoding='utf-8').strip())
    os.environ.setdefault('EP052_ALLOWED_HOSTS', '127.0.0.1,localhost,172.22.96.1')
    uvicorn.run('lean_exchange.api:create_app', factory=True,
                host=os.environ.get('EP052_BIND_HOST', '0.0.0.0'), port=8056)
