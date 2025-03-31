# PowerShell script to set up all MCP servers
# This script checks for and installs all necessary dependencies for the MCP servers

# Function to check if a command exists
function Test-CommandExists {
    param (
        [string]$Command
    )
    
    $exists = $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
    return $exists
}

# Function to print section headers
function Write-Header {
    param (
        [string]$Title
    )
    
    Write-Host ""
    Write-Host "===== $Title ====="
    Write-Host ""
}

# Check and install Node.js and npm
function Setup-Node {
    Write-Header "Checking Node.js and npm"
    
    if (Test-CommandExists "node") {
        $nodeVersion = node -v
        $npmVersion = npm -v
        Write-Host "Node.js $nodeVersion and npm $npmVersion are already installed."
    } else {
        Write-Host "Node.js and/or npm are not installed."
        Write-Host "Please install Node.js from https://nodejs.org/"
        exit 1
    }
}

# Check and install Python dependencies
function Setup-Python {
    Write-Header "Checking Python"
    
    if (Test-CommandExists "python") {
        $pythonVersion = python --version
        Write-Host "$pythonVersion is installed."
        
        # Check if pip is installed
        if (Test-CommandExists "pip") {
            Write-Host "pip is installed."
        } else {
            Write-Host "pip is not installed. Installing pip..."
            Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
            python get-pip.py
            Remove-Item "get-pip.py"
        }
        
        # Install Python dependencies
        Write-Header "Installing Python dependencies"
        
        Write-Host "Installing TAB API MCP dependencies..."
        pip install httpx mcp[server] starlette uvicorn python-dotenv
        
        Write-Host "Installing mcp-server-aidd..."
        pip install mcp-server-aidd
        
        Write-Host "Python dependencies installed successfully."
    } else {
        Write-Host "Python is not installed."
        Write-Host "Please install Python from https://www.python.org/downloads/"
        exit 1
    }
}

# Install Smithery CLI
function Setup-Smithery {
    Write-Header "Installing Smithery CLI"
    
    if (-not (Test-CommandExists "smithery")) {
        Write-Host "Installing Smithery CLI..."
        npm install -g @smithery/cli
    } else {
        Write-Host "Smithery CLI is already installed."
    }
}

# Install UV
function Setup-UV {
    Write-Header "Installing UV"
    
    if (-not (Test-CommandExists "uv")) {
        Write-Host "Installing UV..."
        pip install uv
    } else {
        Write-Host "UV is already installed."
    }
    
    if (-not (Test-CommandExists "uvx")) {
        Write-Host "Installing UVX..."
        pip install uvx
    } else {
        Write-Host "UVX is already installed."
    }
}

# Clone and set up freqtrade-mcp
function Setup-FreqtradeMCP {
    Write-Header "Setting up freqtrade-mcp"
    
    $freqtradeMcpPath = "C:\Users\adam\freqtrade-mcp"
    
    if (Test-Path $freqtradeMcpPath) {
        Write-Host "freqtrade-mcp directory exists. Updating repository..."
        Set-Location $freqtradeMcpPath
        git pull
    } else {
        Write-Host "freqtrade-mcp directory not found. Cloning repository..."
        git clone https://github.com/kukapay/freqtrade-mcp.git $freqtradeMcpPath
        Set-Location $freqtradeMcpPath
    }
    
    # Install dependencies
    Write-Host "Installing freqtrade-mcp dependencies..."
    pip install -r requirements.txt
    
    Set-Location $PSScriptRoot
    Write-Host "freqtrade-mcp setup completed."
}

# Install Smithery MCP servers
function Install-SmitheryServers {
    Write-Header "Installing Smithery MCP servers"
    
    # Install @smithery-ai/server-sequential-thinking
    Write-Host "Installing @smithery-ai/server-sequential-thinking..."
    smithery install @smithery-ai/server-sequential-thinking
    
    # Install @browserbasehq/mcp-browserbase
    Write-Host "Installing @browserbasehq/mcp-browserbase..."
    smithery install @browserbasehq/mcp-browserbase
    
    # Install @ashley-ha/mcp-manus
    Write-Host "Installing @ashley-ha/mcp-manus..."
    npx -y @smithery/cli@latest install @ashley-ha/mcp-manus
    
    # Install @IzumiSy/mcp-duckdb-memory-server
    Write-Host "Installing @IzumiSy/mcp-duckdb-memory-server..."
    npx -y @smithery/cli@latest install @IzumiSy/mcp-duckdb-memory-server
    
    # Install @capecoma/winterm-mcp
    Write-Host "Installing @capecoma/winterm-mcp..."
    smithery install @capecoma/winterm-mcp
    
    # Install mcp-server-ccxt
    Write-Host "Installing mcp-server-ccxt..."
    npx -y @smithery/cli@latest install mcp-server-ccxt
    
    # Install @simonb97/server-win-cli
    Write-Host "Installing @simonb97/server-win-cli..."
    npx -y @smithery/cli@latest install @simonb97/server-win-cli
    
    # Install @sidharthrajaram/mcp-sse
    Write-Host "Installing @sidharthrajaram/mcp-sse..."
    npx -y @smithery/cli install @sidharthrajaram/mcp-sse --client claude
    
    Write-Host "Smithery MCP servers installed successfully."
}

# Main setup function
function Main {
    Write-Header "MCP Servers Setup"
    
    # Setup Node.js and npm
    Setup-Node
    
    # Setup Python and dependencies
    Setup-Python
    
    # Install Smithery CLI
    Setup-Smithery
    
    # Install UV
    Setup-UV
    
    # Clone and set up freqtrade-mcp
    Setup-FreqtradeMCP
    
    # Install Smithery MCP servers
    Install-SmitheryServers
    
    Write-Header "Setup Complete"
    Write-Host "All MCP servers have been set up successfully."
    Write-Host "To copy the configuration to MCP-Chat, run: cd config && .\copy-config.ps1"
    Write-Host "To start the TAB API MCP server, run: .\start-tab-api-mcp.bat"
    Write-Host "To start the MCP-Chat server, run: .\start-mcp-chat.bat"
}

# Run the main function
Main