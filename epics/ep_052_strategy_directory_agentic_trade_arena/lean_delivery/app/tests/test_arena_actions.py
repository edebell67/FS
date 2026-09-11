# VERSION HISTORY v1.0.0 · 2026-09-10 · Verify authenticated, idempotent Arena movement events.
from uuid import uuid4

from fastapi.testclient import TestClient

from lean_exchange.api import create_app


def auth(record):
    return {'Authorization': 'Bearer ' + record['token']}


def test_agent_move_is_recorded_and_drives_public_projection():
    app = create_app()
    owner = app.state.authority.create_owner('Movement owner')
    with TestClient(app) as client:
        agent = client.post('/v1/owner/agents', json={'name': 'Walker'}, headers=auth(owner)).json()
        body = {'request_id': str(uuid4()), 'action': 'MOVE', 'destination': 'breakout_r', 'pace': 'slow'}
        moved = client.post('/v1/me/arena-actions', json=body, headers=auth(agent))
        assert moved.status_code == 200
        assert moved.json()['outcome'] == 'MOVEMENT_ACCEPTED'
        assert client.post('/v1/me/arena-actions', json=body, headers=auth(agent)).json() == moved.json()
        assert client.post('/v1/me/arena-actions', json=body | {'destination': 'breakout'}, headers=auth(agent)).status_code == 409
        event = client.get('/v1/owner/activity-audit', params={'operation': 'MOVE'}, headers=auth(owner)).json()['items'][0]
        assert event['agent_id'] == agent['agent_id']
        assert event['details']['destination'] == 'breakout_r'
        assert event['details']['pace'] == 'slow'
