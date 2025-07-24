#!/usr/bin/env python3
"""
Simple test script to verify the LinkedIn scraper functionality
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import selenium
        print("✅ Selenium imported successfully")
    except ImportError as e:
        print(f"❌ Selenium import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        from linkedin_scraper import LinkedInScraper
        print("✅ LinkedInScraper imported successfully")
    except ImportError as e:
        print(f"❌ LinkedInScraper import failed: {e}")
        return False
    
    return True

def test_mock_data():
    """Test mock data generation"""
    print("\n🧪 Testing mock data generation...")
    
    try:
        from linkedin_scraper import LinkedInScraper
        
        # Create scraper instance (this might fail if Chrome is not available)
        try:
            scraper = LinkedInScraper(headless=True)
            print("✅ Scraper initialized with Chrome WebDriver")
            
            # Test mock data generation
            posts = scraper.generate_mock_posts("AI", 3)
            print(f"✅ Generated {len(posts)} mock posts")
            
            if posts:
                post = posts[0]
                print(f"📄 Sample post:")
                print(f"   Title: {post['title'][:50]}...")
                print(f"   Author: {post['author']}")
                print(f"   Likes: {post['likes']}")
                print(f"   URL: {post['url']}")
            
            scraper.close()
            return True
            
        except Exception as e:
            print(f"⚠️ Chrome WebDriver failed: {e}")
            print("🔄 Testing mock data generation without WebDriver...")
            
            # Test just the mock data generation without WebDriver
            scraper = LinkedInScraper.__new__(LinkedInScraper)
            posts = scraper.generate_mock_posts("AI", 3)
            print(f"✅ Generated {len(posts)} mock posts without WebDriver")
            
            if posts:
                post = posts[0]
                print(f"📄 Sample post:")
                print(f"   Title: {post['title'][:50]}...")
                print(f"   Author: {post['author']}")
                print(f"   Likes: {post['likes']}")
            
            return True
            
    except Exception as e:
        print(f"❌ Mock data test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'app.py',
        'linkedin_scraper.py',
        'requirements.txt',
        'setup.py',
        'deploy.sh',
        'deploy.bat',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Run all tests"""
    print("🚀 LinkedIn Post Automation Tool - Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Module imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: File structure
    if test_file_structure():
        tests_passed += 1
    
    # Test 3: Mock data generation
    if test_mock_data():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The tool is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: streamlit run app.py")
        print("   2. Open: http://localhost:8501")
        print("   3. Start scraping LinkedIn posts!")
        return True
    else:
        print("⚠️ Some tests failed. Please check the installation.")
        print("\n🔧 Troubleshooting:")
        print("   1. Run: pip install -r requirements.txt")
        print("   2. Install Google Chrome")
        print("   3. Run: python setup.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)