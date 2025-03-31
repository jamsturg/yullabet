#!/bin/bash

# Yullabet Setup Script for macOS
# This script sets up the Yullabet environment on macOS

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print section headers
print_header() {
    echo ""
    echo "===== $1 ====="
    echo ""
}

# Make all shell scripts executable
make_scripts_executable() {
    print_header "Making scripts executable"
    
    chmod +x start-tab-api-mcp.sh
    chmod +x start-mcp-chat.sh
    chmod +x config/copy-config.sh
    
    echo "All scripts are now executable."
}

# Check and install Node.js and npm
setup_node() {
    print_header "Checking Node.js and npm"
    
    if command_exists node && command_exists npm; then
        node_version=$(node -v)
        npm_version=$(npm -v)
        echo "Node.js $node_version and npm $npm_version are already installed."
    else
        echo "Node.js and/or npm are not installed."
        echo "Please install Node.js from https://nodejs.org/"
        echo "Alternatively, you can use Homebrew: brew install node"
        exit 1
    fi
}

# Check and install Python dependencies
setup_python() {
    print_header "Checking Python"
    
    if command_exists python3; then
        python_version=$(python3 --version)
        echo "$python_version is installed."
        
        # Check if pip is installed
        if command_exists pip3; then
            echo "pip is installed."
        else
            echo "pip is not installed. Installing pip..."
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            python3 get-pip.py
            rm get-pip.py
        fi
        
        # Install Python dependencies
        print_header "Installing Python dependencies"
        
        echo "Installing TAB API MCP dependencies..."
        pip3 install httpx mcp[server] starlette uvicorn python-dotenv
        
        echo "Python dependencies installed successfully."
    else
        echo "Python 3 is not installed."
        echo "Please install Python 3 from https://www.python.org/downloads/"
        echo "Alternatively, you can use Homebrew: brew install python"
        exit 1
    fi
}

# Setup MCP-Chat
setup_mcp_chat() {
    print_header "Setting up MCP-Chat"
    
    if [ -d "mcp-chat" ]; then
        echo "MCP-Chat directory exists. Installing dependencies..."
        cd mcp-chat
        npm install
        cd ..
    else
        echo "MCP-Chat directory not found. Cloning repository..."
        git clone https://github.com/Flux159/mcp-chat.git
        cd mcp-chat
        npm install
        cd ..
    fi
    
    echo "MCP-Chat setup completed."
}

# Copy configuration
copy_config() {
    print_header "Copying configuration"
    
    # Create .mcpchat directory if it doesn't exist
    mkdir -p "$HOME/.mcpchat/chats"
    
    # Run the copy-config.sh script
    cd config
    ./copy-config.sh
    cd ..
    
    echo "Configuration copied successfully."
}

# Main setup function
main() {
    print_header "Yullabet Setup for macOS"
    
    # Make scripts executable
    make_scripts_executable
    
    # Setup Node.js and npm
    setup_node
    
    # Setup Python and dependencies
    setup_python
    
    # Setup MCP-Chat
    setup_mcp_chat
    
    # Copy configuration
    copy_config
    
    print_header "Setup Complete"
    echo "To start the TAB API MCP server, run: ./start-tab-api-mcp.sh"
    echo "To start the MCP-Chat server, run: ./start-mcp-chat.sh"
    echo "Open http://localhost:3000 in your browser to access MCP-Chat"
}

# Run the main function
main