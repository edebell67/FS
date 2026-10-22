# VERSION HISTORY v1.7.0 · 2026-09-13 · Add owner-scoped credential replacement for an existing agent identity.
# v1.6.0 · 2026-09-13 · Expose administrator capability without changing the owner credential schema.
# v1.5.0 · 2026-09-11 · Add expiring single-use owner invitations for deterministic agent ownership.
# v1.4.0 · 2026-09-10 · Bind freely admitted agents to the owner who enabled Arena admission.
from hashlib import sha256
import secrets
# v1.3.0 · 2026-09-10 · Issue unique scoped agent identities through open Arena admission.
# v1.2.0 · 2026-09-10 · Add owner-controlled persisted Arena entry policy and public policy discovery.
# v1.1.0 · 2026-09-02 · Seed new participant allocations once when an owner registers an agent.
# v1.0.0 · 2026-09-02 · Owner-scoped provision/revoke/read APIs; no public self-registration.
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import Field

from .auth import Authority
from .contracts import Contract
from .runtime_assignments import assign


class AgentRegistration(Contract):
    name: str = Field(min_length=1, max_length=128)


class ArenaAccessPolicy(Contract):
    public_access: bool


class DirectorySourcePolicy(Contract):
    source: str = Field(pattern='^(sql|pg)$')


class OpenAgentAdmission(Contract):
    name: str = Field(default='Visiting agent', min_length=1, max_length=128)
    invitation_token: str | None = Field(default=None, min_length=20, max_length=512)


class AgentInvitationRequest(Contract):
    expires_in_seconds: int = Field(default=900, ge=60, le=86400, strict=True)
    model_profile_id: str | None = None
    domain_type: str = Field(default='generic', min_length=3, max_length=120)
    purpose: str = Field(default='general', min_length=1, max_length=120)
    approval_policy: str = Field(default='confirm_side_effects', pattern='^(confirm_side_effects|preauthorised|observe_only)$')


