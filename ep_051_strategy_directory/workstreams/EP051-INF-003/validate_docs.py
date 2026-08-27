"""Documentation completeness check. Version 1.0.0 (2026-08-23)."""
from pathlib import Path
root=Path(__file__).parents[2]
readme=(root/"README.md").read_text(encoding="utf-8");ops=(root/"deploy"/"OPERATIONS.md").read_text(encoding="utf-8")
for term in ("300–500","combined_trades_closed","combined_trades_open","target reached","NO-GO","Quick start"):assert term in readme
for term in ("Start and verify","Incident and rollback","owner-scoped","offline/synthetic"):assert term in ops
print("documentation validation passed")

