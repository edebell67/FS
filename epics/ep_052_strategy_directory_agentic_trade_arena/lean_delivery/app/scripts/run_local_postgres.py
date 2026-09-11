# VERSION HISTORY v1.1.0 · 2026-09-11 · Expose local Arena on all interfaces with explicit trusted hosts.
# v1.0.1 · 2026-09-10 · Accept a BOM-prefixed local pgpass entry.
# v1.0.0 · 2026-09-10 · Launch local EP052 against the existing PostgreSQL database without exposing credentials.
import os
from pathlib import Path

import uvicorn


def database_url():
    path = Path(os.environ['APPDATA']) / 'postgresql' / 'pgpass.conf'
    for line in path.read_text(encoding='utf-8').splitlines():
        fields = line.lstrip('\ufeff').strip().split(':', 4)
        if len(fields) == 5 and fields[:4] == ['localhost', '5432', 'tradedb', 'postgres']:
            return 'postgresql://postgres:' + fields[4] + '@localhost:5432/tradedb'
    raise RuntimeError('Local tradedb credential entry not found')


if __name__ == '__main__':
    os.environ['EP052_DATABASE_URL'] = database_url()
    os.environ.setdefault('EP052_ALLOWED_HOSTS', '127.0.0.1,localhost,172.22.96.1')
    uvicorn.run('lean_exchange.api:create_app', factory=True,
                host=os.environ.get('EP052_BIND_HOST', '0.0.0.0'), port=8056)
