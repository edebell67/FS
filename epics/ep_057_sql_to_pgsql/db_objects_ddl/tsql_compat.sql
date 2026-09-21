-- =============================================================================
-- SECTION 0: T-SQL COMPATIBILITY HELPERS FOR POSTGRESQL
-- These functions enable seamless execution of ported SQL Server views & functions.
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS tsql_compat;

-- 1. ISNULL equivalent (variadic or 2-arg)
CREATE OR REPLACE FUNCTION tsql_compat.isnull(val anyelement, fallback anyelement)
RETURNS anyelement LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
    SELECT COALESCE(val, fallback);
$$;

-- 2. TRY_CONVERT / TRY_CAST numeric
CREATE OR REPLACE FUNCTION tsql_compat.try_convert_numeric(val text)
RETURNS numeric LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS $$
BEGIN
    RETURN val::numeric;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$;

-- 3. TRY_CONVERT / TRY_CAST float
CREATE OR REPLACE FUNCTION tsql_compat.try_convert_float(val text)
RETURNS double precision LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS $$
BEGIN
    RETURN val::double precision;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$;

-- 4. TRY_CONVERT / TRY_CAST timestamp
CREATE OR REPLACE FUNCTION tsql_compat.try_convert_datetime(val text)
RETURNS timestamp LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS $$
BEGIN
    RETURN val::timestamp;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$;

-- 5. DATEADD helper
CREATE OR REPLACE FUNCTION tsql_compat.dateadd(datepart text, num integer, dt timestamp)
RETURNS timestamp LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS $$
BEGIN
    CASE lower(datepart)
        WHEN 'year', 'yy', 'yyyy' THEN RETURN dt + (num || ' year')::interval;
        WHEN 'month', 'mm', 'm' THEN RETURN dt + (num || ' month')::interval;
        WHEN 'day', 'dd', 'd' THEN RETURN dt + (num || ' day')::interval;
        WHEN 'hour', 'hh' THEN RETURN dt + (num || ' hour')::interval;
        WHEN 'minute', 'mi', 'n' THEN RETURN dt + (num || ' minute')::interval;
        WHEN 'second', 'ss', 's' THEN RETURN dt + (num || ' second')::interval;
        WHEN 'millisecond', 'ms' THEN RETURN dt + (num || ' millisecond')::interval;
        ELSE RETURN dt + (num || ' ' || datepart)::interval;
    END CASE;
END;
$$;

-- 6. DATEDIFF helper
CREATE OR REPLACE FUNCTION tsql_compat.datediff(datepart text, dt1 timestamp, dt2 timestamp)
RETURNS bigint LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS $$
BEGIN
    CASE lower(datepart)
        WHEN 'year', 'yy', 'yyyy' THEN 
            RETURN (EXTRACT(YEAR FROM dt2) - EXTRACT(YEAR FROM dt1))::bigint;
        WHEN 'month', 'mm', 'm' THEN 
            RETURN ((EXTRACT(YEAR FROM dt2) - EXTRACT(YEAR FROM dt1)) * 12 + (EXTRACT(MONTH FROM dt2) - EXTRACT(MONTH FROM dt1)))::bigint;
        WHEN 'day', 'dd', 'd' THEN 
            RETURN (dt2::date - dt1::date)::bigint;
        WHEN 'hour', 'hh' THEN 
            RETURN (EXTRACT(EPOCH FROM (dt2 - dt1)) / 3600)::bigint;
        WHEN 'minute', 'mi', 'n' THEN 
            RETURN (EXTRACT(EPOCH FROM (dt2 - dt1)) / 60)::bigint;
        WHEN 'second', 'ss', 's' THEN 
            RETURN EXTRACT(EPOCH FROM (dt2 - dt1))::bigint;
        WHEN 'millisecond', 'ms' THEN 
            RETURN (EXTRACT(EPOCH FROM (dt2 - dt1)) * 1000)::bigint;
        ELSE 
            RETURN (EXTRACT(EPOCH FROM (dt2 - dt1)) / 86400)::bigint;
    END CASE;
END;
$$;

-- 7. CHARINDEX helper
CREATE OR REPLACE FUNCTION tsql_compat.charindex(substr text, str text, start_pos integer DEFAULT 1)
RETURNS integer LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
    SELECT CASE 
        WHEN start_pos <= 1 THEN POSITION(substr IN str)
        ELSE 
            CASE 
                WHEN POSITION(substr IN SUBSTRING(str FROM start_pos)) > 0 
                THEN POSITION(substr IN SUBSTRING(str FROM start_pos)) + start_pos - 1
                ELSE 0
            END
    END;
$$;

-- 8. STRING_SPLIT equivalent table function
CREATE OR REPLACE FUNCTION tsql_compat.string_split(str text, delim text)
RETURNS TABLE (value text) LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
    SELECT unnest(string_to_array(str, delim));
$$;

-- Add tsql_compat to default schema search path
SET search_path TO public, tsql_compat;
