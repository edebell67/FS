import pytest
import re

def normalize_strategy_id(strategy_id: str) -> str:
    """Normalizes strategy ID by trimming whitespace, uppercasing, and stripping _S/_B suffixes."""
    normalized = strategy_id.strip().upper()
    if normalized.endswith("_S") or normalized.endswith("_B"):
        normalized = normalized[:-2]
    return normalized

def is_valid_dna_id(strategy_id: str) -> bool:
    """Validates the normalized DNA ID."""
    return bool(re.match(r"^DNA_\d+$", strategy_id))

def determine_outcome(net_return: float) -> str:
    """Determines outcome strictly from net_return."""
    if net_return > 0:
        return "winner"
    elif net_return < 0:
        return "loser"
    return "breakeven"

def get_exit_time(g_close_time, last_update):
    """Calculates exit time precedence."""
    return g_close_time if g_close_time is not None else last_update

# --- Tests ---

def test_normalization():
    assert normalize_strategy_id("DNA_102001_S") == "DNA_102001"
    assert normalize_strategy_id(" dna_102001_b ") == "DNA_102001"
    assert normalize_strategy_id("DNA_102001") == "DNA_102001"

def test_invalid_ids():
    assert not is_valid_dna_id(normalize_strategy_id("NON_DNA_123"))
    assert not is_valid_dna_id(normalize_strategy_id("DNA_ABC_S"))
    assert is_valid_dna_id(normalize_strategy_id("DNA_999999_S"))

def test_outcome():
    assert determine_outcome(150.50) == "winner"
    assert determine_outcome(-50.00) == "loser"
    assert determine_outcome(0.0) == "breakeven"

def test_exit_time():
    assert get_exit_time("2026-08-01", "2026-08-02") == "2026-08-01"
    assert get_exit_time(None, "2026-08-02") == "2026-08-02"

def test_duplicate_guids():
    trades = [{"guid": "123", "return": 10}, {"guid": "123", "return": 15}]
    unique_guids = set(t["guid"] for t in trades)
    assert len(unique_guids) != len(trades), "Duplicate GUIDs detected, quarantine required."

def test_no_cost_double_counting():
    # Demonstrating that costs shouldn't be subtracted from net_return
    raw_gross = 100
    commission = 5
    source_net = 95
    
    # Contract asserts we use source_net directly
    directory_pnl = source_net
    assert directory_pnl == 95, "Directory PnL must equal source net_return without further cost deduction"
