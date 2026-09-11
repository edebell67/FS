# VERSION HISTORY v1.2.0 · 2026-09-10 · Verify open-admitted agents remain reachable by the administering owner.
# v1.1.0 · 2026-09-10 · Verify persisted owner-controlled open Arena entry does not open action/private APIs.
# v1.0.0 · 2026-09-02 · Exercise actual owner/agent access, durable revoke/expiry, input/rate limits and secret redaction.
import json
from uuid import uuid4

from fastapi.testclient import TestClient

from lean_exchange.api import create_app
from lean_exchange.config import Settings, load_settings


def auth(credential):
    return {'Authorization': 'Bearer ' + credential['token']}


def test_owner_can_open_and_close_read_only_arena_without_opening_actions():
    app = create_app()
    owner = app.state.authority.create_owner('Policy owner')
    with TestClient(app) as client:
        assert client.get('/v1/arena/access-policy').json()['entry_mode'] == 'token_required'
        assert client.get('/v1/arena/activity').status_code == 401
        assert client.put('/v1/owner/arena-access', json={'public_access': True}).status_code == 401
        opened = client.put('/v1/owner/arena-access', json={'public_access': True}, headers=auth(owner))
        assert opened.status_code == 200 and opened.json()['entry_mode'] == 'open'
        assert client.get('/v1/arena/activity').status_code == 200
        assert client.get('/v1/arena/connections').status_code == 200
        assert client.get('/v1/strategies').status_code == 200
        assert client.post('/v1/connections', json={}).status_code == 401
        assert client.post('/participant/v1/me/queries', json={}).status_code == 401
        assert client.post('/v1/trades', json={}).status_code == 401
        assert client.get('/v1/owner/agents').status_code == 401
        admitted = client.post('/v1/agents/access', json={'name': 'Open visitor'})
        assert admitted.status_code == 201
        visitor = admitted.json()
        owned = client.get('/v1/owner/agents', headers=auth(owner)).json()['items']
        assert visitor['agent_id'] in {item['agent_id'] for item in owned}
        sent = client.post('/v1/owner/feedback', headers=auth(owner), json={
            'request_id': str(uuid4()), 'agent_ids': [visitor['agent_id']], 'message': 'Owner is online.'})
        assert sent.status_code == 200
        inbox = client.get('/v1/me/feedback', headers=auth(visitor)).json()['items']
        assert inbox[0]['message'] == 'Owner is online.'
    with TestClient(create_app()) as restarted:
        assert restarted.get('/v1/arena/access-policy').json()['entry_mode'] == 'open'
        assert restarted.get('/v1/arena/activity').status_code == 200
        assert restarted.put('/v1/owner/arena-access', json={'public_access': False}, headers=auth(owner)).status_code == 200
        assert restarted.get('/v1/arena/activity').status_code == 401


def test_owner_scoped_registration_and_durable_revocation(tmp_path):
    app = create_app()
    first = app.state.authority.create_owner('Owner A')
    second = app.state.authority.create_owner('Owner B')
    with TestClient(app) as client:
        assert client.get('/v1/me').status_code == 401
        agent = client.post('/v1/owner/agents', json={'name': 'Visiting Hermes'}, headers=auth(first)).json()
        assert client.get('/v1/me', headers=auth(agent)).json()['role'] == 'agent'
        assert client.get('/v1/owner/agents', headers=auth(agent)).status_code == 403
        assert client.get('/v1/owner/agents', headers=auth(second)).json()['items'] == []
        assert client.delete('/v1/owner/credentials/' + agent['credential_id'], headers=auth(second)).status_code == 404
        assert client.get('/v1/me', headers=auth(agent)).status_code == 200
        assert client.delete('/v1/owner/credentials/' + agent['credential_id'], headers=auth(first)).status_code == 200
        assert client.get('/v1/me', headers=auth(agent)).status_code == 401
    with TestClient(create_app()) as restarted:
        assert restarted.get('/v1/me', headers=auth(agent)).status_code == 401
        assert restarted.get('/v1/me', headers=auth(first)).status_code == 200
    with app.state.authority.store.transaction() as db:
        text = json.dumps([dict(row) for row in db.execute('SELECT * FROM activity')])
        stored = json.dumps([dict(row) for row in db.execute('SELECT * FROM credentials')])
        assert all(credential['token'] not in text + stored for credential in (first, second, agent))
        failed = db.execute('SELECT * FROM activity WHERE status_code=401').fetchall()
        assert failed and all(row['agent_id'] is None for row in failed)


def test_credential_expiry_and_rate_limits_configurable():
    now = [100.0]
    cfg = Settings.model_validate(load_settings().model_dump() | {'credential_ttl_seconds': 10, 'requests_per_window': 3})
    app = create_app(cfg, clock=lambda: now[0])
    owner = app.state.authority.create_owner('Owner')
    with TestClient(app) as client:
        assert client.get('/v1/me', headers=auth(owner)).status_code == 200
        now[0] = 111.0
        assert client.get('/v1/me', headers=auth(owner)).status_code == 401
        assert client.get('/health').status_code == 200
        assert client.get('/health').status_code == 429
        now[0] = 180.0
        assert client.get('/health').status_code == 200


def test_oversized_input_rejected_without_recording_body():
    cfg = Settings.model_validate(load_settings().model_dump() | {'max_body_bytes': 128})
    app = create_app(cfg)
    with TestClient(app) as client:
        response = client.post('/v1/owner/agents', content='PRIVATE-BODY' * 100)
        assert response.status_code == 413
        assert client.get('/v1/me?token=PRIVATE-QUERY').status_code == 401
    with app.state.authority.store.transaction() as db:
        events = json.dumps([dict(row) for row in db.execute('SELECT * FROM activity')])
        assert 'PRIVATE' not in events
