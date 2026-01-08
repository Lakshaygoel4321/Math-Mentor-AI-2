"""
Quick Run Script - Use this after initial setup
"""

import subprocess
import os

if __name__ == "__main__":
    if not os.path.exists(".env"):
        print("⚠️  .env file not found! Please run setup_and_run.py first")
    elif not os.path.exists("rag/vectorstore/index.faiss"):
        print("⚠️  Vector store not found! Please run setup_and_run.py first")
    else:
        print("🚀 Starting Math Mentor...")
        subprocess.run(["streamlit", "run", "app.py"])
