"""
Market Prices API - Main Entry Point

DB-free market price delivery service.
Runs on port 8002 by default (parallel to existing 8001).

Usage:
    python main.py              # Run on default port 8002
    python main.py --port 8003  # Run on custom port
"""

import argparse
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(
        description="Market Prices API - DB-free price delivery"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8002,
        help="Port to run on (default: 8002)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("MARKET PRICES API")
    print("=" * 50)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print("DB:   None (in-memory only)")
    print("=" * 50)
    print()
    print("Endpoints:")
    print(f"  http://{args.host}:{args.port}/api/vw_000_crypto_quotes")
    print(f"  http://{args.host}:{args.port}/api/vw_000_futures_quotes")
    print(f"  http://{args.host}:{args.port}/api/vw_000_fx_quotes")
    print(f"  http://{args.host}:{args.port}/api/health")
    print()

    import uvicorn
    uvicorn.run(
        "api:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
