import re
import sys

def check_js_syntax(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    
    for i, js in enumerate(scripts):
        # Save JS to a temp file and check with node
        temp_js = f"temp_script_{i}.js"
        with open(temp_js, 'w', encoding='utf-8') as f_js:
            f_js.write(js)
        
        print(f"Checking script block {i}...")
        import subprocess
        try:
            result = subprocess.run(['node', '--check', temp_js], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Syntax Error in block {i}:")
                print(result.stderr)
            else:
                print(f"Block {i} syntax OK.")
        except Exception as e:
            print(f"Could not run node check: {e}")

if __name__ == "__main__":
    check_js_syntax(sys.argv[1])
