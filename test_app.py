#!/usr/bin/env python3
"""
Test script to verify the LinkedIn automation tool structure
"""

import sys
import os

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'setup.py',
        'README.md',
        'deploy.sh',
        'deploy.bat'
    ]
    
    print("🔍 Checking file structure...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
    
    return all(os.path.exists(file) for file in required_files)

def test_app_imports():
    """Test if the main app file has correct imports"""
    print("\n🔍 Checking app.py imports...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            
        required_imports = [
            'import streamlit as st',
            'import pandas as pd',
            'from selenium import webdriver',
            'from selenium.webdriver.common.by import By',
            'from selenium.webdriver.support.ui import WebDriverWait',
            'from selenium.webdriver.support import expected_conditions as EC'
        ]
        
        for import_line in required_imports:
            if import_line in content:
                print(f"✅ {import_line}")
            else:
                print(f"❌ {import_line} - Missing")
                
        return all(import_line in content for import_line in required_imports)
        
    except FileNotFoundError:
        print("❌ app.py not found")
        return False

def test_streamlit_structure():
    """Test if the Streamlit app has proper structure"""
    print("\n🔍 Checking Streamlit app structure...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            
        required_elements = [
            'st.set_page_config',
            'class LinkedInScraper',
            'def search_linkedin_posts',
            'def generate_mock_posts',
            'st.sidebar',
            'st.form',
            'st.progress',
            'def main()'
        ]
        
        for element in required_elements:
            if element in content:
                print(f"✅ {element}")
            else:
                print(f"❌ {element} - Missing")
                
        return all(element in content for element in required_elements)
        
    except FileNotFoundError:
        print("❌ app.py not found")
        return False

def main():
    """Main test function"""
    print("🧪 LinkedIn Keyword Post Automation Tool - Structure Test")
    print("=" * 60)
    
    # Test file structure
    files_ok = test_file_structure()
    
    # Test imports
    imports_ok = test_app_imports()
    
    # Test Streamlit structure
    structure_ok = test_streamlit_structure()
    
    print("\n📊 Test Results:")
    print("=" * 30)
    print(f"File Structure: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"App Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Streamlit Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    
    if all([files_ok, imports_ok, structure_ok]):
        print("\n🎉 All tests passed! The application structure is correct.")
        print("\n📋 Next steps:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Run the app: streamlit run app.py")
        print("3. Open browser to http://localhost:8501")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
    
    return all([files_ok, imports_ok, structure_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)