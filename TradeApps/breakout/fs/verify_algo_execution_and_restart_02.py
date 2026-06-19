import os
import subprocess
import time
from datetime import datetime
import json
import logging
# [2025-12-26 V20251226_0320] Changed to use fs\\config.json for kill switch
# from algo_stop import stop_app

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# [2025-12-26 V20251226_0333] Removed folder creation - not needed for breakout strategies
# def check_and_create_directories(base_directory):
#     """
#     Checks for the existence of specified directories in the given base directory.
#     Creates the directories if they do not exist.
#     """
#     # Define the list of directories to check
#     directories = ["trades_open", "trades_closed", "excel", "ml", "blog", "price_simulated"]
#
#     # Iterate over each directory
#     for directory in directories:
#         # Form the full path to the directory
#         dir_path = os.path.join(base_directory, directory)
#         
#         # Check if the directory exists
#         if not os.path.exists(dir_path):
#             # If not, create the directory
#             os.makedirs(dir_path)
#             logging.info(f"Created directory: {dir_path}")
#         else:
#             logging.info(f"Directory already exists: {dir_path}")


def get_sleep_duration(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config.get('sleep_duration', 60)  # Default to 60 seconds if not found
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading configuration file: {e}")
        return 60

def get_kill_switch(config_file):
    """Read kill_switch from fs\\config.json. [2025-12-26 V20251226_0320]"""
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config.get('kill_switch', False)  # Default to False if not found
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading kill_switch from config: {e}")
        return False

folder_path = os.path.dirname(__file__)  # Get the directory where the script is located

# Automatically find all script files in the folder [2025-12-26 V20251226_0400 - Fixed filenames]
file_names = [f for f in os.listdir(folder_path) if (f.endswith('.py') and 'open_link' in f) or f in [
    #'momentum.py',
    #'momentum_r.py',
    'price_capture_daemon.py'
    'breakout.py',
    'breakout_R.py',
    'breakout_Rev.py',
    'breakout_R_Rev.py',
    'trade_viewer_api.py',
    'top_one_generator.py',
    'summary_net_generator.py',
    "grid_live_monitor.py",
    "open_trade_price_refresher.py",
    "pnl_cache_refresh_service.py",
    "weighted_race.py",
    "dna_frequency_net.py",
    "dna_frequency_alt.py",
    "extract_live_trades.py",
    "automated_strategy_picker.py",
    "archive.py",
    "archive_cld.py",
    "strategy_snapshot_15m_generator.py"
    ]]

# [2025-12-26 V20251226_0320] Commented out blog trade scheduled task
# special_file_name = 'blog_trade_capture_and_gen_content_llm.py'
# special_file_time = "23:00"

processes = {}  # Mapping of full script paths to subprocess.Popen objects

def cleanup_stale_strategies():
    """Surgically kills background breakout processes on startup [V20260104_0214]"""
    logging.info("Performing surgical cleanup of background breakout processes...")
    try:
        my_pid = os.getpid()
        monitor_name = os.path.basename(__file__)
        # [V20260104_0215] Optimized PowerShell filter and added safety timeout
        ps_cmd = (
            f'powershell -Command "'
            f'Get-CimInstance Win32_Process -Filter \\"Name = \'python.exe\'\\" | '
            f'Where-Object {{ ($_.CommandLine -like \'*breakout*\') -and '
            f'($_.CommandLine -notlike \'*{monitor_name}*\') -and '
            f'($_.ProcessId -ne {my_pid}) }} | '
            f'Stop-Process -Force -ErrorAction SilentlyContinue'
            f'"'
        )
        try:
            # Add a 10s timeout to prevent hanging the startup sequence
            subprocess.run(ps_cmd, shell=True, check=False, capture_output=True, timeout=10)
            logging.info("Cleanup complete.")
        except subprocess.TimeoutExpired:
            logging.warning("Cleanup timed out after 10s. Proceeding to strategy launch to avoid hang.")
    except Exception as e:
        logging.error(f"Cleanup error: {e}")

def main():
    base_directory = os.path.dirname(__file__)  # Get the directory where the script is located
    config_file = os.path.join(base_directory, 'config.json')
    sleep_duration = get_sleep_duration(config_file)
    # [V20260104_0227] Cleanup disabled to prevent startup hang as user manages terminals manually.
    # cleanup_stale_strategies()


    try:
        while True:
            # [2025-12-26 V20251226_0320] Check kill switch from fs\\config.json
            if get_kill_switch(config_file):
                logging.info("Kill switch activated in fs\\config.json. Stopping the program.")
                break

            for file_name in file_names:
                script_path = os.path.join(folder_path, file_name)

                # Check if the process is alive
                if script_path in processes:
                    if processes[script_path].poll() is None:
                        # Process is still running
                        logging.info(f'{script_path} is already running')
                        continue

                # At this point, the process is either not started or has stopped
                logging.info(f'{script_path} is not running, restarting...')

                # Terminate the old process if it exists
                if script_path in processes and processes[script_path].poll() is not None:
                    processes[script_path].terminate()

                # Start a new process (background mode)
                try:
                    logging.info(f"Starting {file_name} with cwd={folder_path}")
                    processes[script_path] = subprocess.Popen(['python', script_path], cwd=folder_path)
                except Exception as e:
                    logging.error(f"Failed to start {script_path}: {e}")

            # [2025-12-26 V20251226_0320] Commented out blog trade scheduled task
            # # Check if it's time to run the special file
            # current_time = datetime.now().strftime("%H:%M")
            # special_script_path = os.path.join(folder_path, special_file_name)
            # if current_time == special_file_time:
            #     if special_script_path not in processes or processes[special_script_path].poll() is not None:
            #         logging.info(f"Starting special script {special_script_path} at {special_file_time}")
            #         try:
            #             processes[special_script_path] = subprocess.Popen(['python', special_script_path])
            #         except Exception as e:
            #             logging.error(f"Failed to start {special_script_path}: {e}")

            time.sleep(sleep_duration)
    except KeyboardInterrupt:
        logging.info("Shutdown requested...exiting.")
    finally:
        for proc in processes.values():
            if proc.poll() is None:
                proc.terminate()
                proc.wait()

if __name__ == "__main__":
    main()


