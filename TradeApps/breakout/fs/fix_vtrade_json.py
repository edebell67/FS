"""
Quick script to fix malformed V-Trade JSON files with duplicate closing braces.
[2025-12-25 V20251225_0405]
"""
import json
from pathlib import Path
from paths import BREAKOUT_LEGACY_JSON_ROOT

def fix_vtrade_json_files(base_dir):
    """Remove duplicate closing braces from V-Trade JSON files."""
    virtual_dirs = list(Path(base_dir).rglob('virtual'))
    
    fixed_count = 0
    for vdir in virtual_dirs:
        for json_file in vdir.glob('vt_*.json'):
            try:
                # Read the file content as text
                with open(json_file, 'r') as f:
                    content = f.read()
                
                # Try to parse as JSON
                data = json.loads(content)
                
                # Rewrite with clean JSON
                with open(json_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                fixed_count += 1
                print(f"Fixed: {json_file.name}")
                
            except json.JSONDecodeError as e:
                print(f"Error in {json_file.name}: {e}")
            except Exception as e:
                print(f"Unexpected error in {json_file.name}: {e}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    base_dir = str(BREAKOUT_LEGACY_JSON_ROOT)
    fix_vtrade_json_files(base_dir)
