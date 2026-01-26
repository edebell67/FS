import os
import re
import fastapi
import pyodbc
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import decimal
import datetime
import traceback
import json
from pathlib import Path

# [V20260126_0900] File for persisting live grid selections
GRID_LIVE_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live.json")

# Configure Python logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception in request: %s %s", request.method, request.url)
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Check server logs for details."}
    )

# Middleware to log each request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Incoming request: %s %s", request.method, request.url)
    response = await call_next(request)
    logger.info("Response status: %s for %s %s", response.status_code, request.method, request.url)
    return response

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug flag and DB credentials
DEBUG = True
SERVER = os.getenv("DB_SERVER", "tcp:EDS,1433")
USERNAME = os.getenv("DB_USER", "sqlaccessfromapi")
PASSWORD = os.getenv("DB_PASS", "apiaccess@4321")

# --- Pydantic Model for Trade Lifecycle Snapshot ---
class TradeLifecycleSnapshotData(BaseModel):
    session_id: str = Field(..., max_length=36)
    app_trade_id: int
    guid: str = Field(..., max_length=36)
    timestamp: datetime.datetime
    event_type: str = Field(..., max_length=10)
    trade_type: str = Field(..., max_length=4)
    product: str = Field(..., max_length=50)
    entry_price: float
    quantity: float
    commission: float
    current_price: Optional[float] = None
    current_pnl: Optional[float] = None
    alt_pnl: Optional[float] = None
    is_active: bool
    trailing_stop_active: bool
    current_trailing_stop_level: Optional[float] = None
    peak_net_return_since_trailing_active: Optional[float] = None
    is_flipped: str = Field('N', max_length=1)
    close_reason: Optional[str] = Field(None, max_length=255)
    close_price: Optional[float] = None
    strategy_config: str
    trade_signal: Optional[str] = Field(None, max_length=8)

# --- Pydantic Model for Grid Live Toggle ---
class GridLiveToggle(BaseModel):
    group: str
    active: bool
    models: List[Dict[str, str]] # List of {model: str, product: str}

# --- Database helper functions ---
def connect_to_db(database_name: str):
    # [V20260109_0005] [2026-01-09 00:05] Enhanced logging for connection clarity
    logger.info("Connecting to database: '%s'...", database_name)
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};DATABASE={database_name};"
            f"UID={USERNAME};PWD={PASSWORD}"
        )
        conn = pyodbc.connect(conn_str)
        # [V20260109_0005] [2026-01-09 00:05] Include DB name in success message
        logger.info("Successfully connected to database: '%s'", database_name)
        return conn
    except Exception as e:
        logger.error("Database connection error: %s", e)
        return None


def get_all_views(conn):
    logger.debug("Fetching all view names...")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS")
        views = [row[0] for row in cursor.fetchall()]
        logger.debug("Views fetched: %s", views)
        return views
    except Exception as e:
        logger.error("Error fetching views: %s", e)
        return []

