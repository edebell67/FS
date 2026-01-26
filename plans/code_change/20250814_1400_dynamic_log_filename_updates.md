# Dynamic Log Filename Updates

Date: 2025-08-14

## Summary

Updated all strategy files (`_sim.py` and `_live.py`) in the `algo_viewer/strategy_library` directory to use dynamic log filenames instead of hardcoded names. This change makes the code more maintainable and prevents issues when copying or renaming files.

## Files Modified

### _sim.py Files
1. `01_str_topPerformerAtAvgPrice_sim.py`
2. `02_str_topPerformerCopy2hr_sim.py`
3. `02_str_topPerformerCopy_sim.py`
4. `03_str_topPerformerAtPriceSpread_sim.py`
5. `04_str_topPerformerByCount_sim.py`

### _live.py Files
1. `01_str_topPerformerAtAvgPrice_live.py`
2. `02_str_topPerformerCopy2hr_live.py`
3. `02_str_topPerformerCopy_live.py`
4. `03_str_topPerformerAtPriceSpread_live.py`
5. `04_str_topPerformerByCount_Live.py`

## Change Details

Modified the LOG_FILE assignment in each file from:
```python
LOG_FILE = os.path.join(STRATEGY_DIR, "logs", "filename.log")
```

To:
```python
LOG_FILE = os.path.join(STRATEGY_DIR, "logs", f"{os.path.splitext(os.path.basename(__file__))[0]}.log")
```

This change ensures that each file automatically uses its own filename (without extension) as the log filename, making the code more maintainable and reducing errors when files are copied or renamed.

## Benefits

1. **Maintainability**: No need to manually update log filenames when copying or renaming strategy files
2. **Consistency**: All log files will match their corresponding Python script names
3. **Error Reduction**: Eliminates potential mismatches between script names and log filenames

## Future Enhancement Plan: Daily Log Rotation

To ensure log files are generated once daily while keeping simple filenames:

### Implementation Plan

1. Create a function that checks the creation date of the existing log file
2. If the file exists and was created today, append to it
3. If the file exists but was created yesterday or earlier:
   - Rename it with a timestamp (e.g., `strategy_name_20250813.log`)
   - Create a new file with the standard name (`strategy_name.log`)
4. If no file exists, create a new one with the standard name

### Implementation Code

```python
import os
import logging
from datetime import datetime

def setup_daily_log_file(log_file_path):
    """Set up log file with daily rotation based on file creation date."""
    # If log file exists, check its creation date
    if os.path.exists(log_file_path):
        # Get file creation time
        creation_time = os.path.getctime(log_file_path)
        creation_date = datetime.fromtimestamp(creation_time).date()
        current_date = datetime.now().date()
        
        # If file was created on a previous day, rename it
        if creation_date < current_date:
            # Rename with timestamp
            timestamp = creation_date.strftime("%Y%m%d")
            base_name = os.path.splitext(log_file_path)[0]
            extension = os.path.splitext(log_file_path)[1]
            new_name = f"{base_name}_{timestamp}{extension}"
            os.rename(log_file_path, new_name)
            # A new file with standard name will be created by logging
    
    # Set up logging with standard filename
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
```

This approach maintains simple filenames while ensuring daily log rotation based on file creation dates.