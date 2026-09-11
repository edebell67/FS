# VERSION HISTORY v1.4.0 · 2026-09-10 · Bind freely admitted agents to the owner who enabled Arena admission.
# v1.3.0 · 2026-09-10 · Issue unique scoped agent identities through open Arena admission.
# v1.2.0 · 2026-09-10 · Add owner-controlled persisted Arena entry policy and public policy discovery.
# v1.1.0 · 2026-09-02 · Seed new participant allocations once when an owner registers an agent.
# v1.0.0 · 2026-09-02 · Owner-scoped provision/revoke/read APIs; no public self-registration.
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field

from .auth import Authority
from .contracts import Contract
from .participant_funds import initialise


class AgentRegistration(Contract):
    name: str = Field(min_length=1, max_length=128)


class ArenaAccessPolicy(Contract):
    public_access: bool


class OpenAgentAdmission(Contract):
    name: str = Field(default='Visiting agent', min_length=1, max_length=128)


def router(authority: Authority):
    routes = APIRouter()
    store = authority.store

    @routes.get('/v1/me')
    def identity(actor=Depends(authority.authenticate)):
        return {key: actor[key] for key in ('owner_id', 'agent_id', 'role', 'expires_at')}

    @routes.get('/v1/arena/access-policy')
    def arena_access_policy():
        public = authority.arena_public()
        return {'public_access': public, 'entry_mode': 'open' if public else 'token_required'}

    @routes.put('/v1/owner/arena-access')
    def set_arena_access(request: ArenaAccessPolicy, actor=Depends(authority.owner)):
        value = 'true' if request.public_access else 'false'
        with store.transaction(immediate=True) as db:
            db.execute("INSERT INTO metadata(key,value) VALUES ('arena_public_access',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (value,))
            if request.public_access:
                db.execute("INSERT INTO metadata(key,value) VALUES ('arena_admission_owner_id',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (actor['owner_id'],))
        return {'public_access': request.public_access,
                'entry_mode': 'open' if request.public_access else 'token_required'}

    @routes.post('/v1/agents/access', status_code=201)
    def open_agent_access(request: OpenAgentAdmission):
        if not authority.arena_public():
            raise HTTPException(403, 'Arena admission requires an owner-issued agent credential')
        with store.transaction(immediate=True) as db:
            admission_owner = db.execute("SELECT value FROM metadata WHERE key='arena_admission_owner_id'").fetchone()
            if not admission_owner:
                raise HTTPException(503, 'An owner must re-enable open admission before agents can join')
            owner_id = admission_owner['value']
            agent_id = str(uuid4())
            db.execute('INSERT INTO agents VALUES (?,?,?)', (agent_id, owner_id, request.name))
            initialise(db, agent_id, authority.settings.seed_funds)
            credential = authority.issue(db, owner_id, agent_id, 'agent')
        return credential | {'name': request.name, 'admission': 'open'}

    @routes.post('/v1/owner/agents', status_code=201)
    def register(request: AgentRegistration, actor=Depends(authority.owner)):
        with store.transaction() as db:
            agent_id = str(uuid4())
            db.execute('INSERT INTO agents VALUES (?,?,?)', (agent_id, actor['owner_id'], request.name))
            initialise(db, agent_id, authority.settings.seed_funds)
            return authority.issue(db, actor['owner_id'], agent_id, 'agent')

    @routes.get('/v1/owner/agents')
    def agents(actor=Depends(authority.owner)):
        with store.transaction() as db:
            return {'items': [dict(row) for row in db.execute('SELECT id,name FROM agents WHERE owner_id=? ORDER BY id', (actor['owner_id'],))]}

    @routes.delete('/v1/owner/credentials/{credential_id}')
    def revoke(credential_id: UUID, actor=Depends(authority.owner)):
        with store.transaction() as db:
            result = db.execute('UPDATE credentials SET revoked=1 WHERE id=? AND owner_id=?',
                                (str(credential_id), actor['owner_id']))
            if result.rowcount == 0:
                raise HTTPException(404, 'Credential not found')
        return {'revoked': True, 'credential_id': credential_id}

    return routes