def router(authority: Authority, initialise_agent=lambda db, agent_id, settings: None):
    routes = APIRouter()
    store = authority.store

    @routes.get('/v1/me')
    def identity(actor=Depends(authority.authenticate)):
        return {key: actor[key] for key in ('owner_id', 'agent_id', 'role', 'expires_at')} | {'is_admin': authority.is_admin(actor)}

    @routes.post('/v1/owner/session')
    def create_owner_session(request: Request, response: Response, actor=Depends(authority.owner)):
        raw, session_id, now = secrets.token_urlsafe(48), str(uuid4()), authority.clock()
        expires_at = actor['expires_at']
        with store.transaction(immediate=True) as db:
            db.execute('INSERT INTO owner_web_sessions(id,token_hash,owner_id,created_at,expires_at) VALUES (?,?,?,?,?)',
                       (session_id, sha256(raw.encode()).hexdigest(), actor['owner_id'], now, expires_at))
        response.set_cookie('ep052_owner_session', raw, max_age=max(1, int(expires_at-now)),
                            httponly=True, secure=request.url.scheme == 'https', samesite='strict', path='/')
        return {'connected': True, 'owner_id': actor['owner_id'], 'expires_at': expires_at}

    @routes.delete('/v1/owner/session')
    def delete_owner_session(request: Request, response: Response, actor=Depends(authority.owner)):
        raw = request.cookies.get('ep052_owner_session')
        if raw:
            with store.transaction(immediate=True) as db:
                db.execute('UPDATE owner_web_sessions SET revoked=1 WHERE token_hash=? AND owner_id=?',
                           (sha256(raw.encode()).hexdigest(), actor['owner_id']))
        response.delete_cookie('ep052_owner_session', path='/', samesite='strict')
        return {'signed_out': True}

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

    @routes.get('/v1/arena/directory-source')
    def directory_source():
        with store.transaction() as db:
            row = db.execute("SELECT value FROM metadata WHERE key='directory_source'").fetchone()
        source = row['value'] if row and row['value'] in ('sql', 'pg') else 'sql'
        return {'source': source, 'pg_available': bool(authority.settings.directory_url_pg)}

    @routes.put('/v1/owner/directory-source')
    def set_directory_source(request: DirectorySourcePolicy, actor=Depends(authority.owner)):
        if request.source == 'pg' and not authority.settings.directory_url_pg:
            raise HTTPException(409, 'No alternate directory source is configured for this instance')
        with store.transaction(immediate=True) as db:
            db.execute("INSERT INTO metadata(key,value) VALUES ('directory_source',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (request.source,))
        return {'source': request.source}

    @routes.post('/v1/agents/access', status_code=201)
    def open_agent_access(request: OpenAgentAdmission):
        with store.transaction(immediate=True) as db:
            now = authority.clock()
            invitation = None
            if request.invitation_token:
                digest = sha256(request.invitation_token.encode()).hexdigest()
                invitation = db.execute(
                    'SELECT * FROM agent_invitations WHERE token_hash=? FOR UPDATE',
                    (digest,)).fetchone()
                if not invitation or invitation['claimed_at'] is not None or invitation['expires_at'] <= now:
                    raise HTTPException(403, 'Agent invitation is invalid, expired or already used')
                owner_id = invitation['owner_id']
            else:
                if not authority.arena_public():
                    raise HTTPException(403, 'Arena admission requires an owner invitation')
                admission_owner = db.execute("SELECT value FROM metadata WHERE key='arena_admission_owner_id'").fetchone()
                if not admission_owner:
                    raise HTTPException(503, 'An owner must re-enable open admission before agents can join')
                owner_id = admission_owner['value']
            agent_id = str(uuid4())
            db.execute('INSERT INTO agents VALUES (?,?,?)', (agent_id, owner_id, request.name))
            initialise_agent(db, agent_id, authority.settings)
            if invitation and invitation['model_profile_id']:
                assign(db, agent_id, invitation['domain_type'] or 'generic', invitation['model_profile_id'], 'available', now=now)
            credential = authority.issue(db, owner_id, agent_id, 'agent')
            if invitation:
                db.execute('UPDATE agent_invitations SET claimed_at=?,agent_id=? WHERE id=?',
                           (now, agent_id, invitation['id']))
        return credential | {'name': request.name,
                             'admission': 'invitation' if invitation else 'open'}

    @routes.post('/v1/owner/agent-invitations', status_code=201)
    def create_agent_invitation(request: AgentInvitationRequest, actor=Depends(authority.owner)):
        raw_token = secrets.token_urlsafe(32)
        invitation_id = str(uuid4())
        created_at = authority.clock()
        expires_at = created_at + request.expires_in_seconds
        with store.transaction() as db:
            selected_profile = None
            if request.model_profile_id and not db.execute(
                    'SELECT id FROM model_profiles WHERE id=? AND owner_id=? AND enabled=1',
                    (request.model_profile_id, actor['owner_id'])).fetchone():
                raise HTTPException(404, 'MODEL_PROFILE_NOT_FOUND')
            if request.model_profile_id:
                selected_profile = db.execute(
                    'SELECT runtime_type,model_id,authentication_mode FROM model_profiles WHERE id=?',
                    (request.model_profile_id,)).fetchone()
            db.execute('''INSERT INTO agent_invitations
                (id,token_hash,owner_id,created_at,expires_at,model_profile_id,domain_type,purpose,approval_policy)
                VALUES (?,?,?,?,?,?,?,?,?)''',
                (invitation_id, sha256(raw_token.encode()).hexdigest(), actor['owner_id'], created_at, expires_at,
                 request.model_profile_id, request.domain_type, request.purpose, request.approval_policy))
        return {'invitation_id': invitation_id, 'invitation_token': raw_token,
                'expires_at': expires_at, 'single_use': True, 'model_profile_id': request.model_profile_id,
                'domain_type': request.domain_type, 'purpose': request.purpose,
                'approval_policy': request.approval_policy,
                'runtime_type': selected_profile['runtime_type'] if selected_profile else None,
                'model_id': selected_profile['model_id'] if selected_profile else None,
                'authentication_mode': selected_profile['authentication_mode'] if selected_profile else None}

    @routes.post('/v1/owner/agents', status_code=201)
    def register(request: AgentRegistration, actor=Depends(authority.owner)):
        with store.transaction() as db:
            agent_id = str(uuid4())
            db.execute('INSERT INTO agents VALUES (?,?,?)', (agent_id, actor['owner_id'], request.name))
            initialise_agent(db, agent_id, authority.settings)
            return authority.issue(db, actor['owner_id'], agent_id, 'agent')

    @routes.get('/v1/owner/agents')
    def agents(actor=Depends(authority.owner)):
        with store.transaction() as db:
            return {'items': [dict(row) | {'agent_id': row['id']} for row in db.execute(
                '''SELECT id,name FROM agents WHERE owner_id=? AND NOT EXISTS
                   (SELECT 1 FROM retired_agents r WHERE r.agent_id=agents.id) ORDER BY id''',
                (actor['owner_id'],))]}

    @routes.post('/v1/owner/agents/{agent_id}/retire')
    def retire_agent(agent_id: UUID, actor=Depends(authority.owner)):
        agent_id, now = str(agent_id), authority.clock()
        with store.transaction(immediate=True) as db:
            if not db.execute('SELECT id FROM agents WHERE id=? AND owner_id=?',
                              (agent_id, actor['owner_id'])).fetchone():
                raise HTTPException(404, 'OWNED_AGENT_NOT_FOUND')
            db.execute('''INSERT INTO retired_agents(agent_id,owner_id,retired_at,reason)
                          VALUES (?,?,?,'owner_requested_clean_start') ON CONFLICT(agent_id) DO NOTHING''',
                       (agent_id, actor['owner_id'], now))
            db.execute('UPDATE connections SET disconnected=1 WHERE agent_id=? AND disconnected=0', (agent_id,))
            db.execute("UPDATE credentials SET revoked=1 WHERE agent_id=? AND role='agent' AND revoked=0", (agent_id,))
            db.execute("UPDATE agent_runtime_assignments SET execution_status='disabled',updated_at=? WHERE agent_id=?",
                       (now, agent_id))
            db.execute('''INSERT INTO owner_events(event_id,owner_id,agent_id,event_type,payload,created_at)
                          VALUES (?,?,?,?,?,?)''', (str(uuid4()), actor['owner_id'], agent_id,
                          'agent.retired', '{"reason":"owner_requested_clean_start"}', now))
        return {'agent_id': agent_id, 'status': 'retired', 'identity_preserved': True,
                'credentials_revoked': True, 'connections_closed': True}

    @routes.post('/v1/owner/agents/{agent_id}/credentials', status_code=201)
    def replace_agent_credential(agent_id: UUID, actor=Depends(authority.owner)):
        try:
            return authority.replace_owned_agent_credential(actor['owner_id'], str(agent_id))
        except ValueError:
            raise HTTPException(404, 'Owned agent not found')

    @routes.delete('/v1/owner/credentials/{credential_id}')
    def revoke(credential_id: UUID, actor=Depends(authority.owner)):
        with store.transaction() as db:
            result = db.execute('UPDATE credentials SET revoked=1 WHERE id=? AND owner_id=?',
                                (str(credential_id), actor['owner_id']))
            if result.rowcount == 0:
                raise HTTPException(404, 'Credential not found')
        return {'revoked': True, 'credential_id': credential_id}

    return routes
