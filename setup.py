#!/usr/bin/env python3
"""
LinkedIn Post Automation Tool - Setup Script
Automatically installs dependencies and configures Chrome WebDriver
"""

import os
import sys
import subprocess
import platform
import requests
import zipfile
import shutil
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install requirements
    result = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    if result is not None:
        print("✅ Requirements installed successfully!")
        return True
    else:
        print("❌ Failed to install requirements")
        return False

def check_chrome_installation():
    """Check if Chrome is installed"""
    print("🔍 Checking Chrome installation...")
    
    chrome_paths = {
        'Windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ],
        'Darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ],
        'Linux': [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium'
        ]
    }
    
    system = platform.system()
    paths = chrome_paths.get(system, [])
    
    for path in paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            return True
    
    # Try command line
    try:
        if system == 'Windows':
            run_command('where chrome', check=True)
        else:
            run_command('which google-chrome || which chromium-browser', check=True)
        print("✅ Chrome found in PATH")
        return True
    except:
        pass
    
    print("❌ Chrome not found. Please install Google Chrome:")
    print("   Windows: https://www.google.com/chrome/")
    print("   macOS: https://www.google.com/chrome/")
    print("   Linux: sudo apt-get install google-chrome-stable")
    return False

def setup_webdriver():
    """Setup Chrome WebDriver using webdriver-manager"""
    print("🚗 Setting up Chrome WebDriver...")
    
    try:
        # Test webdriver-manager
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Download and setup ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver installed at: {driver_path}")
        
        # Test the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        driver.quit()
        
        print("✅ WebDriver test successful!")
        return True
        
    except Exception as e:
        print(f"❌ WebDriver setup failed: {str(e)}")
        return False

def create_test_script():
    """Create a test script to verify the setup"""
    test_script = '''#!/usr/bin/env python3
"""
Test script for LinkedIn Post Automation Tool
"""

import sys
from linkedin_scraper import LinkedInScraper

def test_scraper():
    """Test the LinkedIn scraper functionality"""
    print("🧪 Testing LinkedIn Scraper...")
    
    try:
        # Initialize scraper
        scraper = LinkedInScraper(headless=True)
        print("✅ Scraper initialized successfully")
        
        # Test mock data generation
        posts = scraper.generate_mock_posts("AI", 3)
        print(f"✅ Generated {len(posts)} mock posts")
        
        # Display sample post
        if posts:
            post = posts[0]
            print(f"\\n📄 Sample Post:")
            print(f"   Title: {post['title'][:50]}...")
            print(f"   Author: {post['author']}")
            print(f"   Likes: {post['likes']}")
            print(f"   URL: {post['url']}")
        
        # Close scraper
        scraper.close()
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1)
'''
    
    with open('test_setup.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Test script created: test_setup.py")

def main():
    """Main setup function"""
    print("🚀 LinkedIn Post Automation Tool - Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        sys.exit(1)
    
    # Check Chrome
    if not check_chrome_installation():
        print("⚠️  Chrome not found. The scraper will use mock data.")
        print("   Install Chrome for full functionality.")
    
    # Setup WebDriver
    if not setup_webdriver():
        print("⚠️  WebDriver setup failed. The scraper will use mock data.")
    
    # Create test script
    create_test_script()
    
    print("\\n🎉 Setup completed successfully!")
    print("\\n📋 Next steps:")
    print("   1. Run test: python test_setup.py")
    print("   2. Start app: streamlit run app.py")
    print("   3. Open browser: http://localhost:8501")
    
    # Run test automatically
    print("\\n🧪 Running automatic test...")
    test_result = run_command("python test_setup.py")
    if test_result is not None:
        print("✅ Automatic test passed!")
    else:
        print("⚠️  Automatic test failed, but setup is complete.")

if __name__ == "__main__":
    main()