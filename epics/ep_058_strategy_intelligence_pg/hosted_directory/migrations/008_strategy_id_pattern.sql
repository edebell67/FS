-- EP058: PostgreSQL tradedb has lowercase / underscored model ids (e.g. dna_300144); matches contracts.py (?i)^DNA_[A-Za-z0-9_]+$
ALTER TABLE directory_strategy DROP CONSTRAINT IF EXISTS directory_strategy_strategy_id_check;
ALTER TABLE directory_strategy ADD CONSTRAINT directory_strategy_strategy_id_check CHECK (strategy_id ~* '^DNA_[A-Za-z0-9_]+$');
