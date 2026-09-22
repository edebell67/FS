# VERSION HISTORY v1.16.0 · 2026-09-13 · Mount owner insight and agent portfolio challenge APIs.
# v1.15.0 · 2026-09-13 · Mount owner event streaming and same-identity connection recovery APIs.
# v1.14.0 · 2026-09-11 · Advertise cumulative-return settlement and remove perpetual-price readiness language.
# v1.13.0 · 2026-09-11 · Advertise automatic selected-catalogue test pricing. Superseded before release.
# v1.12.0 · 2026-09-06 · create_app's `database` param is now a Postgres connection URL (was a SQLite file Path); Store(database_url) reads EP052_DATABASE_URL/DATABASE_URL when omitted.
# v1.11.0 · 2026-09-05 · Read allowed hosts from EP052_ALLOWED_HOSTS so hosted deploys aren't rejected by TrustedHostMiddleware.
# v1.10.0 · 2026-09-02 · Advertise the read-only live Arena workspace.
# v1.9.0 · 2026-09-02 · Serve authenticated shared Arena projections with resumable filtering.
# v1.8.0 · 2026-09-02 · Expose private positions and owner value-change reconciliation from recorded prices/trades.
# v1.7.2 · 2026-09-02 · Advertise verified trade-report links and updated visitor rules after live settlement verification.
# v1.7.1 · 2026-09-02 · Expose non-secret instance identity and bound-quote count for review/sync provenance.
# v1.7.0 · 2026-09-02 · Mount recorded trades and priced inventory; missing valuation inputs fail closed.
# v1.6.1 · 2026-09-02 · Publish feedback/HOLD rule revision.
# v1.6.0 · 2026-09-02 · Serve API-driven owner feedback workspace, with no simulated agent controls.
# v1.5.0 · 2026-09-02 · Expose private feedback/replies and external HOLD reports; trade linking remains unavailable.
# v1.4.1 · 2026-09-02 · Advertise funded-query visitor rule revision.
# v1.4.0 · 2026-09-02 · Participant allocations and paid intelligence delivery with durable recovery.
# v1.3.1 · 2026-09-02 · Advertise updated visiting-rule version for live connection instructions.
# v1.3.0 · 2026-09-02 · Mount durable owner/agent authentication, independent connections and safe activity access.
# v1.2.0 · 2026-09-02 · Publish executable contract schemas and validation-only routes for review.
# v1.1.0 · 2026-09-02 · Expose read-only source diagnostics without claiming tradable inventory or prices.
# v1.0.0 · 2026-09-02 · Live discovery/configuration/rule delivery; only implemented capabilities advertised.
import os
from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .config import APP_ROOT, Settings, load_settings
from .providers import DirectoryProvider, DirectorySnapshot, ProviderError
from .records import Store
from .auth import Authority
from . import access, activity, connections, feedback, decisions, views, connection_recovery, kernel_events_api, model_profiles, operations
from .domain import ArenaDomainAdapter, EmptyDomain, StrategyTradingDomain
from .feature_controls import enabled as feature_enabled
from .runtime_registry import default_registry
import time

RULES_ROOT = APP_ROOT.parents[1] / 'rules'


def create_app(settings: Settings | None = None, rules_root: Path | None = None,
               directory: DirectoryProvider | None = None, database: str | None = None, clock=time.time,
               intelligence_provider=None, domain: ArenaDomainAdapter | None = None) -> FastAPI:
    cfg = settings or load_settings()
    root = rules_root or RULES_ROOT
    authority = Authority(Store(database), cfg, clock)  # database: Postgres URL, or None to read EP052_DATABASE_URL/DATABASE_URL
    provider = directory or DirectoryProvider(cfg, store=authority.store)
    requested_domain = domain or StrategyTradingDomain(insights_enabled=cfg.owner_insights_enabled,
                                                         challenges_enabled=cfg.agent_challenges_enabled)
    with authority.store.transaction() as db:
        domain_adapter = requested_domain if feature_enabled(db, 'domain', requested_domain.manifest.domain_type) else EmptyDomain()
    app = FastAPI(title='EP052 Lean Exchange API', version='0.1.0',
                  description='Visiting-agent API. Only listed endpoints are implemented; no agent runner.')
    default_hosts = '127.0.0.1,localhost,testserver'
    allowed_hosts = [h.strip() for h in os.environ.get('EP052_ALLOWED_HOSTS', default_hosts).split(',') if h.strip()]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
    app.add_middleware(activity.ActionMiddleware, authority=authority)
    app.state.authority = authority
    app.state.runtime_registry = default_registry()
    app.include_router(access.router(authority, domain_adapter.initialise_agent))
    app.include_router(connections.router(authority))
    app.include_router(activity.router(authority))
    app.include_router(feedback.router(authority))
    app.include_router(decisions.router(authority))
    app.include_router(views.router())
    app.include_router(connection_recovery.router(authority))
    app.include_router(model_profiles.router(authority, app.state.runtime_registry))
    app.include_router(kernel_events_api.router(authority))
    app.include_router(operations.router(authority))
    for domain_router in domain_adapter.routers(authority, provider, settings=cfg, rules_root=root,
                                                intelligence_provider=intelligence_provider):
        app.include_router(domain_router)
    app.state.domain = domain_adapter
    domain_adapter.configure(app, authority, provider, cfg)

    @app.get('/health')
    def health():
        return ({'status': 'ok', 'environment': cfg.environment, 'service': 'ep052-lean-exchange',
                'domain': domain_adapter.name, 'features': {
                    'owner_insights': cfg.owner_insights_enabled,
                    'agent_challenges': cfg.agent_challenges_enabled},
                'domain_metrics': app.state.domain_metrics})

    @app.get('/v1/domain/manifest')
    def domain_manifest():
        from dataclasses import asdict
        return {'domain': asdict(domain_adapter.manifest),
                'owner_panels': [asdict(panel) for panel in domain_adapter.owner_panels()]}

    @app.get('/v1/exchange')
    def exchange():
        with authority.store.transaction() as db:
            instance_id = db.execute("SELECT value FROM metadata WHERE key='instance_id'").fetchone()['value']
            domain_discovery = domain_adapter.discovery(db, cfg)
        return {
            'instance_id': instance_id,
            'environment': cfg.environment,
            'configuration': cfg.model_dump(mode='json'),
            'capabilities': ['discovery', 'rules', 'directory_source_inspection', 'contract_validation',
                             'owner_agent_credentials', 'connections', 'scoped_activity',
                             'feedback_api', 'feedback_view', 'owner_event_stream', 'connection_recovery',
                             *domain_discovery['capabilities']],
            'not_yet_available': [],
            'openapi': '/openapi.json',
            'directory_source': '/v1/providers/directory',
            'contracts': '/v1/contracts',
        } | domain_discovery

    @app.get('/v1/providers/directory', response_model=DirectorySnapshot)
    def directory_source():
        """Inspect the existing public source. This is not an available-to-buy endpoint."""
        try:
            return provider.fetch()
        except ProviderError as exc:
            raise HTTPException(503, detail={'code': str(exc), 'retryable': True}) from exc

    return app
