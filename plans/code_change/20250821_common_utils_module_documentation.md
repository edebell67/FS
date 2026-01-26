# Gemini Coder - Common Utilities Module Documentation

## 1. Overview

This document details the creation and usage of a new common utilities module within the `algo_viewer` project. The primary goal of this module is to centralize reusable functions that can be accessed by various scripts across different parts of the application, specifically from `algo_viewer/strategy_library` and `tradepanel`.

## 2. Module Location and Structure

A new directory, `common_utils`, has been created under `algo_viewer`. This structure ensures that the module is accessible from both `strategy_library` (a sibling directory) and `tradepanel` (a separate top-level module that can import from `algo_viewer`).

The new directory and file are located at:
*   `C:\Users\edebe\eds\algo_viewer\common_utils\`
*   `C:\Users\edebe\eds\algo_viewer\common_utils\trade_execution_utils.py`

To ensure proper Python package recognition and import functionality, `__init__.py` files have been created in the following locations:
*   `C:\Users\edebe\eds\algo_viewer\__init__.py`
*   `C:\Users\edebe\eds\algo_viewer\common_utils\__init__.py`

## 3. `trade_execution_utils.py`

This file currently contains the `execute_trade_reusable` function, designed to encapsulate the logic for calling the trade execution API endpoint.

### `execute_trade_reusable` Function

This function provides a standardized and reusable way to send trade execution requests to the FastAPI server.

**Function Signature**:
```python
def execute_trade_reusable(
    execute_trade_endpoint: str,
    script_name: str,
    signal_type: str,
    model_name: str,
    price: Optional[float] = None,
    logger: Optional[logging.Logger] = None
) -> bool:
```

**Parameters**:
*   `execute_trade_endpoint` (str): The full URL of the trade execution API endpoint (e.g., `"http://127.0.0.1:8000/api/execute_trade/"`).
*   `script_name` (str): A string identifying the script or strategy that is initiating the trade. This is used for the `trade_reason` field in the API payload.
*   `signal_type` (str): The type of trade to execute, typically `"buy"` or `"sell"`.
*   `model_name` (str): The name of the trading model associated with this trade.
*   `price` (Optional[float]): The price at which the trade is intended to be executed. **Note**: As of this documentation, this parameter is passed to the function but is *not* included in the JSON payload sent to the API. If the API requires this, the function's internal payload construction would need modification.
*   `logger` (Optional[logging.Logger]): An optional `logging.Logger` instance. If provided, the function will use this logger for its messages, allowing for integration with the calling script's logging configuration. If `None`, it uses its own module-level logger.

**Return Value**:
*   `bool`: Returns `True` if the API call was successful (HTTP status code 2xx), and `False` otherwise (e.g., network error, bad HTTP status, JSON decoding error).

**Payload Sent to API**:
The function constructs a JSON payload with the following structure:
```json
{
    "model": "model_name_value",
    "signal": "signal_type_value",
    "trade_reason": "script_name_value"
}
```

## 4. How to Access and Use the Function

To use `execute_trade_reusable` from other scripts, you need to import it.

### Example Import and Usage (from `strategy_library` or `tradepanel`):

```python
import logging
# Configure your logger as needed in your script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
my_script_logger = logging.getLogger(__name__)

# Import the reusable function
from algo_viewer.common_utils.trade_execution_utils import execute_trade_reusable

# Define your specific parameters
EXECUTE_TRADE_API_ENDPOINT = "http://127.0.0.1:8000/api/execute_trade/"
CURRENT_SCRIPT_IDENTIFIER = "MyStrategy001" # Or os.path.splitext(os.path.basename(__file__))[0]

# Example of calling the function
if __name__ == "__main__":
    success = execute_trade_reusable(
        execute_trade_endpoint=EXECUTE_TRADE_API_ENDPOINT,
        script_name=CURRENT_SCRIPT_IDENTIFIER,
        signal_type="buy",
        model_name="TopPerformerModel",
        price=1.23456, # Optional, and currently not sent in payload
        logger=my_script_logger # Pass your script's logger
    )

    if success:
        my_script_logger.info("Trade execution request sent successfully.")
    else:
        my_script_logger.error("Failed to send trade execution request.")
```

By centralizing this function, future changes to the trade execution API interaction can be managed in a single location, reducing code duplication and improving maintainability.
