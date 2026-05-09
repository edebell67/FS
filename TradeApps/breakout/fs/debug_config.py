import os
import json

path = os.path.join(os.path.dirname(__file__), 'config.json')
print(f"Checking {path}")
try:
    with open(path, 'r') as f:
        content = f.read()
        print(f"Raw content len: {len(content)}")
        data = json.loads(content)
    print("Run Mode:", data.get('run_mode'))
except Exception as e:
    print("Error:", e)
