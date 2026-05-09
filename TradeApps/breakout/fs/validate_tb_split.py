
import json
import os
import sys
from pathlib import Path

# Add current dir to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from trade_viewer_api import _run_top_x_multi_chart_workflow
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def test_split_logic():
    mode = "live"
    date_str = "2026-04-13"
    
    # Load workflow config
    workflow_path = Path("workflows.json")
    if not workflow_path.exists():
        print("workflows.json not found")
        return

    with open(workflow_path, "r") as f:
        data = json.load(f)
        workflows = data.get("workflows", [])
        
    wf = next((w for w in workflows if w["id"] == "top_x_multi_chart_workflow"), None)
    if not wf:
        print("top_x_multi_chart_workflow not found")
        return

    # Test Case 1: t_split_for_tb = False (Expected: TB creation fails for single charts)
    print("\n--- Test Case 1: t_split_for_tb = False ---")
    wf_false = json.loads(json.dumps(wf))
    wf_false["config"]["t_split_for_tb"] = False
    # Use indices to ensure we have data today
    wf_false["config"]["product_type"] = "indices"
    wf_false["config"]["product_types"] = ["indices"]
    
    result_false = _run_top_x_multi_chart_workflow(mode, date_str, wf_false)
    print(f"Success: {result_false.get('success')}")
    print(f"Message: {result_false.get('message')}")
    
    # Check TB results
    tb_res = result_false.get("tb", {})
    if isinstance(tb_res, dict):
        details = tb_res.get("details", [])
        if details:
            for d in details:
                print(f"TB for {d.get('product_type')}: created={d.get('created')}, reason={d.get('reason')}")
        else:
            print(f"TB created: {tb_res.get('created')}, reason: {tb_res.get('reason')}")

    # Test Case 2: t_split_for_tb = True (Expected: TB creation succeeds via splitting)
    print("\n--- Test Case 2: t_split_for_tb = True ---")
    wf_true = json.loads(json.dumps(wf))
    wf_true["config"]["t_split_for_tb"] = True
    wf_true["config"]["product_type"] = "indices"
    wf_true["config"]["product_types"] = ["indices"]
    
    result_true = _run_top_x_multi_chart_workflow(mode, date_str, wf_true)
    print(f"Success: {result_true.get('success')}")
    print(f"Message: {result_true.get('message')}")
    
    tb_res = result_true.get("tb", {})
    if isinstance(tb_res, dict):
        details = tb_res.get("details", [])
        if details:
            for d in details:
                print(f"TB for {d.get('product_type')}: created={d.get('created')}, reason={d.get('reason')}")
        else:
            print(f"TB created: {tb_res.get('created')}, reason: {tb_res.get('reason')}")

if __name__ == "__main__":
    test_split_logic()
