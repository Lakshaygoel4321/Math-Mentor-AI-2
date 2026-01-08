"""
Setup and Run Script for Math Mentor
This script automates the setup process and starts the Streamlit app
"""

import os
import sys
import subprocess

def print_step(message):
    """Print step with formatting"""
    print("\n" + "="*60)
    print(f"🚀 {message}")
    print("="*60 + "\n")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"▶️  {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(e.stderr)
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_step("Checking Dependencies")
    
    required_packages = [
        "streamlit",
        "langchain",
        "openai",
        "whisper",
        "easyocr",
        "faiss-cpu",
        "sympy"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print_step("Creating Required Directories")
    
    directories = [
        "rag/knowledge_base",
        "rag/vectorstore",
        "memory",
        "agents",
        "multimodal",
        "utils"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    return True

def setup_knowledge_base():
    """Setup knowledge base"""
    print_step("Setting Up Knowledge Base")
    
    if os.path.exists("create_knowledge_base.py"):
        return run_command("python create_knowledge_base.py", "Knowledge base creation")
    else:
        print("⚠️  create_knowledge_base.py not found, skipping...")
        return True

def build_vectorstore():
    """Build vector store"""
    print_step("Building Vector Store")
    
    # Check if vectorstore already exists
    if os.path.exists("rag/vectorstore/index.faiss"):
        print("ℹ️  Vector store already exists")
        rebuild = input("Do you want to rebuild it? (y/N): ").lower()
        if rebuild != 'y':
            print("✅ Using existing vector store")
            return True
    
    if os.path.exists("rag/vectorstore/vectorstore.py"):
        return run_command("python rag/vectorstore/vectorstore.py", "Vector store creation")
    else:
        print("⚠️  vectorstore.py not found, skipping...")
        return True

def check_env_file():
    """Check if .env file exists"""
    print_step("Checking Environment Variables")
    
    if not os.path.exists(".env"):
        print("⚠️  .env file not found!")
        print("\nPlease create a .env file with your API keys:")
        print("OPENAI_API_KEY=your_key_here")
        
        create_env = input("\nCreate .env file now? (y/N): ").lower()
        if create_env == 'y':
            api_key = input("Enter your OpenAI API key: ").strip()
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            print("✅ .env file created!")
            return True
        else:
            return False
    else:
        print("✅ .env file exists")
        return True

def start_streamlit():
    """Start Streamlit app"""
    print_step("Starting Streamlit App")
    
    print("🌐 Launching Math Mentor...")
    print("📝 The app will open in your browser")
    print("⚠️  Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Math Mentor stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error starting Streamlit: {e}")

def main():
    """Main setup and run function"""
    print("\n" + "🧮 " * 30)
    print("   MATH MENTOR - Setup & Launch Script")
    print("🧮 " * 30 + "\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install dependencies first: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Create directories
    if not create_directories():
        print("\n❌ Failed to create directories")
        sys.exit(1)
    
    # Step 3: Check environment variables
    if not check_env_file():
        print("\n⚠️  Please set up your .env file before continuing")
        sys.exit(1)
    
    # Step 4: Setup knowledge base
    setup_knowledge_base()
    
    # Step 5: Build vector store
    build_vectorstore()
    
    # Step 6: Start Streamlit
    print_step("Setup Complete!")
    print("✅ All setup steps completed successfully!")
    
    start = input("\n🚀 Start Math Mentor now? (Y/n): ").lower()
    if start != 'n':
        start_streamlit()
    else:
        print("\n✅ Setup complete! Run 'streamlit run app.py' to start the app.")

if __name__ == "__main__":
    main()