def get_view_data(conn, view_name: str, page: int = 1, page_size: int = 100, model: Optional[str] = None, signal: Optional[str] = None, tradeable: Optional[int] = None, trade_reason: Optional[str] = None, product: Optional[str] = None, session_id: Optional[str] = None, _sort: Optional[str] = None, _limit: Optional[int] = None, created_gt: Optional[str] = None, created_lt: Optional[str] = None): # 2025-08-23, V1.2: Added created_gt parameter. # 2025-12-08, V20251208_01: Added session_id and _limit parameters. # 2026-01-25, V20260125_2245: Added created_lt.
    logger.debug("Fetching data from view %s, page=%d, page_size=%d, model=%s, signal=%s, tradeable=%s, trade_reason=%s, product=%s, _sort=%s, _limit=%s, created_gt=%s, created_lt=%s", view_name, page, page_size, model, signal, tradeable, trade_reason, product, _sort, _limit, created_gt, created_lt) # 2025-08-23, V1.2: Added created_gt to log. # 2025-12-08, V20251208_01: Added _limit to log. # 2026-01-25: Added created_lt to log.
    try:
        cursor = conn.cursor()
        
        # Start building the query
        # Handle TOP clause for _limit first
        select_clause = "SELECT "
        if _limit is not None and _limit > 0:
            select_clause += f"TOP {_limit} "
        select_clause += "* FROM " + view_name

        query = select_clause
        
        # Add WHERE clause if model or signal are provided
        where_clauses = []
        if model:
            where_clauses.append(f"model = '{model}'")
        if signal:
            where_clauses.append(f"signal = '{signal}'")
        if tradeable is not None:
            where_clauses.append(f"tradeable = {tradeable}")
        if trade_reason:
            where_clauses.append(f"trade_reason = '{trade_reason}'")
        if product: # 2025-08-11 - Added product filter.
            where_clauses.append(f"product = '{product}'")
        if session_id: # 2025-12-08, V20251208_01: Added session_id filter.
            where_clauses.append(f"session_id = '{session_id}'")
        # 2025-08-23, V1.2: Add created_gt filter
        if created_gt:
            where_clauses.append(f"created >= '{created_gt}'")
        # 2026-01-25, V20260125_2245: Add created_lt filter
        if created_lt:
            where_clauses.append(f"created < '{created_lt}'")
            
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Add ORDER BY clause if _sort is provided
        order_by_clause = ""
        if _sort:
            if _sort.startswith('-'):
                field = _sort[1:]
                direction = 'DESC'
            else:
                field = _sort
                direction = 'ASC'
            
            # Basic validation for field to prevent SQL injection
            if re.match(r'^[a-zA-Z0-9_]+$', field):
                order_by_clause = f"ORDER BY {field} {direction}"
            else:
                # If invalid field, default to something safe or raise error
                logger.warning(f"Invalid sort field '{field}' provided. Falling back to default order.")
                order_by_clause = "ORDER BY (SELECT 1)" # Fallback
        else:
            order_by_clause = "ORDER BY (SELECT 1)" # Default order if no sort specified but OFFSET/FETCH needs it
        
        query += f" {order_by_clause}"

        # Apply OFFSET/FETCH for pagination only if _limit is NOT used
        if _limit is None or _limit <= 0:
            offset_rows = (page - 1) * page_size
            query += f" OFFSET {offset_rows} ROWS FETCH NEXT {page_size} ROWS ONLY"

        logger.debug("Executing query: %s", query)
        cursor.execute(query)
        cols = [c[0] for c in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        for r in rows:
            for k, v in r.items():
                if isinstance(v, decimal.Decimal):
                    r[k] = float(v)
                if isinstance(v, (datetime.date, datetime.datetime)):
                    r[k] = v.isoformat()
        logger.debug("Fetched %d rows from %s", len(rows), view_name)
        return rows
    except Exception as e:
        logger.error("Error fetching data from view %s: %s", view_name, e)
        return None


def get_view_metadata(conn, view_name: str):
    logger.debug("Fetching metadata for view %s", view_name)
    try:
        cursor = conn.cursor()
        query = (
            "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
            f"WHERE TABLE_NAME = '{view_name}' COLLATE SQL_Latin1_General_CP1_CI_AS"
        )
        logger.debug("Executing metadata query: %s", query)
        cursor.execute(query)
        meta = [{"column_name": r[0], "data_type": r[1]} for r in cursor.fetchall()]
        logger.debug("Metadata entries: %d", len(meta))
        return meta
    except Exception as e:
        logger.error("Error fetching metadata for view %s: %s", view_name, e)
        return None


def execute_insert(conn, table_name: str, data: Dict):
    logger.debug("Inserting into %s: %s", table_name, data)
    try:
        cursor = conn.cursor()
        cols, ph, vals = [], [], []
        for col, val in data.items():
            if val is None:
                continue
            cols.append(col)
            ph.append('?')
            if isinstance(val, bool):
                vals.append(1 if val else 0)
            elif isinstance(val, datetime.datetime):
                vals.append(val.isoformat(sep=' ', timespec='milliseconds'))
            else:
                vals.append(val)
        query = (
            f"INSERT INTO {table_name} (" + ", ".join(cols) + ") "
            f"VALUES (" + ", ".join(ph) + ")"
        )
        logger.debug("Insert query: %s", query)
        logger.debug("Values: %s", vals)
        cursor.execute(query, tuple(vals))
        conn.commit()
        logger.debug("Insert committed.")
        return True
    except pyodbc.Error as ex:
        conn.rollback()
        logger.exception("DB insert error: %s", ex)
        raise HTTPException(status_code=500, detail=f"DB insert error: {ex}")
    except Exception as e:
        conn.rollback()
        logger.exception("Unexpected insert error: %s", e)
        raise HTTPException(status_code=500, detail=f"Unexpected insert error: {e}")

# --- API Endpoints ---
@app.get("/api/views")
async def list_views(request: Request, db: str = fastapi.Query("tradedb")):
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    views = get_all_views(conn)
    conn.close()
    return {"views": views}

@app.get("/api/rt_group_metrics")
async def get_rt_group_metrics_sp(request: Request, db: str = fastapi.Query("tradedb"), product: Optional[str] = fastapi.Query(None)):
    """
    Fetches aggregated RT group metrics by executing the sp_get_rt_group_metrics stored procedure
    and retrieving the max_rt_group_quantity from the config table.
    """
    logger.info("Executing get_rt_group_metrics_sp for db=%s, product=%s", db, product)
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # 1. Execute the stored procedure for live metrics
        if product:
            cursor.execute("{CALL dbo.sp_get_rt_group_metrics (?)}", product)
        else:
            cursor.execute("{CALL dbo.sp_get_rt_group_metrics}")
        
        row = cursor.fetchone()
        metrics = {}
        if row:
            columns = [column[0] for column in cursor.description]
            for i, col in enumerate(columns):
                val = row[i]
                if isinstance(val, decimal.Decimal):
                    metrics[col] = float(val)
                else:
                    metrics[col] = val
        
        # 2. Fetch the max_rt_group_quantity from dbo.config
        cursor.execute("SELECT config_value FROM dbo.config WHERE config_name = 'max_rt_group_quantity'")
        config_row = cursor.fetchone()
        
        if config_row and config_row[0] is not None:
            # Assuming the config_value is stored as a string that can be converted to a number
            try:
                metrics['max_rt_group_quantity'] = float(config_row[0])
            except (ValueError, TypeError):
                metrics['max_rt_group_quantity'] = 0 # Default if conversion fails
                logger.error("'max_rt_group_quantity' in dbo.config is not a valid number: %s", config_row[0])
        else:
            metrics['max_rt_group_quantity'] = 0 # Default value if not found
            logger.warning("'max_rt_group_quantity' not found in dbo.config table.")
            
        logger.debug("Successfully fetched and combined RT group metrics: %s", metrics)
        # The client expects a list within the 'data' key
        return JSONResponse({"data": [metrics]})

    except Exception as e:
        logger.exception("Error executing sp_get_rt_group_metrics or fetching config: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to execute stored procedure or fetch config: {e}")
    finally:
        if conn:
            conn.close()

@app.get("/api/{view_name}")
async def get_view(view_name: str, request: Request, db: str = fastapi.Query("tradedb"), page: int = fastapi.Query(1, gt=0), page_size: int = fastapi.Query(100, gt=0), model: Optional[str] = fastapi.Query(None), signal: Optional[str] = fastapi.Query(None), tradeable: Optional[int] = fastapi.Query(None), trade_reason: Optional[str] = fastapi.Query(None), product: Optional[str] = fastapi.Query(None), session_id: Optional[str] = fastapi.Query(None), _sort: Optional[str] = fastapi.Query(None), _limit: Optional[int] = fastapi.Query(None, gt=0), created_gt: Optional[str] = fastapi.Query(None), created_lt: Optional[str] = fastapi.Query(None)): # 2025-08-23, V1.2: Added created_gt query parameter. # 2025-12-08, V20251208_01: Added session_id and _limit query parameters. # 2026-01-25: Added created_lt query parameter.
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # [V20260125_1130] Radical Performance Fix: Sync P&L Cache for the Chart View
    if view_name == "vwCombined_trades_closed_output_top200" and db == "tradedb":
        try:
            logger.info("Syncing P&L Cache for request...")
            cursor = conn.cursor()
            cursor.execute("{CALL dbo.sp_refresh_dna_pnl_cache}")
            conn.commit()
        except Exception as e:
            logger.warning("Cache sync failed (non-critical): %s", e)

    data = get_view_data(conn, view_name, page, page_size, model, signal, tradeable, trade_reason, product, session_id, _sort, _limit, created_gt, created_lt) # 2025-08-23, V1.2: Passed created_gt to get_view_data. # 2025-12-08, V20251208_01: Passed session_id and _limit to get_view_data. # 2026-01-25: Passed created_lt.
    if data is None:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from view: {view_name}")
    metadata = get_view_metadata(conn, view_name)
    if metadata is None:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to fetch metadata for view: {view_name}")
    conn.close()
    return JSONResponse({"metadata": metadata, "data": data})

@app.post("/api/execute_trade/")
async def execute_trade_sp(trade_details: dict, db: str = fastapi.Query("tradedb")):
    model = trade_details.get("model")
    signal = trade_details.get("signal")
    reason = trade_details.get("trade_reason") # 2025-08-11 - Changed key from 'reason' to 'trade_reason'.
    if not model or not signal or not reason:
        logger.error(f"Bad Request: Missing model, signal, or reason. Payload: {trade_details}") # 2025-08-11 - Log specific 400 error detail.
        raise HTTPException(status_code=400, detail="Missing 'model', 'signal', or 'reason'")
    try:
        mi = int(model)
    except (ValueError, TypeError):
        logger.error(f"Bad Request: Invalid model: {model}. Payload: {trade_details}") # 2025-08-11 - Log specific 400 error detail.
        raise HTTPException(status_code=400, detail=f"Invalid 'model': {model}")
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cur = conn.cursor()
        sp = "{CALL dbo.sp_001_copy_trade_as_tradeable(?, ?, ?)}"
        logger.debug("Executing SP: %s with params (%s, %s, %s)", sp, mi, signal, reason)
        cur.execute(sp, mi, signal, reason)
        conn.commit()
        logger.debug("SP executed successfully.")
        return JSONResponse({"message": "Trade executed", "model": model, "signal": signal, "reason": reason})
    except pyodbc.Error as ex:
        conn.rollback()
        logger.exception("DB error during SP execution: %s", ex)
        raise HTTPException(status_code=500, detail=f"DB error: {ex}")
    except Exception as e:
        conn.rollback()
        logger.exception("Unexpected error during SP execution: %s", e)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        conn.close()



@app.post("/api/execute_trade_sim/")
async def execute_trade_sp(trade_details: dict, db: str = fastapi.Query("tradedb_sim2")):
    model = trade_details.get("model")
    signal = trade_details.get("signal")
    reason = trade_details.get("trade_reason") # 2025-08-11 - Changed key from 'reason' to 'trade_reason'.
    if not model or not signal or not reason:
        logger.error(f"Bad Request: Missing model, signal, or reason. Payload: {trade_details}") # 2025-08-11 - Log specific 400 error detail.
        raise HTTPException(status_code=400, detail="Missing 'model', 'signal', or 'reason'")
    try:
        mi = int(model)
    except (ValueError, TypeError):
        logger.error(f"Bad Request: Invalid model: {model}. Payload: {trade_details}") # 2025-08-11 - Log specific 400 error detail.
        raise HTTPException(status_code=400, detail=f"Invalid 'model': {model}")
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cur = conn.cursor()
        sp = "{CALL dbo.sp_001_copy_trade_as_tradeable(?, ?, ?)}"
        logger.debug("Executing SP: %s with params (%s, %s, %s)", sp, mi, signal, reason)
        cur.execute(sp, mi, signal, reason)
        conn.commit()
        logger.debug("SP executed successfully.")
        return JSONResponse({"message": "Trade executed", "model": model, "signal": signal, "reason": reason})
    except pyodbc.Error as ex:
        conn.rollback()
        logger.exception("DB error during SP execution: %s", ex)
        raise HTTPException(status_code=500, detail=f"DB error: {ex}")
    except Exception as e:
        conn.rollback()
        logger.exception("Unexpected error during SP execution: %s", e)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        conn.close()


@app.post("/api/trade_lifecycle_snapshots")
async def post_trade_lifecycle_snapshots(snapshots: List[TradeLifecycleSnapshotData], db: str = fastapi.Query("tradedb")):
    conn = connect_to_db(db)
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cnt = 0
        for s in snapshots:
            d = s.dict(by_alias=False, exclude_unset=True)
            if isinstance(d.get('timestamp'), datetime.datetime):
                d['timestamp'] = d['timestamp'].isoformat(sep=' ', timespec='milliseconds')
            for k in ['is_active', 'trailing_stop_active']:
                if k in d and isinstance(d[k], bool):
                    d[k] = 1 if d[k] else 0
            execute_insert(conn, "trade_lifecycle_snapshots", d)
            cnt += 1
        return JSONResponse({"message": f"Inserted {cnt} snapshots."})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error processing snapshots: %s", e)
        raise HTTPException(status_code=500, detail=f"Error processing snapshots: {e}")
    finally:
        conn.close()

# --- [V20260126_0900] Grid Live Trading Endpoints ---
@app.get("/api/grid_live")
async def get_grid_live():
    if not GRID_LIVE_FILE.exists():
        return {"success": True, "live_models": {}}
    try:
        with open(GRID_LIVE_FILE, "r") as f:
            data = json.load(f)
        return {"success": True, "live_models": data}
    except Exception as e:
        logger.error(f"Failed to read grid_live.json: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/grid_live/toggle")
async def toggle_grid_live(payload: GridLiveToggle):
    try:
        data = {}
        if GRID_LIVE_FILE.exists():
            with open(GRID_LIVE_FILE, "r") as f:
                data = json.load(f)
        
        if payload.active:
            data[payload.group] = payload.models
        elif payload.group in data:
            del data[payload.group]
            
        with open(GRID_LIVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
            
        logger.info(f"Grid Live Toggle: {payload.group} set to {payload.active}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Failed to toggle grid_live.json: {e}")
        raise HTTPException(status_code=500, detail=str(e))
