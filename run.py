"""
DTS App Entrypoint Script

This script runs the DTS FastAPI application without the need to type 
a long uvicorn command. Supports both development and production modes.

Usage:
    python run.py dev     # Development mode (reload enabled)
    python run.py prod    # Production mode (no reload)
"""

import sys
import uvicorn


def run_dev() -> None:
    """Run the FastAPI app in development mode with auto-reload."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


def run_prod() -> None:
    """Run the FastAPI app in production mode without reload."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    # Check CLI argument for mode
    mode = sys.argv[1] if len(sys.argv) > 1 else "dev"

    if mode == "prod":
        run_prod()
    else:
        run_dev()
