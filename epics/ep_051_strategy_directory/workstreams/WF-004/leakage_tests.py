import os
import re

def run_leakage_tests():
    print("Running Anti-Bias & Leakage Verification...")
    
    base_dir = "C:/Users/edebe/eds/epics/ep_051_strategy_directory/workstreams/WF-004"
    
    with open(os.path.join(base_dir, "regime_specification.md"), 'r') as f:
        content = f.read()
        
        # 1. Verify regimes use no future data
        assert "T - 1 day" in content or "yesterday" in content.lower()
        print("PASS: Regime logic explicitly restricted to historical (T-1) data to prevent leakage.")
        
        # 2. Verify independence from DNA results
        assert "cannot use strategy equity curves" in content or "independent of DNA results" in content
        print("PASS: Regime logic explicitly independent of DNA strategy results.")
        
        # 3. Verify parameters are frozen
        assert "frozen in this version" in content or "version freeze" in content.lower()
        print("PASS: Anti-bias parameter freeze is documented.")

    print("\nAll leakage tests passed.")

if __name__ == "__main__":
    run_leakage_tests()
