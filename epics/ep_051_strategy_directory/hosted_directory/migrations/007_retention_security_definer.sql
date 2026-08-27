-- EP051 least-privilege cross-owner retention entry point.
BEGIN;

DO $$
DECLARE owner_oid oid;
BEGIN
  SELECT oid INTO owner_oid FROM pg_roles WHERE rolname='ep051_retention_owner';
  IF owner_oid IS NULL THEN
    CREATE ROLE ep051_retention_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT BYPASSRLS;
  ELSE
    ALTER ROLE ep051_retention_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT BYPASSRLS;
    IF EXISTS (SELECT 1 FROM pg_auth_members WHERE roleid=owner_oid OR member=owner_oid) THEN
      RAISE EXCEPTION 'ep051_retention_owner must have no role memberships or members';
    END IF;
    IF EXISTS (
      SELECT 1 FROM pg_shdepend d
      WHERE d.refclassid='pg_authid'::regclass AND d.refobjid=owner_oid AND d.deptype='o'
        AND NOT (d.classid='pg_proc'::regclass AND d.objid=COALESCE(to_regprocedure('public.intelligence_purge_expired_history()')::oid,0::oid))
    ) THEN
      RAISE EXCEPTION 'ep051_retention_owner owns an unrelated database object';
    END IF;
    IF EXISTS (
      SELECT 1 FROM pg_shdepend d
      WHERE d.refclassid='pg_authid'::regclass AND d.refobjid=owner_oid AND d.deptype='a'
        AND NOT (d.classid='pg_class'::regclass AND d.objid='public.intelligence_user_history'::regclass)
    ) THEN
      RAISE EXCEPTION 'ep051_retention_owner has an unrelated database grant';
    END IF;
    REVOKE ALL ON public.intelligence_user_history FROM ep051_retention_owner;
  END IF;
END $$;

CREATE OR REPLACE FUNCTION public.intelligence_purge_expired_history()
RETURNS bigint
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog
AS $$
DECLARE removed bigint;
BEGIN
  DELETE FROM public.intelligence_user_history WHERE expires_at<=pg_catalog.now();
  GET DIAGNOSTICS removed = ROW_COUNT;
  RETURN removed;
END;
$$;

ALTER FUNCTION public.intelligence_purge_expired_history() OWNER TO ep051_retention_owner;
REVOKE ALL ON FUNCTION public.intelligence_purge_expired_history() FROM PUBLIC;
GRANT DELETE ON public.intelligence_user_history TO ep051_retention_owner;
GRANT SELECT(expires_at) ON public.intelligence_user_history TO ep051_retention_owner;
-- Deployment provisioning grants EXECUTE on this function to the dedicated maintenance role only.

COMMIT;
