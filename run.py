"""
FAIRSHIFT Local Server Launcher
Usage: python run.py
"""
import os
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print(f"Starting FAIRSHIFT on http://{HOST}:{PORT} ...")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
