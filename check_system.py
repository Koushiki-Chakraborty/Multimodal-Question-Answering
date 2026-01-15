"""
Quick test script to verify all components are working correctly
"""
import os
import sys
import requests

def check_docker():
    """Check if Docker is running"""
    print("1. Checking Docker...")
    try:
        import subprocess
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✓ Docker is running")
            return True
        else:
            print("   ✗ Docker is not running")
            return False
    except Exception as e:
        print(f"   ✗ Cannot check Docker: {e}")
        return False

def check_grobid():
    """Check if GROBID server is accessible"""
    print("2. Checking GROBID server...")
    try:
        response = requests.get("http://localhost:8070/api/isalive", timeout=5)
        if response.status_code == 200 and response.text.strip() == "true":
            print("   ✓ GROBID server is running at http://localhost:8070")
            return True
        else:
            print(f"   ✗ GROBID server responded with: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Cannot connect to GROBID: {e}")
        print("   → Start GROBID with: docker-compose up -d")
        return False

def check_env():
    """Check if .env file exists and is configured"""
    print("3. Checking .env file...")
    if not os.path.exists('.env'):
        print("   ✗ .env file not found")
        print("   → Create .env file with: GROQ_API_KEY=\"your_key_here\"")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY' in content and len(content.strip()) > 20:
            print("   ✓ .env file exists and appears configured")
            return True
        else:
            print("   ✗ .env file exists but GROQ_API_KEY not properly set")
            return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("4. Checking Python dependencies...")
    
    # List of (import_name, install_name)
    required_packages = [
        ('dotenv', 'python-dotenv'),
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4'),
        ('langchain', 'langchain'),
        ('langchain_core', 'langchain-core'),
        ('langchain_community', 'langchain-community'),
        ('langchain_groq', 'langchain-groq'),
        ('langchain_huggingface', 'langchain-huggingface'),
        ('faiss', 'faiss-cpu'),
        ('sentence_transformers', 'sentence-transformers')
    ]
    
    missing = []
    
    for import_name, install_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(install_name)
    
            
    if not missing:
        print(f"   ✓ All required packages installed")
        return True
    else:
        print(f"   ✗ Missing packages: {', '.join(missing)}")
        print("   → Run: pip install -r requirements.txt")
        return False

def check_pdf():
    """Check if PDF files exist in source/ directory"""
    print("5. Checking for PDF files...")
    
    if not os.path.exists('source'):
        print("   ✗ 'source' directory missing")
        print("   → Create 'source' folder and add PDFs there")
        return False
        
    pdfs = [f for f in os.listdir('source') if f.lower().endswith('.pdf')]
    
    if pdfs:
        print(f"   ✓ Found {len(pdfs)} PDF(s) in source/ directory")
        return True
    else:
        print("   ⚠ 'source' directory exists but contains no PDFs")
        print("   → Add some PDF files to 'source/' to get started")
        return True  # Not a blocker, just a warning

def main():
    print("=" * 60)
    print("RAG System - Component Check")
    print("=" * 60)
    print()
    
    checks = [
        check_docker(),
        check_grobid(),
        check_env(),
        check_dependencies(),
        check_pdf()
    ]
    
    print()
    print("=" * 60)
    if all(checks[:4]):  # First 4 are critical
        print("✓ All critical components are ready!")
        print("  You can now run: python rag_cli.py")
    else:
        print("✗ Some components need attention. Fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
