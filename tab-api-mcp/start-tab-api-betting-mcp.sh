#!/bin/bash
echo "Starting TAB API Betting MCP server..."

if [ -z "$TAB_CLIENT_ID" ]; then
    echo "WARNING: TAB_CLIENT_ID environment variable is not set"
    echo "You will be prompted to enter your TAB API Client ID"
fi

if [ -z "$TAB_CLIENT_SECRET" ]; then
    echo "WARNING: TAB_CLIENT_SECRET environment variable is not set"
    echo "You will be prompted to enter your TAB API Client Secret"
fi

python -m tab_api_mcp.betting --port 8082

echo "TAB API Betting MCP server stopped."