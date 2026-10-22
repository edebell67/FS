"""Maintain one independently authenticated EP052 Arena agent connection.

VERSION HISTORY v1.3.0 · 2026-09-10 · Translate booth-navigation messages into recorded Arena MOVE actions.
v1.2.0 · 2026-09-10 · Continuously receive and acknowledge owner messages.
v1.1.0 · 2026-09-10 · Request and retain a unique open-admission identity in memory.
v1.0.0 · 2026-09-10 · Identity validation, connection, heartbeat,
read-only inspection and clean disconnect without persisting bearer credentials.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import uuid4


class ArenaError(RuntimeError):
    pass


class Client:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token

    def call(self, method: str, path: str, body=None):
        payload = None if body is None else json.dumps(body).encode()
        headers = {'Authorization': 'Bearer ' + self.token} if self.token else {}
        if payload is not None:
            headers['Content-Type'] = 'application/json'
        try:
            request = Request(self.base_url + path, data=payload, headers=headers, method=method)
            with urlopen(request, timeout=20) as response:
                return json.load(response)
        except HTTPError as exc:
            try:
                detail = json.load(exc).get('detail', 'request rejected')
            except Exception:
                detail = 'request rejected'
            raise ArenaError(f'{method} {path}: HTTP {exc.code} — {detail}') from None
        except URLError as exc:
            raise ArenaError(f'Arena unavailable: {exc.reason}') from None

    def identity(self):
        identity = self.call('GET', '/v1/me')
        if identity.get('role') != 'agent' or not identity.get('agent_id'):
            raise ArenaError('Credential is not an assigned agent credential')
        return identity


def output(value):
    print(json.dumps(value, indent=2, sort_keys=True), flush=True)


def receive_feedback(client: Client, cursor: int) -> int:
    page = client.call('GET', '/v1/me/feedback?' + urlencode({'after': cursor}))
    for item in page.get('items', []):
        client.call('POST', f"/v1/me/feedback/{item['id']}/ack")
        output({
            'type': 'owner_feedback',
            'feedback_id': item['id'],
            'message': item['message'],
            'created_at': item['created_at'],
            'acknowledged': True,
        })
        instruction = item['message'].lower()
        booth = next((name for name in ('breakout_r_rev', 'breakout_rev', 'breakout_r', 'breakout', 'intelligence')
                      if re.search(r'\b' + re.escape(name) + r'\b', instruction)), None)
        if booth and any(word in instruction for word in ('walk', 'move', 'go', 'proceed', 'head', 'visit')):
            pace = 'slow' if 'slow' in instruction else 'fast' if 'fast' in instruction else 'normal'
            movement = client.call('POST', '/v1/me/arena-actions', {
                'request_id': str(uuid4()), 'action': 'MOVE', 'destination': booth, 'pace': pace})
            output({'type': 'arena_action', **movement,
                    'notice': 'Movement accepted by Arena; do not claim arrival before observing completion.'})
    return page.get('next_cursor', cursor)


def run(client: Client, heartbeat_seconds: float, message_seconds: float):
    identity = client.identity()
    exchange = client.call('GET', '/v1/exchange')
    expiry = exchange['configuration']['connection_expiry_seconds']
    if heartbeat_seconds <= 0 or heartbeat_seconds >= expiry:
        raise ArenaError(f'Heartbeat must be greater than zero and below the {expiry}s connection expiry')
    if message_seconds <= 0:
        raise ArenaError('Message polling interval must be greater than zero')
    connection = client.call('POST', '/v1/connections', {'request_id': str(uuid4()), 'purpose': 'strategy_trading'})
    output({'agent_id': identity['agent_id'], 'connection_id': connection['id'], 'active': connection['active']})
    stopping = False

    def stop(_signum, _frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    try:
        feedback_cursor = 0
        next_heartbeat = time.monotonic() + heartbeat_seconds
        next_feedback = time.monotonic()
        while not stopping:
            now = time.monotonic()
            if now >= next_feedback:
                feedback_cursor = receive_feedback(client, feedback_cursor)
                next_feedback = now + message_seconds
            if now >= next_heartbeat:
                client.call('POST', f"/v1/connections/{connection['id']}/heartbeat")
                print(f"heartbeat agent={identity['agent_id']}", flush=True)
                next_heartbeat = now + heartbeat_seconds
            time.sleep(min(.5, max(.05, min(next_feedback, next_heartbeat) - time.monotonic())))
    finally:
        client.call('DELETE', f"/v1/connections/{connection['id']}")
        print(f"disconnected agent={identity['agent_id']}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description='EP052 Arena agent API client')
    parser.add_argument('command', choices=('run', 'identity', 'strategies', 'activity', 'move'))
    parser.add_argument('--base-url', default='http://127.0.0.1:8056')
    parser.add_argument('--heartbeat-seconds', type=float, default=60)
    parser.add_argument('--message-seconds', type=float, default=5)
    parser.add_argument('--name', default='Visiting agent')
    parser.add_argument('--destination', choices=('breakout', 'breakout_r', 'breakout_r_rev', 'breakout_rev', 'intelligence'), default='intelligence')
    parser.add_argument('--pace', choices=('slow', 'normal', 'fast'), default='normal')
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args(argv)
    token = os.environ.get('EP052_AGENT_TOKEN', '').strip()
    client = Client(args.base_url, token)
    if args.command == 'run':
        if not token:
            admitted = client.call('POST', '/v1/agents/access', {'name': args.name})
            client.token = admitted['token']
            output({'admission': admitted['admission'], 'agent_id': admitted['agent_id'], 'name': admitted['name']})
        run(client, args.heartbeat_seconds, args.message_seconds)
    elif not token:
        parser.error('Set EP052_AGENT_TOKEN for read-only commands, or use run to request open admission')
    elif args.command == 'identity':
        output(client.identity())
    elif args.command == 'strategies':
        client.identity()
        output(client.call('GET', '/v1/strategies?availability=available'))
    elif args.command == 'move':
        client.identity()
        movement = client.call('POST', '/v1/me/arena-actions', {
            'request_id': str(uuid4()),
            'action': 'MOVE',
            'destination': args.destination,
            'pace': args.pace
        })
        output({'type': 'arena_action', **movement})
    else:
        client.identity()
        output(client.call('GET', '/v1/arena/activity?' + urlencode({'after': 0, 'limit': args.limit})))


if __name__ == '__main__':
    try:
        main()
    except ArenaError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
