#!/bin/bash
echo "Installing TAB API MCP..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Install the package in development mode
pip install -e .
# Make the scripts executable
chmod +x start-tab-api-mcp.sh
chmod +x start-tab-api-betting-mcp.sh
chmod +x start-tab-api-mcp-combined.sh
chmod +x run_tests.sh
chmod +x run_tests.sh

echo "TAB API MCP installed successfully."
echo "You can now run the server using:"
echo "  ./start-tab-api-mcp-combined.sh (recommended)"
echo "Or run individual servers:"
echo "  ./start-tab-api-mcp.sh"
echo "  ./start-tab-api-betting-mcp.sh"