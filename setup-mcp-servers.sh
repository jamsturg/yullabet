#!/bin/bash

# Shell script to set up all MCP servers
# This script checks for and installs all necessary dependencies for the MCP servers

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
        
        echo "Installing mcp-server-aidd..."
        pip3 install mcp-server-aidd
        
        echo "Python dependencies installed successfully."
    else
        echo "Python 3 is not installed."
        echo "Please install Python 3 from https://www.python.org/downloads/"
        echo "Alternatively, you can use Homebrew: brew install python"
        exit 1
    fi
}

# Install Smithery CLI
setup_smithery() {
    print_header "Installing Smithery CLI"
    
    if ! command_exists smithery; then
        echo "Installing Smithery CLI..."
        npm install -g @smithery/cli
    else
        echo "Smithery CLI is already installed."
    fi
}

# Install UV
setup_uv() {
    print_header "Installing UV"
    
    if ! command_exists uv; then
        echo "Installing UV..."
        pip3 install uv
    else
        echo "UV is already installed."
    fi
    
    if ! command_exists uvx; then
        echo "Installing UVX..."
        pip3 install uvx
    else
        echo "UVX is already installed."
    fi
}

# Clone and set up freqtrade-mcp
setup_freqtrade_mcp() {
    print_header "Setting up freqtrade-mcp"
    
    freqtrade_mcp_path="$HOME/freqtrade-mcp"
    
    if [ -d "$freqtrade_mcp_path" ]; then
        echo "freqtrade-mcp directory exists. Updating repository..."
        cd "$freqtrade_mcp_path"
        git pull
    else
        echo "freqtrade-mcp directory not found. Cloning repository..."
        git clone https://github.com/kukapay/freqtrade-mcp.git "$freqtrade_mcp_path"
        cd "$freqtrade_mcp_path"
    fi
    
    # Install dependencies
    echo "Installing freqtrade-mcp dependencies..."
    pip3 install -r requirements.txt
    
    cd "$OLDPWD"
    echo "freqtrade-mcp setup completed."
}

# Install Smithery MCP servers
install_smithery_servers() {
    print_header "Installing Smithery MCP servers"
    
    # Install @smithery-ai/server-sequential-thinking
    echo "Installing @smithery-ai/server-sequential-thinking..."
    smithery install @smithery-ai/server-sequential-thinking
    
    # Install @browserbasehq/mcp-browserbase
    echo "Installing @browserbasehq/mcp-browserbase..."
    smithery install @browserbasehq/mcp-browserbase
    
    # Install @ashley-ha/mcp-manus
    echo "Installing @ashley-ha/mcp-manus..."
    npx -y @smithery/cli@latest install @ashley-ha/mcp-manus
    
    # Install @IzumiSy/mcp-duckdb-memory-server
    echo "Installing @IzumiSy/mcp-duckdb-memory-server..."
    npx -y @smithery/cli@latest install @IzumiSy/mcp-duckdb-memory-server
    
    # Install @capecoma/winterm-mcp
    echo "Installing @capecoma/winterm-mcp..."
    smithery install @capecoma/winterm-mcp
    
    # Install mcp-server-ccxt
    echo "Installing mcp-server-ccxt..."
    npx -y @smithery/cli@latest install mcp-server-ccxt
    
    # Install @simonb97/server-win-cli
    echo "Installing @simonb97/server-win-cli..."
    npx -y @smithery/cli@latest install @simonb97/server-win-cli
    
    # Install @sidharthrajaram/mcp-sse
    echo "Installing @sidharthrajaram/mcp-sse..."
    npx -y @smithery/cli install @sidharthrajaram/mcp-sse --client claude
    
    echo "Smithery MCP servers installed successfully."
}

# Make all shell scripts executable
make_scripts_executable() {
    print_header "Making scripts executable"
    
    chmod +x start-tab-api-mcp.sh
    chmod +x start-mcp-chat.sh
    chmod +x config/copy-config.sh
    
    echo "All scripts are now executable."
}

# Main setup function
main() {
    print_header "MCP Servers Setup"
    
    # Make scripts executable
    make_scripts_executable
    
    # Setup Node.js and npm
    setup_node
    
    # Setup Python and dependencies
    setup_python
    
    # Install Smithery CLI
    setup_smithery
    
    # Install UV
    setup_uv
    
    # Clone and set up freqtrade-mcp
    setup_freqtrade_mcp
    
    # Install Smithery MCP servers
    install_smithery_servers
    
    print_header "Setup Complete"
    echo "All MCP servers have been set up successfully."
    echo "To copy the configuration to MCP-Chat, run: cd config && ./copy-config.sh"
    echo "To start the TAB API MCP server, run: ./start-tab-api-mcp.sh"
    echo "To start the MCP-Chat server, run: ./start-mcp-chat.sh"
}

# Run the main function
main