#!/bin/bash

# LinkedIn Post Automation Tool - Dynamic Deployment Script
# This script sets up the complete Python + Selenium environment

echo "🚀 LinkedIn Post Automation Tool - Dynamic Deployment"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip"
        exit 1
    fi
    
    print_success "pip found"
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install requirements
install_requirements() {
    print_status "Installing Python requirements..."
    
    # Upgrade pip first
    $PIP_CMD install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
        print_success "Requirements installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Check Chrome installation
check_chrome() {
    print_status "Checking Google Chrome installation..."
    
    if command -v google-chrome &> /dev/null; then
        CHROME_VERSION=$(google-chrome --version 2>&1)
        print_success "Chrome found: $CHROME_VERSION"
        return 0
    elif command -v chromium-browser &> /dev/null; then
        CHROME_VERSION=$(chromium-browser --version 2>&1)
        print_success "Chromium found: $CHROME_VERSION"
        return 0
    else
        print_warning "Chrome not found. Installing Chrome..."
        install_chrome
    fi
}

# Install Chrome (Ubuntu/Debian)
install_chrome() {
    if command -v apt-get &> /dev/null; then
        print_status "Installing Chrome via apt-get..."
        
        # Add Google's signing key
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        
        # Add Chrome repository
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
        
        # Update and install
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
        
        print_success "Chrome installed successfully"
    else
        print_warning "Cannot auto-install Chrome. Please install manually:"
        print_warning "  Ubuntu/Debian: sudo apt-get install google-chrome-stable"
        print_warning "  CentOS/RHEL: sudo yum install google-chrome-stable"
        print_warning "  macOS: Download from https://www.google.com/chrome/"
    fi
}

# Run setup script
run_setup() {
    print_status "Running setup script..."
    
    if [ -f "setup.py" ]; then
        $PYTHON_CMD setup.py
        print_success "Setup completed"
    else
        print_error "setup.py not found"
        exit 1
    fi
}

# Test the installation
test_installation() {
    print_status "Testing installation..."
    
    if [ -f "test_setup.py" ]; then
        $PYTHON_CMD test_setup.py
        if [ $? -eq 0 ]; then
            print_success "Installation test passed"
        else
            print_warning "Installation test failed, but continuing..."
        fi
    else
        print_warning "test_setup.py not found, skipping test"
    fi
}

# Start the Streamlit app
start_app() {
    print_status "Starting LinkedIn Post Automation Tool..."
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Application Details:"
    echo "   • Tool: LinkedIn Post Automation with Python + Selenium"
    echo "   • UI: Streamlit Web Interface"
    echo "   • Features: Dynamic web scraping, real-time data extraction"
    echo "   • URL: http://localhost:8501"
    echo ""
    echo "🚀 Starting the application..."
    echo "   Press Ctrl+C to stop the server"
    echo ""
    
    # Start Streamlit
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
}

# Main execution
main() {
    check_python
    check_pip
    create_venv
    install_requirements
    check_chrome
    run_setup
    test_installation
    start_app
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}[INFO]${NC} Deployment interrupted by user"; exit 1' INT

# Run main function
main

print_success "Deployment completed successfully!"