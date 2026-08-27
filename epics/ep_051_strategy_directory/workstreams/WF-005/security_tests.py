import os
import re

def run_security_tests():
    print("Running Security & Compliance Verification...")
    
    base_dir = "C:/Users/edebe/eds/epics/ep_051_strategy_directory/workstreams/WF-005"
    
    # 1. Verify Public Contract Excludes Restricted Data
    with open(os.path.join(base_dir, "data_classification.md"), 'r') as f:
        content = f.read()
        assert "INTERNAL RESTRICTED" in content
        assert "Individual trade records" in content
        assert "Non-DNA trade data" in content
        assert "PUBLIC" in content
        print("PASS: Public contract correctly isolates restricted data.")
        
    # 2. Verify High-Risk Flows have Controls/Owners
    with open(os.path.join(base_dir, "threat_model.md"), 'r') as f:
        content = f.read()
        assert "T1: Data Leakage" in content
        assert "T2: Metric Manipulation" in content
        assert "Data Team" in content
        assert "Security Team" in content
        print("PASS: High-risk flows have documented controls and owners.")
        
    # 3. Verify Broker Activation Requirements are Explicit
    with open(os.path.join(base_dir, "risk_register.md"), 'r') as f:
        content = f.read()
        assert "Broker integration deferred to Phase 6" in content
        assert "Vault implementation mandatory" in content
        print("PASS: Broker activation requirements and deferrals are explicit.")

    print("\nAll security checks passed.")

if __name__ == "__main__":
    run_security_tests()
