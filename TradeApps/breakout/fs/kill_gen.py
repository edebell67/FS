import os
import subprocess
import signal

def kill_generator():
    try:
        output = subprocess.check_output('wmic process where "name=\'python.exe\'" get CommandLine,ProcessId', shell=True).decode()
        for line in output.splitlines():
            if 'summary_net_generator.py' in line:
                parts = line.split()
                if parts:
                    pid = parts[-1]
                    print(f"Killing PID {pid}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], shell=True)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kill_generator()
