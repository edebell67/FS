# VERSION HISTORY v1.0.0 · 2026-09-10 · Record agent-submitted spatial actions for the Arena projection.
import json
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from .arena import emit
from .contracts import Contract


class ArenaAction(Contract):
    request_id: UUID
    action: Literal['MOVE']
    destination: Literal['breakout', 'breakout_r', 'breakout_r_rev', 'breakout_rev', 'intelligence']
    pace: Literal['slow', 'normal', 'fast'] = 'normal'


def router(authority):
    routes, store = APIRouter(), authority.store

    @routes.post('/v1/me/arena-actions')
    def record(request: ArenaAction, actor=Depends(authority.agent)):
        source_key = 'arena-action:' + actor['agent_id'] + ':' + str(request.request_id)
        with store.transaction(immediate=True) as db:
            prior = db.execute('SELECT * FROM arena_events WHERE source_key=?', (source_key,)).fetchone()
            if prior:
                payload = json.loads(prior['payload'])
                if payload.get('destination') != request.destination or payload.get('pace') != request.pace:
                    raise HTTPException(409, 'REQUEST_ID_CONFLICT')
                return {'event_id': prior['event_id'], 'cursor': prior['cursor'], **payload}
            payload = {'action': 'MOVE', 'destination': request.destination, 'pace': request.pace,
                       'affected': {'type': 'arena_booth', 'id': request.destination},
                       'effect': f"Agent started moving to the {request.destination} booth",
                       'outcome': 'MOVEMENT_ACCEPTED'}
            emit(db, source_key=source_key, agent_id=actor['agent_id'], operation='MOVE',
                 resource_id=request.destination, request_id=str(request.request_id), payload=payload)
            row = db.execute('SELECT event_id,cursor FROM arena_events WHERE source_key=?', (source_key,)).fetchone()
            return {'event_id': row['event_id'], 'cursor': row['cursor'], **payload}

    return routes
